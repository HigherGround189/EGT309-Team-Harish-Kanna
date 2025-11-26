"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 1.0.0
"""

import logging

logger = logging.getLogger(__name__)

from kedro.config import OmegaConfigLoader
from kedro.io import DataCatalog

import numpy as np

# Define catalog to load dataset
conf_loader = OmegaConfigLoader(
    conf_source="conf", base_env="base", default_run_env="local"
)
conf_catalog = conf_loader["catalog"]
catalog = DataCatalog.from_config(conf_catalog)


def random_distribution(df, target, val="none"):
    df_temp = df.copy()
    col = df_temp[target]
    if val == "none":
        temp_col = col[~col.isna()]
        tobe_fill = col.isna()
    else:
        temp_col = col[col != val]
        tobe_fill = col == val
    distribution = temp_col.value_counts(normalize=True).tolist()
    labels = temp_col.value_counts().index.tolist()
    fill_mask = tobe_fill
    fill = np.random.choice(labels, size=fill_mask.sum(), p=distribution)  # type: ignore
    df_temp.loc[fill_mask, target] = fill
    return df_temp


def reindex_target_col(df):
    cols = df.columns.tolist()
    cols.remove("Subscription Status")
    cols.append("Subscription Status")
    df_reorganized = df.reindex(columns=cols)
    return df_reorganized


def clean_clientId(df):
    df_new = df.drop("Client ID", axis=1)
    return df_new


def clean_age(df):
    df_temp = df.copy()
    df_temp["Age"] = df_temp["Age"].map(lambda x: x.split()[0])
    df_temp["Age"] = df_temp["Age"].astype(int)
    df_new = random_distribution(df_temp, target="Age", val=150)
    return df_new


def clean_occupation(df):
    df_new = df.drop(df[df["Occupation"] == "unknown"].index, axis=0)
    return df_new


def clean_maritalStatus(df):
    df_new = df.drop(df[df["Marital Status"] == "unknown"].index, axis=0)
    return df_new


def clean_creditDefault(df):
    df_new = df.drop("Credit Default", axis=1)
    return df_new


def clean_housingLoan(df):
    df_new = df.drop("Housing Loan", axis=1)
    return df_new


def clean_personalLoan(df):
    df_temp = df.copy()
    df_new = random_distribution(df_temp, target="Personal Loan")
    return df_new


def clean_contactMethod(df):
    df_new = df.copy()
    df_new["Contact Method"].replace(
        ["Cell", "Telephone"], ["cellular", "telephone"], inplace=True
    )
    return df_new


def clean_campaignCalls(df):
    df_new = df.copy()
    df_new["Campaign Calls"] = df_new["Campaign Calls"].apply(lambda x: abs(x))
    return df_new


def clean_previousContactDays(df):
    df_new = df.copy()
    df_new["Previously Contacted"] = df_new["Previous Contact Days"] != 999
    df_new.replace({"Previous Contact Days": 999}, -1, inplace=True)
    df_new = reindex_target_col(df_new)
    return df_new


def clean_subscriptionStatus(df):
    df_new = df.copy()
    df_new["Subscription Status"].replace({"yes": 1, "no": 0}, inplace=True)
    df_new["Subscription Status"] = df_new["Subscription Status"].astype(bool)
    return df_new
