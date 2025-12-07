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

from .nodes import split_dataset, train_model


def create_pipeline(**kwargs) -> Pipeline:
    # Loader is used to load all configurations defined within the /conf/base/** dir
    conf_loader = OmegaConfigLoader(
        conf_source=str(Path.cwd() / settings.CONF_SOURCE),
        **settings.CONFIG_LOADER_ARGS,
    )
    parameters = conf_loader["parameters"]

    nodes = []
    nodes.append(
        # Node that splits the dataset into training and testing data
        Node(
            func=split_dataset,
            inputs=["cleaned_bmarket", "params:parameters_model_training"],
            outputs=["X_train", "X_test", "y_train", "y_test"],
            name="split_dataset_node",
        )
    )

    model_registry = parameters["model_registry_config"]
    for config in model_registry.values():
        if not config.get("train_now", True):
            continue

        config_name = config["model_config_key"]
        model_name = config["name"]
        # Creates a node for each model that has train_now=True
        nodes.append(
            Node(
                func=train_model,
                inputs=[
                    "X_train",
                    "y_train",
                    f"params:{config_name}",
                    "params:parameters_model_training",
                ],
                outputs=[f"{model_name}_model_weights", f"{model_name}_best_params"],
                name=f"train_{model_name}_node",
            )
        )

    return Pipeline(
        namespace="Model Training", prefix_datasets_with_namespace=False, nodes=nodes
    )
