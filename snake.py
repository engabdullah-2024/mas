# snake.py — One-file Snake game (pygame)
# Author: Senior Python build
# Features: fixed-timestep movement, pause, restart, wrap toggle, persistent high score, clean structure.

import os
import sys
import random
from collections import deque
import pygame as pg

# -----------------------------
# Config (easy to tweak)
# -----------------------------
TILE_SIZE = 24
GRID_W, GRID_H = 28, 20                  # total tiles in each dimension
SCREEN_W, SCREEN_H = GRID_W*TILE_SIZE, GRID_H*TILE_SIZE

MOVE_EVERY_MS = 110                      # snake moves once per this many ms (fixed step)
START_LEN = 4
BG_COLOR = (18, 18, 20)
SNAKE_HEAD = (40, 200, 120)
SNAKE_BODY = (30, 150, 95)
FOOD_COLOR = (235, 64, 52)
GRID_COLOR = (40, 42, 46)
TEXT_COLOR = (225, 225, 230)
PAUSE_OVERLAY = (0, 0, 0, 120)

FONT_NAME = pg.font.get_default_font()
HISCORE_FILE = "snake_highscore.txt"

# Directions (dx, dy)
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

class SnakeGame:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Snake — pygame (One File)")
        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pg.time.Clock()
        self.font_small = pg.font.Font(FONT_NAME, 18)
        self.font_big = pg.font.Font(FONT_NAME, 36)

        self.show_grid = False
        self.wrap = False

        self.reset()
        self.hiscore = self.load_hiscore()

    def reset(self):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = deque([(cx - i, cy) for i in range(START_LEN)])  # head is leftmost
        self.direction = RIGHT
        self.pending_dir = RIGHT
        self.spawn_food()
        self.score = 0
        self.dead = False
        self.paused = False
        self.accum_time = 0  # for fixed-timestep movement

    def load_hiscore(self):
        try:
            if os.path.exists(HISCORE_FILE):
                with open(HISCORE_FILE, "r", encoding="utf-8") as f:
                    return int(f.read().strip() or "0")
        except Exception:
            pass
        return 0

    def save_hiscore(self):
        try:
            if self.score > self.hiscore:
                with open(HISCORE_FILE, "w", encoding="utf-8") as f:
                    f.write(str(self.score))
        except Exception:
            # not fatal if writing fails
            pass

    def spawn_food(self):
        free = [(x, y) for x in range(GRID_W) for y in range(GRID_H) if (x, y) not in self.snake]
        self.food = random.choice(free) if free else None

    def handle_input(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.save_hiscore()
                pg.quit()
                sys.exit(0)
            elif e.type == pg.KEYDOWN:
                if e.key in (pg.K_ESCAPE,):
                    self.save_hiscore()
                    pg.quit()
                    sys.exit(0)
                elif e.key in (pg.K_p,):
                    if not self.dead:
                        self.paused = not self.paused
                elif e.key in (pg.K_r,):
                    self.save_hiscore()
                    self.reset()
                elif e.key in (pg.K_g,):
                    self.show_grid = not self.show_grid
                elif e.key in (pg.K_w,):
                    self.wrap = not self.wrap

                # Direction changes (prevent reversing into yourself)
                elif e.key in (pg.K_UP, pg.K_w):
                    self.try_set_dir(UP)
                elif e.key in (pg.K_DOWN, pg.K_s):
                    self.try_set_dir(DOWN)
                elif e.key in (pg.K_LEFT, pg.K_a):
                    self.try_set_dir(LEFT)
                elif e.key in (pg.K_RIGHT, pg.K_d):
                    self.try_set_dir(RIGHT)

    def try_set_dir(self, new_dir):
        # Can't reverse directly into the opposite direction in the same tick
        if new_dir != OPPOSITE.get(self.direction, None):
            self.pending_dir = new_dir

    def step(self):
        if self.dead or self.paused:
            return

        # Fixed timestep for movement
        self.accum_time += self.clock.get_time()
        while self.accum_time >= MOVE_EVERY_MS:
            self.accum_time -= MOVE_EVERY_MS
            self.direction = self.pending_dir

            head_x, head_y = self.snake[0]
            dx, dy = self.direction
            nx, ny = head_x + dx, head_y + dy

            if self.wrap:
                nx %= GRID_W
                ny %= GRID_H
            else:
                # Wall collision
                if nx < 0 or nx >= GRID_W or ny < 0 or ny >= GRID_H:
                    self.dead = True
                    self.save_hiscore()
                    return

            new_head = (nx, ny)

            # Self collision
            if new_head in self.snake:
                self.dead = True
                self.save_hiscore()
                return

            # Move snake
            self.snake.appendleft(new_head)

            # Eat / grow
            if self.food and new_head == self.food:
                self.score += 1
                if self.score > self.hiscore:
                    self.hiscore = self.score
                self.spawn_food()
            else:
                self.snake.pop()

    def draw_grid(self):
        for x in range(0, SCREEN_W, TILE_SIZE):
            pg.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_H), 1)
        for y in range(0, SCREEN_H, TILE_SIZE):
            pg.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_W, y), 1)

    def draw_snake(self):
        # head
        if self.snake:
            hx, hy = self.snake[0]
            head_rect = pg.Rect(hx*TILE_SIZE, hy*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pg.draw.rect(self.screen, SNAKE_HEAD, head_rect, border_radius=6)

            # eyes (tiny)
            center = head_rect.center
            eye_r = max(2, TILE_SIZE // 8)
            dx, dy = self.direction
            eye_offset = TILE_SIZE // 5
            pg.draw.circle(self.screen, (10, 40, 30), (center[0] + dx*eye_offset - dy*eye_offset//2,
                                                      center[1] + dy*eye_offset + dx*eye_offset//2), eye_r)
            pg.draw.circle(self.screen, (10, 40, 30), (center[0] + dx*eye_offset + dy*eye_offset//2,
                                                      center[1] + dy*eye_offset - dx*eye_offset//2), eye_r)

        # body
        for i, (x, y) in enumerate(list(self.snake)[1:]):
            r = pg.Rect(x*TILE_SIZE+2, y*TILE_SIZE+2, TILE_SIZE-4, TILE_SIZE-4)
            pg.draw.rect(self.screen, SNAKE_BODY, r, border_radius=5)

    def draw_food(self):
        if not self.food:
            return
        x, y = self.food
        r = pg.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pg.draw.rect(self.screen, FOOD_COLOR, r.inflate(-6, -6), border_radius=8)

    def draw_hud(self):
        left = f"Score: {self.score}"
        right = f"High: {self.hiscore}   {'WRAP: ON' if self.wrap else 'WRAP: OFF'}"
        l_surf = self.font_small.render(left, True, TEXT_COLOR)
        r_surf = self.font_small.render(right, True, TEXT_COLOR)

        self.screen.blit(l_surf, (8, 6))
        self.screen.blit(r_surf, (SCREEN_W - r_surf.get_width() - 8, 6))

    def draw_pause_or_gameover(self):
        if self.paused or self.dead:
            overlay = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)
            overlay.fill(PAUSE_OVERLAY)
            self.screen.blit(overlay, (0, 0))

            if self.dead:
                title = "Game Over"
                sub = "Press R to restart — Esc to quit"
            else:
                title = "Paused"
                sub = "Press P to resume — R to restart"

            t_surf = self.font_big.render(title, True, TEXT_COLOR)
            s_surf = self.font_small.render(sub, True, TEXT_COLOR)
            self.screen.blit(t_surf, (SCREEN_W//2 - t_surf.get_width()//2, SCREEN_H//2 - 40))
            self.screen.blit(s_surf, (SCREEN_W//2 - s_surf.get_width()//2, SCREEN_H//2 + 6))

    def draw(self):
        self.screen.fill(BG_COLOR)
        if self.show_grid:
            self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_hud()
        self.draw_pause_or_gameover()
        pg.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.step()
            self.draw()
            # Limit render FPS; movement uses fixed timestep via accum_time
            self.clock.tick(60)

if __name__ == "__main__":
    SnakeGame().run()
