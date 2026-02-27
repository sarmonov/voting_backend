from pydantic import BaseModel


class VoteRequest(BaseModel):
    candidate_id: int


class VoteResponse(BaseModel):
    message: str
    tx_status: bool
