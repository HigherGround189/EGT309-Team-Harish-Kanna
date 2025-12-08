# Written by Lee Ying Ray (233466E)
# Autoformatted & Linted with Ruff
# Docstrings follow Google's Python Docstring Format

from pathlib import Path

from flask import Flask, abort, jsonify, send_file, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="vue-dist/", static_url_path="")
socketio = SocketIO(app, cors_allowed_origins="*")

# Directory containing saved models
SAVED_MODEL_DIR = Path(__file__).parent / "saved_models"

# To track if training has finished
current_training_status = "ongoing"


# Home Route
@app.route("/", methods=["GET"])
def index():
    """
    Home Route for app. Returns index.html from the static_folder "vue-dist".
    """
    return send_from_directory(app.static_folder, "index.html")


# Check current training status
@app.route("/api/training-status", methods=["GET"])
def training_status():
    """
    Route for frontend to check current model training status.

    Returns:
        JSON: A JSON object containing a key-value pair of the current Training Status ("ongoing" | "completed")
    """
    return jsonify({"Training status": current_training_status})


# List all models in SAVED_MODEL_DIR
@app.route("/api/models", methods=["GET"])
def list_models():
    """
    Retrieve all models, including all urls for model resources

    Returns:
        JSON: A JSON object containing all models and their resources
        Return Example:
        {
            "RandomForestClassifier": {
                "RandomForestClassifier_auc_roc_curve.png": "/api/RandomForestClassifier_auc_roc_curve.png",
                "RandomForestClassifier_metrics.json": "/api/RandomForestClassifier_metrics.json",
            }
        }

    Route Example:
        GET /api/models
    """
    models = {}

    # Example:
    # saved_models/
    # ├── RandomForestClassifier/
    # └── XGBoostClassifier/
    # In this case, the following loop would iterate through "RandomForestClassifier/" and "XGBoostClassifier/"
    for model_folder in SAVED_MODEL_DIR.iterdir():
        # Skip file if not directory (shouldn't happen, but good to have in case)
        if not model_folder.is_dir():
            continue

        model_name = model_folder.name

        # Collect all files in each model folder (guard against directories & .pkl files, although there shouldn't be any)
        files = [
            file.name
            for file in model_folder.iterdir()
            if file.is_file() and file.suffix != ".pkl"
        ]

        # Construct API Urls for frontend to fetch
        file_urls = {file: f"/api/{model_name}/{file}" for file in files}
        models[model_name] = file_urls

    return jsonify(models)


# Dyanmic route for serving files (eg: parameters.json)
@app.route("/api/<model>/<filename>", methods=["GET"])
def serve_file(model: str, filename: str):
    """
    Dyanamically returns requested file.

    Args:
        model (str): The model which the filename belongs to.
        filename (str): The file being requested

    Returns:
        Response: A response object containing the file data.

    Route Example:
        GET /api/RandomForestClassifier/RandomForestClassifier_metrics.json
    """
    # Create path for specific Model (eg: SAVED_MODEL_DIR/XGBoost/)
    model_dir = SAVED_MODEL_DIR / model

    # Check if the Model directory actually exists
    if not model_dir.exists():
        abort(404, f"Model {model} not found")

    # Create path for specific File being requested (eg: SAVED_MODEL_DIR/XGBoost/parameters.json)
    file_path = model_dir / filename

    # Check if specific File actually exists
    if not file_path.exists():
        abort(404, f"File {filename} not found for model {model}")

    return send_file(file_path)


# Notify frontend via websockets if training has completed
@app.route("/training-complete", methods=["GET"])
def update_frontend():
    """
    Emits websocket event to notify frontend that training is complete

    Returns:
        Str: Message indicating frontend is updated.
    """
    global current_training_status
    current_training_status = "completed"
    socketio.emit("trainingComplete", {"key": current_training_status})
    return "Updated Frontend that training is complete"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5500, debug=True, allow_unsafe_werkzeug=True)
