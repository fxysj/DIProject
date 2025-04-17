# Tool Calling#
# Some LLMs (OpenAI, Anthropic, Gemini, Ollama, etc.) support tool calling directly over API calls -- this means tools and functions can be called without specific prompts and parsing mechanisms
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI

load_dotenv(verbose=True)
import os

class Song(BaseModel):
    name:str
    artist:str


def generate_song(name: str, artist: str) -> Song:
    """Generates a song with provided name and artist."""
    return {"name": name, "artist": artist}

tool = FunctionTool.from_defaults(fn=generate_song)

llm = OpenAI(model="gpt-4o",api_base=os.getenv("OPENAI_API_BASE_URL"),
                      api_key=os.getenv("OPENAI_API_KEY"))
response = llm.predict_and_call(
    [tool],
    "Pick a random song for me",
)
print(str(response))
