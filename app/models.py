from pydantic import BaseModel

class GenerateRequest(BaseModel):
    topic: str
    pages_count: int
    style: str = "educational"
    max_tokens: int = 800

class SiteMetadata(BaseModel):
    site_id: str
    title: str
    filepath: str
