from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import repositories, schemas

router = APIRouter()

@router.get("/driver/{driver_ref}", response_model=schemas.DriverResponse)
def read_driver(driver_ref: str, db: Session= Depends(get_db)):
	driver = repositories.get_driver_by_ref(db, driver_ref= driver_ref)

	if driver is None:
		raise HTTPException(status_code=404, detail="Driver not found")
	return driver