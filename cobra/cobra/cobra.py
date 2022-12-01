from tkinter import *
import random


window_width = 800
window_height = 450
game_running = True


def create_block():
    global food
    xpos = 10 * random.randint(1, (window_width - 10) / 10)
    ypos = 10 * random.randint(1, (window_height - 10) / 10)
    food = c.create_oval(xpos, ypos,
                          xpos + 10, ypos + 10,
                          fill="red")

class Score(object):

    def __init__(self):
        self.score = 0
        self.x = 55
        self.y = 15
        c.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20",
                      fill="black", tag="score", state='hidden')

    def increment(self):
        c.delete("score")
        self.score += 1
        c.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20",
                      fill="black", tag="score")

    def reset(self):
        c.delete("score")
        self.score = 0

def main():
    global game_running
    if game_running:
        s.move()

        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        if x2 > window_width or x1 < 0 or y1 < 0 or y2 > window_height:
            game_running = False

        elif head_coords == c.coords(food):
            s.add_segment()
            c.delete(food)
            create_block()

        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    game_running = False

        root.after(100, main)
    else:
        set_state(restart_text, 'normal')

class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x + 10, y + 10,
                                           fill="green")
                                           
class Cobra(object):
    def __init__(self, segments):
        self.segments = segments

        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}

        self.vector = self.mapping["Right"]

    def move(self):
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0] * 10, y1 + self.vector[1] * 10,
                 x2 + self.vector[0] * 10, y2 + self.vector[1] * 10)

    def add_segment(self):
        score.increment()
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - 10
        y = last_seg[3] - 10
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)

def set_state(item, state):
    c.itemconfigure(item, state=state)
    c.itemconfigure(food, state='hidden')


def clicked(event):
    global game_running
    s.reset_snake()
    game_running = True
    c.delete(food)
    score.reset()
    c.itemconfigure(restart_text, state='hidden')
    start_game()

def start_game():
    global s
    create_block()
    s = create_snake()

    c.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    segments = [Segment(10, 10),
                Segment(20, 10),
                Segment(30, 10)]
    return Cobra(segments)
    
def close_win(root):
    exit()

root = Tk()
root.title("Cobra")

c = Canvas(root, width=window_width, height=window_height, bg="white")
c.grid()

c.focus_set()

                               
restart_text = c.create_text(window_width / 2, window_height - window_height / 3,
                             font='Arial 20',
                             fill='black',
                             text="Play Again",
                             state='hidden')


c.tag_bind(restart_text, "<Button-1>", clicked)

score = Score()

start_game()

root.mainloop()
