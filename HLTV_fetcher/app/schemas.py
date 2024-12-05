from pydantic import BaseModel
from datetime import datetime


class Article(BaseModel):
    
    id: int
    title: str
    author: str
    timestamp: datetime
    url: str
    description: str
    content: str
    