import pygame


class Div:
    def __init__(self, size: tuple, pos: tuple):
        self.surface = pygame.Surface(size)
        self.hit_box = self.surface.get_rect()
        self.hit_box.topleft = pos

    def is_under(self, point: tuple) -> bool:
        if self.hit_box.collidepoint(point):
            return True
        return False

    def get_relative_pos(self, point: tuple) -> tuple:
        return point[0] - self.hit_box.left, point[1] - self.hit_box.top


def get_screen_text_for(text: str, size: int):
    font = pygame.font.SysFont("Arial", size)
    screen_text = font.render(text, True, (255, 255, 255))
    return screen_text
