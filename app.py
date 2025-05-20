from flask import Flask, Response, render_template, request, jsonify
import json
import xml.etree.ElementTree as ET
import csv
import io 
import pandas as pd
import os

app = Flask(__name__)

# Load the CSV file
CSV_FILE_PATH = '1000_ml_jobs_us.csv'
ml_jobs_data = None

def load_csv_data():
    global ml_jobs_data
    if os.path.exists(CSV_FILE_PATH):
        ml_jobs_data = pd.read_csv(CSV_FILE_PATH)
        return True
    return False

# Load the CSV data when the app starts
load_csv_data()

# Sample user data for basic examples
data = {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

# Route for JSON response
@app.route('/json')
def get_json():
    return Response(json.dumps(data), mimetype='application/json')

# Route for XML response
@app.route('/xml')
def get_xml():
    root = ET.Element("user")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    xml_str = ET.tostring(root, encoding='unicode')
    return Response(xml_str, mimetype='application/xml')

# Route for CSV response
@app.route('/csv')
def get_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)
    return Response(output.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=data.csv"})

@app.route('/html-string')
def get_html_string():
    html_content = """
    <html>
    <head><title>Lamar's simple Web Server</title></head>
    <body>
        <h1>Welcome to Lamar's simple Web Server</h1>
        <p>This is a simple web server that serves JSON, XML, and CSV data.</p>
        </body>
    </html>""" 
    return Response(html_content, mimetype='text/html')

@app.route('/')
def get_html_file():
    return render_template('index.html')

# Basic Routing with object request
@app.route('/user/<id>')
def get_user(id):
    return {"user_id": id, "message": f"User {id} requested"}

# ML Jobs CSV data routes
@app.route('/ml-jobs')
def get_ml_jobs():
    if ml_jobs_data is None:
        return jsonify({"error": "ML jobs data not loaded"}), 500
    
    # Get query parameters for filtering
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Convert to dict for JSON serialization
    jobs = ml_jobs_data.iloc[start_idx:end_idx].to_dict(orient='records')
    
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(ml_jobs_data),
        "total_pages": (len(ml_jobs_data) + per_page - 1) // per_page,
        "data": jobs
    })

@app.route('/ml-jobs/<int:job_id>')
def get_ml_job(job_id):
    if ml_jobs_data is None:
        return jsonify({"error": "ML jobs data not loaded"}), 500
    
    if job_id < 0 or job_id >= len(ml_jobs_data):
        return jsonify({"error": "Job not found"}), 404
    
    job = ml_jobs_data.iloc[job_id].to_dict()
    return jsonify(job)

@app.route('/ml-jobs/search')
def search_ml_jobs():
    if ml_jobs_data is None:
        return jsonify({"error": "ML jobs data not loaded"}), 500
    
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query is required"}), 400
    
    # Search in job titles and descriptions
    results = ml_jobs_data[
        ml_jobs_data['job_title'].str.lower().str.contains(query, na=False) | 
        ml_jobs_data['job_description_text'].str.lower().str.contains(query, na=False)
    ]
    
    return jsonify({
        "query": query,
        "count": len(results),
        "data": results.head(20).to_dict(orient='records')  # Limit to 20 results
    })

@app.route('/ml-jobs/download')
def download_ml_jobs():
    if ml_jobs_data is None:
        return jsonify({"error": "ML jobs data not loaded"}), 500
    
    output = io.StringIO()
    ml_jobs_data.to_csv(output, index=False)
    
    return Response(
        output.getvalue(), 
        mimetype='text/csv', 
        headers={"Content-Disposition": "attachment;filename=ml_jobs_data.csv"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)