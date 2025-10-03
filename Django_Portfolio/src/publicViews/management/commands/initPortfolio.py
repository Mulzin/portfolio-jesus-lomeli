from django.core.management.base import BaseCommand
import requests
import os
import json
import sys

class Command(BaseCommand):
    help = 'Initialize portfolio data'

    def handle(self, *args, **options):
        try:
            portfolio_dict = update_portfolio_dict()
            write_portfolio_json(portfolio_dict)
            self.stdout.write(self.style.SUCCESS('Portfolio data initialized successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error initializing portfolio data: {e}'))
            sys.exit(1)

def update_portfolio_dict():
    portfolio_dict = {}

    portfolio_url = os.environ.get('REPO_URL')
    if not portfolio_url:
        raise ValueError("REPO_URL environment variable not set.")

    response = get_request(portfolio_url)
    if response is None:
        raise ConnectionError(f"Failed to fetch portfolio data from {portfolio_url}")

    try:
        portfolio_data = response.json()
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from {portfolio_url}: {e}")

    for project in portfolio_data:
        title = project.get('path')
        if not title:
            continue  # Skip if no path

        try:
            details = get_project_details(title)
            portfolio_dict[title] = details
        except Exception as e:
            print(f"Warning: Failed to get details for project '{title}': {e}")

    return portfolio_dict

def get_request(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None

def get_project_details(project_name) -> dict:
    raw_url = os.environ.get('RAW_REPO_URL')
    if not raw_url:
        raise ValueError("RAW_REPO_URL environment variable not set.")
    json_url = f'{raw_url}{project_name}/info.json'
    json_file = get_request(json_url)
    if json_file is None:
        raise ConnectionError(f"Failed to fetch project details from {json_url}")
    try:
        details_dict = json.loads(json_file.text)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from {json_url}: {e}")
    return details_dict

def write_portfolio_json(portfolio_dict):
    json_path = os.environ.get('JSON_PATH')
    if not json_path:
        raise ValueError("JSON_PATH environment variable not set.")
    try:
        with open(json_path, 'w') as f:
            json.dump(portfolio_dict, f, indent=4)
    except Exception as e:
        raise IOError(f"Failed to write portfolio JSON to {json_path}: {e}")
