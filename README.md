# EGT309 Team Harish Kanna

## Section A - Contributors

### Leong Jun Hoe - 230633N@mymail.nyp.edu.sg
- Data Preprocessing
- Feature Analysis
- Feature Engineering 

### Lee Ying Ray - 233466E@mymail.nyp.edu.sg
- Pipeline Development
- Pipeline Containerisation
- Repository Automation

### Zhang Zhe Xiang - 232842C@mymail.nyp.edu.sg
- Model Training
- Model Tuning
- Model Evaluation

## Section B - Folder Overview
```
EGT309-Team-Harish-Kanna                Folder Explanations:
├── conf                                <-- Pipeline Configuration
│   ├── base
│   │   └──parameters_model_config      <-- Model Parameter Configuration
│   └── local
├── data                                <-- Pipeline Data
│   ├── 01_raw
│   ├── 02_intermediate
│   ├── 03_primary
│   ├── 04_feature
│   ├── 05_model_input
│   ├── 06_models
│   ├── 07_model_output
│   └── 08_reporting
├── notebooks
├── saved_models                        <-- Models Trained & Evaluated 
│   ├── AdaBoostClassifier
│   ├── CatBoostClassifier
│   ├── LightGBMClassifier
│   ├── RandomForestClassifier
│   └── XGBoostClassifier
├── src
│   └── egt309_pipeline
│       └── pipelines                   <-- Individual Namespaced Pipelienes
│           ├── data_preparation
│           ├── model_evaluation
│           └── model_training
└── visualisation-server                <-- Webapp to view Model Results
```

## Section C - Execution Instructions

## Section D - Pipeline Design & Flow

## Section E - Overview & key findings from Exploratory Data Analysis (EDA) 
### 1. Overview of EDA
The dataset provided in this project comprises 41,188 records of bank marketing data containing client attributes and marketing campaign calls such as age, occupation, contact method and campaign calls. The primary objective of the analysis is to perform EDA to gain insights and findings into overall structure, quality and predictive usefulness of the features before training machine learning models.

The analysis examined the missingness, outliers, distribution, feature dependencies and the overall suitability of features for machine learning. Advanced techniques such as MCAR assessment, mutual information analysis, and one hot aware feature selection were applied to guide appropriate imputation, preprocessing and feature engineering.

### 2. Key Findings of EDA
#### Null Handling
Missingness of the columns were evaluated using:
- Missingno visualization such as Dendrogram, Matrix and Heatmap
- Little MCAR Test
- Mutual Information between feature with missing values and other columns

All these evaluation results showed that the columns behaved closely as Missing Completely At Random (MCAR), meaning the missing values could not be reliably predicted using other variables.

Therefore, the chosen imputation techniques were designed for independent practices:
- Random Distribution Imputation
- KNN Imputation (use as a variantion for model training)

#### Dependencies Analysis
Statistical techniques were also conducted for relationship checking:
- Pairwise Correlation (Numeric)
- Mutual Information
- Chi Square Test

Most features showed low but non-zero dependency with the target (Subscription Status), indicating weak but potentially useful predictive signals. The features also have non-linear relationships, including numeric.

#### Pre-feature Selection
Mutual information combined with SelectKBest and SelectPercentile was applied on integer and one hot encoded features separately. Across all four approaches, Previously Contacted, Contact Method and Campaign Calls consistently ranked as most important. Certain values of Marital Status (married and single) and levels of education also contributed to prediction values for the target, indicating that both demographic and campaign-related attributes are useful for predicting subscription behaviour.

#### Dealing with imbalance class
Analyzing the class ditribution of Subscription Status, there is a huge imbalance 88.7% (No) and 11.3% (Yes), suggesting the need for techniques like SMOTE or stratified sampling during model training. 


## Section F - Feature Processing



| Feature Names | Data Type | Issues Identified | Processing / Transformation Applied | Reason
|:-------|:---------:|:-------:|:---------:|:-------:|

## Section G - Model Choice Overview

## Section H - Model Evaluation

## Section I - Model Deployment Considerations