import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ✅ Lade die Backend-URL für deinen Node/Mongo-Dienst
backend_url = os.getenv(
    "backend_url",
    (
        "http://nadinalijeva-3030.theiadockernext-0-labs-prod-"
        "theiak8s-4-tor01.proxy.cognitiveclass.ai:3030"
    ),
)

# ✅ Lade die Sentiment Analyzer URL (Code Engine Microservice)
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    "http://localhost:5050/",
)

print("DEBUG: backend_url =", backend_url)
print("DEBUG: sentiment_analyzer_url =", sentiment_analyzer_url)


# ==========================================================
# Function: get_request
# ==========================================================
def get_request(endpoint, **kwargs):
    """Send GET request to backend service (Node app)."""
    params = ""
    if kwargs:
        params = "&".join([f"{key}={value}" for key, value in kwargs.items()])

    # Compose full URL
    request_url = f"{backend_url}{endpoint}"
    if params:
        request_url += f"?{params}"

    print(f"DEBUG: GET from {request_url}")

    try:
        response = requests.get(request_url, timeout=5)
        # Raise HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()
        print("DEBUG: response OK")
        return response.json()
    except Exception as err:
        print(f"❌ Network exception occurred: {err}")
        return []


# ==========================================================
# Function: analyze_review_sentiments
# ==========================================================
def analyze_review_sentiments(text):
    """Dummy sentiment analyzer (returns neutral)."""
    return {"label": "neutral"}


# ==========================================================
# Function: get_dealer_from_node
# ==========================================================
def get_dealer_from_node(dealer_id):
    """Fetch a single dealer by ID from Node backend."""
    endpoint = f"/fetchDealer/{dealer_id}"
    print(f"DEBUG: Fetch dealer from {endpoint}")
    return get_request(endpoint)
