import uvicorn
import os

if __name__ == "__main__":
    print("Starting Student Food Management System...")
    print("Open http://127.0.0.1:8000 in your browser.")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
