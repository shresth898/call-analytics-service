from sqlalchemy.future import select
from app.db.models import Call

async def get_call_by_id(session, call_id: str):
    result = await session.execute(select(Call).where(Call.call_id == call_id))
    return result.scalar_one_or_none()

async def list_calls(session, skip: int = 0, limit: int = 10):
    result = await session.execute(select(Call).offset(skip).limit(limit))
    return result.scalars().all()

async def create_call(session, call_data: dict):
    call = Call(**call_data)
    session.add(call)
    await session.commit()
    await session.refresh(call)
    return call
