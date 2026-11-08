"""Учебный проект-игра змейка."""
from random import choice, randint

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона — чёрный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self):
        """Инициализирует начальную позицию и цвет объекта."""
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.body_color = None

    def draw(self):
        """Отрисовывает игровой объект."""
        pass


class Apple(GameObject):
    """Класс яблока, которое появляется на игровом поле."""

    def __init__(self):
        """Инициализирует яблоко и задаёт его цвет."""
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions):
        """Случайным образом размещает яблоко вне змейки.

        Args:
            snake_positions: Список координат сегментов змейки.
        """
        while True:
            random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (random_x, random_y)

            if self.position not in snake_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(
            self.position, (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, отвечающий за её движение и отрисовку."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну ячейку игрового поля."""
        self.last = self.positions[-1]

        head_x = self.get_head_position()[0]
        head_y = self.get_head_position()[1]

        # Проверка выхода за границы:
        if head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE

        elif head_x >= SCREEN_WIDTH:
            head_x = 0

        if head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE

        elif head_y >= SCREEN_HEIGHT:
            head_y = 0

        if self.direction == RIGHT:
            self.positions.insert(
                0, (head_x + RIGHT[0] * GRID_SIZE, head_y)
            )

        elif self.direction == LEFT:
            self.positions.insert(
                0, (head_x + LEFT[0] * GRID_SIZE, head_y)
            )

        elif self.direction == UP:
            self.positions.insert(
                0, (head_x, head_y + UP[1] * GRID_SIZE)
            )

        elif self.direction == DOWN:
            self.positions.insert(
                0, (head_x, head_y + DOWN[1] * GRID_SIZE)
            )

    def draw(self):
        """Отрисовывает змейку и удаляет предыдущий хвост."""
        if self.last:
            last_rect = pygame.Rect(
                self.last, (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen, BOARD_BACKGROUND_COLOR, last_rect
            )

        for position in self.positions:
            rect = pygame.Rect(
                position, (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает координаты головы змейки.

        Returns:
            Кортеж с координатами головы.
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки после столкновения."""
        self.length = 1
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.positions = [self.position]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш управления змейкой.

    Args:
        game_object: Игровой объект, направление которого меняется.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                and game_object.direction != DOWN
            ):
                game_object.next_direction = UP

            elif (
                event.key == pygame.K_DOWN
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN

            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT

            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def load_record():
    """Загружает рекорд из файла record.txt.

    Returns:
        Сохранённый рекорд или 1, если файл отсутствует
        или содержит некорректное значение.
    """
    try:
        with open('record.txt', 'r') as file:
            return int(file.read())

    except (FileNotFoundError, ValueError):
        return 1


def save_record(record):
    """Сохраняет новый рекорд в файл record.txt.

    Args:
        record: Значение рекорда для сохранения.
    """
    with open('record.txt', 'w') as file:
        file.write(str(record))


def main():
    """Запускает игру и управляет основным игровым циклом."""
    # Инициализация PyGame:
    pygame.init()

    record = load_record()

    # Создание экземпляров классов:
    apple = Apple()
    snake = Snake()

    apple.randomize_position(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()

        clock.tick(SPEED)

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

            if snake.length > record:
                record = snake.length
                save_record(record)

        else:
            snake.positions.pop()

        apple.draw()
        snake.draw()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
