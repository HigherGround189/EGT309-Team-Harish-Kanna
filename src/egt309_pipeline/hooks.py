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
        """
        Prints Banner Text after Kedro Context is created (before pipeline is run)
        """

        # Created with https://www.patorjk.com/software/taag/#p=display&f=ANSI+Shadow&t=EGT309+TEAM%0AHarish+Kanna&x=none&v=4&h=4&w=80&we=false
        block_banner_text = """
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

        pipline_start_alert = "Pipeline Starting..."

        # Taken from https://uigradients.com/#SlightOceanView and https://uigradients.com/#Magic
        banner_colours = ["#a8c0ff", "#a17fe0", "#3f2b96"]
        text_colours = ["#a8c0ff", "#a17fe0"]

        console.print(
            Gradient(text=block_banner_text, colors=banner_colours),
            justify="center",
        )

        console.print(
            Gradient(text=pipline_start_alert, colors=text_colours),
            justify="center",
        )


class TrainingCompleteHook:
    @hook_impl
    def after_pipeline_run(self):
        """
        Sends a request to the visualisation server's /training-complete route.
        This is to update the server that the pipeline has completed (aka training is done),
        so that the server can requery the model metrics to display.
        """

        # The primary url should automatically resolve to the visualisation-server docker container, assuming the pipeline is ran in a container as well.
        # If the primary url can't be contacted (meaning that the pipeline is running outside a container), the fallback localhost url is used instead.
        primary_url = "http://visualisation-server:5500/training-complete"
        fallback_url = "http://localhost:5500/training-complete"

        try:
            response = requests.get(primary_url, timeout=3)
            response.raise_for_status()  # Raise error if request is unsucessful

            logger.info("Model Evaluation Completed! Sucessfully reloaded frontend!")

            # Prints banner text after pipeline ends (similar to start)
            # Created with https://www.patorjk.com/software/taag/#p=display&f=ANSI+Shadow&t=PIPELINE%0ACOMPLETE&x=none&v=4&h=4&w=80&we=false
            # Indentation might seem slightly messed up but it will display normally in container logs
            block_banner_text = """
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

            banner_colours = ["#a8c0ff", "#a17fe0", "#3f2b96"]
            text_colours = ["#a8c0ff", "#a17fe0"]

            console.print(
                Gradient(text=block_banner_text, colors=banner_colours),
                justify="center",
            )

            console.print(
                Gradient(text=visualisation_server_alert, colors=text_colours),
                justify="center",
                style="underline",
            )

        except Exception as exception:
            # If visualisation-server:5500 can't be reached, we can assume that the pipeline is being ran outside a container.
            # Hence, we will try localhost:5500 instead.

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
