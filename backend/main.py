from pathlib import Path

from flask import Flask, abort, jsonify, send_file, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="vue-dist/", static_url_path="")
socketio = SocketIO(app, cors_allowed_origins="*")

# Directory containing saved models
SAVED_MODEL_DIR = Path(__file__).parent / "saved_models"


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# List all models in SAVED_MODEL_DIR
@app.route("/api/models")
def list_models():
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
@app.route("/api/<model>/<filename>")
def serve_file(model, filename):
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


@app.route("/connection-test")
def connection_test():
    socketio.emit("connectionTest", {"message": "Hello from Flask!"})
    return "Event sent!"


@app.route("/training-complete")
def update_frontend():
    socketio.emit("trainingComplete", {"key": False})
    return "Updated Frontend that training is complete"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5500, debug=True, allow_unsafe_werkzeug=True)
