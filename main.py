import secrets
from fastapi import FastAPI, HTTPException, Depends
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

@app.post("/url",response_model=schemas.URL)
def create_url(url: schemas.URLBase,db: Session = Depends(get_db)):
    print("I am here?")
    # breakpoint()
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400,detail="Not a URL")

    # try:
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
    # except Exception as e:
    #     raise HTTPException(status_code=500,detail=str(e))
