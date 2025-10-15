import os
# from math_tutoring_agent import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import Agent, Runner
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()


gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
  raise ValueError("GEMINI_API_KEY not found in userdata")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta",
)
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=external_client
)
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=(True)

)