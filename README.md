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
├── saved_models                        <-- Models saved here after Evaluation 
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

### Prerequisites

- `docker` and `docker compose` must be installed.

### Steps to run Pipeline

1.  Clone the repository and navigate to the project directory:
    ```bash
    git clone https://github.com/HigherGround189/EGT309-Team-Harish-Kanna.git
    cd EGT309-Team-Harish-Kanna
    ```
2.  Run "run.sh". It will will automatically pull the images from DockerHub, and launch the containers. 
    ```bash
    ./run.sh
    ```
> **Note**: You may need to run `chmod +x run.sh` before running it.

`run.sh` 

If you want to <u>**build the images from source**</u> (instead of pulling images from DockerHub):
```bash
docker compose up --build
```

### Steps to launch Development Server

_Assuming that the repository is already cloned:_

1.  Run "dev.sh". It will will automatically pull the development server image from DockerHub, and launch the container. 
    ```bash
    ./dev.sh
    ```
> **Note**: You may need to run `chmod +x dev.sh` before running it.

If you want to <u>**build the image from source**</u> (instead of pulling it from DockerHub):
```bash
docker compose -f development.docker-compose.yml up --build
```

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



| Feature Names | Data Type | Issues Identified | Processing / Transformation Applied | Reason |
|:-------|:---------:|:-------:|:---------:|:-------:|
|`Client ID`| Category | No predictive value | Dropped | Identifier; Not useful for model |
|`Age`| Number | Text included ('years old'), outlier 150 | Removed 'years old' & Impute 150 | Standardization and correcting invalid value |
|`Occupation`| Category | Contained 'unknown' | Removed 'unknown' | Avoid meaningless category |
|`Marital Status`| Category | Contained 'unknown' | Removed 'unknown' | Avoid meaningless category |
|`Education Level`| Category | - | - | - |
|`Credit Default`| Category | High imbalance class | Dropped | Not useful for model |
|`Housing Loan`| Category | 60% missing data | Dropped | MCAR & Too huge number of missing values to be imputed fairly |
|`Personal Loan`| Category | 10% missing data | Impute nan | MCAR & Missing values handled with Random Distribution Imputation |
|`Contact Method`| Category | Inconsistent category naming ('cel' & 'Telephone') | Rename 'cel' with 'cellular' & 'Telephone' with 'telephone' | Standardization; Ensure clean processing |
|`Campaign Calls`| Number | Negative values present | Converted to positive with absolute | Negative values are invalid; Mirrored distribution (likely error in negative) |
|`Previous Contact Days`| Number | No association with Subscription Status | Dropped | Avoid meaningless feature |
|`Previously Contacted`| Boolean | Derived from Previous Contact Days | True if not 999; False if 999 | Clear indicator for model training |
|`Subscription Status`| Boolean | Text ('yes';'no') & heavily imbalanced | Convert to binary (True if 'yes'; False if 'no') | Target variable; Require stratified sampling during model training & Appropriate type conversion |

## Section G - Model Choice Overview

## Section H - Model Evaluation

## Section I - Model Deployment Considerations