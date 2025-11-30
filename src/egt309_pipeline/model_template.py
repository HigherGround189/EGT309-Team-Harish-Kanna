import os

from model_template_utils import *
from sklearn.model_selection import GridSearchCV
from skopt import BayesSearchCV


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
            scoring="f1",  # Due to class imbalance
            n_jobs=-1,  # Use all CPU threads
            verbose=2,
            return_train_score=True,
        )

        gs.fit(X, y)

        self.best_params = gs.best_params_
        self.best_model = gs.best_estimator_
        if hasattr(gs.best_estimator_, "n_estimators"):
            self.best_epoch = gs.best_estimator_.n_estimators
        else:
            self.best_epoch = getattr(gs.best_estimator_, "n_iter_")

    def run_bayessearch(self, X, y):
        bs = BayesSearchCV(
            estimator=self.model,
            search_spaces=self.param_grid,
            cv=self.cv,
            scoring="f1",  # Due to class imbalance
            n_jobs=-1,  # Use all CPU threads
            verbose=2,
            return_train_score=True,
            n_iter=self.n_iterations,
        )

        bs.fit(X, y)

        self.best_params = bs.best_params_
        self.best_model = bs.best_estimator_
        if hasattr(bs.best_estimator_, "n_estimators"):
            self.best_epoch = bs.best_estimator_.n_estimators
        else:
            self.best_epoch = getattr(bs.best_estimator_, "n_iter_")

    def write_info_to_disk(self, X, y, folder_path):
        # Create new folder
        save_dir = os.path.join(folder_path, self.title)
        os.makedirs(save_dir, exist_ok=True)

        # Save model weights
        save_model_weights(save_dir=save_dir, title=self.title, model=self.best_model)

        # Write hyperparameters in JSON file
        write_hyperparam_to_file(save_dir=save_dir, best_params=self.best_params)

        y_pred = self.best_model.predict(X)

        # Plot confusion matrix
        plot_cm(save_dir=save_dir, title=self.title, y=y, y_pred=y_pred)

        # Save metrics in dataframe
        save_model_scores(save_dir=save_dir, y=y, y_pred=y_pred)
