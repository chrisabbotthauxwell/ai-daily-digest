import os

from fastapi import FastAPI

app = FastAPI(title="AI Daily Digest API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "sha": os.environ.get("GIT_SHA", "dev")}
