import pygame
import time
import random
import cv2
from tkinter import messagebox

# Construct the GUI game
pygame.init()

WIDTH, HEIGHT = 867, 606
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create the window
pygame.display.set_caption("Sea Clean")  # the game title
BG = pygame.transform.scale(pygame.image.load("images/Sea.png"), (WIDTH, HEIGHT))
TRASH = ["images/Bottle.png",
         "images/can.png", "images/Banana.png", "images/Paper.png", "images/Bamba.png"]
TURTLES = ["images/GrayT.png", "images/YellowT.png",
           "images/BrownT.png", "images/BlueT.png",
           "images/PurpleT.png"]
TRASHOBJ = []
OIL = []
QUESTIONS = ["does every type of plastic material and plastic object we use today can be found in the ocean?",
             "Are there 30 kg of plastic litter in the ocean?",
             "About 50%-85% of the oil that leaks in the middle of the sea will eventually reach the shore.",
             "Above 50% of plastic is recycled worldwide."]
ANSWERS = ["That's right!",
           "Correct!!! every year, between 4.8 and 12.7 million tonnes of the plastic waste produced on land eventually"
           "reach the ocean.",
           "Amazing!!",
           "Great job, less then 18% of plastic is recycled worldwide."]
# Set a variable to store the current movable image object
moving_obj = None
FPS = 15
FONT = pygame.font.SysFont("comicsans", 30)

for i in range(1, 5):
    path = f"oilImages/{i}.png"
    OIL.append(path)


def draw2(BG, img_path):
    WIN.blit(BG, (0, 0))
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    WIN.blit(img, (0, 0))


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
        self.rect.center = random.randint(self.vel, WIDTH - self.vel), random.randint(self.vel, HEIGHT - self.vel)
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
        self.rect.center = random.randint(self.vel, WIDTH - self.vel), random.randint(self.vel, HEIGHT - self.vel)


def lose_window():
    cap = cv2.VideoCapture('vids/game over.mov')  # שם של קובץ

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
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
            cv2.imshow('frame', frame)
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
        if ret:
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def backstory_introduction():
    cap = cv2.VideoCapture('vids/nnkdfjfl.mp4')  # שם של קובץ

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
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
    startmenu = pygame.transform.scale(startmenu, (867, 606))
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

                if (button_pos[0] < mouse_pos[0] < button_pos[0] + button_size[0]) and (
                        button_pos[1] < mouse_pos[1] < button_pos[1] + button_size[1]):
                    lvl1()
            # start the main game


def draw_garbage(img):
    return TrashObj(img)


def draw_turtle(img):
    return TurtleObj(img)


glass_t = draw_turtle('images/PurpleT.png')
metal_t = draw_turtle('images/GrayT.png')
organic_t = draw_turtle('images/BrownT.png')
paper_t = draw_turtle('images/BlueT.png')
plastic_t = draw_turtle('images/YellowT.png')


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
        if glass_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Bottle.png":
            TRASHOBJ.remove(trash_obj)
        elif metal_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/can.png":
            TRASHOBJ.remove(trash_obj)
        elif plastic_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Bamba.png":
            TRASHOBJ.remove(trash_obj)
        elif organic_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Banana.png":
            TRASHOBJ.remove(trash_obj)
        elif paper_t.rect.colliderect(trash_obj.rect) and trash_obj.get_path() == "images/Paper.png":
            TRASHOBJ.remove(trash_obj)


def lvl1():
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
                lvl1()
                # code to return to the program
            else:
                run = False
                # code to quit the program

        if not TRASHOBJ:
            wining_window()
            lvl2()

        # Check for collision between turtle and trash objects
        check_collision()

        # Check for mouse events on the current movable object
        for event in pygame.event.get():  # a loop that runs threw all the events on pygame

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


def lvl2():
    img_index = 0
    i = 0

    draw2(BG, OIL[img_index])

    # main loop
    while i <= 3:

        answer = messagebox.askquestion(f"Question number: {i + 1}", QUESTIONS[i])

        if i % 2 == 0:
            if answer == "yes":
                messagebox.showinfo("", ANSWERS[i])
            else:
                while messagebox.askquestion(f"Question number: {i + 1}", QUESTIONS[i]) != "yes":
                    if img_index > 3:
                        lose_window()
                        ans = messagebox.askquestion("You lost...", "Wanna try again?")

                        if ans == "yes":
                            lvl2()
                            # code to return to the program
                        else:
                            pygame.quit()
                            # code to quit the program

                    messagebox.showerror("Wrong!", "Try again")
                    img_index += 1
                    draw2(BG, OIL[img_index])
                    pygame.display.update()
                messagebox.showinfo("", ANSWERS[i])
        else:
            if answer == "no":
                messagebox.showinfo("", ANSWERS[i])
            else:
                while messagebox.askquestion(f"Question number: {i + 1}", QUESTIONS[i]) != "no":
                    if img_index > 3:
                        lose_window()
                        ans = messagebox.askquestion("You lost...", "Wanna try again?")

                        if ans == "yes":
                            lvl2()
                            # code to return to the program
                        else:
                            pygame.quit()
                            # code to quit the program

                    messagebox.showerror("Wrong!", "Try again")
                    img_index += 1
                    draw2(BG, OIL[img_index])
                    pygame.display.update()
                messagebox.showinfo("", ANSWERS[i])
        i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        draw2(BG, OIL[img_index])
        pygame.display.update()

    wining_window()
    pygame.quit()


def main():
    play_music()
    backstory_introduction()
    opening()
    welcome_window()


if __name__ == '__main__':
    main()