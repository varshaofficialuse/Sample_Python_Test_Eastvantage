from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from geopy.distance import geodesic
import logging
import uvicorn
from sql_app.enums import ServerDetails
from sql_app.database import SessionLocal
from sql_app.models import *

app = FastAPI(
    description="<b>Sample Test Using FastAPI and SQL lite</b>",
    title="Eastvantage Test",
    docs_url='/EastVantage_Docs',
    contact = { "email" : "cvajay69@gmail.com",
             "name" : "Ajay Chevula Vadde"}
)






# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# CRUD operations
@app.post("/addresses/", response_model=AddressResponse)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    try:
        db_address = Address(**address.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    except Exception as e:
        logger.error(f"Error creating address: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    try:
        db_address = db.query(Address).filter(Address.id == address_id).first()
        if db_address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        for key, value in address.dict().items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
        return db_address
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating address: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/addresses/{address_id}", response_model=dict)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    try:
        db_address = db.query(Address).filter(Address.id == address_id).first()
        if db_address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        db.delete(db_address)
        db.commit()
        return {"ok": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting address: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/addresses/{address_id}", response_model=AddressResponse)
def read_address(address_id: int, db: Session = Depends(get_db)):
    try:
        db_address = db.query(Address).filter(Address.id == address_id).first()
        if db_address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        return db_address
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error reading address: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/addresses/nearby/", response_model=list[AddressResponse])
def get_nearby_addresses(location: Location, db: Session = Depends(get_db)):
    try:
        addresses = db.query(Address).all()
        nearby_addresses = []
        for address in addresses:
            if geodesic((location.latitude, location.longitude), (address.latitude, address.longitude)).km <= location.distance:
                nearby_addresses.append(address)
        return nearby_addresses
    except Exception as e:
        logger.error(f"Error retrieving nearby addresses: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")






if __name__ == "__main__":
    uvicorn.run(port=ServerDetails.port.value,host=ServerDetails.host.value,reload=True,app='main:app')