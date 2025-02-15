from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.chain import chain
import vertexai
import os

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

vertexai.init(project=GCP_PROJECT_ID, location="us-central1")
app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(app, chain, path="/prompt-creator")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)