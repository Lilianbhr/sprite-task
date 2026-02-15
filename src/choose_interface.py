import pygame
import general


class Choose:
    def __init__(self):
        self.elements = []
        self.mood_1 = general.Button("mood_1", "test", (500, 500), (255, 0, 0))
        self.elements.append(self.mood_1)

    def update(self, active_input: str) -> str:
        if active_input == "mouse_click":
            mouse_pos = pygame.mouse.get_pos()
            for elt in self.elements:
                if elt.collided(mouse_pos):
                    return elt.get_destination()
        return ""

    def display(self, screen: pygame.Surface):
        self.mood_1.display(screen)
