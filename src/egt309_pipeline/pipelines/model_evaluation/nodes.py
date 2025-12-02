"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 1.0.0
"""

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

#################
# Miscellaneous #
#################


def _measure_error(y_test, y_pred, y_proba):
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred, average="binary"),
        "micro_f1_score": f1_score(y_test, y_pred, average="micro"),
        "macro_f1_score": f1_score(y_test, y_pred, average="macro"),
        "weighted_f1_score": f1_score(y_test, y_pred, average="weighted"),
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


def _plot_permutation_importance(model, X_test, y_test, params):
    r = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=params["permutation_feature_importance_n_repeats"],
        random_state=params["random_state"],
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


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series, params):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = _measure_error(y_test, y_pred, y_proba)
    fig_cm = _plot_confusion_matrix(y_test, y_pred)
    fig_auc_roc = _plot_auc_roc(y_test, y_proba, metrics["auc_roc"])
    fig_fea = _plot_permutation_importance(model, X_test, y_test, params)

    return metrics, fig_cm, fig_auc_roc, fig_fea
