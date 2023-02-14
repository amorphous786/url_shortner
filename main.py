import secrets
from fastapi import FastAPI, HTTPException, Depends,Request
from fastapi.responses import RedirectResponse

import validators,schemas
import models, schemas
from database import SessionLocal,engine
from sqlalchemy.orm import Session
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return "Welcom to the URL shortner API..."

@app.post("/url",response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase,db: Session = Depends(get_db)):
    print("I am here?")

    if not validators.url(url.target_url):
        raise HTTPException(status_code=400,detail="Not a URL")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url = url.target_url,
        key = key,
        secret_key = secret_key,
        is_active=True
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
    return db_url

@app.get("/all_urls")
def all_urls(db:Session=Depends(get_db),response_model=schemas.URLInfo):
    db_urls = db.query(models.URL).all()
    return db_urls

@app.get("/{url_key}")
def to_targeted_url(url_key:str,request:Request,db: Session = Depends(get_db)):
    db_url = (db.query(models.URL).filter(models.URL.key==url_key,
                                          models.URL.is_active).first())
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=404,
                            detail=f"no url found with key {url_key}")