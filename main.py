from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Welcom to the URL shortner API..."