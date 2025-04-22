from fastapi import FastAPI
from api.routes import router
import sys
from pathlib import Path
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the STORM project to the Python path (adjust as needed)
sys.path.insert(0, str(Path(__file__).parent.parent / "storm"))

app = FastAPI(
    title="STORM API Wrapper",
    description="A FastAPI wrapper around Stanford STORM",
    version="0.1.0"
)

app.include_router(router, prefix="/storm")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)