from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from app.chains.create_prompt_chain import chain as create_prompt_chain
from app.chains.generate_response_chain import chain as generate_response_chain
from app.utils.helpers import extract_template_and_variables
import vertexai
import os

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

vertexai.init(project=GCP_PROJECT_ID, location="us-central1")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/prompt-creator/invoke")
async def prompt_creator_invoke(request_data: dict):
    objective = request_data["input"]["objective"]
    llm_output = create_prompt_chain.invoke({"objective": objective})
    extracted_data = extract_template_and_variables(llm_output)
    return JSONResponse(extracted_data)

@app.post("/generate-response/invoke")
async def generate_response_invoke(request_data: dict):
    prompt_template = request_data["input"]["promptTemplate"]
    input_variables = request_data["input"]["variables"]
    formatted_prompt = prompt_template.format(**input_variables)
    llm_response = generate_response_chain.invoke({"promptTemplate": formatted_prompt})
    return JSONResponse({"llm_response": llm_response})

add_routes(app, create_prompt_chain, path="/prompt-creator")
add_routes(app, generate_response_chain, path="/generate-response")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)