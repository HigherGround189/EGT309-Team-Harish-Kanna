from flask import Flask, jsonify, send_file, abort
from pathlib import Path

app = Flask(__name__, static_folder="dist")

# Directory containing saved models
SAVED_MODEL_DIR = Path(__file__).parent / "saved_models"

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

        # Collect all files in each model folder (guard against directories, although there shouldn't be any)
        files = [f.name for f in model_folder.iterdir() if f.is_file()]

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

if __name__ == "__main__":
    app.run(debug=True)
