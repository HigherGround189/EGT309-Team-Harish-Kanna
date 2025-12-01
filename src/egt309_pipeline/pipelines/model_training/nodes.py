"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 1.0.0
"""

import importlib
from typing import Any, Dict, Tuple

import GPUtil
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
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


def _measure_error(y_test, y_pred, y_proba):
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "auc_roc": roc_auc_score(y_test, y_proba),
    }


def _plot_confusion_matrix(y_test, y_pred):
    fig_cm = plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    ax = sns.heatmap(cm, annot=True, fmt="d")
    labels = ["False", "True"]
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_ylabel("Actual")
    ax.set_xlabel("Predicted")
    plt.close(fig_cm)

    return fig_cm


def _plot_auc_roc(y_test, y_proba, auc_score):
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig_roc = plt.figure(figsize=(8, 6))

    plt.plot(fpr, tpr, label=f"AUC = {auc_score:.2f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc=4)

    plt.close(fig_roc)
    return fig_roc


def _plot_permutation_importance(model, X_test, y_test, n_repeats=2, random_state=42):
    r = permutation_importance(
        model, X_test, y_test, n_repeats=n_repeats, random_state=random_state
    )

    perm_importance_df = pd.DataFrame(
        {
            "Feature": X_test.columns,
            "Importance": r.importances_mean,
            "Std": r.importances_std,
        }
    ).sort_values(by="Importance", ascending=False)

    fig_fea = plt.figure(figsize=(10, 6))

    sns.barplot(data=perm_importance_df, x="Importance", y="Feature")
    plt.tight_layout()

    plt.close(fig_fea)
    return fig_fea


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


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = _measure_error(y_test, y_pred, y_proba)
    fig_cm = _plot_confusion_matrix(y_test, y_pred)
    fig_auc_roc = _plot_auc_roc(y_test, y_proba, metrics["auc_roc"])
    fig_fea = _plot_permutation_importance(model, X_test, y_test)

    return metrics, fig_cm, fig_auc_roc, fig_fea
