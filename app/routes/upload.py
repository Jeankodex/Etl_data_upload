# app/routes/upload.py
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import pandas as pd

from app.services.excel_inspector import inspect_excel
from app.config.sheet_config import SHEET_CONFIG
from app.services.table_manager import create_table
from app.services.data_inserter import insert_sheet_data

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"xlsx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/form", methods=["GET"])
def upload_form():
    return render_template("upload.html")


@upload_bp.route("/upload", methods=["POST"])
def upload_excel():
    """Upload Excel, inspect sheets, create tables, and insert data."""
    
    # -----------------------
    # Step 0: Validate upload
    # -----------------------
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only .xlsx allowed"}), 400

    # -----------------------
    # Step 1: Save file
    # -----------------------
    filename = secure_filename(file.filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # -----------------------
    # Step 2: Inspect Excel
    # -----------------------
    inspect_excel(file_path)

    # -----------------------
    # Step 3: Create tables dynamically
    # -----------------------
    for sheet, config in SHEET_CONFIG.items():
        header_row = config["header_row"]
        unique_key = config["unique_key"].lower()

        # Read header row only
        df_header = pd.read_excel(file_path, sheet_name=sheet, header=header_row-1, nrows=0)
        columns = [c.strip().lower().replace(" ", "_") for c in df_header.columns]

        # Create table
        create_table(sheet, columns, unique_key)

    # -----------------------
    # Step 4: Insert Excel data into tables
    # -----------------------
    insert_sheet_data(file_path)

    # -----------------------
    # Step 5: Return response
    # -----------------------
    return jsonify({
        "message": "File uploaded, tables created, and data inserted successfully",
        "filename": filename
    }), 200
