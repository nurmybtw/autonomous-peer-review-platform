from fastapi import APIRouter
from pydantic import BaseModel

from model.model import pare

router = APIRouter()

class Body(BaseModel):
    abstract: str

@router.post("/")
def classify(body: Body):
    abstract = body.abstract
    categories = pare.get_categories([abstract])
    return {
        "categories": categories[0]
    }