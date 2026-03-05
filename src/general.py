"""
Ce fichier contient l'ensemble des ressources abstraites
utilisées depuis n'importe quel endroit du système.
"""

import pygame


class Div:
    """
    Composant à la source de la structure par emboitement du projet.
    """
    def __init__(self, size: tuple, pos: tuple):
        self.surface = pygame.Surface(size)
        self.hit_box = self.surface.get_rect()
        self.hit_box.topleft = pos

    def is_under(self, point: tuple) -> bool:
        if self.hit_box.collidepoint(point):
            return True
        return False

    def get_relative_pos(self, point: tuple) -> tuple:
        """ Donne la position relative d'un point
        à l'interieur de lui même (depuis son parent) """
        return point[0] - self.hit_box.left, point[1] - self.hit_box.top

# ============================================================================


class Button(Div):
    """
    Div qui ne contient qu'un seul texte centré.
    """
    def __init__(self, size: tuple, pos: tuple, name: str):
        super().__init__(size, pos)
        self.name = get_screen_text_for(name, size[1] // 3)
        self.name_rect = self.name.get_rect()
        self.name_rect.center = (
            self.surface.get_width() // 2,
            self.surface.get_height() // 2,
        )
        self.surface.fill((50, 0, 0))

    def display(self, screen: pygame.surface):
        self.surface.blit(self.name, self.name_rect)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class CheckBox(Div):
    """
    Div qui n'existe qu'en deux états disctincts.
    """
    def __init__(self, size: tuple, pos: tuple, state=False):
        super().__init__(size, pos)
        self.state = state
        self.color_state()

    def switch_state(self):  # --------------------------------------
        if self.state:
            self.state = False
        else:
            self.state = True
        self.color_state()

    def color_state(self):  # ---------------------------------------
        """ L'état est représenté visuellement par une couleur. """
        if self.state:
            self.surface.fill((255, 255, 0))
        else:
            self.surface.fill((255, 0, 255))

    def get_state(self):  # -----------------------------------------
        return self.state

    def display(self, screen: pygame.Surface):  # -------------------
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class Text(Div):
    """
    Manage le texte affiché sur une surface pour
    lui permettre de s'adapter à la taille du conteneur.
    """
    def __init__(self, size: tuple, pos: tuple, text: str, font_size: int):
        super().__init__(size, pos)
        self.raw_text = text
        self.font_size = font_size

        # Text for screen
        self.screen_text = []
        self.wrap()

    def wrap(self):  # ----------------------------------------------
        """
        Gère l'attribution des positions de chaque mots du texte fournit.
        """
        # initialisation
        x = 0
        y = 0
        words = []

        # Words builing
        word = ""
        for char in self.raw_text:
            if char == " ":
                if word:
                    words.append(word)
                    word = ""
                words.append(char)
            else:
                word += char
        if word:
            words.append(word)

        # Récuperation de la taille de chaque mot
        for word in words:
            screen_word = get_screen_text_for(word, self.font_size)
            word_rect = screen_word.get_rect()

            # Si c'est le premier mot sur la ligne
            if x == 0:
                word_rect.topleft = (x, y)
                x += word_rect.width

            # Si le mot rentre entièrement sur la ligne
            elif x + word_rect.width <= self.hit_box.right:
                word_rect.topleft = (x, y)
                x += word_rect.width

            # Le mot dépasse de la ligne
            else:
                x = 0
                y += word_rect.height
                word_rect.topleft = (x, y)
                x += word_rect.width

            self.screen_text.append((screen_word, word_rect))

    def display(self, screen: pygame.Surface):  # -------------------
        for elt in self.screen_text:
            self.surface.blit(elt[0], elt[1])
        screen.blit(self.surface, self.hit_box)

# ============================================================================


def get_screen_text_for(text: str, size: int):
    """ Renvoie un texte sous un format exploitable
    pour l'affichage de pygame """
    font = pygame.font.SysFont("Arial", size)
    screen_text = font.render(text, True, (255, 255, 255))
    return screen_text
