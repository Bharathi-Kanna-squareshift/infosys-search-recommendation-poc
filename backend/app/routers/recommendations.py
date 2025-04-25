# app/routers/recommendations.py
import httpx
import json
import traceback
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.config import ( # Import specific config variables needed
    ELASTICSEARCH_HISTORY_SEARCH_URL,
    ELASTICSEARCH_SEMANTIC_SEARCH_URL,
    ELASTICSEARCH_HEADERS, # Use shared ES headers
    GEMINI_API_URL
)

router = APIRouter()

@router.get("/{user_id}", response_model=Dict[str, Any]) # Path relative to prefix
async def get_recommendations(user_id: str):
    """
    Retrieves the last 5 search terms for a user, asks Gemini to identify
    key topics from these terms, and then uses those topics for semantic search.
    """
    search_terms: List[str] = []

    # --- Stage 1: Fetch Search Terms ---
    history_es_query = {
        "size": 5,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"processor.event": "transaction"}},
                    {"term": {"user.id": user_id}},
                    {"term": {"labels.search_action": "submit"}},
                    {"exists": {"field": "labels.search_term"}}
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}],
        "_source": ["labels.search_term"]
    }

    async with httpx.AsyncClient() as client:
        try:
            print(f"\nFetching history from: {ELASTICSEARCH_HISTORY_SEARCH_URL}")
            response = await client.post(
                ELASTICSEARCH_HISTORY_SEARCH_URL,
                json=history_es_query,
                headers=ELASTICSEARCH_HEADERS, # Use shared headers
                timeout=20.0
            )
            response.raise_for_status()
            es_response_json = response.json()

            hits = es_response_json.get("hits", {}).get("hits", [])
            for hit in hits:
                term = hit.get("_source", {}).get("labels", {}).get("search_term")
                if term:
                    search_terms.append(term)

            print("--- User Search History ---")
            if search_terms:
                for i, term in enumerate(search_terms):
                    print(f"{i+1}. {term}")
            else:
                print("No search terms found.")
            print("-" * 27)

        except httpx.HTTPStatusError as exc:
             print(f"Error fetching history: {exc.response.status_code} - {exc.response.text}")
             raise HTTPException(status_code=exc.response.status_code, detail="Error fetching search history")
        except httpx.RequestError as exc:
             print(f"Request error fetching history: {exc}")
             raise HTTPException(status_code=503, detail="Service Unavailable (History)")
        except Exception as exc:
             print(f"Unexpected error fetching history:")
             traceback.print_exc()
             raise HTTPException(status_code=500, detail="Internal Server Error (History)")

    # --- Stage 2: Get Key Topics from Gemini ---
    if not search_terms:
        print("No search terms found, returning empty recommendations.")
        return {"hits": {"total": {"value": 0, "relation": "eq"}, "max_score": None, "hits": []}}

    history_keywords_formatted = "\n".join([f"- {term}" for term in search_terms])
    gemini_prompt = f"""
Analyze the following list of a user's recent search terms:
{history_keywords_formatted}

Based *only* on these terms, identify the 2 or 3 primary topics or categories the user seems most interested in.
Provide these topics as a short, concise phrase or a comma-separated list of keywords suitable for a subsequent search query.
Do not add any explanatory text, introductory phrases like "Based on the searches...", or concluding remarks. Just output the topics/keywords.

Example Output 1: data science, machine learning libraries
Example Output 2: python programming
"""

    print("\n--- Prompt Sent to Gemini ---")
    print(gemini_prompt.strip())
    print("-" * 29)

    gemini_payload = {
      "contents": [{"parts": [{"text": gemini_prompt}]}],
      # Add generationConfig if needed, e.g.,
      # "generationConfig": {
      #   "temperature": 0.3,
      #   "maxOutputTokens": 50
      # }
    }

    extracted_topics = ""
    async with httpx.AsyncClient() as client:
        try:
            print(f"Sending request to Gemini: {GEMINI_API_URL}")
            response = await client.post(GEMINI_API_URL, json=gemini_payload, timeout=25.0)
            response.raise_for_status()
            gemini_response_json = response.json()

            # Safer parsing based on Gemini API structure
            candidates = gemini_response_json.get("candidates", [])
            if candidates and isinstance(candidates, list):
                first_candidate = candidates[0]
                content = first_candidate.get("content", {})
                parts = content.get("parts", [])
                if parts and isinstance(parts, list):
                    first_part = parts[0]
                    extracted_topics = first_part.get("text", "").strip()
            print(f"Gemini Response Text: '{extracted_topics}'") # Log raw response

            if not extracted_topics:
                 print("Gemini did not return topics, using fallback.")
                 extracted_topics = ", ".join(search_terms) # Fallback

        except httpx.HTTPStatusError as exc:
            print(f"Gemini API Error: {exc.response.status_code} - {exc.response.text}")
            print("Using fallback search terms due to Gemini API error.")
            extracted_topics = ", ".join(search_terms) # Fallback
        except httpx.RequestError as exc:
            print(f"Gemini Request Error: {exc}")
            print("Using fallback search terms due to Gemini request error.")
            extracted_topics = ", ".join(search_terms) # Fallback
        except (KeyError, IndexError, TypeError) as e:
             print(f"Error parsing Gemini response: {e}")
             print(f"Raw Gemini Response: {gemini_response_json}")
             print("Using fallback search terms due to Gemini parsing error.")
             extracted_topics = ", ".join(search_terms) # Fallback
        except Exception as exc:
            print(f"Unexpected error during Gemini request:")
            traceback.print_exc()
            print("Using fallback search terms due to unexpected error.")
            extracted_topics = ", ".join(search_terms) # Fallback

    # --- Stage 3: Perform Semantic Search ---
    semantic_query_text = extracted_topics # Already determined above

    semantic_es_query = {
        "size": 10,
        "_source": ["title.text", "url"], # Adjust source fields as needed
        "query": {
            "semantic": {
                "field": "body_content", # Ensure this matches your semantic model field
                "query": semantic_query_text
            }
        }
    }

    print("\n--- Semantic Search Query (Elasticsearch) ---")
    print(f"Query Text Used: '{semantic_query_text}'")
    print(json.dumps(semantic_es_query, indent=2))
    print("-" * 42)

    async with httpx.AsyncClient() as client:
        try:
            print(f"Sending semantic search to: {ELASTICSEARCH_SEMANTIC_SEARCH_URL}")
            response = await client.post(
                ELASTICSEARCH_SEMANTIC_SEARCH_URL,
                json=semantic_es_query,
                headers=ELASTICSEARCH_HEADERS, # Use shared headers
                timeout=30.0
            )
            response.raise_for_status()
            print("Semantic search successful.")
            return response.json() # Return final result

        except httpx.HTTPStatusError as exc:
            print(f"Elasticsearch Semantic Error: {exc.response.status_code} - {exc.response.text}")
            raise HTTPException(status_code=exc.response.status_code, detail="Error during semantic search")
        except httpx.RequestError as exc:
            print(f"Elasticsearch Request Error: {exc}")
            raise HTTPException(status_code=503, detail="Service Unavailable (Semantic Search)")
        except Exception as exc:
             print(f"Unexpected error during semantic search:")
             traceback.print_exc()
             raise HTTPException(status_code=500, detail=f"Internal Server Error (Semantic Search): {exc}")