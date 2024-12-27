import pyxel

class SnakeGame:
    def __init__(self):
        pyxel.init(240, 180, fps=35)  # Reduced screen size and slightly increased FPS for faster gameplay
        pyxel.title = "Snake Game"
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.snake = [(120, 88)]  # Adjusted initial position to align with the grid
        self.food = self.generate_food()  # Generate initial food position
        self.direction = (1, 0)  # Moving right
        self.next_direction = self.direction
        self.game_over = False
        self.speed_counter = 0  # Used to control snake movement speed

    def generate_food(self):
        while True:
            food_x = pyxel.rndi(0, (pyxel.width // 8) - 1) * 8
            food_y = pyxel.rndi(0, (pyxel.height // 8) - 1) * 8
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # Direction control (WASD and Arrow Keys)
        if (pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP)) and self.direction != (0, 1):
            self.next_direction = (0, -1)
        elif (pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN)) and self.direction != (0, -1):
            self.next_direction = (0, 1)
        elif (pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_LEFT)) and self.direction != (1, 0):
            self.next_direction = (-1, 0)
        elif (pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.KEY_RIGHT)) and self.direction != (-1, 0):
            self.next_direction = (1, 0)

        # Slow down the snake movement
        self.speed_counter += 1
        if self.speed_counter % 5 != 0:  # Adjusted for faster gameplay
            return

        # Move the snake
        self.direction = self.next_direction
        head = self.snake[-1]
        new_head = (head[0] + self.direction[0] * 8, head[1] + self.direction[1] * 8)

        # Check for collisions
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= pyxel.width or new_head[1] >= pyxel.height):
            self.game_over = True
            return

        self.snake.append(new_head)

        # Check for food collision
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop(0)

    def draw(self):
        pyxel.cls(0)

        if self.game_over:
            pyxel.text(pyxel.width // 2 - 35, pyxel.height // 2 - 10, "GAME OVER!", 7)
            pyxel.text(pyxel.width // 2 - 45, pyxel.height // 2, "Press R to restart", 7)
            pyxel.text(pyxel.width // 2 - 30, pyxel.height // 2 + 10, f"Score: {len(self.snake)}", 8)
            return

        # Draw the snake
        for segment in self.snake:
            pyxel.rect(segment[0], segment[1], 8, 8, 11)

        # Draw the food
        pyxel.rect(self.food[0], self.food[1], 8, 8, 8)

        # Display score
        pyxel.text(10, 10, f"Score: {len(self.snake)}", 7)

SnakeGame()
