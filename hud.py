import pygame
from constants import *

class Text():
    def __init__(self, string, antialiased=True, color=Colors.WHITE):
        self.font = pygame.font.Font('assets/Abrushow.ttf', 24)
        self.antialiased = antialiased
        self.color = color
        self.text = self.font.render(string, self.antialiased, self.color)
        self.rect = self.text.get_rect()


class UpdatableText(Text):
    def __init__(self, string, obj, attr=None, update_rect_after_re_render=False):
        self.string = string
        self.attr = attr if attr else self.string.lower().replace(" ", "_")
        self.obj = obj
        self.update_rect_after_re_render = update_rect_after_re_render

        super().__init__(self.build_formatted_text())

    def build_formatted_text(self):
        value = getattr(self.obj, self.attr)
        return f"{self.string}: {str(value)}"

    def re_render(self):
        self.text = self.font.render(self.build_formatted_text(), self.antialiased, self.color)
        if self.update_rect_after_re_render:
            self.rect = self.text.get_rect()


class HUD:
    def __init__(self, *items):
        self.items = items
        self.updatable_items = [i for i in self.items if type(i) == UpdatableText]

    def draw(self, window):
        for item in self.items:
            window.blit(item.text, item.rect)

    def update(self):
        for item in self.updatable_items:
            item.re_render()