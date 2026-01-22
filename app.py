from flask import Flask, render_template_string
from redis import Redis
import os
import json

app = Flask(__name__)

db = Redis(host=os.environ.get('REDIS_HOST', 'db'), port=6379, decode_responses=True)

initial_companies = [
    {"name": "Google", "industry": "Tech", "country": "USA"},
    {"name": "CD Projekt Red", "industry": "Gaming", "country": "Poland"},
    {"name": "Spotify", "industry": "Music", "country": "Sweden"}
]

def init_db():
    if not db.exists('companies_list'):
        db.set('companies_list', json.dumps(initial_companies))

@app.route('/')
def index():
    data_from_db = db.get('companies_list')
    companies = json.loads(data_from_db) if data_from_db else []

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project</title>
    </head>
    <body>
            <h1>Company</h1>
            <table>
                <tr>
                    <th>Company Name</th>
                    <th>Industry</th>
                    <th>Country</th>
                </tr>
                {% for company in companies %}
                <tr>
                    <td>{{ company.name }}</td>
                    <td>{{ company.industry }}</td>
                    <td>{{ company.country }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, companies=companies)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)