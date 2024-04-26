from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
import openai
import os


consultRouter = APIRouter()

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@consultRouter.get("/agents")
async def list_agents():
    try:
        models = openai.Model.list()
        return {"models": models.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@consultRouter.get("/consult/{agent_id}")
async def get_agent_response(agent_id: str, prompt: str):
    try:
        response = openai.Completion.create(
            model=agent_id,  # Specify the agent/model ID here
            prompt=prompt,
            max_tokens=100  # You can adjust this value
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the server using command: uvicorn main:app
