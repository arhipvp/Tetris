import pygame
import sys
import random

# Game configuration
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0),    # Z
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[2, 0, 0],
     [2, 2, 2]],
    [[0, 0, 3],
     [3, 3, 3]],
    [[4, 4],
     [4, 4]],
    [[0, 5, 5],
     [5, 5, 0]],
    [[0, 6, 0],
     [6, 6, 6]],
    [[7, 7, 0],
     [0, 7, 7]]
]

def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))][::-1] for x in range(len(shape[0]))]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]

    def rotate(self):
        self.shape = rotate(self.shape)

class Tetris:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.new_piece()
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        self.piece = Piece(COLS // 2 - len(shape[0]) // 2, 0, shape)

    def collide(self, dx, dy, shape=None):
        if shape is None:
            shape = self.piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = x + self.piece.x + dx
                    ny = y + self.piece.y + dy
                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def freeze(self):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.piece.y][x + self.piece.x] = cell
        self.clear_lines()
        self.new_piece()
        if self.collide(0, 0):
            self.__init__()

    def clear_lines(self):
        new_board = [row for row in self.board if any(v == 0 for v in row)]
        lines_cleared = ROWS - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0] * COLS)
        self.board = new_board
        self.score += lines_cleared

    def move(self, dx, dy):
        if not self.collide(dx, dy):
            self.piece.x += dx
            self.piece.y += dy
        elif dy:
            self.freeze()

    def rotate_piece(self):
        new_shape = rotate(self.piece.shape)
        if not self.collide(0, 0, new_shape):
            self.piece.shape = new_shape

    def drop(self):
        while not self.collide(0, 1):
            self.piece.y += 1
        self.freeze()

    def draw(self, surface):
        surface.fill(BLACK)
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, COLORS[cell-1], (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, GRAY, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    px = (self.piece.x + x) * CELL_SIZE
                    py = (self.piece.y + y) * CELL_SIZE
                    pygame.draw.rect(surface, self.piece.color, (px, py, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(surface, GRAY, (px, py, CELL_SIZE, CELL_SIZE), 1)


def main():
    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0
    fall_speed = 500  # milliseconds

    running = True
    while running:
        delta = clock.tick(FPS)
        fall_time += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    game.drop()
        if fall_time > fall_speed:
            fall_time = 0
            game.move(0, 1)
        game.draw(surface)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
