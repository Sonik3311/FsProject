from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db

router = APIRouter(prefix="/allergens", tags=["allergens"])


@router.get("/matrix")
def allergen_matrix(db: Session = Depends(get_db)):
    return crud.allergen_matrix(db)