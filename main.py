import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.adapters.api.app:create_app", factory=True, reload=True)
