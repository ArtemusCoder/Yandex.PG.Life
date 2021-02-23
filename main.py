import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 30
        self.top = 30
        self.cell_size = 50

    def get_click(self, mouse_pos):
        self.get_cell(mouse_pos)

    def on_click(self, cell_x, cell_y):
        if self.board[cell_y][cell_x] == 0:
            self.board[cell_y][cell_x] = 1
            return True
        if self.board[cell_y][cell_x] == 1:
            self.board[cell_y][cell_x] = 0
            return True

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if (0 <= cell_x < self.width) and (0 <= cell_y < self.height):
            self.on_click(cell_x, cell_y)
        else:
            return None

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size,
                    self.cell_size), 2)
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 0:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        self.left + 2 + x * self.cell_size, self.top + y * self.cell_size + 2,
                        self.cell_size - 3,
                        self.cell_size - 3), 0)


class Live(Board):
    def __init__(self, width, height, left, top, cell_size):
        super().__init__(width, height)
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell_x, cell_y):
        super().on_click(cell_x, cell_y)
        print(self.count_neighborhood(cell_x, cell_y))

    def count_neighborhood(self, x, y):
        count = 0
        delta = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        for dx, dy in delta:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                if self.board[new_y][new_x] == 1:
                    count += 1
        return count

    def next_move(self):
        new_board = [[0] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0 and self.count_neighborhood(x, y) == 3:
                    new_board[y][x] = 1
                elif self.board[y][x] == 1 and 2 <= self.count_neighborhood(x, y) <= 3:
                    new_board[y][x] = 1
                else:
                    new_board[y][x] = 0
        self.board = new_board


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Реакция на события от мыши')
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('black'))
    running = True
    simulation = False
    fps = 60
    board = Live(40, 40, 10, 10, 17)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
                if event.button == 4:
                    if fps > 6:
                        fps -= 5
                if event.button == 5:
                    if fps < 80:
                        fps += 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation = False if simulation else True
        if simulation:
            board.next_move()
            clock.tick(fps)
        screen.fill(pygame.Color('black'))
        board.render()
        pygame.display.flip()
    pygame.quit()
