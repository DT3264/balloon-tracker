import uvicorn

# uvicorn app.app:app --host 0.0.0.0 --port 4557 --reload --debug --workers 3
# uvicorn main:app  --reload
uvicorn.run("main:app")