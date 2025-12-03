"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 1.0.0
"""

import importlib
import logging
from typing import Any, Dict, Tuple, Type

import sklearn

logger = logging.getLogger(__name__)
sklearn.set_config(transform_output="pandas")

import GPUtil
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from skopt import BayesSearchCV
from skopt.space import Categorical, Integer, Real

#############
# Utilities #
#############


def _parse_search_space(search_space: dict) -> Dict[str, Any]:
    """
    Parses a dictionary into skopt.space objects.
    Converting to skopt.space objects is necessary before passing into BayesSearchCV as 'search_spaces' parameters.

    If unsure of what 'search_spaces' is, refer to 'specifying_model_config.md' documentation!!

    Parameters
    ----------
    search_space: dict
        Dictionary specifing search_space range of parameters; Defined in conf/base/parameters_model_config/*.yml under header 'search_space'

    Returns
    -------
    Dict[str, Any]
        Dictionary with parameters wrapped in skopt.space objects

    Example
    -------
        space = {
            'x': {'type': 'Integer', 'low': 1, 'high': 10},
            'y': {'type': 'Categorical', 'categories': ['a', 'b']}
        }

        _parse_search_space(space)
        {'x': Integer(1, 10), 'y': Categorical(['a', 'b'])}
    """
    bayes_search_params = {}
    for identifier, values in search_space.items():
        value_type = values["type"]

        if value_type == "Integer":
            bayes_search_params[identifier] = Integer(values["low"], values["high"])

        # Checks 'Real' type for prior parameter and parses as kwargs
        elif value_type == "Real":
            kwargs = {
                k: v for k, v in values.items() if k not in ["type", "low", "high"]
            }
            bayes_search_params[identifier] = Real(
                values["low"], values["high"], **kwargs
            )

        elif value_type == "Categorical":
            bayes_search_params[identifier] = Categorical(values["categories"])

    return bayes_search_params


def _get_model_class(class_path: str) -> Type[BaseEstimator]:
    """
    Imports and returns a class from a dotted string path.

    Parameters
    ----------
    class_path: str
        Full path in the 'package.module.ClassName' format

    Returns
    -------
    Type[BaseEstimator]
        Python class of the dotted string path

    Example
    -------
    python_class = _get_model_class("sklearn.ensemble.RandomForestClassifier")
    """
    # Split string one dot <.> from the right
    module_path, class_name = class_path.rsplit(".", 1)

    # Import model class library with importlib
    module = importlib.import_module(module_path)

    # Returns model class
    return getattr(module, class_name)


def _init_model(
    X_train: pd.DataFrame, model_config: Dict, options: Dict
) -> Type[BaseEstimator]:
    """
    Initializes a ML model object with model confiuration specified in model's *.yml file.
    Moves uses cuda if specified in model's configuration.

    If unsure of what 'search_spaces' and 'options' should be, refer to 'specifying_model_config.md' documentation!!

    Parameters
    ----------
    X_train: pd.DataFrame
        Training data; Used to detect categorial features for catboost classifier

    model_config: Dict
        Model base hyperparameter configuration; Defined in conf/base/parameters_model_config/*.yml under header 'model_params'

    options: Dict
        Execution confiuration; Defined in parameters_execution_configuration.yml under header 'execution_config'

    Returns
    -------
    Type[BaseEstimator]
        Initialise model instance
    """
    model_class = _get_model_class(model_config["class"])

    model_params = model_config.get("model_params", {})

    # For device configuration of auto, the following
    # code block will switch model training device to
    # 'cpu' or 'cuda' depending on existing hardware
    if model_params.get("device") == "auto":
        device = "cuda" if GPUtil.getAvailable() else "cpu"
        model_params["device"] = device
        logger.debug(f"Selected: {device}")

    # CatboostClassifier requires to specify category features in its parameters
    # for proper training
    if model_config["class"] == "catboost.CatBoostClassifier":
        model_params["cat_features"] = X_train.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        model_config["data_encoding"] = None
        logger.debug("Added categorical cat_features")

    return model_class(random_state=options["random_state"], **model_params)


def _build_preprocessor(X_train: pd.DataFrame, model_config: dict) -> ColumnTransformer:
    """
    Creates dataset transformation object.
    Used for applying One-Hit, Label (Oritental) encoding on the entire dataset.
    You can also refuse to apply any encoding to the dataset.

    Parameters
    ----------
    X_train: pd.DataFrame
        Training data; Used to determine categorical and numerical columns in the dataset

    model_config:
        Model base hyperparameter configuration.
        Used to check datset how dataset should be encoded, as well as if the dataset requires scaling.

        If encoding is not specified as a parameter, One-Hot encoding will be applied by default.;

        Defined in conf/base/parameters_model_config/*.yml under header 'model_params'

    Returns
    -------
    ColumnTransformer
        Defines how dataset should be transformed: (OHE/Label/None) w/o Scaling
    """

    # Returns subset of DataFrame cols based on col dtypes
    categorical_cols = X_train.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    numerical_cols = X_train.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    preprocessing_steps = []
    data_encoding = model_config.get(
        "data_encoding", "ohe"
    ).lower()  # Default encoding is one-hot encoding

    if data_encoding == "ohe":
        logger.debug("Applying One-Hot Encoding")
        encoding_transformer = (
            "ohe",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            categorical_cols,
        )
        preprocessing_steps.append(encoding_transformer)

    elif data_encoding == "label":
        logger.debug("Applying Label Encoding")
        encoding_transformer = (
            "label",
            OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
            categorical_cols,
        )
        preprocessing_steps.append(encoding_transformer)

    elif data_encoding == "none":
        logger.debug("Skipped encoding")
        pass

    # Applies dataset scaling if required
    if model_config.get("requires_scaling", False):
        scaling_transformer = ("scaler", StandardScaler(), numerical_cols)
        preprocessing_steps.append(scaling_transformer)
        logger.debug("Applied Standard Scaling")

    return ColumnTransformer(
        transformers=preprocessing_steps, remainder="passthrough", n_jobs=-1
    )


#########
# Nodes #
#########


def split_dataset(df: pd.DataFrame, options: Dict) -> Tuple:
    """
    Splits the dataframe and applies stratification.

    Parameters
    ----------
    df: pd.DataFrame
        Dataset to be split

    options: Dict
        Configuration that specifies train test split ratio and random state;
        Defined in parameters_execution_configuration.yml under header 'execution_config'

    Returns
    -------
    Tuple
        Returns train test split
    """
    X = df.drop("Subscription Status", axis=1)
    y = df["Subscription Status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=options["test_size"],
        random_state=options["random_state"],
        stratify=y,
    )

    return X_train, X_test, y_train, y_test


def train_model(
    X_train: pd.DataFrame, y_train: pd.DataFrame, model_config: Dict, options: Dict
) -> Tuple[BaseEstimator, Dict]:
    """
    Trains a model using Bayesian Optimization for hyperparameter tuning

    Parameters
    ----------
    X_train: pd.DataFrame
        Features of the training dataset

    Y_train: pd.DataFrame
        Targets of the training dataset

    model_config: Dict
        Defined in conf/base/parameters_model_config/*.yml under header '<model_header>'

    options: Dict
        Defined in parameters_execution_configuration.yml under header 'execution_config'
    """

    # Initialize model object
    model = _init_model(X_train, model_config, options)

    # Create dataset preprocessor object
    preprocessor = _build_preprocessor(X_train, model_config)

    # Pipes ColumnTransformer object to Pipeline object
    # When dataset is passed into the Pipeline object, the necessary dataset
    # preprocessing steps are applied before being fit to the model
    # Docs: https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html
    if preprocessor:
        model_to_tune = Pipeline(
            steps=[("preprocessor", preprocessor), ("model", model)]
        )
        prefix = (
            "model__"  # Pipeline object requires to add prefix in front of parameters
        )

    else:
        model_to_tune = model
        prefix = ""

    search_space = model_config.get("search_space", {})
    search_space = {f"{prefix}{k}": v for k, v in search_space.items()}
    param_grid = _parse_search_space(search_space)

    # Use StratifiedKFold over KFold due to imbalanced datset
    cv_strategy = StratifiedKFold(
        n_splits=options["cv_splits"],
        shuffle=True,
        random_state=options["random_state"],
    )

    bs = BayesSearchCV(
        estimator=model_to_tune,
        search_spaces=param_grid,
        cv=cv_strategy,
        scoring="f1",  # F1 is used due to class imbalance
        n_jobs=-1,
        verbose=0,
        n_iter=options["bayes_search_n_iters"],
        random_state=options["random_state"],
    )

    bs.fit(X_train, y_train)
    return bs.best_estimator_, bs.best_params_
