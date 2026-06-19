from typing import Optional

class JazzGoblin:
    music: bool = False
    rhythm: bool = False
    my_man: bool = False

    def __init__(self, music: bool = False, rhythm: bool = False, my_man: bool = False):
        self.music = music
        self.rhythm = rhythm
        self.my_man = my_man

    def ask_for_more(self):
        if self.music and self.rhythm and self.my_man:
            print("who could ask for anything more?")
        else:
            print("I could ask for more, yeah.")

    def feed(self, food: Optional[bool] = False):
        if food:
            print("nom nom nom")
            self.ask_for_more()
        else:
            print("> : (")

# Klingon poetry below
