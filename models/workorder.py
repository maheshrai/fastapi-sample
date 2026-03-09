from pydantic import BaseModel


class Crew(BaseModel):
    amcrew: str
    orgid: str
    amcrewtype: str | None
    description: str | None
