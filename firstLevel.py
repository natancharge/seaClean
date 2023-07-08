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
    "images/Bottle.png",
    "images/can.png",
    "images/Banana.png",
    "images/Paper.png",
    "images/Bamba.png"
]
TURTLES = [
    "images/GrayT.png",
    "images/YellowT.png",
    "images/BrownT.png",
    "images/BlueT.png",
    "images/PurpleT.png"
]
TRASHOBJ = []
# Set a variable to store the current movable image object
moving_obj = None
FPS = 15
FONT = pygame.font.SysFont("comicsans", 30)


def play_music():
    pygame.mixer.music.load('scott-buckley-jul.mp3')

    # Set preferred volume
    pygame.mixer.music.set_volume(0.2)

    # Play the music
    pygame.mixer.music.play()


class TrashObj:
    def __init__(self, img_path):
        # Take image as input
        self.img = pygame.image.load(img_path)
        self.vel = 10
        # Draw rectangle around the image
        self.rect = self.img.get_rect()
        self.rect.center = (
            random.randint(self.vel, WIDTH - self.vel),
            random.randint(self.vel, HEIGHT - self.vel),
        )
        self.img_path = img_path

    def get_path(self):
        return self.img_path


class TurtleObj:
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


def lose_window():
    cap = cv2.VideoCapture('vids/game over.mov')  # שם של קובץ

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            WIN.blit(frame, (0, 0))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def wining_window():
    cap = cv2.VideoCapture('vids/win.mov')  # שם של קובץ

    while cap.isOpened():
        time.sleep(0.1)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            WIN.blit(frame, (WIDTH / 2 - 70, 500))

            if cv2.waitKey(FPS) & 0xFF == ord('q'):
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

        if pygame.event.get() == pygame.QUIT:
            pygame.quit()

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
    cap = cv2.VideoCapture('vids/nnkdfjfl.mp4')  # שם של קובץ

    while cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.flip(frame, 0)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if pygame.event.get() == pygame.QUIT:
            pygame.quit()

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


def welcome_window():
    button_pos = (WIDTH / 2 - 70, 500)
    button_size = (150, 50)
    WIN.set_alpha(128)
    surface = pygame.Surface(button_size)
    surface.set_alpha(128)  # alpha level
    surface.fill((255, 255, 255))  # this fills the entire surface
    startmenu = pygame.image.load('images/start (2).png')
    startmenu = pygame.transform.scale(startmenu, (WIDTH, HEIGHT))
    run = True
    while run:
        pygame.time.delay(10)
        WIN.blit(startmenu, (0, 0))
        # draw button
        WIN.blit(surface, button_pos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if (
                    button_pos[0] < mouse_pos[0] < button_pos[0] + button_size[0]
                ) and (button_pos[1] < mouse_pos[1] < button_pos[1] + button_size[1]):
                    run = False
                    main()
            # start the main game


def draw_garbage(img):
    return TrashObj(img)


def draw_turtle(img):
    return TurtleObj(img)


organic_t = draw_turtle('images/BrownT.png')
metal_t = draw_turtle('images/GrayT.png')
paper_t = draw_turtle('images/BlueT.png')
plastic_t = draw_turtle('images/YellowT.png')
glass_t = draw_turtle('images/PurpleT.png')


def draw(BG, img_obj, elapsed_time):
    # Draw the background, trash images, and update the screen
    WIN.blit(BG, (0, 0))
    for img_obj in TRASHOBJ:
        WIN.blit(img_obj.img, img_obj.rect)
    time_text = FONT.render(f"Time: {round(100 - elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))


def draw_t(turtle_obj):
    WIN.blit(turtle_obj.img, turtle_obj.rect)


def check_collision():
    global TRASHOBJ
    # Check if any trash object has collided with the turtle
    for trash_obj in TRASHOBJ:
        if organic_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Banana.png":
            TRASHOBJ.remove(trash_obj)
        elif metal_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/can.png":
            TRASHOBJ.remove(trash_obj)
        elif glass_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Bottle.png":
            TRASHOBJ.remove(trash_obj)
        elif plastic_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Bamba.png":
            TRASHOBJ.remove(trash_obj)
        elif paper_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Paper.png":
            TRASHOBJ.remove(trash_obj)


def main():
    global moving_obj

    for img in TRASH:
        img_obj = draw_garbage(img)
        TRASHOBJ.append(img_obj)

    # Set running and time values
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    spawn_time = start_time

    # main loop
    while run:
        elapsed_time = time.time() - start_time
        # Spawn new images every 15 seconds
        current_time = time.time()

        if current_time - spawn_time > 15:
            # Iterate over the trash images to draw them and check for collision
            for img in TRASH:
                img_obj = draw_garbage(img)
                TRASHOBJ.append(img_obj)
            spawn_time = current_time

        if len(TRASHOBJ) == 15 or elapsed_time > 100:
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
            wining_window()
            run = False

        # Check for collision between turtle and trash objects
        check_collision()

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

            elif event.type == pygame.MOUSEBUTTONUP and moving_obj is not None and moving_obj.rect.collidepoint(
                    event.pos):
                moving_obj = None

            # Make your image move continuously
            elif event.type == pygame.MOUSEMOTION and moving_obj:
                moving_obj.rect.move_ip(event.rel)

        draw(BG, img_obj, elapsed_time)
        draw_t(organic_t)
        draw_t(metal_t)
        draw_t(glass_t)
        draw_t(plastic_t)
        draw_t(paper_t)

        pygame.display.update()  # Update the GUI pygame
        clock.tick(FPS)  # set FPS

    pygame.quit()  # ends the game


if __name__ == '__main__':
    play_music()
    backstory_introduction()
    opening()
    welcome_window()