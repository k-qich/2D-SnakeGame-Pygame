from constants import *
import pygame as pg


# Base class for any entity
class Entity(pg.sprite.Sprite):
    def __init__(self, x, y, colour):
        super().__init__()
        self.colour = colour

        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(self.colour)

        # defines boundaries of sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class SnakeHead(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
        # player attributes
        self.dx = TILE_SIZE
        self.dy = 0

        # keeps track of players last position
        self.last_posx = x
        self.last_posy = y

    def update(self):
        # save snake's last position
        self.last_posx = self.rect.x
        self.last_posy = self.rect.y

        # update snake's position
        self.rect.x += self.dx
        self.rect.y += self.dy


class SnakeBody(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)

        # keeps track of the body's last position
        self.last_posx = x
        self.last_posy = y


class Apple(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
