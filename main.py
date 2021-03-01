import pygame
import pygame.freetype
import os
import sys
from random import randint
from copy import deepcopy


def load_image(name, colorkey=None):
    fullname = os.path.join('pygame_data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    def __init__(self, coords, size, color, active_color,
                 text, text_color, text_active_color, font=None):
        pass


class Menu:
    def __init__(self, buttons):
        self.buttons = buttons

    def render(self, source, n=-1):
        for index, btn in enumerate(self.buttons):
            if index == n:
                color = btn[3]
                text_color = btn[6]
            else:
                color = btn[2]
                text_color = btn[5]
            font = pygame.font.Font(btn[7], 30)
            text = font.render(btn[4], True, text_color)
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = btn[1][0] // 2 - text_w // 2
            text_y = btn[1][1] // 2 - text_h // 2

            pygame.draw.rect(source, color, (btn[0] + btn[1]))
            source.blit(text, (text_x + btn[0][0], text_y + btn[0][1]))
        # pygame.display.flip()

    def menu(self, source):
        process = True
        while process:
            pos = pygame.mouse.get_pos()
            for index, btn in enumerate(self.buttons):
                n = -1
                if pos[0] >= btn[0][0] and pos[1] >= btn[0][1] and \
                        pos[0] <= btn[0][0] + btn[1][0] and \
                        pos[1] <= btn[0][1] + btn[1][1]:
                    n = index
                self.render(source, n)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, btn in enumerate(self.buttons):
                        n = -1
                        if pos[0] >= btn[0][0] and pos[1] >= btn[0][1] \
                                and pos[0] <= btn[0][0] + btn[1][0] \
                                and pos[1] <= btn[0][1] + btn[1][1]:
                            n = index
                            # в зависимости от кнопки какие то действия
            pygame.display.flip()


class Player(pygame.sprite.Sprite):
    image = load_image("ufo.png")

    def __init__(self, group, width, height):
        super().__init__(group)
        self.width = width
        self.height = height
        img = pygame.transform.scale(Player.image, (70, 70))
        self.image = img
        self.rect = self.image.get_rect()
        self.velocity = 0
        self.position = 250
        self.rect.x = 100
        self.rect.y = 200
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.height - 70 > self.rect.y + self.velocity >= 0:
            self.rect.x = 100
            self.rect.y = self.rect.y + self.velocity
        else:
            if self.rect.y + self.velocity < 0:
                self.rect.y = 0
            if self.height - 70 <= self.rect.y + self.velocity:
                self.rect.y = self.height - 60
            self.velocity = 0
        if self.velocity <= 20:
            self.velocity += 1


class Obstacle(pygame.sprite.Sprite):
    image_1 = load_image("meteorite_1.png")

    def __init__(self, group, width, height):
        super().__init__(group)
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(Obstacle.image_1, (382, 150))
        self.rect = self.image.get_rect()
        self.y_pos = randint(0, height - self.rect.height)
        self.rect.y = self.y_pos
        self.rect.x = 600
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.x = self.rect.x - 12

    def is_active(self):
        if self.rect.x + self.rect.width < 0:
            return False
        return True


class Game:
    def __init__(self, width, height):
        self.is_running = False
        self.width = width
        self.height = height
        self.player_group = pygame.sprite.Group()
        self.player = Player(self.player_group, width, height)
        self.obstacles = list()
        self.obstacles_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.backgrounds = [pygame.sprite.Sprite(self.background_group),
                            pygame.sprite.Sprite(self.background_group)]
        self.init_background()
        self.score = 0
        self.render()

    def reset(self):
        self.is_running = True
        self.player_group = pygame.sprite.Group()
        self.player = Player(self.player_group, width, height)
        self.obstacles = list()
        self.obstacles_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.backgrounds = [pygame.sprite.Sprite(self.background_group),
                            pygame.sprite.Sprite(self.background_group)]
        self.score = 0
        self.init_background()

    def init_background(self):
        image = load_image("background.png")
        self.img_wdh = image.get_rect().width
        self.backgrounds[0].rect = image.get_rect()
        self.backgrounds[0].rect.x = 0
        self.backgrounds[0].rect.y = 0
        self.backgrounds[0].image = image
        self.backgrounds[1].rect = image.get_rect()
        self.backgrounds[1].rect.x = self.img_wdh
        self.backgrounds[1].rect.y = 0
        self.backgrounds[1].image = image

    def update(self):
        if self.is_running:
            self.player.update()
            self.move_background()
            self.update_obstacles()

            self.render()

    def stop(self):
        self.is_running = False

    def render(self):
        self.background_group.draw(screen)
        self.player_group.draw(screen)
        self.obstacles_group.draw(screen)
        textsurface = pygame.font.SysFont('calibri', 25, bold=True).render(f'SCORE: {self.score}',
                                                                True,
                                                                (204, 204, 204))
        pygame.Surface.blit(screen, textsurface, (300, 10))

    def click(self):
        self.player.velocity = -12

    def move_background(self):
        self.backgrounds[0].rect.x = self.backgrounds[0].rect.x - 10
        self.backgrounds[1].rect.x = self.backgrounds[1].rect.x - 10
        if self.backgrounds[0].rect.x < -self.img_wdh:
            self.backgrounds[0].rect.x = self.img_wdh - 1
        if self.backgrounds[1].rect.x < -self.img_wdh:
            self.backgrounds[1].rect.x = self.img_wdh - 1

    def update_obstacles(self):
        new_obstacles = list()
        for obstacle in self.obstacles:
            if obstacle.is_active():
                obstacle.move()
                new_obstacles.append(obstacle)
            if pygame.sprite.collide_mask(obstacle, self.player):
                self.stop()
            if abs(obstacle.rect.x - self.player.rect.x + 1) <= 6:
                self.score += 1
        self.obstacles = new_obstacles.copy()

    def add_obstacle(self):
        obstacle = Obstacle(self.obstacles_group, self.width, self.height)
        self.obstacles.append(obstacle)


if __name__ == '__main__':
    width = 500
    height = 500
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Cosmos')
    screen = pygame.display.set_mode((width, height), vsync=1)
    running = True
    game_font = pygame.freetype.SysFont('calibri', 14)
    game = Game(width, height)
    game.render()
    CREATE_OBSTACLE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_OBSTACLE_EVENT, 1200)

    start_menu = Menu([[(100, 100), (300, 100), 'black', 'grey',
                        'Start Game', 'white', 'red', None],
                       [(100, 280), (300, 100), 'black', 'grey',
                        'Quit', 'white', 'red', None]]
                      )
    while running:
        start_menu.menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.click()
                if event.button == 2:  # Сделал функции сброса и остановки
                    game.reset()  # Работают пока на кнопки мыши,
                if event.button == 3:  # надо сделать чтобы экран вылазил
                    game.stop()  # и там по кнопкам это настроить
            if event.type == pygame.MOUSEWHEEL:
                game.add_obstacle()
            if event.type == CREATE_OBSTACLE_EVENT:
                game.add_obstacle()
        game.update()
        pygame.display.flip()
        clock.tick(30)
