from fastapi import APIRouter
from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import list_calls,get_call_by_id
from app.ai.embeddings import get_similar_calls
from app.ai.analytics import get_agent_leaderboard
from fastapi.responses import JSONResponse
from fastapi import HTTPException


router = APIRouter()


@router.get("/calls")
async def get_calls(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    calls = await list_calls(db, skip=skip, limit=limit)
    return {"calls": calls}


@router.get("/calls/{call_id}")
async def get_call(call_id: str, db: AsyncSession = Depends(get_db)):
    call = await get_call_by_id(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@router.get("/calls/{call_id}/recommendations")
async def recommendations(call_id: str, db: AsyncSession = Depends(get_db)):
    reference_call = await get_call_by_id(db, call_id)
    if not reference_call:
        raise HTTPException(status_code=404, detail="Call not found")

    all_calls = await list_calls(db, skip=0, limit=1000)  # or load all without limit
    similar_call_ids = get_similar_calls(reference_call, all_calls)

    # You can add OpenAI nudge generation later
    nudges = [
        "Try to empathize more",
        "Ask clarifying questions",
        "Recap key points at end"
    ]
    return {"similar_calls": similar_call_ids, "nudges": nudges}


@router.get("/analytics/agents")
async def agent_analytics(db: AsyncSession = Depends(get_db)):
    leaderboard = await get_agent_leaderboard(db)
    return {"analytics": leaderboard}