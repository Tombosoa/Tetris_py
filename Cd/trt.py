import random
import os
import sys
import time

FORMS = [
    [[
        '.....',
        '.....',
        '.....',
        '0000.',
        '.....'
    ],
        [
            '.....',
            '..0..',
            '..0..',
            '..0..',
            '..0..'
        ]], [
        [
            '.....',
            '.....',
            '..0..',
            '.000.',
            '.....'
        ], [
            '.....',
            '..0..',
            '.00..',
            '..0..',
            '.....'
        ], [
            '.....',
            '.....',
            '.000.',
            '..0..',
            '.....'
        ], [
            '.....',
            '..0..',
            '..00.',
            '..0..',
            '.....'
        ]],
]

COLORS = ['red', 'green', 'blue', 'yellow']

GRID_SIZE = 10

WIDTH = GRID_SIZE * 10
HEIGHT = GRID_SIZE * 20


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(FORMS)
        return Tetromino(self.width // 2, 0, shape)

    def valid_move(self, piece, x, y, rotation):
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == '0' and (self.grid[piece.y + i + y][piece.x + j + x] != 0):
                        return False
                except IndexError:
                    return False
        return True

    def clear_lines(self):
        lines_cleared = 0
        for i, row in enumerate(self.grid[:-1]):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        return lines_cleared

    def update(self):
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

    def lock_piece(self, piece):
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == '0':
                    self.grid[piece.y + i][piece.x + j] = piece.color
        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100
        self.current_piece = self.new_piece()

        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
        return lines_cleared


def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def main():
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
    fall_time = 0
    fall_speed = 50

    while True:
        bg_color = generate_random_color()

        os.system(f'echo -ne "\033]11;rgb: {bg_color[0]}/{bg_color[1]}/{bg_color[2]}\007')
        if os.isatty(sys.stdin.fileno()):
            keys = os.popen('stty -icanon -echo; cat').read()

        if 'q' in keys:
            break
        if 'f' in keys:
            if game.valid_move(game.current_piece, -1, 0, 0):
                game.current_piece.x -= 1
        if 's' in keys:
            if game.valid_move(game.current_piece, 1, 0, 0):
                game.current_piece.x += 1
        if 'x' in keys:
            if game.valid_move(game.current_piece, 0, 1, 0):
                game.current_piece.y += 1
        if 'e' in keys:
            game.current_piece.rotate()

        fall_time += time.time()
        if fall_time >= fall_speed:
            game.update()
            fall_time = 0

        print(f"score: {game.score}")

        for i in range(game.height):
            for j in range(game.width):
                if game.grid[i][j] != 0:
                    print('#', end='')
                else:
                    print(' ', end='')
                print()


if __name__ == "__main__":
    main()
