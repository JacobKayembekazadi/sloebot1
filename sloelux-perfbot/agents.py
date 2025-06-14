from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent, LoopAgent
from tools import fetch_pagespeed, classify_issues, optimize_image
import os
from typing import ClassVar

WATCHLIST = ["https://sloelux.com", "https://sloelux.com/collections/frontpage"]

class MetricsCollector(LlmAgent):
    tools: ClassVar = [fetch_pagespeed]
    prompt: ClassVar[str] = "For each URL in {{ WATCHLIST }}, call fetch_pagespeed and return raw JSON list."

class IssueClassifier(LlmAgent):
    tools: ClassVar = [classify_issues]
    prompt: ClassVar[str] = "Call classify_issues on each JSON from previous step and return unique labels."

class FixImagesAgent(SequentialAgent):
    tools: ClassVar = [optimize_image]
    workflow: ClassVar[list] = ["find_assets", "optimize_image"]

class MessengerAgent(LlmAgent):
    prompt: ClassVar[str] = "Summarise the run (start metrics ➔ end metrics) in ≤200 words and include next steps."

bot = LoopAgent(
    name="loop_agent",
    sub_agents=[
        MetricsCollector(name="metrics_collector", model="gemini-pro"),
        IssueClassifier(name="issue_classifier", model="gemini-pro"),
        ParallelAgent(name="parallel_agent", sub_agents=[FixImagesAgent(name="fix_images_agent")]),
        MessengerAgent(name="messenger_agent", model="gemini-pro")
    ]
)

if __name__ == "__main__":
    import asyncio
    from google.adk.agents.invocation_context import InvocationContext, new_invocation_context_id
    from google.adk.sessions.in_memory_session_service import InMemorySessionService
    from google.adk.sessions.session import Session

    session_service = InMemorySessionService()
    session = Session(
        id="dry_run_session",
        app_name="sloelux_perf_bot",
        user_id="dry_run_user",
        state={},
        events=[],
        last_update_time=0.0
    )
    context = InvocationContext(
        session_service=session_service,
        session=session,
        agent=bot,
        invocation_id=new_invocation_context_id()
    )

    async def run_agent():
        async for event in bot.run_async(context):
            print(event)

    asyncio.run(run_agent()) 