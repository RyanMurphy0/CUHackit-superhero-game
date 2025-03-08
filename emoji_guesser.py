import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic_core.core_schema import none_schema
from scripts.regsetup import description

from models import EmojiPair, Superhero

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

class EmojiGuesser:
    @staticmethod
    def guess_superhero(emoji_pair: EmojiPair) -> Superhero:
        try:
            prompt = (f"I'm thinking of a superhero that can be represented by these two emojies: {emoji_pair.emoji1}"
                      f"and {emoji_pair.emoji2}. Who am I thinking of? Respond with a superhero even if you're not sure."
                      f" Respond with just the name of the superhero")
            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": "You are an assistant that guesses superheroes based on emoji pairs"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens = 100,
                temperature = 0.5,
            )

            content = response.choices[0].message.content.strip()

            parts = content.split(":", 1)

            if len(parts) > 1:
                name = parts[0].strip()
            else:
                name = content
            return Superhero(
                name=name,
                emoji_pair=emoji_pair
            )
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return Superhero(
                name = "Unknown Hero",
                emoji_pair=emoji_pair
            )