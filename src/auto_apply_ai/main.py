"""Main module for Auto Apply AI."""
import uvicorn
from auto_apply_ai.api.api import app


def main():
    """Main function for the application."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
