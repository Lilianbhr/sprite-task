import pygame
from src.components.general import Div
from src.components.general import get_screen_text_for


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
        self.screen_text = self.wrap(self.raw_text)

    def wrap(self, text: str, origin=(0, 0)) -> list:  # ----------------------------------------------
        """
        Gère l'attribution des positions de chaque mots du texte fournit.
        """
        # initialisation
        screen_text = []
        x, y = origin
        words = []

        # Words building
        word = ""
        for char in text:
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
            elif x + word_rect.width <= self.hit_box.width:
                word_rect.topleft = (x, y)
                x += word_rect.width

            # Le mot dépasse de la ligne
            else:
                x = 0
                y += word_rect.height
                word_rect.topleft = (x, y)
                x += word_rect.width

            screen_text.append((screen_word, word_rect))

        return screen_text

    def display(self, screen: pygame.Surface):  # -------------------
        self.surface.fill((0, 0, 0))
        for elt in self.screen_text:
            self.surface.blit(elt[0], elt[1])
        screen.blit(self.surface, self.hit_box)
