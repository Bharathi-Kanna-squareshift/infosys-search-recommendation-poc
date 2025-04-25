# app/models.py
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

# Add other request/response models here if needed