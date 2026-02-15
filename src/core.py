class Core:
    def __init__(self):
        self.current_mode = None
        self.active_input = ""

    def modify_input(self, new: str) -> None:
        self.active_input = new

    def run(self):
        self.display()
        self.modify_input("")

    def display(self):
        if self.active_input:
            print(self.active_input)
