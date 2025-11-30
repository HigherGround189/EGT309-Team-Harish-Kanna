"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 1.0.0
"""

import logging

logger = logging.getLogger(__name__)

from typing import Any, Tuple, Union

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Define catalog to load dataset
# conf_loader = OmegaConfigLoader(
#     conf_source="conf", base_env="base", default_run_env="local"
# )
# conf_catalog = conf_loader["catalog"]
# catalog = DataCatalog.from_config(conf_catalog)

def _my_knnimputer(df: pd.DataFrame, target_col: str, target_val: Any=None, corr_cols: list=None, n_neighbors: int=5):
  """
  Impute target values such as missing data with KNN
  Ensure all columns in corr_cols are encoded or numeric

  paramters:
  ----------
  df: pd.DataFrame
    Input DataFrame

  target_col: str
    Column to be impute

  target_val: Any
    Value in target column to be impute

  corr_cols: list
    Correlated columns to assist in KNN imputation
  
  n_neighbors: int
    Set the number of similar groups (nearest neighbours) to look 
    at when estimating a missing value.
  """
  df_copy = df.copy()
  imputer = KNNImputer(n_neighbors=n_neighbors)

  if target_val is not None:
    df_copy[target_col] = df_copy[target_col].replace({target_val: np.nan})

  if corr_cols is not None:
    final_corr_cols = corr_cols if target_col in corr_cols else corr_cols.append(target_col)
    df_copy[final_corr_cols] = imputer.fit_transform(df_copy[final_corr_cols])
  else:
    df_copy[target_col] = imputer.fit_transform(df_copy[[target_col]])

  return df_copy


def _random_distribution(
    df: pd.DataFrame, target_col: str, target_val: Any = None
) -> pd.DataFrame:
    """
    Apply random distribution imputation to selected column

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame

    target: str
        Selected column to impute

    target_val: Any
        Selected value (data) to be impute
        input: "none" (default) or specific value from column
        example:
        "none"    : imputes all the np.nan or None in specified column
        150       : imputes all values with 150 in the specified column
        "unknown" : imputes all values with unknown in the specified column
    """
    df_temp = df.copy()
    col = df_temp[target_col]
    if target_val is None:
        temp_col = col[~col.isna()]
        tobe_fill = col.isna()
    else:
        temp_col = col[col != target_val]
        tobe_fill = col == target_val
    distribution = temp_col.value_counts(normalize=True).tolist()
    labels = temp_col.value_counts().index.tolist()
    fill_mask = tobe_fill
    fill = np.random.choice(labels, size=fill_mask.sum(), p=distribution)  # type: ignore
    df_temp.loc[fill_mask, target_col] = fill
    return df_temp


def _reindex_target_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Move position of Subscription Status column (target/label) to the back

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    cols = df.columns.tolist()
    cols.remove("Subscription Status")
    cols.append("Subscription Status")
    df_reorganized = df.reindex(columns=cols)
    return df_reorganized


def clean_clientId(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Client ID column
    Function action: Drop Client Id column

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.drop("Client ID", axis=1)
    return df_new


def extract_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Age column
    Function actions: Remove 'years' and keep the age number as integer

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_temp = df.copy()
    df_temp["Age"] = df_temp["Age"].map(lambda x: x.split()[0])
    df_temp["Age"] = df_temp["Age"].astype(int)
    return df_temp

def impute_age(df: pd.DataFrame, impute_method: str = "randdist") -> pd.DataFrame:
    """
    Impute the value 150 in Age.
    This function includes two techniques of imputing are random distribution and KNN
    1. Random Distribution can be applied right after extract age
    2. (!) KNN can only be applied after all the data cleaning is completed (!)
        interger encoding will be performed only within KNN automatically

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame

    impute_method: str
        "randdist" (default) or "knn"
            randdist: random distribution imputation
            knn: KNN imputation
    """
    df_temp = df.copy()
    match impute_method:
        case "randdist":
            df_new = _random_distribution(df_temp, target_col="Age", target_val=150)
    
        case "knn":
            corr_cols = ['Occupation', 'Marital Status', 'Education Level', 'Subscription Status','Previous Contact Days']
            df_encoded_temp = int_encode(df_temp)
            df_new = _my_knnimputer(df_encoded_temp, target_col="Age", target_val=150, corr_cols=corr_cols) 

    return df_new


def clean_occupation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Occupation column
    Function action: Drop rows with 'unknown'

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.drop(df[df["Occupation"] == "unknown"].index, axis=0)
    return df_new


def clean_maritalStatus(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Marital Status column
    Function action: drop rows with 'unknown'

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.drop(df[df["Marital Status"] == "unknown"].index, axis=0)
    return df_new


def clean_creditDefault(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Credit Default column
    Function action: 'Drop Credit Default Column

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.drop("Credit Default", axis=1)
    return df_new


def clean_housingLoan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Housing Loan column
    Function action: Drop Housing Loan Column

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.drop("Housing Loan", axis=1)
    return df_new


def clean_personalLoan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Personal Loan column
    Function action: Apply random distribution imputation to Personal Loan column

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_temp = df.copy()
    df_new = _random_distribution(df_temp, target="Personal Loan")
    return df_new


def clean_contactMethod(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Contact Method column
    Function action: Rename 'Cell' value with 'cellular' and 'Telephone' with 'telephone'

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.copy()
    df_new["Contact Method"].replace(
        ["Cell", "Telephone"], ["cellular", "telephone"], inplace=True
    )
    return df_new


def clean_campaignCalls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Campaign Calls column
    Function action: Absolute/Convert all negative values to positive

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.copy()
    df_new["Campaign Calls"] = df_new["Campaign Calls"].apply(lambda x: abs(x))
    return df_new


def clean_previousContactDays(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Previous Contact Days column
    Function action: Rename 999 to -1 and added a Previously Contacted column
                    as boolean:
                    False = no prior contact
                    True = got prior contact

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.copy()
    df_new["Previously Contacted"] = df_new["Previous Contact Days"] != 999
    df_new.replace({"Previous Contact Days": 999}, -1, inplace=True)
    df_new = _reindex_target_col(df_new)
    return df_new


def clean_subscriptionStatus(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning on Subscription Status column
    Function action: Rename 'yes' with 1 and 'no' with 0 and convert to boolean type

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    df_new = df.copy()
    df_new["Subscription Status"].replace({"yes": 1, "no": 0}, inplace=True)
    df_new["Subscription Status"] = df_new["Subscription Status"].astype(bool)
    return df_new


def encoder_selection(encoder: str = "ohe") -> Union[OneHotEncoder, LabelEncoder]:
    """
    Select One Hot Encoding or Integer Encoding method

    parameters:
    -----------
    encoder: "ohe" (default) or "int"
        ohe: one hot encoding
        int: integer encoding
    """
    match encoder:
        case "ohe":
            encoder = OneHotEncoder()
        case "int":
            encoder = LabelEncoder()
        case _:
            raise ValueError("encoder must be 'ohe' or 'int'")
    return encoder


def ohe_encode(df: pd.DataFrame) -> pd.DataFrame:
    """
    One hot encode all object type columns in input DataFrame

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    encoder = encoder_selection("ohe")
    df_copy = df.copy()
    df_encode = pd.DataFrame(index=df_copy.index)

    for col in df_copy.columns:
        if df_copy[col].dtype == "object":
            encoded = encoder.fit_transform(df_copy[[col]])
            value_col = encoder.get_feature_names_out([col])
            encoded_df = pd.DataFrame(encoded, columns=value_col, index=df_copy.index)
            df_encode = pd.concat([df_encode, encoded_df], axis=1)
        else:
            df_encode[col] = df_copy[col]
    return df_encode


def int_encode(df: pd.DataFrame) -> pd.DataFrame:
    """
    Integer encode all object type columns in input DataFrame

    parameters:
    -----------
    df: pd.DataFrame
        Input DataFrame
    """
    encoder = encoder_selection("int")
    df_copy = df.copy()
    df_encode = pd.DataFrame(index=df_copy.index)

    for col in df_copy.columns:
        if df_copy[col].dtype == "object":
            df_encode[col] = encoder.fit_transform(df_copy[col])
        else:
            df_encode[col] = df_copy[col]
    return df_encode


def my_train_test_split(
    df: pd.DataFrame, val_sample: bool = False, test_size: int = 0.2, rs: int = 42
) -> Union[
    Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series],
]:
    """
    Split input DataFrame into train, test and val(optional)

    parameters:
    -----------
    df: pd.DataFrame
      Input DataFrame

    val_sample: bool
      State whether to generate validation data sample

    test_size: int
      State the size of test dataset

    rs: int
      Set random state for randomness
    """
    label = "Subscription Status"
    X, y = df.drop(label, axis=1), df[label]
    if val_sample:
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=test_size, random_state=rs, stratify=y
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=rs, stratify=y_temp
        )
        return X_train, X_val, X_test, y_train, y_val, y_test

    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=rs, stratify=y
        )
        return X_train, X_test, y_train, y_test


def smote(
    X_train: pd.DataFrame, y_train: pd.Series, rs: int = 42
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Apply SMOTE to training dataset

    X_train: pd.DataFrame
      Input features training dataset

    y_train: pd.Series
      Input label training dataset

    rs: int
      Set random state for randomness
    """
    smote = SMOTE(random_state=rs)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    X_train_res, y_train_res = pd.DataFrame(X_train_res), pd.Series(y_train_res)
    return X_train_res, y_train_res