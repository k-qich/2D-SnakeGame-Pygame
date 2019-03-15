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
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)


class SnakeHead(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
        # player attributes
        self.dx = TILE_SIZE
        self.dy = 0

        self.last_movement_time = 0
        self.movement_interval = PLAYER_SPEED       # how fast the snake will be moving

    def update(self):
        t_now = pg.time.get_ticks()

        # regulate snake's movement speed
        if t_now - self.last_movement_time > self.movement_interval:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.last_movement_time = t_now


class SnakeBody:
    pass


class Apple(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
