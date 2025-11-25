"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 1.0.0
"""

from kedro.config import OmegaConfigLoader
from kedro.io import DataCatalog
import pandas as pd
import logging

# Logger Config
logger = logging.getLogger(__name__)
logger.warning("Issue warning")
logger.info("Send information")
logger.debug("Useful information for debugging")

# Define catalog to load dataset
conf_loader = OmegaConfigLoader(conf_source="conf", base_env="base", default_run_env="local")
conf_catalog = conf_loader["catalog"]
catalog = DataCatalog.from_config(conf_catalog)
