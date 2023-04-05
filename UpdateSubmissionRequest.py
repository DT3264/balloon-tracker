from pydantic import BaseModel


class UpdateSubmissionRequest(BaseModel):
    username: str
    problem_index: int
