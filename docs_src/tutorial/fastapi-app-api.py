"""The FastAPI REST API for the song bank."""
from typing import Any

from fastapi import FastAPI

app = FastAPI()


@app.post("/")
async def create_song(song: Any):
    """User can add a new song's lyrics"""
    return {"message": f"create song {song}"}


@app.delete("/{title}")
async def remove_song(title: str):
    """User can remove a song of a given title"""
    return {"message": f"remove song {title}"}


@app.put("/{title}")
async def update_song(title: str, song: Any):
    """User can update a song of a given title"""
    return {"message": f"update song '{title}' with {song}"}


@app.get("/{title}")
async def get_song(title: str):
    """User can get a song's lyrics, given a song title."""
    return {"message": f"get song of title: '{title}'"}


@app.get("/")
async def find_songs(q: str, skip: int = 0, limit: int = 20):
    """User can search for any songs whose title begins with a certain phrase."""
    return {"message": f"find songs with title starting with: '{q}'"}
