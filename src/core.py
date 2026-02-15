from choose_interface import Choose
from list_interface import TaskList


class Core:
    def __init__(self, screen):
        self.screen = screen
        self.current_mode = Choose()
        self.active_input = ""

    def modify_input(self, new: str) -> None:
        self.active_input = new

    def run(self):
        self.update()
        self.current_mode.display(self.screen)
        self.modify_input("")

    def update(self):
        ret = self.current_mode.update(self.active_input)
        if ret:
            print(ret)
