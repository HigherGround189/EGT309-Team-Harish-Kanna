"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 1.0.0
"""

import importlib
import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

import GPUtil
import pandas as pd
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
    bayes_search_params = {}
    for identifier, values in search_space.items():
        value_type = values["type"]

        if value_type == "Integer":
            bayes_search_params[identifier] = Integer(values["low"], values["high"])

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


def _get_model_class(class_path: str):
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

def _init_model(X_train, model_config: dict, options: dict) -> Any:
    model_class = _get_model_class(model_config["class"])

    model_params = model_config.get("model_params", {})

    if model_params.get("device") == "auto":
        device = "cuda" if GPUtil.getAvailable() else "cpu"
        model_params["device"] = device
        logger.debug(f"Selected: {device}")

    if model_config["class"] == "catboost.CatBoostClassifier":
        model_params["cat_features"] = X_train.select_dtypes(include=["object", "category"]).columns.tolist()
        model_config["data_encoding"] = None
        logger.debug("Added categorical cat_features")

    return model_class(random_state=options["random_state"], **model_params)

def _build_preprocessor(X_train, model_config: dict) -> ColumnTransformer:
    categorical_cols = X_train.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    numerical_cols = X_train.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    preprocessing_steps = []
    data_encoding = model_config.get("data_encoding", "ohe").lower()

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

    elif data_encoding == None:
        logger.debug("Skipped encoding")
        pass

    if model_config.get("requires_scaling", False):
        scaling_transformer = ("scaler", StandardScaler(), numerical_cols)
        preprocessing_steps.append(scaling_transformer)
        logger.debug("Applied Standard Scaling")

    return ColumnTransformer(transformers=preprocessing_steps, remainder="passthrough", n_jobs=-1)

#########
# Nodes #
#########


def split_dataset(df: pd.DataFrame, options: dict) -> Tuple:
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


def train_model(X_train, y_train, model_config: dict, options: dict):

    model = _init_model(X_train, model_config, options)
    preprocessor = _build_preprocessor(X_train, model_config)

    # https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html
    if preprocessor:
        model_to_tune = Pipeline(
            steps=[("preprocessor", preprocessor), ("model", model)]
        )
        prefix = "model__"

    else:
        model_to_tune = model
        prefix = ""

    search_space = model_config.get("search_space", {})
    search_space = {f"{prefix}{k}": v for k, v in search_space.items()}
    param_grid = _parse_search_space(search_space)

    cv_strategy = StratifiedKFold(
        n_splits=options["cv_splits"],
        shuffle=True,
        random_state=options["random_state"],
    )

    bs = BayesSearchCV(
        estimator=model_to_tune,
        search_spaces=param_grid,
        cv=cv_strategy,
        scoring="f1",  # Due to class imbalance
        n_jobs=-1,
        verbose=0,
        n_iter=options["bayes_search_n_iters"],
        random_state=options["random_state"],
    )

    bs.fit(X_train, y_train)
    return bs.best_estimator_, bs.best_params_
