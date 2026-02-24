# stark_mode.py

import re

class StarkMode:

    def __init__(self):
        self.enabled = True
        self.user_title = "Chefe"
        self.max_words = 25

    # remove símbolos e emojis
    def clean_text(self, text):
        text = re.sub(r"[^\w\s.,!?]", "", text)
        return text

    # estilo de resposta do jarvis
    def format_response(self, text):

        text = self.clean_text(text)

        words = text.split()
        text = " ".join(words[:self.max_words])

        return f"{self.user_title}, {text}"

    # personalidade stark
    def personality_filter(self, text):

        replace_map = {
            "eu acho": "",
            "talvez": "",
            "por favor": "",
            "😊": "",
            "*": ""
        }

        for k, v in replace_map.items():
            text = text.replace(k, v)

        return text

    def process(self, text: str) -> str:
        if not text:
            return text

        # remove duplicação tipo "Chefe Chefe"
        text = text.replace("Chefe, Chefe", "Chefe")
        text = text.replace("Chefe Chefe", "Chefe")

        # evita repetir prefixo
        if not text.startswith("Chefe"):
            text = "Chefe, " + text

        return text