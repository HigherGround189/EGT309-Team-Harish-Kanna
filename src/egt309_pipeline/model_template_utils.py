import os
import json

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
  )

def measure_error(y_true, y_pred, label):
    return pd.Series({
        'accuracy':accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred)},
        name=label)

def write_hyperparam_to_file(save_dir, best_params):
    params_path = os.path.join(save_dir, 'parameters.json')
    with open(params_path, 'w') as f:
        json.dump(best_params, f, indent=4)

def plot_cm(y, y_pred, title, save_dir):
    cm = confusion_matrix(y, y_pred)

    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(cm, annot=True, fmt='d')
    labels = ["False", "True"]
    plt.title(f"Confusion Matrix: {title}")
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_ylabel("Actual")
    ax.set_xlabel("Predicted")

    plot_path = os.path.join(save_dir, 'cmatrix.png')
    plt.savefig(plot_path)
    plt.close()