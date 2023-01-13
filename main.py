from fastapi import FastAPI, HTTPException
import validators,schemas
app = FastAPI()

@app.get("/")
def read_root():
    return "Welcom to the URL shortner API..."

@app.post("/url")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400,detail="Not a URL")
    return f"TODO: Create database entry for: {url.target_url}"
