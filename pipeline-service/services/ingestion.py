import os
from datetime import date, datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from models.customer import Customer
import requests

router = APIRouter(prefix="/api")
MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://localhost:5000").rstrip("/")

@router.post("/ingest")
def ingest_customer_data(db: Session = Depends(get_db)):
    try:
        page, limit, count = 1, 10, 0
        while True:
            url = f"{MOCK_SERVER_URL}/api/customers?page={page}&limit={limit}"
            response=requests.get(url)
            if response.status_code != 200:
                break
            resp = response.json()
            data = resp.get("data") or []
            if len(data)==0:
                break
            for d in data:
                db.merge(Customer(
                    customer_id=d.get("customer_id"),
                    first_name=d.get("first_name"),
                    last_name=d.get("last_name"),
                    email=d.get("email"),
                    phone=d.get("phone"),
                    address=d.get("address"),
                    date_of_birth=date.fromisoformat(d["date_of_birth"]) if d.get("date_of_birth") else None,
                    account_balance=Decimal(str(d["account_balance"])) if d.get("account_balance") is not None else None,
                    created_at=datetime.fromisoformat(d["created_at"].replace("Z", "+00:00")) if d.get("created_at") else None,
                ))
            count += len(data)
            page += 1
        db.commit()
        return JSONResponse(content={"status": "success", "records_processed": count},status_code=status.HTTP_200_OK)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"message": "Something went wrong","error":str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get("/customers")
def get_customers(db: Session = Depends(get_db), page: int = Query(1), limit: int = Query(10)):
    try:
        offset = (page - 1) * limit
        query = db.query(Customer).order_by(Customer.customer_id)
        total = query.count()
        customers = query.offset(offset).limit(limit).all()
        data=[{
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "date_of_birth": customer.date_of_birth.isoformat() if customer.date_of_birth else None,
            "account_balance": float(customer.account_balance) if customer.account_balance is not None else None,
            "created_at": customer.created_at.isoformat() if customer.created_at else None,
        } for customer in customers]
        return JSONResponse(content={"page": page,"limit": limit,"total": total,"data": data},status_code=status.HTTP_200_OK)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"message": "Something went wrong", "error": str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get("/customers/{customer_id}")
def get_single_customer(customer_id: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            return JSONResponse(content={"message": "Not Found"},status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(
            content={
                "customer_id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address,
                "date_of_birth": customer.date_of_birth.isoformat() if customer.date_of_birth else None,
                "account_balance": float(customer.account_balance) if customer.account_balance is not None else None,
                "created_at": customer.created_at.isoformat() if customer.created_at else None,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"message": "Something went wrong", "error": str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
