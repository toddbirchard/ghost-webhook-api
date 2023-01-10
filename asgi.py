"""Application entry point."""
import uvicorn

script_starter = uvicorn.run("app:api", host="0.0.0.0", port=9300, workers=4)

if __name__ == "__main__":
    script_starter
