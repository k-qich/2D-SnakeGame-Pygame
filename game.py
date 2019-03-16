from constants import *
import entity
import pygame as pg
import random
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

        # game vars
        self.apples_eaten = 0
        self.max_length = 0
        self.last_movement_time = 0
        self.movement_interval = PLAYER_SPEED       # how fast the snake will be moving
        self.restart = False

        # game objects
        self.snake_head = None
        self.snake = []

        # sprite groups
        self.snake_sprites = pg.sprite.Group()
        self.snake_body_sprites = pg.sprite.Group()
        self.apple_sprite = pg.sprite.Group()

        self.clock = pg.time.Clock()
        self.running = False

    def init_game_vars(self):
        self.snake_head = entity.SnakeHead(int(self.display_width/TILE_SIZE/2) * TILE_SIZE, int(self.display_height/TILE_SIZE/2) * TILE_SIZE, GREEN)
        self.snake_sprites.add(self.snake_head)
        self.snake.append(self.snake_head)

        self.max_length += 1

    def update(self):
        if not self.apple_sprite:
            self.generate_new_apple()

        t_now = pg.time.get_ticks()

        # regulate snake's movement speed
        if t_now - self.last_movement_time > self.movement_interval:
            self.last_movement_time = t_now
            self.snake_sprites.update()
            self.snake_body_sprites.update()

            # check if snake has collided with itself
            if pg.sprite.spritecollide(self.snake_head, self.snake_body_sprites, False):
                self.running = False

            # check if snake has collided with an apple
            apple_collision = pg.sprite.spritecollide(self.snake_head, self.apple_sprite, False)
            for apple in apple_collision:
                apple.kill()
                self.grow_snake()

                # increment stat tracker
                self.apples_eaten += 1
                self.max_length += 1

            # update the snake's body
            if len(self.snake) > 1:
                for i in range(1, len(self.snake), 1):
                    self.snake[i].last_posx = self.snake[i].rect.topleft[0]
                    self.snake[i].last_posy = self.snake[i].rect.topleft[1]
                    self.snake[i].rect.topleft = (self.snake[i - 1].last_posx, self.snake[i - 1].last_posy)

            # check if player is going out of bounds
            if self.boundary_check():
                self.running = False

    def render(self):
        # rendering the game background
        self.gameDisplay.fill(WHITE)

        # render apple
        self.apple_sprite.draw(self.gameDisplay)

        # render player
        self.snake_sprites.draw(self.gameDisplay)
        self.snake_body_sprites.draw(self.gameDisplay)

        # draw game grid
        for x in range(0, DISPLAY_WIDTH, TILE_SIZE):
            pg.draw.line(self.gameDisplay, BLACK, (x, 0), (x, DISPLAY_HEIGHT))
        for y in range(0, DISPLAY_HEIGHT, TILE_SIZE):
            pg.draw.line(self.gameDisplay, BLACK, (0, y), (DISPLAY_WIDTH, y))

    def game_intro_event_handler(self):
        pass

    def game_event_handler(self):
        keys = pg.key.get_pressed()

        # processing player inputs
        for event in pg.event.get():
            # game window closed
            if event.type == pg.QUIT:
                self.exit()

        # player movement
        if keys[pg.K_LEFT] and self.snake_head.dx == 0:
            self.snake_head.dy = 0
            self.snake_head.dx = -TILE_SIZE
        if keys[pg.K_RIGHT] and self.snake_head.dx == 0:
            self.snake_head.dy = 0
            self.snake_head.dx = TILE_SIZE
        if keys[pg.K_UP] and self.snake_head.dy == 0:
            self.snake_head.dx = 0
            self.snake_head.dy = -TILE_SIZE
        if keys[pg.K_DOWN] and self.snake_head.dy == 0:
            self.snake_head.dx = 0
            self.snake_head.dy = TILE_SIZE

    def game_over_event_handler(self):
        mouse_pos = pg.mouse.get_pos()
        in_menu = True
        restart_btn_col = BLACK
        quit_btn_col = BLACK

        restart_btn = self.display_text(pg.font.SysFont(TEXT_FONT, int(TEXT_SIZE / 1.2)), "RESTART", restart_btn_col, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 50)
        quit_btn = self.display_text(pg.font.SysFont(TEXT_FONT, int(TEXT_SIZE / 1.2)), "QUIT", quit_btn_col, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 100)

        # processing player inputs
        for event in pg.event.get():
            # game window closed
            if event.type == pg.QUIT:
                self.exit()

        # menu button hover for quit
        if restart_btn.collidepoint(mouse_pos):
            restart_btn_col = LIGHTERBLACK
            if pg.mouse.get_pressed()[0] == 1:
                in_menu = False
                self.restart = True

        # menu button hover for quit
        if quit_btn.collidepoint(mouse_pos):
            quit_btn_col = LIGHTERBLACK
            if pg.mouse.get_pressed()[0] == 1:
                in_menu = False

        self.display_text(pg.font.SysFont(TEXT_FONT, TEXT_SIZE), "GAME OVER", BLACK, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 100)
        self.display_text(pg.font.SysFont(TEXT_FONT, int(TEXT_SIZE / 1.5)), "APPLES: " + str(self.apples_eaten), RED, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 50)
        self.display_text(pg.font.SysFont(TEXT_FONT, int(TEXT_SIZE / 1.5)), "LENGTH: " + str(self.max_length), GREEN, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 20)

        restart_btn = self.display_text(pg.font.SysFont(TEXT_FONT, int(TEXT_SIZE / 1.2)), "RESTART", restart_btn_col, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 50)
        quit_btn = self.display_text(pg.font.SysFont(TEXT_FONT, int(TEXT_SIZE / 1.2)), "QUIT", quit_btn_col, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 100)

        return in_menu

    # GAME LOOP
    def game_loop(self):
        print("Game Running!")

        # init game objects
        self.init_game_vars()

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

    def game_over(self):
        print("Game Over")
        is_game_over = True
        menu_box = pg.Rect(0, 0, GAME_OVER_MENU_SIZE, GAME_OVER_MENU_SIZE)
        menu_box.center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
        menu_box2 = pg.Rect(0, 0, GAME_OVER_MENU_SIZE - 2, GAME_OVER_MENU_SIZE - 2)
        menu_box2.center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

        pg.display.flip()

        while is_game_over:
            pg.draw.rect(self.gameDisplay, BLACK, menu_box, 1)
            pg.draw.rect(self.gameDisplay, WHITE, menu_box2)

            is_game_over = self.game_over_event_handler()

            pg.display.flip()

    def display_text(self, font, text, color, x, y):
        display_text = font.render(text, True, color)
        btn = display_text.get_rect()
        btn.center = (x, y)
        self.gameDisplay.blit(display_text, btn)
        return btn

    # returns true/false depending on whether the player has exceeded the game window
    def boundary_check(self):
        return self.snake_head.rect.top < 0 or self.snake_head.rect.bottom > DISPLAY_HEIGHT \
               or self.snake_head.rect.left < 0 or self.snake_head.rect.right > DISPLAY_WIDTH

    # creates a new random position for an apple
    def generate_new_apple(self):
        posy = random.randint(0, int((DISPLAY_HEIGHT - TILE_SIZE)/TILE_SIZE))
        posx = random.randint(0, int((DISPLAY_WIDTH - TILE_SIZE)/TILE_SIZE))
        apple = entity.Apple(posx * TILE_SIZE, posy * TILE_SIZE, RED)
        self.apple_sprite.add(apple)

    # increases the length of the snake upon consuming an apple
    def grow_snake(self):
        # add new snake body to the end of the snake
        snake_body = entity.SnakeBody(self.snake[-1].last_posx, self.snake[-1].last_posy, GREEN)
        self.snake_body_sprites.add(snake_body)
        self.snake.append(snake_body)

    def run(self):
        self.game_loop()
        self.game_over()
        if self.restart:
            self.restart_game()
            self.run()
        else:
            self.exit()

    def restart_game(self):
        # resetting game vars
        self.snake_sprites = pg.sprite.Group()
        self.snake_body_sprites = pg.sprite.Group()
        self.apple_sprite = pg.sprite.Group()

        self.last_movement_time = 0
        self.snake = []

        self.apples_eaten = 0
        self.max_length = 0
        self.restart = False

    def exit(self):
        print("Quitting")
        pg.quit()
        sys.exit()


# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    game = Game(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    game.run()
