from fastapi import APIRouter, HTTPException, Request, FastAPI

router = APIRouter()

@router.get("/")
async def get_dad_joke(request: Request, app: FastAPI):
    url = "https://official-joke-api.appspot.com/random_joke"
    requests_client = request.app.requests_client
    response = await requests_client.get(url)
    
    return response.json()