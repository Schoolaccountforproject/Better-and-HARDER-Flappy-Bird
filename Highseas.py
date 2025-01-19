import pygame
import sys
import random

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Birds But Harder and Better")

# Load images
plane = pygame.image.load("//Users//guojili//PycharmProjects//HighSeas//purepng.com-blue-planeplaneairplaneaeroplanefixed-wing-aircraftaircraftjet-enginepropeller-1701528465657np2uo.png").convert_alpha()
fighter = pygame.image.load("//Users//guojili//PycharmProjects//HighSeas//jet.png").convert_alpha()
bird = pygame.image.load("//Users//guojili//PycharmProjects//HighSeas//png-image-bird-28.png").convert_alpha()
building = pygame.image.load("//Users//guojili//PycharmProjects//HighSeas//purepng.com-big-buildingbuildinghousefactoryresidencedwelling-houseconstructionarcitecture-17015284823564yegk.png").convert_alpha()
target = pygame.image.load("//Users//guojili//PycharmProjects//pythonProject1//Screenshot 2024-12-03 at 8.44.39 AM.png").convert_alpha()
explosion = pygame.image.load("//Users//guojili//PycharmProjects//HighSeas//Explosion-153710_icon.svg.png").convert_alpha()
score_multiplier_img = pygame.image.load("//Users//guojili//PycharmProjects//pythonProject1//2x.png").convert_alpha()
invincibility_img = pygame.image.load("//Users//guojili//PycharmProjects//pythonProject1//download.png").convert_alpha()

# Transform images
plane = pygame.transform.scale(plane, (145, 67))
target = pygame.transform.scale(target, (282, 257))
explosion = pygame.transform.scale(explosion, (56, 51))
score_multiplier_img = pygame.transform.scale(score_multiplier_img, (40, 40))
invincibility_img = pygame.transform.scale(invincibility_img, (40, 40))

# Plane variables
planex, planey = 650, 300
targetx, targety = -281.75, 54

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font("//Users//guojili//PycharmProjects//pythonProject1//Smack Laideth Down 2024.otf", 40)
menu_font = pygame.font.Font(None, 50)
words_font = pygame.font.Font("//Users//guojili//PycharmProjects//pythonProject1//HARRYP__.TTF", 60)
cute_font = pygame.font.Font("//Users//guojili//PycharmProjects//pythonProject1//Cute_Font.ttf", 24)

# Misc
current_option = 0

# Menu backgrounds
menu_background = pygame.image.load("//Users//guojili//PycharmProjects//pythonProject1//newnycguidemain.jpeg").convert()
menu_background = pygame.transform.scale(menu_background, (800, 600))
game_background = pygame.image.load("//Users//guojili//PycharmProjects//pythonProject1//737474.png").convert()
game_background = pygame.transform.scale(game_background, (800, 600))
sakura = pygame.image.load("//Users//guojili//PycharmProjects//pythonProject1//sakura.png").convert()
sakura = pygame.transform.scale(sakura, (800, 600))


# Classes
class Fighter:
    def __init__(self, y):
        self.x = -67.5
        self.y = y
        self.object = pygame.transform.scale(fighter, (67.5, 45))
        self.rect = window.blit(self.object, (self.x, self.y))

    def tick(self):
        self.rect = window.blit(self.object, (self.x, self.y))
        self.x += 2


class Bird:
    def __init__(self, y):
        self.x = -40
        self.y = y
        self.object = pygame.transform.scale(bird, (40, 40))
        self.rect = window.blit(self.object, (self.x, self.y))

    def tick(self):
        self.rect = window.blit(self.object, (self.x, self.y))
        self.x += 1
        self.y += random.choice([-1, 1])


class Building:
    def __init__(self):
        self.x = -140
        self.y = 143
        self.object = pygame.transform.scale(building, (140, 457))
        self.rect = window.blit(self.object, (self.x, self.y))

    def tick(self):
        self.rect = window.blit(self.object, (self.x, self.y))
        self.x += 0.5


# Draw pause menu
def draw_pause_menu(selected_option):
    window.fill((0, 0, 0))  # Fill screen with black
    title = font.render("Paused", True, WHITE)
    window.blit(title, (400 - title.get_width() // 2, 100))

    options = ["Resume", "Restart", "Back to Title"]
    for i, option in enumerate(options):
        color = BLUE if i == selected_option else WHITE
        text = font.render(option, True, color)
        window.blit(text, (400 - text.get_width() // 2, 250 + i * 60))

    pygame.display.flip()

# Pause menu logic
def pause_menu():
    selected_option = 0
    while True:
        draw_pause_menu(selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                elif event.key == pygame.K_SPACE:
                    if selected_option == 0:  # Resume
                        return "resume"
                    elif selected_option == 1:  # Restart
                        return "restart"
                    elif selected_option == 2:  # Back to Title
                        return "title"

# Draw death menu
def draw_death_menu(elapsed_time, selected_option, message=""):
    window.fill((0, 0, 0))  # Fill screen with black
    title = font.render("You Died!", True, WHITE)
    score_text = font.render(f"Score: {elapsed_time}", True, WHITE)
    window.blit(title, (400 - title.get_width() // 2, 100))
    window.blit(score_text, (400 - score_text.get_width() // 2, 200))

    if message:
        message_text = font.render(message, True, WHITE)
        window.blit(message_text, (400 - message_text.get_width() // 2, 260))

    options = ["Restart", "Return to Title"]
    for i, option in enumerate(options):
        color = BLUE if i == selected_option else WHITE
        text = font.render(option, True, color)
        window.blit(text, (400 - text.get_width() // 2, 300 + i * 60))

    pygame.display.flip()

# Death menu logic
def death_menu(elapsed_time):
    selected_option = 0
    while True:
        draw_death_menu(elapsed_time, selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_SPACE:
                    if selected_option == 0:  # Restart
                        return "restart"
                    elif selected_option == 1:  # Back to Title
                        return "title"

# Modified game loop
def game_loop():
    global planex, planey, targetx, targety
    planex, planey = 650, 300  # Reset plane position
    targetx, targety = -281.75, 54  # Reset target position
    obj_list = []
    is_paused = False
    start_time = pygame.time.get_ticks()
    target_active = False  # To track if the target is active
    last_target_time = start_time

    next_phase_time = pygame.time.get_ticks() + random.randint(20000, 30000)  # Random phase start (20-30 seconds)
    dark_night_active = False
    dark_night_start_time = 0

    while True:
        if is_paused:
            action = pause_menu()
            if action == "resume":
                is_paused = False
            elif action == "restart":
                return "restart"  # Signal to restart the game
            elif action == "title":
                return "title"  # Go back to the title page

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_paused = True

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        if not dark_night_active and pygame.time.get_ticks() >= next_phase_time:
            dark_night_active = True
            dark_night_start_time = pygame.time.get_ticks()
            next_phase_time = pygame.time.get_ticks() + random.randint(20000, 30000)  # Set next phase start time

        # End Dark Night Phase after 5 seconds
        if dark_night_active and (pygame.time.get_ticks() - dark_night_start_time) > 5000:
            dark_night_active = False

        timer_text = font.render(f"Score: {elapsed_time}", True, WHITE)

        # Game rendering and logic
        window.fill((135, 206, 235))
        window.blit(game_background, (0, 0))
        plane_rect = window.blit(plane, (planex, planey))
        window.blit(timer_text, (10, 10))

        # Plane movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and planey > 0:
            planey -= 1
        if keys[pygame.K_DOWN] and planey < 530:
            planey += 1
        if keys[pygame.K_LEFT] and planex > 0:
            planex -= 1
        if keys[pygame.K_RIGHT] and planex < 660:
            planex += 1

        # Spawn objects randomly
        chance = random.randint(0, 2000)
        if chance == 1000:
            obj_list.append(Fighter(random.randint(45, 555)))
        chance = random.randint(0, 1500)
        if chance == 750:
            obj_list.append(Bird(random.randint(40, 540)))
        chance = random.randint(0, 5000)
        if chance == 2500:
            obj_list.append(Building())

        # Move objects and check for collisions
        for obj in obj_list:
            obj.tick()
            if obj.x > 1000:
                obj_list.remove(obj)

        for obj in obj_list:
            if plane_rect.colliderect(obj.rect):
                window.blit(game_background, (0, 0))
                window.blit(explosion, (planex, planey))
                pygame.display.flip()
                pygame.time.delay(1000)

                # Show death menu and handle response
                action = death_menu(elapsed_time)
                if action == "restart":
                    return "restart"  # Signal to restart the game
                elif action == "title":
                    return "title"  # Go back to the title page

        if dark_night_active:
            # Overlay a semi-transparent black surface
            dark_overlay = pygame.Surface((800, 600))
            dark_overlay.set_alpha(200)  # Set transparency level (0-255)
            dark_overlay.fill((0, 0, 0))  # Black color
            window.blit(dark_overlay, (0, 0))

        # Target logic: Activate after 40 seconds
        if elapsed_time > 40 and not target_active and (pygame.time.get_ticks() - last_target_time) >= 40000:
            target_active = True
            targetx = -281.75  # Reset target position
            last_target_time = pygame.time.get_ticks()  # Update the last spawn time

        if target_active:
            target_rect = window.blit(target, (targetx, targety))
            targetx += 0.5  # Move the target across the screen

            if plane_rect.colliderect(target_rect):  # Check for collision with the plane
                window.blit(game_background, (0, 0))
                window.blit(explosion, (planex, planey))
                for obj in obj_list:
                    window.blit(obj.object, (obj.x, obj.y))
                pygame.display.flip()
                pygame.time.delay(1000)

                # Show death menu and handle response
                action = death_menu(elapsed_time)
                if action == "restart":
                    return "restart"  # Signal to restart the game
                elif action == "title":
                    return "title"  # Go back to the title page

            if targetx > window.get_width():  # Reset target if it moves off-screen
                target_active = False  # Set target_active to False when target goes off-screen

        pygame.display.flip()

#Game info page
def game_info_menu():
    running = True

    info_lines = [
        "Welcome to My first Game (technically)!",
        "",
        "HOW TO PLAY:",
        "- Use arrow keys to move the plane.",
        "- Avoid obstacles such as the fighter jets and buildings.",
        "",
        "WHAT'S INCLUDED:",
        "- Basically there's a dark phase that randomly spawns in, make sure you get ready!",
        "- This game is pretty hard as spawns are random so let's just say sometimes you run",
        "into dead ends hehe. It's done on purpose so it's more like a luck game for high scores. ",
        "",
        "Something extra:",
        "- I've included a friend of ours in this game! Survive for a certain amount of time to",
        "meet him.",
        "- There's a one out of a thousand chance that in each individual match, you will",
        "encounter the deep hidden secret. Pray for it.",
        "Guys this is my first game, not looking for much but wish you all are having fun (or",
        "being tortured by the dead end combo of jets/birds and the buildings) lol!"
    ]

    while running:
        window.blit(sakura, (0, 0))
        for i, line in enumerate(info_lines):
            rendered_line = cute_font.render(line, True, BLACK)  # White text
            window.blit(rendered_line, (50, 50 + i * 30))  # Space lines vertically

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Press ESC to go back
                running = False  # Exit info menu

        pygame.display.flip()

# Main menu
def main_menu():
    selected_option = 0
    while True:
        draw_menu(selected_option)  # Ensure draw_menu() is updated to include the new option
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3  # Update to handle 3 options (0, 1, 2)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                elif event.key == pygame.K_SPACE:
                    if selected_option == 0:  # Start Game
                        while True:
                            action = game_loop()
                            if action == "restart":
                                continue  # Restart the game
                            elif action == "title":
                                break  # Go back to the title menu
                    elif selected_option == 1:  # Game Info
                        game_info_menu()  # Open the "Game Info" menu
                    elif selected_option == 2:  # Exit
                        pygame.quit()
                        sys.exit()

# Draw main menu
def draw_menu(selected_option):
    window.blit(menu_background, (0, 0))
    title = font.render("Flappy Birds But Harder and Better", True, BLACK)
    window.blit(title, (400 - title.get_width() // 2, 100))

    options = ["Start Game", "Info you need to see", "Exit"]
    for i, option in enumerate(options):
        if i == selected_option:  # Highlight the selected option
            text = font.render(f"> {option} <", True, BLACK)
        else:
            text = font.render(option, True, (255, 255, 255))  # White text
        window.blit(text, (300, 200 + i * 50))  # Render text with spacing

    pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main_menu()







