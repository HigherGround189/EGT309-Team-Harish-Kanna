"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 1.0.0
"""

from pathlib import Path

from kedro.config import (
    OmegaConfigLoader,  # https://docs.kedro.org/en/0.19.10/api/kedro.config.OmegaConfigLoader.html
)
from kedro.framework.project import settings
from kedro.pipeline import Node, Pipeline

from .nodes import evaluate_model, split_dataset, train_model


def create_pipeline(**kwargs) -> Pipeline:
    conf_loader = OmegaConfigLoader(
        conf_source=str(Path.cwd() / settings.CONF_SOURCE),
        **settings.CONFIG_LOADER_ARGS,
    )
    parameters = conf_loader["parameters"]

    nodes = []
    nodes.append(
        Node(
            func=split_dataset,
            inputs=["cleaned_bmarket", "params:misc_options"],
            outputs=["X_train", "X_test", "y_train", "y_test"],
            name="split_dataset_node",
        )
    )

    model_registry = parameters["model_registry"]
    for config in model_registry.values():
        if not config.get("train_now", True):
            continue

        config_name = config["yaml_header"]
        model_name = config["name"]
        nodes.append(
            Node(
                func=train_model,
                inputs=[
                    "X_train",
                    "y_train",
                    f"params:{config_name}",
                    "params:misc_options",
                ],
                outputs=[f"{model_name}_model_weights", f"{model_name}_best_params"],
                name=f"train_{model_name}_node",
            )
        )

        nodes.append(
            Node(
                func=evaluate_model,
                inputs=[f"{model_name}_model_weights", "X_test", "y_test"],
                outputs=[
                    f"{model_name}_metrics",
                    f"{model_name}_confusion_matrix",
                    f"{model_name}_auc_roc_curve",
                    f"{model_name}_feature_importance",
                ],
                name=f"evaluate_{model_name}_node",
            )
        )

    return Pipeline(nodes)
