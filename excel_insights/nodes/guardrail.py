# excel_insights/nodes/guardrail.py
from excel_insights.config import client

def guardrail_check(text: str) -> bool:
    mod = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    return not mod.results[0].flagged
