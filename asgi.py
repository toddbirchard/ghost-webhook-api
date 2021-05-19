"""Application entry point."""
import uvicorn

from clients.log import LOGGER

if __name__ == "__main__":
    uvicorn.run("app:api", host="0.0.0.0", port=9300, workers=4)
    LOGGER.success(f"API successfully started.")
