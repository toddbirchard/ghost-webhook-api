"""Application entry point."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:api", host="0.0.0.0", port=9300, workers=1, reload=True)
