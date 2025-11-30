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
)


def measure_error(y_true, y_pred, label):
    return pd.Series(
        {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred),
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


def save_model_scores(save_dir, y, y_pred):
    test_error = pd.concat([measure_error(y, y_pred, "test")], axis=1)
    test_error.to_csv(os.path.join(save_dir, "test_error.csv"))
