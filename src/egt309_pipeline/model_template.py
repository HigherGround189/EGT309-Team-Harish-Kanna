import os
import joblib
import pandas as pd

from skopt import BayesSearchCV
from sklearn.model_selection import GridSearchCV

from model_template_utils import (
    measure_error,
    write_hyperparam_to_file,
    plot_cm
)

class ModelWrapper:
    def __init__(self, title, model, hyperparameters, param_grid, cv, n_iterations=50):
        self.title = title
        self.model = model(**hyperparameters)
        self.param_grid = param_grid
        self.cv = cv
        self.n_iterations = n_iterations

        self.best_epoch = None
        self.best_params = None
        self.best_model = None

    def run_gridsearch(self, X, y):
        gs = GridSearchCV(
            estimator=self.model,
            param_grid=self.param_grid,
            cv=self.cv,
            scoring='f1',
            n_jobs=-1,
            verbose=2,
            return_train_score=True
        )

        gs.fit(X, y)

        self.best_params = gs.best_params_
        self.best_model = gs.best_estimator_
        if hasattr(gs.best_estimator_, 'n_estimators'):
            self.best_epoch = gs.best_estimator_.n_estimators
        else:
            self.best_epoch = getattr(gs.best_estimator_, 'n_iter_')

    def run_bayessearch(self, X, y):
        bs = BayesSearchCV(
            estimator=self.model,
            search_spaces=self.param_grid,
            cv=self.cv,
            scoring='f1', # Due to class imbalance
            n_jobs=-1,
            verbose=2,
            return_train_score=True,
            n_iter=self.n_iterations
        )

        bs.fit(X, y)

        self.best_params = bs.best_params_
        self.best_model = bs.best_estimator_
        if hasattr(bs.best_estimator_, 'n_estimators'):
            self.best_epoch = bs.best_estimator_.n_estimators
        else:
            self.best_epoch = getattr(bs.best_estimator_, 'n_iter_')

    def write_info_to_disk(self, X, y, folder_path):
        save_dir = os.path.join(folder_path, self.title)
        os.makedirs(save_dir, exist_ok=True)

        model_path = os.path.join(save_dir, f"{self.title}.pkl")
        joblib.dump(self.best_model, model_path)

        # Write hyperparameters in JSON file
        write_hyperparam_to_file(save_dir, self.best_params)

        y_pred = self.best_model.predict(X)

        # Plot confusion matrix
        plot_cm(y, y_pred, self.title, save_dir)

        # Save metrics in dataframe
        test_error = pd.concat([measure_error(y, y_pred, 'test')], axis=1)
        test_error.to_csv(os.path.join(save_dir, 'test_error.csv'))