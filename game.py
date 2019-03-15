from constants import *
import pygame as pg
import sys


# Simple snake game created in pygame
class Game:
    def __init__(self, display_width, display_height):
        # initializing pygame window
        self.display_width = display_width
        self.display_height = display_height
        self.display_name = DISPLAY_TITLE

        pg.init()
        pg.mixer.init()
        self.gameDisplay = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption(self.display_name)

        self.clock = pg.time.Clock()
        self.running = False

    def update(self):
        pass

    def render(self):
        # rendering the game background
        self.gameDisplay.fill(WHITE)

        # draw game grid
        for x in range(0, DISPLAY_WIDTH, TILE_SIZE):
            pg.draw.line(self.gameDisplay, BLACK, (x, 0), (x, DISPLAY_HEIGHT))
        for y in range(0, DISPLAY_HEIGHT, TILE_SIZE):
            pg.draw.line(self.gameDisplay, BLACK, (0, y), (DISPLAY_WIDTH, y))

    def game_event_handler(self):
        # processing player inputs
        for event in pg.event.get():
            # game window closed
            if event.type == pg.QUIT:
                self.exit()

    # GAME LOOP
    def game_loop(self):
        print("Game Running!")
        # game loop
        self.running = True
        while self.running:
            # event handling
            self.game_event_handler()

            # update
            self.update()

            # draw/render
            self.render()

            # pygame double buffering
            pg.display.flip()

            # defining the fps of game
            self.clock.tick(FPS)

    def run(self):
        self.game_loop()
        self.exit()

    def exit(self):
        print("Quitting")
        pg.quit()
        sys.exit()


# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    game = Game(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    game.run()