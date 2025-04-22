from fastapi import APIRouter, HTTPException
from core.storm_interface import run_storm_query
from api.schemas import StormRequest, StormResponse
from fastapi.responses import StreamingResponse
import logging
import asyncio
from typing import AsyncGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

from utils.patch_file_writes import get_memory_file_log

@router.get("/debug/files")
def view_captured_file_outputs():
    return get_memory_file_log()

@router.post("/query", response_model=StormResponse)
@router.post("/query")
async def storm_query(request: StormRequest):
    try:
        result = run_storm_query(request.dict())

        if request.stream:
            return StreamingResponse(
                stream_results(result),
                media_type="text/event-stream",
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no'  # Important for some proxies
                }
            )

        return {"output": result}

    except Exception as e:
        error_msg = str(e)

        async def error_stream():
            yield f"data: Error: {error_msg}\n\n"
            yield "data: [DONE]\n\n"

        if request.stream:
            return StreamingResponse(
                error_stream(),
                media_type="text/event-stream",
                status_code=400
            )
        raise HTTPException(status_code=400, detail=error_msg)


async def stream_results(text: str) -> AsyncGenerator[str, None]:
    """Stream results as clean text without SSE formatting"""
    words = text.split()
    for word in words:
        yield f"{word} "  # Space after each word
        await asyncio.sleep(0.05)
    yield "[DONE]"
