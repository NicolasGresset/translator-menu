"""
Let's build an application that allows me to enter a prompt for a given word and uses
linguee backend api in order to provide an accurate translation
It should use linguee's feature of guessing the sense of the translation
It is meant to only use english <--> french dictionnary as it the 2 main languages
I work on
"""

import requests
import tkinter as tk
from bs4 import BeautifulSoup


class Lingueebackend:
    def __init__(self) -> None:
        self.base_url = "http://www.linguee.fr/francais-anglais/search"

    def get_translation(self, word: str) -> list:
        try:
            response = requests.get(self.base_url, params={"query": word})
            response.raise_for_status()

            # Utilisation de BeautifulSoup pour analyser la réponse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            matching_tags = soup.find_all(
                lambda tag: tag.has_attr("id") and "dictEntry" in tag["id"]
            )

            if not matching_tags or len(matching_tags) == 0:
                return ["No translation found", "", ""]

            nb_translations = min(len(matching_tags), 3)
            translations = ["", "", ""]
            for i in range(nb_translations):
                translations[i] = matching_tags[i].get_text()
            return translations

        except requests.exceptions.RequestException as e:
            return ["No translation found", "", ""]


class Translation(tk.LabelFrame):
    def __init__(self, master=None, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.label1 = tk.Label(self, text="")
        self.label1.grid(row=0, column=0, sticky="nsew")

        self.label2 = tk.Label(self, text="")
        self.label2.grid(row=1, column=0, sticky="nsew")

        self.label3 = tk.Label(self, text="")
        self.label3.grid(row=2, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def update(self, translations: list):
        self.label1.config(text=translations[0])
        self.label2.config(text=translations[1])
        self.label3.config(text=translations[2])


class Prompt(tk.Entry):
    def __init__(self, master=None, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(fg="black")

    def on_query(self, *args):
        self.delete(0, tk.END)


class LingueeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.traductor = Lingueebackend()

        self.title("Linguee App")
        self.geometry("200x300")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        self.create_widgets()

        self.bind("<Escape>", lambda e: self.quit())

    def create_widgets(self):
        self.prompt = Prompt(self)

        self.prompt.grid(row=0, column=0, sticky="nsew")
        self.prompt.focus()
        self.prompt.bind("<Return>", self.on_query)

        self.response = Translation(self)
        self.response.grid(row=1, column=0, sticky="nsew")

    def on_query(self, *args) -> None:
        translations = self.traductor.get_translation(self.prompt.get())
        self.response.update(translations)
        self.prompt.on_query()


if __name__ == "__main__":
    myapp = LingueeApp()
    myapp.mainloop()
