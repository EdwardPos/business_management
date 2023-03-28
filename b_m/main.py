import models
from database import SessionLocal, engine
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Company(BaseModel):
    comp_id: str
    tax_id: str
    email: str
    is_active: bool = Field(
        default=False, description="Check in Contracts 'status'")


class Users(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    hashed_password: str | None = None
    company_id: int


class Contract(BaseModel):
    contr_num: str
    contr_type: str
    service_id: int
    status_id: int
    company_id: int


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Company).all()


@app.get("/companies/users")
async def read_all_by_user(company_id: int, db: Session = Depends(get_db)):
    return db.query(models.Users).filter(
        models.Users.company_id == company_id).all()


@app.get("/companies/contracts")
async def read_all_by_contr(company_id: int, db: Session = Depends(get_db)):
    return db.query(models.Contract).filter(
        models.Contract.company_id == company_id).all()


@app.get("/users/{users_id}")
async def read_users(users_id: int, db: Session = Depends(get_db)):
    users_model = db.query(models.Users).filter(
        models.Users.id == users_id).first()
    if users_model is not None:
        return users_model
    raise http_exception()


# @app.get("/companies/{companies_id}")
# async def read_companies(companies_id: int, db: Session = Depends(get_db)):
#     companies_model = db.query(models.Company).filter(
#         models.Company.id == companies_id).first()
#     if companies_model is not None:
#         return companies_model
#     raise http_exception()


@app.get("/companies/{companies_id}")
async def read_companies(companies_id: int, db: Session = Depends(get_db)):
    companies_model = db.query(models.Company).filter(
        models.Company.comp_id == companies_id).first()
    if companies_model is not None:
        return companies_model
    raise http_exception()


@app.get("/contracts/{contract_id}")
async def read_contract(contract_id: int, db: Session = Depends(get_db)):
    contract_model = db.query(models.Contract).filter(
        models.Contract.id == contract_id).first()
    if contract_model is not None:
        return contract_model
    raise http_exception_contract()


@app.post("/companies")
async def create_company(company: Company, db: Session = Depends(get_db)):
    companies_model = models.Company()
    companies_model.comp_id = company.comp_id
    companies_model.tax_id = company.tax_id
    companies_model.email = company.email
    companies_model.is_active = company.is_active

    db.add(companies_model)
    db.commit()

    return successful_response(201)


@app.post("/users")
async def create_users(users: Users, db: Session = Depends(get_db)):
    users_model = models.Users()
    users_model.email = users.email
    users_model.username = users.username
    users_model.first_name = users.first_name
    users_model.last_name = users.last_name
    # users_model.hashed_password = users.hashed_password
    users_model.company_id = users.company_id

    db.add(users_model)
    db.commit()

    return successful_response(201)


@app.post("/contracts")
async def create_contract(contract: Contract, db: Session = Depends(get_db)):
    contract_model = models.Contract()
    contract_model.contr_num = contract.contr_num
    contract_model.contr_type = contract.contr_type
    contract_model.service_id = contract.service_id
    contract_model.status_id = contract.status_id
    contract_model.company_id = contract.company_id

    db.add(contract_model)
    db.commit()

    return successful_response(201)


@app.put("/companies/{companies_id}")
async def update_companies(companies_id: int, company: Company, db: Session = Depends(get_db)):
    companies_model = db.query(models.Company).filter(
        models.Company.id == companies_id).first()

    if companies_model is None:
        raise http_exception()

    companies_model.comp_id = company.comp_id
    companies_model.tax_id = company.tax_id
    companies_model.email = company.email
    companies_model.is_active = company.is_active

    db.add(companies_model)
    db.commit()

    return successful_response(200)


@app.put("/users/{users_id}")
async def update_users(users_id: int, users: Users, db: Session = Depends(get_db)):
    users_model = db.query(models.Users).filter(
        models.Users.id == users_id).first()

    if users_model is None:
        raise http_exception()

    users_model.email = users.email
    users_model.username = users.username
    users_model.first_name = users.first_name
    users_model.last_name = users.last_name

    db.add(users_model)
    db.commit()

    return successful_response(200)


@app.put("/contracts/{contract_id}")
async def update_contract(contract_id: int, contract: Contract, db: Session = Depends(get_db)):
    contract_model = db.query(models.Contract).filter(
        models.Contract.id == contract_id).first()

    if contract_model is None:
        raise http_exception_contract()

    contract_model.contr_num = contract.contr_num
    contract_model.contr_type = contract.contr_type
    contract_model.service_id = contract.service_id
    contract_model.status_id = contract.status_id

    db.add(contract_model)
    db.commit()

    return successful_response(200)


@app.delete("/companies/{companies_id}")
async def delete_companies(companies_id: int, db: Session = Depends(get_db)):
    companies_model = db.query(models.Company).filter(
        models.Company.id == companies_id).first()
    if companies_model is None:
        raise http_exception()

    db.query(models.Company).filter(models.Company.id == companies_id).delete()
    db.commit()

    return successful_response(200)


@app.delete("/users/{users_id}")
async def delete_users(users_id: int, db: Session = Depends(get_db)):
    users_model = db.query(models.Users).filter(
        models.Users.id == users_id).first()
    if users_model is None:
        raise http_exception()

    db.query(models.Users).filter(models.Users.id == users_id).delete()
    db.commit()

    return successful_response(200)


@app.delete("/contracts/{contract_id}")
async def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    contract_model = db.query(models.Contract).filter(
        models.Contract.id == contract_id).first()
    if contract_model is None:
        raise http_exception_contract()

    db.query(models.Contract).filter(
        models.Contract.id == contract_id).delete()
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception_contract():
    return HTTPException(status_code=404, detail="contract not found")


def http_exception():
    return HTTPException(status_code=404, detail="users not found")
