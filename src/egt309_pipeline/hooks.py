import logging

import requests
from kedro.framework.hooks import hook_impl
from rich.console import Console
from rich_gradient import Gradient

logger = logging.getLogger(__name__)
console = Console(force_terminal=True, _environ={"COLUMNS": "112"}, color_system="256")


class DisplayBannerBeforePipelineRuns:
    @hook_impl
    def after_context_created(self):
        # Created with https://www.patorjk.com/software/taag/#p=display&f=ANSI+Shadow&t=EGT309+TEAM%0AHarish+Kanna&x=none&v=4&h=4&w=80&we=false
        banner_text = """
        ███████╗ ██████╗████████╗██████╗  ██████╗  █████╗     ████████╗███████╗ █████╗ ███╗   ███╗
        ██╔════╝██╔════╝╚══██╔══╝╚════██╗██╔═████╗██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
        █████╗  ██║  ███╗  ██║    █████╔╝██║██╔██║╚██████║       ██║   █████╗  ███████║██╔████╔██║
        ██╔══╝  ██║   ██║  ██║    ╚═══██╗████╔╝██║ ╚═══██║       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
        ███████╗╚██████╔╝  ██║   ██████╔╝╚██████╔╝ █████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
        ╚══════╝ ╚═════╝   ╚═╝   ╚═════╝  ╚═════╝  ╚════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝

        ██╗  ██╗ █████╗ ██████╗ ██╗███████╗██╗  ██╗    ██╗  ██╗ █████╗ ███╗   ██╗███╗   ██╗ █████╗
        ██║  ██║██╔══██╗██╔══██╗██║██╔════╝██║  ██║    ██║ ██╔╝██╔══██╗████╗  ██║████╗  ██║██╔══██╗
        ███████║███████║██████╔╝██║███████╗███████║    █████╔╝ ███████║██╔██╗ ██║██╔██╗ ██║███████║
        ██╔══██║██╔══██║██╔══██╗██║╚════██║██╔══██║    ██╔═██╗ ██╔══██║██║╚██╗██║██║╚██╗██║██╔══██║
        ██║  ██║██║  ██║██║  ██║██║███████║██║  ██║    ██║  ██╗██║  ██║██║ ╚████║██║ ╚████║██║  ██║
        ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝  ╚═╝
        """

        # Taken from https://uigradients.com/#SlightOceanView and https://uigradients.com/#Magic
        gradient_colours = ["#a8c0ff", "#a17fe0", "#3f2b96"]

        console.print(
            Gradient(text=banner_text, colors=gradient_colours), justify="center"
        )

        console.print(
            Gradient(text="Pipeline Starting...", colors=["#a8c0ff", "#a17fe0"]),
            justify="center",
        )


class TrainingCompleteHook:
    @hook_impl
    def after_pipeline_run(self):
        # The primary url should automatically resolve to the visualisation-server docker container, assuming the pipeline is ran in a container as well.
        # If the primary url can't be contacted (meaning that the pipeline is running outside a container), the fallback localhost url is used instead.
        primary_url = "http://visualisation-server:5500/training-complete"
        fallback_url = "http://localhost:5500/training-complete"

        try:
            response = requests.get(primary_url, timeout=3)
            response.raise_for_status()  # Raise error if request is unsucessful

            logger.info("Model Evaluation Completed! Sucessfully reloaded frontend!")

            # Created with https://www.patorjk.com/software/taag/#p=display&f=ANSI+Shadow&t=PIPELINE%0ACOMPLETE&x=none&v=4&h=4&w=80&we=false
            banner_text = """
            ██████╗ ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗
            ██╔══██╗██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝
           ██████╔╝██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗
           ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝
            ██║     ██║██║     ███████╗███████╗██║██║ ╚████║███████╗
            ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝             
                                                                                
              ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗████████╗███████╗
             ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚══██╔══╝██╔════╝
            ██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗     ██║   █████╗  
            ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝     ██║   ██╔══╝  
             ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗   ██║   ███████╗
              ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚══════╝
                                                                                                                          
            """

            visualisation_server_alert = """
            Visualisation Server running at
            http://127.0.0.1:5500/
            """

            gradient_colours = ["#a8c0ff", "#a17fe0", "#3f2b96"]

            console.print(
                Gradient(text=banner_text, colors=gradient_colours), justify="center"
            )

            console.print(
                Gradient(
                    text=visualisation_server_alert, colors=["#a8c0ff", "#a17fe0"]
                ),
                justify="center",
                style="underline",
            )

        except Exception as exception:
            logger.error(
                f"Can't contact visualisation-server container. Is the pipeline running inside a container? Falling back to localhost instead.\nException: {exception}"
            )

            try:
                response = requests.get(fallback_url, timeout=3)
                response.raise_for_status()
                return response.json()

            except Exception as exception:
                logger.error(
                    f"Can't contact Localhost. Is flask server running?\nException: {exception}"
                )
