import cv2
import pygame
import random
import time
from tkinter import messagebox

# Construct the GUI game
pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w - 10, infoObject.current_h - 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create the window
pygame.display.set_caption("Sea Clean")  # the game title
BG = pygame.transform.scale(pygame.image.load("images/Sea.png"), (WIDTH, HEIGHT))
TRASH = [
    "images/can.png",
    "images/Banana.png",
    "images/Bottle.png",
    "images/Paper.png",
    "images/Bamba.png"
]
RULES = [
    "images/Gameplay_explaining.png",
    "images/Glass introduction.png",
    "images/Paper introduction.png",
    "images/Plastic introduction.png"
]
RULES_HEBREW = [
    "images/Gameplay_explaining_hebrew.png",
    "images/Glass introduction_hebrew.png",
    "images/Paper introduction_hebrew.png",
    "images/Plastic introduction_hebrew.png"
]
TRASHOBJ, TURTLEOBJ = [], []
# Set a variable to store the current movable image object
moving_obj = None
FPS = 60
FONT = pygame.font.SysFont("open sans", 111, True, True)
gui_font = pygame.font.Font(None, 30)
hebrew = False
# variables for tracking the number of objects on the WIN
lvl = 1
trash_spawn = 15
trash_iterator = 5
locations = []
correct_sfx = pygame.mixer.Sound('sound/correct-6033.mp3')
correct_sfx.set_volume(0.1)

def play_music():
    pygame.mixer.music.load('sound/scott-buckley-jul.mp3')

    # Set preferred volume
    pygame.mixer.music.set_volume(0.5)

    # Play the music
    pygame.mixer.music.play(-1)  


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"images/exp{i}.png") for i in range(1, 6)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        self.explosion_start_time = time.time()
        self.explosion_speed = 4

    def update(self):
        self.counter += 1

        if self.is_finished():
            lose_window()
            self.kill()

        if self.index < len(self.images) - 1 and self.counter >= self.explosion_speed:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index == len(self.images) - 1 and self.counter >= self.explosion_speed:
            self.kill()

    def is_finished(self):
        return self.index == len(self.images) - 1 and self.counter >= self.explosion_speed


class Button:
    def __init__(self, text, width, height, pos, elevation, gui_font=gui_font, font_size=None):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        if font_size is not None:
            gui_font = pygame.font.SysFont('open sans', font_size, True, True)

        # Define the top rectangle for the button
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#0F52BA'

        # Define the bottom rectangle for the button (used for elevation effect)
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#002366'

        # Render the text on the button
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # Update positions based on elevation
        self.update_positions()

        # Draw the button on the screen
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def update_positions(self):
        # Update positions of elements based on elevation
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

    def check_click(self):
        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#FA8072'
            if pygame.mouse.get_pressed()[0]:
                # Button pressed
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                # Mouse released
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    return False
        else:
            # Mouse not over the button
            self.dynamic_elevation = self.elevation
            self.top_color = '#0F52BA'
        return True


class TrashObj:
    def __init__(self, img_path):
        # Take image as input
        self.img = pygame.image.load(img_path)
        self.vel = 100
        # Draw rectangle around the image
        self.rect = self.img.get_rect()
        self.rect.center = (
            random.randint(self.vel, WIDTH - self.vel),
            random.randint(self.vel, HEIGHT - self.vel),
        )
        self.img_path = img_path
        # Border size
        self.border_size = 3

        # Create a new surface with the new dimensions
        self.bordered_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        # Update the bordered surface with the initial image
        self.update_bordered_surface()

    def update_bordered_surface(self):
        self.bordered_surface.fill((0, 0, 0, 0))  # Clear the surface
        t_mask = pygame.mask.from_surface(self.img)

        # Blit the character image onto the bordered surface at the calculated position
        image_position = (self.border_size, self.border_size)  # Offset by the border size
        self.bordered_surface.blit(self.img, image_position)

        # Draw the outline onto the bordered surface
        t_outline = t_mask.outline()
        adjusted_outline = [(p[0] + self.border_size, p[1] + self.border_size) for p in t_outline]
        pygame.draw.polygon(self.bordered_surface, (255, 255, 255), adjusted_outline, width=self.border_size)

    def get_path(self):
        return self.img_path


def check_and_append(x, y, vel):
    while (x, y) in locations or (x, y) in [loc for loc in locations if isinstance(loc, tuple)]:
        x = random.randint(vel, WIDTH - vel)
        y = random.randint(vel, HEIGHT - vel)
    locations.append((x, y))
    return (x, y)


class TurtleObj:
    def __init__(self, img_path):
        # Take image as input
        self.img_path = img_path
        self.i = 0
        self.images = [pygame.image.load(path) for path in self.img_path]
        self.img = self.images[self.i]
        self.vel = 100 
        self.speed = 1
        self.direction = 1
        self.rect = self.img.get_rect()
        x = random.randint(self.vel, WIDTH - self.vel)
        y = random.randint(self.vel, HEIGHT - self.vel)
        self.rect.center = check_and_append(x, y, self.vel)

        # Border size
        self.border_size = 1

        # Create a new surface with the new dimensions
        self.bordered_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Update the bordered surface with the initial image
        self.update_bordered_surface()

    def update_bordered_surface(self):
        self.bordered_surface.fill((0, 0, 0, 0))  # Clear the surface
        t_mask = pygame.mask.from_surface(self.img)

        # Blit the character image onto the bordered surface at the calculated position
        self.bordered_surface.blit(self.img, (self.border_size, self.border_size))

        # Draw the outline onto the bordered surface
        t_outline = t_mask.outline()
        pygame.draw.polygon(self.bordered_surface, (255, 255, 255), t_outline, width=self.border_size)

    def rotate(self):
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.rotate(self.images[i], 180)
        self.img = self.images[self.i]
        self.update_bordered_surface()

    def move(self):
        self.rect.move_ip(self.speed * self.direction, 0)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
            self.rotate()

    def update_img(self):
        self.i = (self.i + 1) % len(self.images)
        self.img = self.images[self.i]
        self.update_bordered_surface()


class SeaMine(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, mine_image_path):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(mine_image_path)
        self.vel = 120
        self.rect = self.image.get_rect()

        # Determine the initial side of appearance (0: top, 1: right, 2: bottom, 3: left)
        self.side = random.choice([0, 1, 2, 3])
        self.x_speed = 2
        self.y_speed = 2
        self.explosion = None

        if self.side == 0:  # Top
            self.rect.centerx = random.randint(self.vel, screen_width - self.vel)
            self.rect.bottom = 0
        elif self.side == 1:  # Right
            self.rect.right = screen_width
            self.rect.centery = random.randint(self.vel, screen_height - self.vel)
        elif self.side == 2:  # Bottom
            self.rect.centerx = random.randint(self.vel, screen_width - self.vel)
            self.rect.top = screen_height
        elif self.side == 3:  # Left
            self.rect.left = 0
            self.rect.centery = random.randint(self.vel, screen_height - self.vel)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Handle bouncing off the sides of the screen
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.y_speed *= -1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.x_speed *= -1

    def collide(self, player_rect, explosion_group):
        if self.rect.colliderect(player_rect):
            self.explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(self.explosion)
            self.kill()


def draw_t(turtle_obj):
    WIN.blit(turtle_obj.bordered_surface, turtle_obj.rect)

def lose_window():
    cap = cv2.VideoCapture('vids/game over.mov')  # שם של קובץ

    while cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.flip(frame, 0)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            WIN.blit(frame, (WIDTH / 2 - frame.get_width() / 2, HEIGHT / 2 - frame.get_height() / 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check for the quit event
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    return  # Exit the function and close the window
        else:
            break
        time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()

    ans = messagebox.askquestion("You lost...", "Wanna try again?")
    if ans == "yes":
        TRASHOBJ.clear()
        start_time = time.time() + 100
        spawn_time = start_time
        main()
        # code to return to the program
    else:
        pygame.quit()
        # code to quit the program

def winning_window():
    cap = cv2.VideoCapture('vids/win.mov')  # שם של קובץ

    while cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.flip(frame, 0)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            WIN.blit(frame, (WIDTH / 2 - frame.get_width() / 2, HEIGHT / 2 - frame.get_height() / 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check for the quit event
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    return  # Exit the function and close the window
        else:
            break
        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()

def opening():
    cap = cv2.VideoCapture('vids/SEE CLEAN (3).mp4')  # שם של קובץ
    while cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.flip(frame, 0)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            WIN.blit(frame, (WIDTH / 2 - frame.get_width() / 2, HEIGHT / 2 - frame.get_height() / 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check for the quit event
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    return  # Exit the function and close the window
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def backstory_introduction():
    # DR_voice = pygame.mixer.Sound('sound/Introduction.mp3') #TODO: Rerecord the sound
    # DR_voice.set_volume(0.8)

    if hebrew:
            cap = cv2.VideoCapture('vids/Backstory_hebrew.mp4')
    else:
        cap = cv2.VideoCapture('vids/Backstory.mp4')
    
    skip_btn = Button('Skip', 135, 35, (WIDTH - 200, HEIGHT - 50), 5)
        
    run = cap.isOpened()
    while run:
        WIN.fill((0, 0, 0))

        # DR_voice.play()
        ret, frame = cap.read()

        frame = cv2.flip(frame, 0)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            WIN.blit(frame, (WIDTH / 2 - frame.get_width() / 2, HEIGHT / 2 - frame.get_height() / 2))
            skip_btn.draw(WIN)
            run = skip_btn.check_click()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check for the quit event
                    cap.release()
                    cv2.destroyAllWindows()
                    # DR_voice.stop()
                    pygame.quit()
                    return  # Exit the function and close the window
        else:
            break

    # DR_voice.stop()
    cap.release()
    cv2.destroyAllWindows()


def welcome_window():
    global hebrew

    startmenu = pygame.image.load('images/start (2).png').convert_alpha()
    startmenu = pygame.transform.scale(startmenu, (WIDTH, HEIGHT))


    start_btn = Button('START', 270 ,70, (WIDTH / 2 - 135, HEIGHT / 2 + HEIGHT / 3), 10, FONT)
    quit_btn = Button('QUIT', 270, 70, (WIDTH / 2 - 135, HEIGHT / 2), 10, FONT)
    language_btn = Button('Language', 270, 70, (WIDTH / 2 - 135, HEIGHT / 8), 10, FONT, 77)

    run = True
    while run:
        startmenu.set_alpha(255)
        pygame.time.delay(10)
        WIN.blit(startmenu, (0, 0))
        # draw button
        start_btn.draw(WIN)
        quit_btn.draw(WIN)
        language_btn.draw(WIN)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if start_btn.check_click() == False:
            run = False
        elif quit_btn.check_click() == False:
            pygame.quit()
        elif language_btn.check_click() == False:
            msg = messagebox.askquestion("Language", "Would you like to change your language?\nתרצה לשנות את שפת המשחק לעברית?")
            if msg == "yes":
                hebrew = True
    # start the main game
    backstory_introduction()

def draw_garbage(img):
    return TrashObj(img)

def draw_turtle(img):
    return TurtleObj(img)

def draw(elapsed_time):
    # Draw the trash images, and update the WIN
    for img_obj in TRASHOBJ:
        WIN.blit(img_obj.bordered_surface, img_obj.rect)
    time_text = FONT.render(f"Time: {round(100 - elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

def draw_rules():
    if hebrew:
        img = pygame.transform.scale(pygame.image.load(RULES_HEBREW[lvl-1]), (WIDTH, HEIGHT))
    else:
        img = pygame.transform.scale(pygame.image.load(RULES[lvl-1]), (WIDTH, HEIGHT))
    continue_btn = Button('Continue', 135, 35, (WIDTH - 200, HEIGHT - 50), 5)
    run = True
    while run:
        for event in pygame.event.get():  # a loop that runs through all the events on pygame
            # Close if the user quits the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        WIN.blit(img, (0, 0))
        continue_btn.draw(WIN)
        run = continue_btn.check_click()
        pygame.display.update()  # Update the GUI pygame

def check_collision(moving_obj):
    global TRASHOBJ
    # Check if any trash object has collided with the turtle
    for trash_obj in TRASHOBJ:
        if metal_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/can.png" and trash_obj == moving_obj:
            TRASHOBJ.remove(trash_obj)
            correct_sfx.play()
        elif organic_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Banana.png" and trash_obj == moving_obj:
            TRASHOBJ.remove(trash_obj)
            correct_sfx.play()
        elif glass_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Bottle.png" and trash_obj == moving_obj:
            TRASHOBJ.remove(trash_obj)
            correct_sfx.play()
        elif paper_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Paper.png" and trash_obj == moving_obj:
            TRASHOBJ.remove(trash_obj)
            correct_sfx.play()
        elif plastic_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Bamba.png" and trash_obj == moving_obj:
            TRASHOBJ.remove(trash_obj)
            correct_sfx.play()

metal_t = draw_turtle(['images/GrayT.png', 'images/MetalTM.png'])
organic_t = draw_turtle(['images/BrownT.png', 'images/OrganicTM.png'])
glass_t = draw_turtle(['images/PurpleT.png', 'images/GlassTM.png'])
paper_t = draw_turtle(['images/BlueT.png', 'images/PaperTM.png'])
plastic_t = draw_turtle(['images/YellowT.png', 'images/PlasticTM.png'])
TURTLEOBJ = [metal_t, organic_t, glass_t, paper_t, plastic_t]

def main():
    global moving_obj, lvl, trash_iterator, trash_spawn

    for i in range(trash_iterator):
        for img in range(0, lvl+1):
            img_obj = draw_garbage(TRASH[img])
            TRASHOBJ.append(img_obj)

    # Create a sprite group for explosions
    explosion_group = pygame.sprite.Group()
    # Create a sprite group for mines
    mine_group = pygame.sprite.Group()

    # Set running and time values
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    spawn_time = spawn_time1 = start_time
    mine_spawn_timer = 0  # Initialize the mine spawn timer

    # main loop
    while run:
        elapsed_time = time.time() - start_time
        # Spawn new images every 15 seconds
        current_time = current_time1 = time.time()

        if current_time - spawn_time > trash_spawn:
            # Iterate over the trash images to draw them and check for collision
            for img in range(0, lvl+1):
                img_obj = draw_garbage(TRASH[img])
                TRASHOBJ.append(img_obj)
            spawn_time = current_time

        if len(TRASHOBJ) >= 15 or elapsed_time > 100:
            # if time is over then you lost
            # if all the WIN is full of garbage then you lost
            lose_window()

        if not TRASHOBJ:
            winning_window()
            if lvl >= 4:
                run = False
            else:
                lvl += 1
                trash_iterator -= 1
                trash_spawn -= 1
                for i in TURTLEOBJ:
                    i.speed += 1
                draw_rules()
                main()

        # Check for collision between turtle and trash objects
        check_collision(moving_obj)

        # Check for mouse events on the current movable object
        for event in pygame.event.get():  # a loop that runs through all the events on pygame

            # Close if the user quits the game
            if event.type == pygame.QUIT:
                run = False

            # Making the image move
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for img in TRASHOBJ:
                    if img.rect.collidepoint(event.pos):
                        moving_obj = img  # The object we are moving
                        break

            elif event.type == pygame.MOUSEBUTTONUP and moving_obj is not None and moving_obj.rect.collidepoint(event.pos):
                moving_obj = None

            # Make your image move continuously
            elif event.type == pygame.MOUSEMOTION and moving_obj:
                moving_obj.rect.move_ip(event.rel)

        WIN.blit(BG, (0, 0))
        for t in range(0, lvl+1):
            draw_t(TURTLEOBJ[t])
            if current_time1 - spawn_time1 >= 1:
                for j in range(0, lvl+1):
                    TURTLEOBJ[j].update_img()
                spawn_time1 = current_time1
            TURTLEOBJ[t].move()
        draw(elapsed_time)

        if lvl >= 4:
            # Update and draw explosions
            explosion_group.update()
            explosion_group.draw(WIN)

            # Update and draw mines
            mine_group.update()
            mine_group.draw(WIN)

            # Iterate over the mines to check for collision with the player
            if moving_obj is not None:
                for mine in mine_group:
                    mine.collide(moving_obj.rect, explosion_group)

            # Spawn a new mine every 8 seconds
            current_time = time.time()
            if current_time - mine_spawn_timer >= 8:
                new_mine = SeaMine(WIDTH, HEIGHT, "images/image.png")
                mine_group.add(new_mine)
                mine_spawn_timer = current_time

        pygame.display.update()  # Update the GUI pygame
        clock.tick(FPS)  # set FPS

    pygame.quit()  # ends the game

if __name__ == '__main__':
    play_music()
    opening()
    welcome_window()
    draw_rules()
    main()