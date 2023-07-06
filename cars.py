from tkinter import *
import random
import os

window_width, window_height = 500, 800

# Global Variables
DELAY = 20 # 20ms delay before redrawing the interface
SCORE = -1
GAME_RUNNING = False
CAR_X = 133 # start car on left
CAR_Y = 0
TOP_SCORE = 0
PERSON_X = window_width / 2 # x-coordinates of the person

# Initialise window
window = Tk()
window.resizable(width = False, height = False)
window.title("Safey Road")
window.geometry(f'{window_width}x{window_height}')


# Checks the existing top score
if os.path.isfile("top_score.txt"):
  with open("top_score.txt", "r") as f:
    TOP_SCORE = int(f.read())
else:
  with open("top_score.txt", "w") as f:
    f.write(str(TOP_SCORE))

canvas = Canvas(window, width = window_width, height = window_height, background='#7F9CB0', highlightthickness=0)
canvas.pack()

welcome_text = canvas.create_text(window_width / 2, 300, text=f'Safey Road', font='Impact 80', fill='#ffffff', anchor=CENTER)
best_score = canvas.create_text(window_width / 2, 400, text=f'Highscore: {TOP_SCORE}', font='Impact 40', fill='#ffffff', anchor=CENTER)
play_again_text = canvas.create_text(window_width / 2, 450, text='Tap left or right key to start!', font='Impact 25', fill='#ffffff', anchor=CENTER)


person_img = PhotoImage(file='img/person.png')
person = canvas.create_image(PERSON_X, window_height - 100, image=person_img)

car_img = PhotoImage(file='img/car.png')
car = canvas.create_image(CAR_X, CAR_Y, image=car_img)
score_display = canvas.create_text(window_width - 25, 50, text="0", font='Impact 60', fill='#ffffff', anchor=E)

def decide_car_spawn():
  global CAR_X
  global SCORE
  global DELAY
  road_choice = [133, window_width - 133]
  road_choice_hard = [133, window_width - 133, window_width / 2]

  SCORE += 1
  canvas.itemconfig(score_display, text=str(SCORE))
  if SCORE < 10:
    CAR_X = random.choice(road_choice)
  else:
    CAR_X = random.choice(road_choice_hard)

def person_left(e):
  global PERSON_X
  global GAME_RUNNING

  if GAME_RUNNING == TRUE:
    PERSON_X -= 20

    if PERSON_X <= 50:
      PERSON_X = 50
    canvas.coords(person, PERSON_X, window_height - 100)
  else:
    restart_game()

def person_right(e):
  global PERSON_X
  person_speed = 20 + 2 * (SCORE // 8)
  if GAME_RUNNING == TRUE:
    PERSON_X += person_speed

    if PERSON_X >= window_width - 50:
      PERSON_X = window_width - 50
    canvas.coords(person, PERSON_X, window_height - 100)
  else:
    restart_game()

def car_down():
  global CAR_Y
  global GAME_RUNNING
  car_speed = 7 + SCORE // 5 #increases car speed by 1 every 5 increase in score

  CAR_Y += car_speed
  canvas.coords(car, CAR_X, CAR_Y)

  if CAR_Y >= window_height + 100:
    CAR_Y = 0
    decide_car_spawn()

  if GAME_RUNNING == True:
    window.after(DELAY, car_down)

def draw_roadline():
  height = 0
  line_width = 3
  line_height = 30
  while height < window_height:
    roadline = canvas.create_rectangle(250 - (line_width / 2), height, 250 + (line_height / 2), height + line_height, fill='#ffffff')
    height += 2 * (line_height + line_width)
  canvas.tag_raise(person) # makes sure that person img is above roadlines

def detect_collision():
  global TOP_SCORE
  global GAME_RUNNING
  global DELAY

  if (CAR_Y >= window_height - 220 and CAR_Y <= window_height) and (PERSON_X > CAR_X - 130 and PERSON_X < CAR_X + 130):
    GAME_RUNNING = False
    if SCORE > TOP_SCORE:
      TOP_SCORE = SCORE
      with open("top_score.txt", "w") as f:
        f.write(str(TOP_SCORE))
    gameover_screen()

  if GAME_RUNNING == True:
    window.after(DELAY, detect_collision)

def restart_game():
  global CAR_X
  global DELAY
  global SCORE
  global GAME_RUNNING
  global CAR_X
  global CAR_Y

  DELAY = 20
  SCORE = -1
  GAME_RUNNING = True
  CAR_X = 133 # start car on left
  CAR_Y = 100
  try:
    canvas.delete(score_current)
    canvas.delete(best_score)
    canvas.delete(fill_rectangle)
    canvas.delete(play_again_text)
  except:
    canvas.delete(welcome_text)
    canvas.delete(best_score)
    canvas.delete(play_again_text)

  decide_car_spawn()
  draw_roadline()
  window.after(DELAY, car_down)
  window.after(DELAY, detect_collision)

def gameover_screen():
  global TOP_SCORE
  global SCORE
  global score_current
  global best_score
  global fill_rectangle
  global play_again_text
  fill_rectangle = canvas.create_rectangle(0, 0, window_width, window_height, fill='#7F9CB0')
  score_current = canvas.create_text(80, 300, text=f'Score: {SCORE}', font='Impact 50', fill='#ffffff', anchor=W)
  best_score = canvas.create_text(80, 370, text=f'Highscore: {TOP_SCORE}', font='Impact 50', fill='#ffffff', anchor=W)
  play_again_text = canvas.create_text(80, 440, text='Left or right key to play again!', font='Impact 30', fill='#ffffff', anchor=W)

window.after(DELAY, car_down)
window.after(DELAY, detect_collision)
window.bind("<Left>", person_left)
window.bind("<Right>", person_right)
window.mainloop()