import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logger = logging.getLogger(__name__)

# Get URLs from environment variables
backend_url = os.getenv('backend_url', 'http://localhost:3030')
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', 'http://localhost:5050/')

def get_request(endpoint):
    url = f"{backend_url}{endpoint}"
    logger.debug(f"Making request to URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        data = response.json()      # Convert the response to JSON
        if not isinstance(data, (dict, list)):  # Ensure it's a dictionary or list
            logger.error(f"Unexpected data type: {type(data)}")
            raise ValueError("Data is not JSON serializable")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        raise

def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    logger.debug(f"Analyzing sentiment with URL: {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {"error": "Request failed"}
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return {"error": "Value error"}

def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    logger.debug(f"Posting review with URL: {request_url}")
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {"error": "Request failed"}
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return {"error": "Value error"}

