import logging

import requests
from kedro.framework.hooks import hook_impl

logger = logging.getLogger(__name__)


class TrainingCompleteHook:
    @hook_impl
    def after_pipeline_run(self):
        # The primary url should automatically resolve to the visualisation-server docker container, assuming the pipeline is ran in a container as well.
        # If the primary url can't be contacted (meaning that the pipeline is running outside a container), the fallback localhost url is used instead.
        primary_url = "http://visualisation-server:5500/training-complete"
        fallback_url = "http://localhost:5500/training-complete"

        try:
            response = requests.get(primary_url, timeout=10)
            response.raise_for_status()  # Raise error if request is unsucessful

            logger.info("Model Evaluation Completed! Sucessfully reloaded frontend!")

        except Exception as exception:
            logger.error(
                f"Can't contact visualisation-server container. Is the pipeline running inside a container? Falling back to localhost instead.\nException: {exception}"
            )

            try:
                response = requests.get(fallback_url, timeout=10)
                response.raise_for_status()
                return response.json()

            except Exception as exception:
                logger.error(
                    f"Can't contact Localhost. Is flask server running?\nException: {exception}"
                )
