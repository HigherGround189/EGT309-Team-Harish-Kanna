FULL_TRAINING = train eval
ALL_STEPS = prepare $(FULL_TRAINING)

.PHONY: data-prep train eval train_eval all

data-prep:
	uv run kedro run --pipeline data_preparation

train:
	uv run kedro run --pipeline model_training

eval:
	uv run kedro run --pipeline model_evaluation

train_eval:
	$(FULL_TRAINING)

all:
	$(ALL_STEPS)