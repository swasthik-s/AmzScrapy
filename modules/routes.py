import io
import pandas as pd
from flask import request, render_template, jsonify, send_from_directory
from datetime import datetime
import time
from .scraper import get_product_details_by_asin
from .config import load_marketplaces

# Store results globally for download
results = []
output_file_path = ""

def index():
    global results, output_file_path
    marketplaces = load_marketplaces()  # Load marketplaces from config

    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.csv'):
            # Read ASINs from the uploaded CSV file
            file_contents = io.StringIO(file.read().decode('utf-8'))
            df = pd.read_csv(file_contents)
            asin_list = df['ASIN'].tolist()  # Assuming the column is named 'ASIN'

            results = []
            for asin in asin_list:
                title, price, brand_name = get_product_details_by_asin(asin)
                results.append({'ASIN': asin, 'Title': title, 'Price': price, 'Brand': brand_name})
                time.sleep(2)  # Wait for 2 seconds between requests to avoid overloading the server

            # Prepare CSV file path
            current_date = datetime.now().strftime('%Y-%m-%d')
            output_file_path = f'output_{current_date}.csv'
            return jsonify(results)  # Send back the results for table display

    return render_template('index.html', marketplaces=marketplaces)


def download_file():
    global output_file_path
    if output_file_path:
        result_df = pd.DataFrame(results)
        result_df.to_csv(output_file_path, index=False)
        return send_from_directory('.', output_file_path, as_attachment=True)
    return "No file available for download."
