from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas

from database import SessionLocal, engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Hotel Food Management System"}


@app.post("/foods")
def add_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):

    new_food = models.Food(
        name=food.name,
        price=food.price
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    return new_food


@app.get("/foods")
def get_foods(db: Session = Depends(get_db)):

    foods = db.query(models.Food).all()

    return foods

@app.post("/customers")
def add_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):

    new_customer = models.Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@app.get("/customers")
def get_customers(
    db: Session = Depends(get_db)
):

    customers = db.query(models.Customer).all()

    return customers

@app.get("/customers/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if customer is None:
        return {"message": "Customer not found"}

    return customer

@app.put("/customers/{customer_id}")
def update_customer(
    customer_id: int,
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):

    existing_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if existing_customer is None:
        return {"message": "Customer not found"}

    existing_customer.name = customer.name
    existing_customer.phone = customer.phone
    existing_customer.email = customer.email

    db.commit()
    db.refresh(existing_customer)

    return existing_customer

@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if customer is None:
        return {"message": "Customer not found"}

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted"}