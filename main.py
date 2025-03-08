import os
import json
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.core.window import Window
from models import EmojiPair, Superhero, UserRecord
from emoji_guesser import EmojiGuesser

Window.size = (800, 600)
SUPERHEROES_FILE = "superheroes.json"

class SuperheroCard(BoxLayout):
    name = StringProperty("")
    emojis = StringProperty("")

class SuperheroEmojiApp(BoxLayout):
    def __init__ (self, **kwargs):
        super(SuperheroEmojiApp, self).__init__(**kwargs)
        self.user_record = self._load_user_record()

        self._display_saved_superheroes()

    def _load_user_record(self) -> UserRecord:
        if os.path.exists(SUPERHEROES_FILE):
            try:
                with open(SUPERHEROES_FILE, 'r') as file:
                    data = json.load(file)
                    return UserRecord.model_validate(data)
            except Exception as e:
                print(f"Error loading superheroes: {e}")
                return UserRecord()
        return UserRecord()

    def _save_user_record(self):
        with open(SUPERHEROES_FILE, 'w') as file:
            json.dump(self.user_record.model_dump(), file)

    def _display_saved_superheroes(self):
        for hero in self.user_record.superheroes:
            self._add_superhero_card(hero)

    def _add_superhero_card(self, superhero: Superhero):
        card = SuperheroCard()
        card.name = superhero.name
        card.emojis = f"{superhero.emoji_pair.emoji1} + {superhero.emoji_pair.emoji2}"
        self.ids.superhero_grid.add_widget(card)

    def guess_superhero(self):
        emoji1 = self.ids.emoji1_input.text.strip()
        emoji2 = self.ids.emoji2_input.text.strip()

        if not emoji1 or not emoji2:
            return
        self.ids.emoji1_input.text = ""
        self.ids.emoji2_input.text = ""
        emoji_pair = EmojiPair(emoji1=emoji1, emoji2=emoji2)
        superhero = EmojiGuesser.guess_superhero(emoji_pair)

        self.user_record.add_superhero(superhero)
        self._save_user_record()

        self._add_superhero_card(superhero)

class SuperheroEmojiGuessApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        return SuperheroEmojiApp()

if __name__ == "__main__":
    SuperheroEmojiGuessApp().run()