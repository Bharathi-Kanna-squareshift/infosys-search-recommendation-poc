# app/routers/search.py
import httpx
import traceback
from fastapi import APIRouter, HTTPException
from app.models import SearchRequest  # Import from models sibling module
from app.config import APPSEARCH_API_URL, APPSEARCH_HEADERS # Import config

router = APIRouter()


@router.post("/search") # Path relative to the prefix defined in main.py
async def proxy_app_search(search_request: SearchRequest):
    """
    Proxies search requests to the Elastic App Search API.
    """
    print(f"Received search request for query: {search_request.query}")
    app_search_payload = {
        "query": search_request.query,
        "result_fields": {
            "title": {"raw": {}, "snippet": {"size": 100, "fallback": True}},
            "url": {"raw": {}},
            "body_content": {"snippet": {"size": 150, "fallback": True}},
        },
        "page": {"size": 20}
    }

    async with httpx.AsyncClient() as client:
        try:
            print(f"Sending request to App Search URL: {APPSEARCH_API_URL}")
            response = await client.post(
                APPSEARCH_API_URL,
                json=app_search_payload,
                headers=APPSEARCH_HEADERS, # Use headers from config
                timeout=15.0
            )
            response.raise_for_status()
            print(f"App Search responded with status: {response.status_code}")
            return response.json()
        except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            print(f"App Search Error Body: {exc.response.text}")
            error_detail = f"App Search Error ({exc.response.status_code})"
            try:
                error_json = exc.response.json()
                if isinstance(error_json.get("errors"), list) and error_json["errors"]:
                    error_detail = f"App Search Error: {error_json['errors'][0]}"
                elif isinstance(error_json.get("error"), str):
                     error_detail = f"App Search Error: {error_json['error']}"
            except Exception:
                pass
            raise HTTPException(status_code=exc.response.status_code, detail=error_detail)
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise HTTPException(status_code=503, detail=f"Service Unavailable: Could not connect to App Search ({exc})")
        except Exception as exc:
             print(f"An unexpected error occurred: {exc}")
             traceback.print_exc() # Keep traceback for unexpected errors
             raise HTTPException(status_code=500, detail=f"Internal Server Error: {exc}")# app/routers/search.py
