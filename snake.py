import pygame
import random
import glob

pygame.init()

# width and height of window
dis_width = 800
dis_height = 600

# colors used in the game
black = (0, 0, 0)
white = (255, 255, 255)
magenta = (255, 0, 255)
blue = (0, 0, 70)
green = (0, 255, 0)
yellow = (255, 255, 102)
orange = (255, 165, 0)
red = (255, 0, 0)

# adjust properties of the snake
snake_block = 30
snake_speed = 15
initial_snake_speed = snake_speed

# set up game display
display = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Worlds")

# clock used for events involving time
clock = pygame.time.Clock()

# different fonts used throughout the game
font_style = pygame.font.SysFont("bahnschrift", 30)
score_font = pygame.font.SysFont("couriernew", 35)
score_font.set_bold(True)


# generate a random background image for the game
def get_background():
    images = [img for img in
              glob.glob("./Backgrounds/*.jpg")
              + glob.glob("./Backgrounds/*.jpeg")
              + glob.glob("./Backgrounds/*.png")
              + glob.glob("./Backgrounds/*.gif")]

    if images:
        return random.choice(images)
    else:
        return ""


# display score to player
def player_score(score):
    value = score_font.render("Your score: " + str(score), True, white)
    value_outline = score_font.render("Your score: " + str(score), True, black)

    display.blit(value_outline, [3, 0])
    display.blit(value, [0, 0])


# add bits to snake from eating
def add_to_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(display, color, [
                         x[0], x[1], snake_block, snake_block])


# generate new random x position for food
def generate_food_x():
    return round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0


# generate new random y position for food
def generate_food_y():
    return round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0


# get a random rgb tuple
def get_random_rgb():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


# play sound when food is eaten
def play_food_sound():
    food_sound = pygame.mixer.Sound(
        "./Sound Effects/mixkit-video-game-retro-click-237.wav")
    pygame.mixer.Sound.play(food_sound)


# play power up sound after a certain amount of food is eaten
def play_power_up_sound():
    power_up_sound = pygame.mixer.Sound(
        "./Sound Effects/mixkit-extra-bonus-in-a-video-game-2045.wav")
    pygame.mixer.Sound.play(power_up_sound)


# play sound when player dies
def play_death_sound():
    death_sound = pygame.mixer.Sound(
        "./Sound Effects/mixkit-electronic-retro-block-hit-2185.wav")
    pygame.mixer.Sound.play(death_sound)


# display a message to the player
def message(msg, color):
    value = font_style.render(msg, True, color)
    temp_surface = pygame.Surface(value.get_size())
    temp_surface.fill(black)
    display.blit(temp_surface, [dis_width / 6.5, dis_height / 2.5])
    display.blit(value, [dis_width / 6.5, dis_height / 2.5])


# keep the game running unless properly ended
def game_loop():
    # keep track of when the game has and has not ended
    game_over = False
    game_close = False

    # where the snake currently is
    x1 = dis_width / 2
    y1 = dis_height / 2

    # the change in the snake's current position
    x1_change = 0
    y1_change = 0

    # used to keep track of snake parts and length
    snake_list = []
    snake_length = 1
    global snake_speed
    snake_speed = initial_snake_speed
    snake_color = get_random_rgb()
    snake_food_since_power_up = 0

    # where food randomly generates on screen
    food_x = generate_food_x()
    food_y = generate_food_y()

    # get random background image
    background_image = get_background()
    if background_image:
        background_image = pygame.image.load(background_image)

    # start background music
    pygame.mixer.init()
    pygame.mixer.music.load("./Music/comfy vibes.mp3")
    pygame.mixer.music.play(-1, 0)

    # keep the game running
    while not game_over and pygame.mixer.music.get_busy():
        # if the player lost, present them with options
        while game_close == True:
            # set game background image, otherwise color if error loading image
            if background_image:
                display.blit(background_image, (0, 0))
            else:
                display.fill(blue)

            message("You lost! Press Q to quit, or C to play again.", white)
            player_score(snake_length - 1)
            pygame.display.update()
            pygame.mixer.music.stop()
            if event.type == pygame.QUIT:
                game_over = True
                break

            # handle the options
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        # handle game exiting and moving the snake around the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -10
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = 10
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -10
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = 10
                    x1_change = 0

        # handle out of bounds
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            play_death_sound()
            game_close = True

        # change the snake's position
        x1 += x1_change
        y1 += y1_change

        # set game background image, otherwise color if error loading image
        if background_image:
            display.blit(background_image, (0, 0))
        else:
            display.fill(blue)

        # draw food on screen
        pygame.draw.rect(display, magenta, [
                         food_x, food_y, snake_block, snake_block])

        # add to snake body as food is eaten
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        # keep the list a proper size for the length
        if len(snake_list) > snake_length:
            del snake_list[0]

        # handle snake eating itself
        for x in snake_list[:-1]:
            if x == snake_head:
                play_death_sound()
                game_close = True

        # when food is eaten, add length to snake, and adjust score
        add_to_snake(snake_block, snake_list, snake_color)
        player_score(snake_length - 1)
        pygame.display.update()

        # generate new food in new random position once one is eaten
        if (x1 == food_x and y1 == food_y):
            # power up player if they have eaten 10 more food
            if snake_food_since_power_up == 9:
                snake_food_since_power_up = 0
                snake_speed += 1
                snake_color = get_random_rgb()
                play_power_up_sound()
            else:
                snake_food_since_power_up += 1
                play_food_sound()

            food_x = generate_food_x()
            food_y = generate_food_y()
            snake_length += 1

        # keep game running at specified snake speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()


# start the game
game_loop()
