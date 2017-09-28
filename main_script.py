import pygame

import random

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake')

icon = pygame.image.load('snake.ico')
pygame.display.set_icon(icon)

pygame.display.update()

block_size = 20

clock = pygame.time.Clock()

small_font = pygame.font.Font(None, 25)
med_font = pygame.font.Font(None, 50)
large_font = pygame.font.Font(None, 80)


def game_intro():
    intro = True
    while intro:
        game_display.fill(white)
        message_to_screen('Welcome to Snake',
                          green,
                          -100,
                          'large')

        message_to_screen('You should eat red boxes',
                          black,
                          -30)
        message_to_screen('Press S to start game or Q to quite',
                          black,
                          30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    intro = False
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_s:
                    intro = False
                    game_loop()


def text_objects(text, color, size):
    if size == 'small':
        text_surface = small_font.render(text, True, color)
    elif size == 'medium':
        text_surface = med_font.render(text, True, color)
    elif size == 'large':
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0, size='small'):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2), (display_height / 2) + y_displace
    game_display.blit(text_surf, text_rect)


def snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(game_display, black, [block[0], block[1], block_size, block_size])


def game_loop():
    fps = 10
    count_apple = 0

    level = 1
    next_level = 2
    level_for_pill = 3

    apple_before = 0
    game_exit = False
    game_over = False

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 0
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    rand_apple_x = round(random.randrange(0, display_width - block_size))  # / 10.0) * 10.0
    rand_apple_y = round(random.randrange(0, display_height - block_size))  # / 10.0) * 10.0

    rand_pill_x = round(random.randrange(0, display_width - block_size))  # / 10.0) * 10.0
    rand_pill_y = round(random.randrange(0, display_height - block_size))  # / 10.0) * 10.0



    while not game_exit:
        pygame.display.set_caption('Snake. Count: %s. Level: %s' % (count_apple, level))
        while game_over:
            message_to_screen('Game over',
                              red,
                              - 50,
                              size='large')

            message_to_screen('Press A to play again or Q to quite',
                              black,
                              50,
                              size='medium')
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    elif event.key == pygame.K_a:
                        game_loop()

        if not (0 < lead_x < display_width and 0 < lead_y < display_height):
            game_over = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        lead_x_change = -block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        lead_x_change = block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_UP:
                        lead_y_change = - block_size
                        lead_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        lead_y_change = block_size
                        lead_x_change = 0

        lead_x += lead_x_change
        lead_y += lead_y_change

        game_display.fill(white)

        apple_thickness = 30
        pygame.draw.rect(game_display, red, [rand_apple_x, rand_apple_y, apple_thickness, apple_thickness])

        snake_head = [lead_x, lead_y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for snake_element in snake_list[:-1]:
            if snake_element == snake_head:
                game_over = True

        if level_for_pill < level:
            level_for_pill += level_for_pill
            pygame.draw.rect(game_display, green, [rand_pill_x, rand_pill_y, apple_thickness, apple_thickness])


        snake(block_size, snake_list)
        pygame.display.update()

        if rand_apple_x < lead_x < rand_apple_x + apple_thickness or rand_apple_x < lead_x + block_size < rand_apple_x + apple_thickness:
            if rand_apple_y < lead_y < rand_apple_y + apple_thickness or rand_apple_y < lead_y + block_size < rand_apple_y + apple_thickness:
                rand_apple_x = round(random.randrange(0, display_width - block_size))  # / 10.0) * 10.0
                rand_apple_y = round(random.randrange(0, display_height - block_size))  # / 10.0) * 10.0
                count_apple += 1
                snake_length += 1

        if apple_before + 5 < count_apple:
            fps += 3
            level += 1
            apple_before = count_apple
        clock.tick(fps)

        if next_level < level:
            next_level += 1

        if rand_pill_x < lead_x < rand_pill_x + apple_thickness or rand_pill_x < lead_x + block_size < rand_pill_x + apple_thickness:
            if rand_pill_y < lead_y < rand_pill_y + apple_thickness or rand_pill_y < lead_y + block_size < rand_pill_y + apple_thickness:
                rand_pill_x = round(random.randrange(0, display_width - block_size))  # / 10.0) * 10.0
                rand_pill_y = round(random.randrange(0, display_height - block_size))  # / 10.0) * 10.0
                snake_length -= 3
                fps -= 2


    pygame.quit()

    quit()


game_intro()
