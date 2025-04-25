# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file (assuming .env is in the parent directory)
# Adjust the path if your .env file is elsewhere relative to this config.py
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Configuration from Environment Variables ---
APPSEARCH_ENDPOINT_BASE = os.getenv("APPSEARCH_ENDPOINT_BASE")
APPSEARCH_ENGINE_NAME = os.getenv("APPSEARCH_ENGINE_NAME")
APPSEARCH_SEARCH_KEY = os.getenv("APPSEARCH_SEARCH_KEY")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000") # Provide a default

# --- Elasticsearch Configuration ---
ELASTICSEARCH_ENDPOINT = os.getenv("ELASTICSEARCH_ENDPOINT")
ELASTICSEARCH_API_KEY = os.getenv("ELASTICSEARCH_API_KEY")
ELASTICSEARCH_RUM_INDEX_PATTERN = os.getenv("ELASTICSEARCH_RUM_INDEX_PATTERN")
ELASTICSEARCH_SEMANTIC_INDEX = os.getenv("ELASTICSEARCH_SEMANTIC_INDEX")

# --- Gemini Configuration ---
GEMINI_API_URL = os.getenv("GEMINI_API_URL") # Make sure this includes the API key in the URL if needed

# --- Basic Validation ---
if not all([APPSEARCH_ENDPOINT_BASE, APPSEARCH_ENGINE_NAME, APPSEARCH_SEARCH_KEY]):
    print("ERROR: Missing required App Search environment variables!")
    exit(1)

if not all([ELASTICSEARCH_ENDPOINT, ELASTICSEARCH_API_KEY, ELASTICSEARCH_RUM_INDEX_PATTERN, ELASTICSEARCH_SEMANTIC_INDEX]):
    print("ERROR: Missing required Elasticsearch environment variables (Endpoint, API Key, RUM Index Pattern, Semantic Index)!")
    exit(1)

if not GEMINI_API_URL:
    print("ERROR: Missing required Gemini environment variable (GEMINI_API_URL)!")
    exit(1)


# --- Construct API URLs ---
APPSEARCH_API_URL = f"{APPSEARCH_ENDPOINT_BASE}/api/as/v1/engines/{APPSEARCH_ENGINE_NAME}/search"
ELASTICSEARCH_HISTORY_SEARCH_URL = f"{ELASTICSEARCH_ENDPOINT}/{ELASTICSEARCH_RUM_INDEX_PATTERN}/_search"
ELASTICSEARCH_SEMANTIC_SEARCH_URL = f"{ELASTICSEARCH_ENDPOINT}/{ELASTICSEARCH_SEMANTIC_INDEX}/_search"

# --- CORS Origins ---
origins = [
    FRONTEND_ORIGIN,
    # Add other allowed origins here
]

# --- Elasticsearch Headers (often reused) ---
ELASTICSEARCH_HEADERS = {
    "Authorization": f"ApiKey {ELASTICSEARCH_API_KEY}",
    "Content-Type": "application/json",
}

# --- AppSearch Headers (often reused) ---
APPSEARCH_HEADERS = {
    "Authorization": f"Bearer {APPSEARCH_SEARCH_KEY}",
    "Content-Type": "application/json",
}

print("--- Configuration Loaded ---")
print(f"App Search Endpoint: {APPSEARCH_ENDPOINT_BASE}/.../{APPSEARCH_ENGINE_NAME}")
print(f"Elasticsearch Endpoint: {ELASTICSEARCH_ENDPOINT}")
print(f"Elasticsearch RUM Index: {ELASTICSEARCH_RUM_INDEX_PATTERN}")
print(f"Elasticsearch Semantic Index: {ELASTICSEARCH_SEMANTIC_INDEX}")
print(f"Gemini API URL: {'Configured' if GEMINI_API_URL else 'Not Configured'}")
print(f"Allowed Frontend Origin: {FRONTEND_ORIGIN}")
print("-" * 26)