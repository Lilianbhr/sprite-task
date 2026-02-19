import pygame


class Button:
    def __init__(self, name: str, dest: str, center: tuple, color: tuple):
        self.screen_text = get_screen_text_for(name, 24)
        self.destination = dest
        self.center = center
        self.screen_rect = self.screen_text.get_rect()
        self.screen_rect.center = self.center
        self.hit_box = self.add_padding(self.screen_rect, 10)
        self.color = color

    def collided(self, mouse_pos: tuple[int, int]) -> bool:
        if self.hit_box.collidepoint(mouse_pos):
            return True
        return False

    def get_destination(self):
        return self.destination

    @staticmethod
    def add_padding(rect: pygame.Rect, padding: int) -> pygame.Rect:
        res = rect.__copy__()
        res.width += padding * 2
        res.height += padding * 2
        res.top -= padding
        res.left -= padding
        return res

    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.hit_box)
        screen.blit(self.screen_text, self.screen_rect)


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
