"""Application entry point."""
from api import init_api

api = init_api()

if __name__ == '__main__':
    api.run(host='0.0.0.0')
