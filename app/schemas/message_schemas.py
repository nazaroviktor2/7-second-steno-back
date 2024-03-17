from pydantic import BaseModel


class MSGIn(BaseModel):
    message: str
    order_id: str
