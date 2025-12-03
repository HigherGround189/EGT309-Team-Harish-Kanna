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
    conf_loader = OmegaConfigLoader(
        conf_source=str(Path.cwd() / settings.CONF_SOURCE),
        **settings.CONFIG_LOADER_ARGS,
    )
    parameters = conf_loader["parameters"]

    nodes = []
    model_registry = parameters["model_registry"]
    for config in model_registry.values():
        if not config.get("evaluate_now", True):
            continue

        model_name = config["name"]
        nodes.append(
            Node(
                func=evaluate_model,
                inputs=[
                    f"{model_name}_model_weights",
                    "X_test",
                    "y_test",
                    "params:model_evaluation_parameters",
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
    return Pipeline(nodes)
