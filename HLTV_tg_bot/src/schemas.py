from pydantic import BaseModel


class TranslatedArticle(BaseModel):
    
    id: int
    title: str
    author: str
    description: str
    content: str