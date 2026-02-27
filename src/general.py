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


class Button(Div):
    def __init__(self, size: tuple, pos: tuple, name: str):
        super().__init__(size, pos)
        self.name = get_screen_text_for(name, size[1] // 3)
        self.name_rect = self.name.get_rect()
        self.name_rect.center = (
            self.surface.get_width() // 2,
            self.surface.get_height() // 2,
        )
        self.surface.fill((0, 0, 50))

    def display(self, screen: pygame.surface):
        self.surface.blit(self.name, self.name_rect)
        screen.blit(self.surface, self.hit_box)


def get_screen_text_for(text: str, size: int):
    font = pygame.font.SysFont("Arial", size)
    screen_text = font.render(text, True, (255, 255, 255))
    return screen_text
