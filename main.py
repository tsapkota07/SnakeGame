# this is followed from youtube from Bro Code's Channel.
# imprt tkinter and random
from tkinter import *
import random

# Constants for the game:
GAME_WIDTH = 1000
GAME_HEIGHT = 700

window = Tk()
#
# # Get screen width and height
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
#
# # Use the screen resolution as your game dimensions
# GAME_WIDTH = screen_width
# GAME_HEIGHT = screen_height

SPEED = 200
SPACE_SIZE = 20
BODY_PARTS = 4
SNAKE_COLOR = "#0000FF"  # GREEN
FOOD_COLOR = "#FFFF00"   # RED
BACKGROUND_COLOR = "#000000"  # BLACK

def start_game():
    global snake, food, direction, score
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)
    start_button.pack_forget()

class Snake:
    def __init__(self):
        self.body = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x ,y, x+SPACE_SIZE, y + SPACE_SIZE,fill = SNAKE_COLOR,tag = "snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH//SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT//SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x, y, x+SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake,food):
    x,y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE # move one space up

    elif direction == 'down':
        y += SPACE_SIZE

    elif direction == 'left':
        x -= SPACE_SIZE

    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x,y) )
    square = canvas.create_rectangle(x,y, x +SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score += 1

        label.config(text = "Score: {}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x,y = snake.coordinates[0]

    if x<0 or x>=GAME_WIDTH:
        return True
    elif y<0 or y>=GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete('all')
    canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2,
                       font = ("Arial", 70),text = "GAME OVER",fill = 'red', tag = 'gameover' )
    start_button.pack(pady=20)

window = Tk()
window.title("Snake Game")
window.attributes("-fullscreen", True)
window.bind('<Escape>', lambda event: window.attributes("-fullscreen", False))


score = 0
direction = 'down'

label = Label(window,
              text="Score:{}".format(score),
              font=('consolas', 40)
              )
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x =int ( (screen_width/2) - window_width/2)
y =int ( (screen_height/2) - window_height/2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# snake = Snake()
# food = Food()
# next_turn(snake,food)
start_button = Button(window, text="Start Game", font=("Arial", 24), command=start_game)
start_button.pack(pady=20)


window.mainloop()