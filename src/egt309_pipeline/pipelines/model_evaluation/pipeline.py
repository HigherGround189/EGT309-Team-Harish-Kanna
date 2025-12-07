"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 1.0.0
"""

from pathlib import Path

from kedro.config import (
    OmegaConfigLoader,  # https://docs.kedro.org/en/0.19.10/api/kedro.config.OmegaConfigLoader.html
)
from kedro.framework.project import settings
from kedro.pipeline import Node, Pipeline  # noqa

from .nodes import evaluate_model


def create_pipeline(**kwargs) -> Pipeline:
    # Loader is used to load all configurations defined within the /conf/base/** dir
    conf_loader = OmegaConfigLoader(
        conf_source=str(Path.cwd() / settings.CONF_SOURCE),
        **settings.CONFIG_LOADER_ARGS,
    )
    parameters = conf_loader["parameters"]

    nodes = []
    model_registry = parameters["model_registry_config"]
    for config in model_registry.values():
        if not config.get("evaluate_now", True):
            continue

        model_name = config["name"]
        # Create nodes to evaluate trained model on test data
        nodes.append(
            Node(
                func=evaluate_model,
                inputs=[
                    f"{model_name}_model_weights",
                    "X_test",
                    "y_test",
                    "params:parameters_model_evaluation",
                ],
                outputs=[
                    f"{model_name}_metrics",
                    f"{model_name}_confusion_matrix",
                    f"{model_name}_auc_roc_curve",
                    f"{model_name}_feature_importance",
                ],
                name=f"evaluate_{model_name}_node",
            )
        )
    return Pipeline(
        namespace="Model Evaluation", prefix_datasets_with_namespace=False, nodes=nodes
    )
