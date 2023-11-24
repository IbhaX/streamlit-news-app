from datetime import datetime
from pydantic import BaseModel, Field, AnyHttpUrl, validator
from typing import Optional, List
import re


class Source(BaseModel):
    id: Optional[str]
    name: str

class Articles(BaseModel):
    source: Source
    author: Optional[str] = Field(default="Anonymous")
    title: str
    description: Optional[str]
    image: Optional[str] = Field(alias="urlToImage", default="https://static.vecteezy.com/system/resources/previews/001/226/460/original/breaking-news-tv-background-vector.jpg")
    published: datetime = Field(alias="publishedAt")
    content: str
    url: AnyHttpUrl
    
    @validator("content")
    def validate_content(cls, value):
        # Remove HTML tags using regex
        cleaned_content = re.sub(r"<.*?>", "", value)
        return cleaned_content.split("[+")[0]

class News(BaseModel):
    status: str
    total_results: int = Field(alias="totalResults")
    articles: List[Articles]