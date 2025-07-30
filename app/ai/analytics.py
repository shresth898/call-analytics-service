import re
from typing import List, Dict, Any
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Call

def compute_agent_ratio(transcript: str) -> float:
    """
    Computes agent talk ratio = agent words / (agent + customer words)
    """
    agent_words, customer_words = 0, 0
    for line in transcript.split("\n"):
        if line.lower().startswith("agent:"):
            agent_words += len(re.findall(r"\w+", line))
        elif line.lower().startswith("customer:"):
            customer_words += len(re.findall(r"\w+", line))
    total = agent_words + customer_words
    return agent_words / total if total else 0.0

async def get_agent_leaderboard(db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Aggregates sentiment score, talk ratio, and total call count per agent.
    Returns leaderboard for /analytics/agents endpoint.
    """
    result = await db.execute(select(Call))
    calls: List[Call] = result.scalars().all()

    agent_stats = defaultdict(lambda: {
        "total_sentiment": 0.0,
        "total_ratio": 0.0,
        "count": 0
    })

    for call in calls:
        if not call.agent_id:
            continue
        agent_stats[call.agent_id]["total_sentiment"] += call.customer_sentiment_score or 0.0
        agent_stats[call.agent_id]["total_ratio"] += call.agent_talk_ratio or 0.0
        agent_stats[call.agent_id]["count"] += 1

    leaderboard = []
    for agent_id, stats in agent_stats.items():
        count = stats["count"]
        leaderboard.append({
            "agent_id": agent_id,
            "average_sentiment": round(stats["total_sentiment"] / count, 3) if count else 0.0,
            "average_talk_ratio": round(stats["total_ratio"] / count, 3) if count else 0.0,
            "total_calls": count
        })

    return leaderboard
