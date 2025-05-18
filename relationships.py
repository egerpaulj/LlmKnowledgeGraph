from nerNel import NerNel


from pydantic import BaseModel


from typing import List


class Relationships(BaseModel):
    relationships: List[NerNel]