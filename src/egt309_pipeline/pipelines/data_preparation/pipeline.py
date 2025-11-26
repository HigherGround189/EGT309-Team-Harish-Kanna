"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from .nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        Node(func=clean_clientId, 
             inputs="bmarket", 
             outputs="df_clientID_cleaned",
             name="clean_clientID_node"),

        Node(func=clean_age, 
             inputs="df_clientID_cleaned", 
             outputs="df_age_cleaned",
             name="clean_age_node"),
        
        Node(func=clean_occupation, 
             inputs="df_age_cleaned", 
             outputs="df_occupation_cleaned",
             name="clean_occupation_node"),

        Node(func=clean_maritalStatus, 
             inputs="df_occupation_cleaned", 
             outputs="df_maritalStatus_cleaned",
             name="clean_maritalStatus_node"),
        
        Node(func=clean_creditDefault, 
             inputs="df_maritalStatus_cleaned", 
             outputs="df_creditDefault_cleaned",
             name="clean_creditDefault_node"),

        Node(func=clean_housingLoan, 
             inputs="df_creditDefault_cleaned", 
             outputs="df_housingLoan_cleaned",
             name="clean_housingLoan_node"),
        
        Node(func=clean_personalLoan, 
             inputs="df_housingLoan_cleaned", 
             outputs="df_personalLoan_cleaned",
             name="clean_personalLoan_node"),

        Node(func=clean_contactMethod, 
             inputs="df_personalLoan_cleaned", 
             outputs="df_contactMethod_cleaned",
             name="clean_contactMethod_node"),
        
        Node(func=clean_campaignCalls, 
             inputs="df_contactMethod_cleaned", 
             outputs="df_campaignCalls_cleaned",
             name="clean_campaignCalls_node"),

        Node(func=clean_previousContactDays, 
             inputs="df_campaignCalls_cleaned", 
             outputs="df_previousContactDays_cleaned",
             name="clean_previousContactDays_node"),
        
        Node(func=clean_subscriptionStatus, 
             inputs="df_previousContactDays_cleaned", 
             outputs="cleaned_bmarket",
             name="clean_subscriptionStatus_node"),
    ])
