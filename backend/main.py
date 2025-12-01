from flask import Flask, jsonify, send_from_directory, abort
from pathlib import Path

app = Flask(__name__, static_folder="dist")

# Directory containing saved models
MODEL_DIR = Path(__file__).parent / "saved_models"

# List all models in MODEL_DIR
@app.route("/api/models")
def list_models():
    models = {}

    # Example:
    # saved_models/
    # ├── RandomForestClassifier/
    # └── XGBoostClassifier/
    # In this case, the following loop would iterate through "RandomForestClassifier/" and "XGBoostClassifier/"
    for model_folder in MODEL_DIR.iterdir():
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

if __name__ == "__main__":
    print(MODEL_DIR)
    app.run(debug=True)
