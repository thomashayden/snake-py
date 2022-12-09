import random
import sys
import time

import pygame as pygame

def add_new_food(food, snake):
  while True:
    randx = int(random.random()*BOARD_WIDTH)
    randy = int(random.random()*BOARD_HEIGHT)
    if (randx, randy) not in food and (randx, randy) not in snake:
      food.append((randx, randy))
      return food

if __name__ == '__main__':
  pygame.init()

  WINDOW_WIDTH = 600
  WINDOW_HEIGHT = 600
  window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

  TIME_PER_TICK = 16.6666 # ms
  TICKS_PER_MOVE = 10
  last_update = time.time_ns()/1000000

  BOARD_WIDTH = 20
  BOARD_HEIGHT = 20

  snake_direction = (1, 0)
  snake = []
  snake.append((10,10))
  snake.append((9,10))

  food = []
  food.append((3,3))

  prevent_updates = False

  while True:
    # Update
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          if prevent_updates:
            snake_direction = (1, 0)
            snake = []
            snake.append((10, 10))
            snake.append((9, 10))

            food = []
            food = add_new_food(food, snake)
            prevent_updates = False
          else:
            pygame.quit()
            sys.exit()
        if event.key == pygame.K_w and snake_direction != (0,1):
          snake_direction = (0, -1)
        if event.key == pygame.K_d and snake_direction != (-1,0):
          snake_direction = (1, 0)
        if event.key == pygame.K_s and snake_direction != (0,-1):
          snake_direction = (0, 1)
        if event.key == pygame.K_a and snake_direction != (1,0):
          snake_direction = (-1, 0)

    if time.time_ns()/1000000 - last_update > TIME_PER_TICK * TICKS_PER_MOVE and not prevent_updates:
      # Good for another step
      new_head = tuple(map(lambda i, j: i + j, snake[0], snake_direction))
      reduce = True
      if new_head in snake:
        # Hit yourself
        print("You hit yourself :(")
        prevent_updates = True
      if new_head[0] < 0 or new_head[0] >= BOARD_WIDTH or new_head[1] < 0 or new_head[1] >= BOARD_HEIGHT:
        # Exited board
        print("You left the board :(")
        prevent_updates = True
      if new_head in food:
        # Ate food
        food.remove(new_head)
        food = add_new_food(food, snake)
        reduce = False
      new_snake = []
      new_snake.append(new_head)
      if reduce:
        new_snake.extend(snake[:-1])
      else:
        new_snake.extend(snake)
      snake = new_snake
      last_update = time.time_ns()/1000000
    # Render
    window.fill((255, 255, 255))
    cell_width = WINDOW_WIDTH/BOARD_WIDTH
    cell_height = WINDOW_HEIGHT/BOARD_HEIGHT

    for i in range(BOARD_WIDTH):
      for j in range(BOARD_HEIGHT):
        pygame.draw.rect(window, (0,0,0), [cell_width*i,cell_height*j, cell_width, cell_height], 1)
    pygame.draw.rect(window, (0,255,255), [cell_width*snake[0][0], cell_height*snake[0][1], cell_width, cell_height], 0)
    for snake_elem in snake[1:]:
      pygame.draw.rect(window, (0,0,255), [cell_width*snake_elem[0], cell_height*snake_elem[1], cell_width, cell_height], 0)
    for f in food:
      pygame.draw.rect(window, (128,128,0), [cell_width*f[0], cell_height*f[1], cell_width, cell_height], 0)
    pygame.display.update()