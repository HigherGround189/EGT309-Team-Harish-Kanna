import json
import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def measure_error(y_true, y_pred, y_pred_proba, label):
    return pd.Series(
        {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred),
            "AUC": roc_auc_score(y_true, y_pred_proba),
        },
        name=label,
    )


def save_model_weights(save_dir, title, model):
    model_path = os.path.join(save_dir, f"{title}.pkl")
    joblib.dump(model, model_path)


def write_hyperparam_to_file(save_dir, best_params):
    params_path = os.path.join(save_dir, "parameters.json")
    with open(params_path, "w") as f:
        json.dump(best_params, f, indent=4)


def plot_auc_roc(save_dir, y, y_pred_proba):
    fpr, tpr, _ = roc_curve(y, y_pred_proba)
    auc_score = roc_auc_score(y, y_pred_proba)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"AUC = {auc_score:.2f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve: ")
    plt.legend(loc=4)

    plot_path = os.path.join(save_dir, "auc_roc.png")
    plt.savefig(plot_path)
    plt.close()


def plot_cm(save_dir, title, y, y_pred):
    cm = confusion_matrix(y, y_pred)

    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(cm, annot=True, fmt="d")
    labels = ["False", "True"]
    plt.title(f"Confusion Matrix: {title}")
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_ylabel("Actual")
    ax.set_xlabel("Predicted")

    plot_path = os.path.join(save_dir, "cmatrix.png")
    plt.savefig(plot_path)
    plt.close()


def save_model_scores(save_dir, y, y_pred, y_pred_proba):
    test_error = pd.concat([measure_error(y, y_pred, y_pred_proba, "test")], axis=1)
    test_error.to_csv(os.path.join(save_dir, "test_error.csv"))
