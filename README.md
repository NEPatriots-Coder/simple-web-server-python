# Simple Web Server with Flask

A lightweight Flask-based web server that demonstrates various data formats (JSON, XML, CSV) and integrates a machine learning jobs dataset.

## Features

- **Multiple Response Formats**: Serves data in JSON, XML, CSV, and HTML formats
- **ML Jobs API**: Access and search through machine learning job listings
- **Pagination**: Efficiently browse large datasets
- **Search Functionality**: Find specific jobs by keywords
- **Data Download**: Export the complete dataset

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/simple-web-server-python.git
   cd simple-web-server-python
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```
   python app.py
   ```

2. Access the server at `http://localhost:5000`

## API Endpoints

### Basic Data Formats

- `GET /` - HTML page from template
- `GET /html-string` - Simple HTML response
- `GET /json` - Sample data in JSON format
- `GET /xml` - Sample data in XML format
- `GET /csv` - Sample data as downloadable CSV
- `GET /user/<id>` - Dynamic route with parameter

### ML Jobs API

- `GET /ml-jobs` - List all ML jobs with pagination
  - Query parameters:
    - `page`: Page number (default: 1)
    - `per_page`: Items per page (default: 10)
  - Example: `/ml-jobs?page=2&per_page=15`

- `GET /ml-jobs/<job_id>` - Get details for a specific job
  - Example: `/ml-jobs/5`

- `GET /ml-jobs/search` - Search for jobs
  - Query parameters:
    - `q`: Search query (required)
  - Example: `/ml-jobs/search?q=machine+learning+engineer`

- `GET /ml-jobs/download` - Download the complete dataset as CSV

## Data Structure

The ML jobs dataset includes the following fields:

- `job_posted_date`: When the job was posted
- `company_address_locality`: City location
- `company_address_region`: State/region
- `company_name`: Employer name
- `company_website`: Company website URL
- `company_description`: Description of the company
- `job_description_text`: Full job description
- `seniority_level`: Job level (Entry, Mid-Senior, etc.)
- `job_title`: Position title

## Dependencies

- Flask: Web framework
- Pandas: Data processing
- Other standard libraries: json, xml, csv, io

## Project Structure

```
simple-web-server-python/
├── app.py                  # Main application file
├── requirements.txt        # Project dependencies
├── 1000_ml_jobs_us.csv     # ML jobs dataset
└── templates/              # HTML templates
    └── index.html          # Main page template
```

## Development

To modify or extend this project:

1. Add new routes in `app.py`
2. Update templates in the `templates` directory
3. Install additional dependencies as needed with `pip install <package>`
4. Update `requirements.txt` with `pip freeze > requirements.txt`

## License

[MIT License](LICENSE)