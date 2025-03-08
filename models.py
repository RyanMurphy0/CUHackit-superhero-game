from pydantic import BaseModel, Field
from typing import List, Optional

class EmojiPair(BaseModel):
    emoji1: str = Field(..., description="First emoji")
    emoji2: str = Field(..., description="Second emoji")

class Superhero(BaseModel):
    name: str = Field(..., description = "name of the superhero")
    description: Optional[str] = Field(None, description="description of superhero")
    emoji_pair: EmojiPair = Field(..., description="Emoji pair that led to this guess")

class UserCode(BaseModel):
    superheroes: List[Superhero] = Field(default_factory=list)

    def add_superhero(self, superhero: Superhero) -> None:
        self.superheroes.append(superhero)
