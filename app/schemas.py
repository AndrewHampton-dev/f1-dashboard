from pydantic import BaseModel, Configdict, Field

class DriverBase(BaseModel):
	id: int 
	driver_ref: str
	code: str 
	number: int 
	full_name: str 
	team: str 
	nationality: str 

	class Config:
		orm_mode = True

class DriveCreate(DriverBase):
	pass