import pygame
import random
import math
from enum import Enum

# Snake
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Snake:
    color = (0, 0, 255)

    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.respawn()

    def respawn(self):
        self.length = 3
        self.body = [(20, 20), (20, 40), (20, 60)]
        self.direction = Direction.DOWN

    def draw(self, game, window):
        for i, segment in enumerate(self.body):
            if i == len(self.body) - 1:
                # Draw the head image for the last segment
                head_image_rotated = pygame.transform.rotate(snake_head_image, self.calculate_rotation()+180)
                window.blit(head_image_rotated, (segment[0], segment[1]))
            else:
                # Draw the body image for the other segments
                body_image_rotated = pygame.transform.rotate(snake_body_image, self.calculate_rotation())
                window.blit(body_image_rotated, (segment[0], segment[1]))

    def calculate_rotation(self):
        angle = 0
        curr_head = self.body[-1]
        if len(self.body) > 1:
            prev_head = self.body[-2]
            dx = curr_head[0] - prev_head[0]
            dy = curr_head[1] - prev_head[1]
            angle = math.degrees(math.atan2(-dy, dx))  # Calculate the angle in degrees
        return angle  # Add this line to return the calculated angle

    def move(self):
        curr_head = self.body[-1]
        if self.direction == Direction.DOWN:
            next_head = (curr_head[0], curr_head[1] + self.block_size)
            self.body.append(next_head)
        elif self.direction == Direction.UP:
            next_head = (curr_head[0], curr_head[1] - self.block_size)
            self.body.append(next_head)
        elif self.direction == Direction.RIGHT:
            next_head = (curr_head[0] + self.block_size, curr_head[1])
            self.body.append(next_head)
        elif self.direction == Direction.LEFT:
            next_head = (curr_head[0] - self.block_size, curr_head[1])
            self.body.append(next_head)

        if self.length < len(self.body) - 1:
            self.body.pop(0)  # Remove the tail segment only if the snake didn't eat the food

    def steer(self, direction):
        if self.direction == Direction.DOWN and direction != Direction.UP:
            self.direction = direction
        elif self.direction == Direction.UP and direction != Direction.DOWN:
            self.direction = direction
        elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
            self.direction = direction
        elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
            self.direction = direction

    def eat(self):
        self.length += 1

    def check_for_food(self, food):
        head = self.body[-1]
        if head[0] == food.x and head[1] == food.y:
            self.eat()
            food.respawn()
            return True
        return False

    def check_tail_collision(self):
        head = self.body[-1]
        has_eaten_tail = False

        for i in range(len(self.body) - 1):
            segment = self.body[i]
            if head[0] == segment[0] and head[1] == segment[1]:
                has_eaten_tail = True

        return has_eaten_tail

    def check_bounds(self):
        head = self.body[-1]
        if head[0] >= self.bounds[0]:
            return True
        if head[1] >= self.bounds[1]:
            return True
        if head[0] < 0:
            return True
        if head[1] < 0:
            return True
        return False

# Food
class Food:
    color = (255, 0, 0)
    x = 100
    y = 100

    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds

    def draw(self, game, window):
        # Draw the apple image instead of a rectangle
        window.blit(apple_image, (self.x, self.y))

    def respawn(self):
        blocks_in_x = (self.bounds[0]) // self.block_size
        blocks_in_y = (self.bounds[1]) // self.block_size
        self.x = random.randint(0, blocks_in_x - 1) * self.block_size
        self.y = random.randint(0, blocks_in_y - 1) * self.block_size

# Clouds
class Cloud:
    color = (255, 255, 255)
    x = 0
    y = 0
    velocity = 1

    def __init__(self, size, bounds):
        self.size = size
        self.bounds = bounds
        self.spawn()

    def spawn(self):
        side = random.randint(1, 4)
        if side == 1:  # Left
            self.x = 0 - self.size
            self.y = random.randint(0, self.bounds[1] - self.size)
        elif side == 2:  # Right
            self.x = self.bounds[0]
            self.y = random.randint(0, self.bounds[1] - self.size)
        elif side == 3:  # Top
            self.x = random.randint(0, self.bounds[0] - self.size)
            self.y = 0 - self.size
        elif side == 4:  # Bottom
            self.x = random.randint(0, self.bounds[0] - self.size)
            self.y = self.bounds[1]

    def move(self):
        self.x += self.velocity
        self.y += self.velocity

        # Wrap around the playfield if the cloud moves beyond the boundaries
        if self.x > self.bounds[0]:
            self.x = 0 - self.size
        if self.y > self.bounds[1]:
            self.y = 0 - self.size

    def draw(self, game, window):
        game.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

def spawn_clouds(clouds, cloud_spawn_rate, cloud_size, bounds):
    while len(clouds) < cloud_spawn_rate:
        cloud = Cloud(cloud_size, bounds)  
        clouds.append(cloud)

# Main
pygame.init()
bounds = (800, 800)
window = pygame.display.set_mode(bounds)

pygame.display.set_caption("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")

# Load the images
apple_image = pygame.image.load("apple_image.jpg").convert()
snake_head_image = pygame.image.load("snake_head_image.jpg").convert()
snake_body_image = pygame.image.load("snake_body_image.jpg").convert()
background_image = pygame.image.load("snake_background.png").convert()

# Scale the images to fit the desired size
apple_image = pygame.transform.scale(apple_image, (20, 20)) 
snake_head_image = pygame.transform.scale(snake_head_image, (20, 20)) 
snake_body_image = pygame.transform.scale(snake_body_image, (20, 20)) 
background_image = pygame.transform.scale(background_image, bounds)

block_size = 20
snake = Snake(block_size, bounds)
food = Food(block_size, bounds)
font = pygame.font.SysFont('comicsans', 150, True)

# Score
score = 3
penis = score
font2 = pygame.font.SysFont('comicsans', 30, True)

def draw_score():
    score_text = font2.render("Score: " + str(len(snake.body) - 4), True, (255, 255, 255))
    window.blit(score_text, (bounds[0] - score_text.get_width() - 10, 10))

def draw_highscore():
    score_text = font2.render("Highscore: " + str(int(penis)-3), True, (255, 255, 255))
    window.blit(score_text, (bounds[0] - score_text.get_width() - 10, 40))

# Clouds
clouds = []
cloud_spawn_rate = 5  # Number of clouds to spawn initially
cloud_size = 50

for cloud in clouds:
            cloud.move()
            if cloud.x >= bounds[0] or cloud.y >= bounds[1]:
                cloud.spawn()

# Spawn initial clouds
for _ in range(5):
    cloud = Cloud(cloud_size, bounds)
    clouds.append(cloud)

delay = 120
timer = pygame.time.get_ticks()

#Main
run = True
game_over = False
while run:

    if pygame.time.get_ticks() - timer >= 15000:
        delay -= 5
        timer = pygame.time.get_ticks()

    pygame.time.delay(delay)


    # Keeps creating a random color
    colr = random.randint(0, 255)
    colg = random.randint(0, 255)
    colb = random.randint(0, 255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_ESCAPE:
                run = False
            else:
                game_over = False
                score = 0  
                snake.respawn()
                food.respawn()
                delay = 120
                
    if not game_over:
        # Steering
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            snake.steer(Direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            snake.steer(Direction.RIGHT)
        elif keys[pygame.K_UP]:
            snake.steer(Direction.UP)
        elif keys[pygame.K_DOWN]:
            snake.steer(Direction.DOWN)
        snake.move()

        # Move and spawn new clouds
        for cloud in clouds:
            cloud.move()
            if cloud.x >= bounds[0] or cloud.y >= bounds[1]:
                cloud.spawn()

        # Check if the snake hits the food
        if snake.check_for_food(food):
            score = len(snake.body)  # Set score = to snake length
            food.respawn()
            if score % 5 == 0:  # Increase cloud spawn rate every 5 points
                cloud_spawn_rate += 1


        # Check for bounds and tail
        if snake.check_bounds() or snake.check_tail_collision():
            game_over = True

        # Draw the background image
        window.blit(background_image, (0, 0))

        if score > penis:
            penis = score

        draw_score()
        draw_highscore()

        snake.draw(pygame, window)
        food.draw(pygame, window)

        # Draw clouds
        for cloud in clouds:
            cloud.draw(pygame, window)
        
        spawn_clouds(clouds, cloud_spawn_rate, cloud_size, bounds)

        pygame.display.update()

    else:
        end_text = font.render('Game Over', True, (colr, colg, colb))
        text_width, text_height = font.size('Game Over')
        window.blit(end_text, ((bounds[0] - text_width) // 2, (bounds[1] - text_height) // 2))
        pygame.display.update()

pygame.quit()
