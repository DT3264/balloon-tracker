import asyncio

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from tinydb import TinyDB, Query
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware

import config
from Fechers.CodeforcesFetcher import CodeforcesFetcher
from UpdateSubmissionRequest import UpdateSubmissionRequest
from Fechers.OmegaupFetcher import OmegaupFetcher

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Delete the database file (in case there was something else before)
db = TinyDB('db.json')
db.storage.write({})
db.close()
db.storage.close()

# Recreate the database file
db = TinyDB('db.json')
tracker = db.table('tracker')

if config.PLATFORM == "OMEGAUP":
    fetcher = OmegaupFetcher()
elif config.PLATFORM == "CODEFORCES":
    fetcher = CodeforcesFetcher()


@app.on_event("startup")
def starting_task() -> None:
    print("Getting initial data")
    initial_data = fetcher.get_initial_data()
    for row in initial_data:
        tracker.insert(row)
    print("Initial data inserted succesfully")
    loop = asyncio.get_event_loop()
    loop.create_task(repetitive_task())


@repeat_every(seconds=int(config.SECONDS_INTERVAL))
def repetitive_task() -> None:
    print("Updating data")
    runs = fetcher.fetch_ac_submissions()
    for run in runs:
        matches = tracker.search(Query().username.matches(run['username']))
        if len(matches) == 0:
            # This might happen because of unofficial participants in CF
            continue
        team = matches[0]
        if team["problems"][run['problem_order']] == 0:
            team["problems"][run['problem_order']] = 1
            tracker.update(team, doc_ids=[team.doc_id])

    print("Data updated correctly")


@app.post('/update-submission/')
async def add_score(request: UpdateSubmissionRequest):
    team = tracker.search(Query().username.matches(request.username))[0]
    if team["problems"][request.problem_index] == 1:
        team["problems"][request.problem_index] = 2
        tracker.update(team, doc_ids=[team.doc_id])
    response = JSONResponse({'success': True})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.get('/get-data/')
async def get_scores():
    data = tracker.all()
    response = JSONResponse({'data': data})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.get("/")
async def read_index():
    return FileResponse('index.html')
