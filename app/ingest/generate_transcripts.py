import json, uuid, random, asyncio
from faker import Faker
from pathlib import Path
from datetime import datetime, timedelta
from app.ai.embeddings import get_embedding
from app.db.database import get_db
from app.db.crud import create_call
from app.ai.sentiment import get_sentiment_score
from app.ai.analytics import compute_agent_ratio

fake = Faker()
OUT_DIR = Path("data/raw/")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_call_data() -> dict:
    transcript = "\n".join([
        f"Agent: {fake.sentence()}",
        f"Customer: {fake.sentence()}",
        f"Agent: {fake.sentence()}",
        f"Customer: {fake.sentence()}",
    ])
    return {
        "call_id": str(uuid.uuid4()),
        "agent_id": fake.uuid4(),
        "customer_id": fake.uuid4(),
        "language": "en",
        "start_time": (datetime.now() - timedelta(minutes=random.randint(0, 10000))).isoformat(),
        "duration_seconds": random.randint(60, 600),
        "transcript": transcript,
        "embedding": get_embedding(transcript),
        "customer_sentiment_score": get_sentiment_score(transcript),
        "agent_talk_ratio": compute_agent_ratio(transcript)
    }

async def ingest_calls(n=200):
    async for db in get_db():
        for i in range(n):
            call_data = generate_call_data()

            # Save raw file for reproducibility
            with open(OUT_DIR / f"call_{i}.json", "w") as f:
                json.dump(call_data, f)

            # Save to database
            await create_call(db, call_data)
        break

if __name__ == "__main__":
    asyncio.run(ingest_calls())
