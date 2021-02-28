import random

import pygame
import pygame.freetype
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('pygame_data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    image = load_image("ufo.png")

    def __init__(self, group, width, height):
        super().__init__(group)
        self.width = width
        self.height = height
        img = pygame.transform.scale(Player.image, (50, 50))
        self.image = img
        self.rect = self.image.get_rect()
        self.velocity = 0.
        self.position = 250
        self.rect.x = 50
        self.rect.y = 200

    def update(self):
        if self.height > self.rect.y + self.velocity > 0:
            self.rect.x = 50
            self.rect.y = self.rect.y + self.velocity
            self.velocity += 1
        else:
            if self.rect.y + self.velocity <= 0:
                velocity = 0


class Obstacle(pygame.sprite.Sprite):
    pass


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player_group = pygame.sprite.Group()
        self.player = Player(self.player_group, width, height)
        self.obstacles = list()

    def render(self):
        self.player_group.draw(screen)
        self.player.update()

    def click(self):
        self.player.velocity = -20


if __name__ == '__main__':
    width = 500
    height = 500
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode((width, height))
    running = True
    GAME_FONT = pygame.freetype.SysFont('calibri', 14)
    game = Game(width, height)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.click()
        screen.fill('white')
        game.render()
        pygame.display.flip()
        clock.tick(30)
