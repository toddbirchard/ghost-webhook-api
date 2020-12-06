"""Application entry point."""
import uvicorn

from app import init_api

api = init_api()

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=5000)
