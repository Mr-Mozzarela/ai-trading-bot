import os
from dotenv import load_dotenv

load_dotenv()

def ask_gpt(prompt: str) -> str:
    """Return a deterministic JSON response for tests."""
    return (
        "{"
        '"action": "rebuild", '
        '"grid_min": 29000, '
        '"grid_max": 31000, '
        '"grid_step": 100, '
        '"cost_estimate": 0, '
        '"reason": "test"'
        "}"
    )
