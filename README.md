# EGT309 Team Harish Kanna

## Section A - Contributers

## Section B - Folder Overview

## Section C - Execution Instructions

## Section D - Pipeline Design & Flow

## Section E - Overview & key findings from EDA 

### 1. Overview of Exploratory Data Analysis (EDA)
The dataset provided in this project comprises 41,188 records of bank marketing data containing client attributes and marketing campaign calls such as age, occupation, contact method and campaign calls. The primary objective of the analysis is to perform EDA to gain insights and findings into overall structure, quality and predictive usefulness of the features before training machine learning models.

The analysis examined the missingness patterns, outliers, distribution shapes, feature dependencies and the overall suitability of features for machine learning.

Advanced techniques such as MCAR assessment, mutual information analysis, and one hot aware feature selection were applied to identify meaningful features and determine the appropriate preprocessing strategy. These findings led to the decisions for imputation and feature engineering.

### 2. Key Findings
#### Null Handling
Missingness of the columns are evaluated using:
- Missingno visualization such as Dendrogram, Matrix and Heatmap
- Little MCAR Test
- Mutual Information between feature with missing values and other columns

All these evaluation results showed that the columns behaved closely as Missing Completely At Random (MCAR), meaning the missing values could not be reliably predicted using other variables (columns).

Therefore, the chosen imputation techniques were designed for independent practices:
- Random Distribution Imputation
- KNN Imputation (use as a variantion for model training)

#### Dependencies Analysis


#### Pre-feature Selection


#### Dealing with imbalance class


## Section F - Feature Processing



| Feature Names | Data Type | Issues Identified | Processing / Transformation Applied | Reason
|:-------|:---------:|:-------:|:---------:|:-------:|

## Section G - Model Choice Overview

## Section H - Model Evaluation

## Section I - Model Deployment Considerations