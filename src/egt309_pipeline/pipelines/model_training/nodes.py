"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 1.0.0
"""

import importlib
from typing import Any, Dict, Tuple

import GPUtil
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split
from skopt import BayesSearchCV
from skopt.space import Categorical, Integer, Real

#################
# Miscellaneous #
#################


def _parse_search_space(search_space: dict) -> Dict[str, Any]:
    bayes_search_params = {}
    for identifier, values in search_space.items():
        value_type = values["type"]

        if value_type == "Integer":
            bayes_search_params[identifier] = Integer(values["low"], values["high"])

        elif value_type == "Real":
            kwargs = {}
            if "prior" in values:
                kwargs["prior"] = values["prior"]
            bayes_search_params[identifier] = Real(
                values["low"], values["high"], **kwargs
            )

        elif value_type == "Categorical":
            categories = [v if v is not None else None for v in values["categories"]]
            bayes_search_params[identifier] = Categorical(categories)

    return bayes_search_params


def _get_model_class(class_path: str):
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

#########
# Nodes #
#########


def split_dataset(df: pd.DataFrame, options: dict) -> Tuple:
    X = df.drop("Subscription Status", axis=1)
    y = df["Subscription Status"]

    X = pd.get_dummies(X, drop_first=False)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=options["test_size"],
        random_state=options["random_state"],
        stratify=y,
    )

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, model_config: dict, options: dict):
    model_class = _get_model_class(model_config["class"])

    model_params = model_config["params"]
    if model_params.get("device") == "auto":
        device = "cuda" if GPUtil.getAvailable() else "cpu"
        model_params["device"] = device
        print(f"Selected: {device}")

    model = model_class(random_state=options["random_state"], **model_params)

    search_space = model_config["search_space"]
    param_grid = _parse_search_space(search_space)

    cv_strategy = StratifiedKFold(
        n_splits=options["cv_splits"],
        shuffle=True,
        random_state=options["random_state"],
    )

    bs = BayesSearchCV(
        estimator=model,
        search_spaces=param_grid,
        cv=cv_strategy,
        scoring="f1",  # Due to class imbalance
        n_jobs=-1,
        verbose=2,
        n_iter=options["n_iter"],
        random_state=options["random_state"],
    )

    bs.fit(X_train, y_train)
    return bs.best_estimator_, bs.best_params_

