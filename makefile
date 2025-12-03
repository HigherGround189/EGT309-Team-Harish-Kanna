.PHONY: data-prep train eval train_eval all

# Default to uv
RUN = uv run

# Alternative options:
# uv:					RUN = uv run (default)
# Conda: 				RUN = conda run -n <your conda env>
# Normal venv:          RUN = .venv/bin/python -m (Linux/macOS)
#                       RUN = .venv\Scripts\python.exe -m (Windows)

FULL_TRAINING = train eval

data-prep:
	$(RUN) kedro run --pipeline data_preparation

train:
	$(RUN) kedro run --pipeline model_training

eval:
	$(RUN) kedro run --pipeline model_evaluation

train_eval:
	$(FULL_TRAINING)

all:
	$(RUN) kedro run