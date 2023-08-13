import pygame
import time
import random
import cv2
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
    "images/Gameplay explaning.png",
    "images/Glass introduction.png",
    "images/Paper introduction.png",
    "images/Plastic introduction.png"
]
TRASHOBJ, TURTLEOBJ = [], []
# Set a variable to store the current movable image object
moving_obj = None
FPS = 15
FONT = pygame.font.SysFont("open sans", 111, True, True)
# varibles for tracking the number of objects on the screen
lvl = 1
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


class TurtleObj:
    def __init__(self, img_path):
        # Take image as input
        self.img_path = img_path
        self.i = 0
        self.images = [pygame.image.load(path) for path in self.img_path]
        self.img = self.images[self.i]
        self.vel = 100 
        self.speed = 2
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

            if cv2.waitKey(1) == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


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

            if cv2.waitKey(1) == 27:
                break
        else:
            break

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

            if cv2.waitKey(1) == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def backstory_introduction():
    cap = cv2.VideoCapture('vids/Backstory.mp4')

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

            if cv2.waitKey(1) == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def welcome_window():
    startmenu = pygame.image.load('images/start (2).png')
    startmenu = pygame.transform.scale(startmenu, (WIDTH, HEIGHT))

    btn = pygame.Rect(WIDTH / 2 - 135, HEIGHT / 2 + HEIGHT / 3, 270 ,70)

    txt = FONT.render("START", 1, "white")
    text_width, text_height = FONT.size("START")
    txt_pos = (WIDTH / 2 - text_width / 2, HEIGHT / 2 + HEIGHT / 3)

    run = True
    while run:
        pygame.time.delay(10)
        WIN.blit(startmenu, (0, 0))
        # draw button
        pygame.draw.rect(WIN, "#004AAD", btn)
        WIN.blit(txt, txt_pos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button
                if btn.collidepoint(mouse_pos):
                    run = False
                    main()
            # start the main game


def draw_garbage(img):
    return TrashObj(img)


def draw_turtle(img):
    return TurtleObj(img)


def draw(img_obj, elapsed_time):
    # Draw the trash images, and update the screen
    for img_obj in TRASHOBJ:
        WIN.blit(img_obj.bordered_surface, img_obj.rect)
    time_text = FONT.render(f"Time: {round(100 - elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

def draw_rules(path):
    img = pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))
    run = True
    while run:
        for event in pygame.event.get():  # a loop that runs through all the events on pygame
            # Close if the user quits the game
            if event.type == pygame.QUIT:
                run = False
        WIN.blit(img, (0, 0))
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

def check_and_append(x, y, vel):
    while (x, y) in locations or (x, y) in [loc for loc in locations if isinstance(loc, tuple)]:
        x = random.randint(vel, WIDTH - vel)
        y = random.randint(vel, HEIGHT - vel)
    locations.append((x, y))
    return (x, y)

metal_t = draw_turtle(['images/GrayT.png', 'images/MetalTM.png'])
organic_t = draw_turtle(['images/BrownT.png', 'images/OrganicTM.png'])
glass_t = draw_turtle(['images/PurpleT.png', 'images/GlassTM.png'])
paper_t = draw_turtle(['images/BlueT.png', 'images/PaperTM.png'])
plastic_t = draw_turtle(['images/YellowT.png', 'images/PlasticTM.png'])
TURTLEOBJ = [metal_t, organic_t, glass_t, paper_t, plastic_t]

def main():
    global moving_obj, lvl, trash_iterator

    for i in range(trash_iterator):
        for img in range(0, lvl+1):
            img_obj = draw_garbage(TRASH[img])
            TRASHOBJ.append(img_obj)

    # Set running and time values
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    spawn_time = spawn_time1 = start_time

    # main loop
    while run:
        elapsed_time = time.time() - start_time
        # Spawn new images every 15 seconds
        current_time = current_time1 = time.time()

        if current_time - spawn_time > 15:
            # Iterate over the trash images to draw them and check for collision
            for img in range(0, lvl+1):
                img_obj = draw_garbage(TRASH[img])
                TRASHOBJ.append(img_obj)
            spawn_time = current_time

        if len(TRASHOBJ) >= 15 or elapsed_time > 100:
            # if time is over then you lost
            # if all the screen is full of garbage then you lost
            lose_window()
            ans = messagebox.askquestion("You lost...", "Wanna try again?")

            if ans == "yes":
                TRASHOBJ.clear()
                start_time = time.time() + 100
                spawn_time = start_time
                main()
                # code to return to the program
            else:
                run = False
                # code to quit the program

        if not TRASHOBJ:
            winning_window()
            if lvl >= 4:
                run = False
            else:
                lvl += 1
                trash_iterator -= 1
                draw_rules(RULES[lvl-1])
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
        draw(img_obj, elapsed_time)

        pygame.display.update()  # Update the GUI pygame
        clock.tick(FPS)  # set FPS

    pygame.quit()  # ends the game


if __name__ == '__main__':
    play_music()
    opening()
    backstory_introduction()
    draw_rules(RULES[0])
    welcome_window()