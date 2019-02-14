from tkinter import *
from time import time
from random import random

class Bar():

    def __init__(self, frame, name, max, starting):
        self.max = max
        self.val = starting
        self.text = StringVar()
        self.name = name
        self.label = Label(frame)
        self.disp()
        self.label.pack()

    def disp(self):
        text_bar = "[" + "|"*int(self.val/10) + " "*(int(self.max/10)-int(self.val/10)) + "]"
        self.text.set(self.name + ": " + str(self.val) + "% " + text_bar)
        self.label.configure(text = self.text.get())

    def add(self, val):
        self.val += val
        self.val = min((self.val, self.max))
        self.val = max((self.val, 0))

    def get(self):
        return self.val


def do_toggle(button : Button, val : BooleanVar):
    if val.get():
        button["text"] = "off"
        val.set(False)
    else:
        button["text"] = "on"
        val.set(True)


class Game():

    # constants
    fuel = 2
    usage = -1

    def __init__(self,rules):
        self.rules = rules

    def main(self):

        # setup tk
        self.window = Tk()
        self.frame = Frame(self.window)
        self.splash = Label(self.frame, text = "Manage those bars!")
        self.splash.pack()

        # variables
        self.reserve = Bar(self.frame, "Reserve", 100, 100)
        self.current = Bar(self.frame, "Power", 100, 50)
        self.filling = BooleanVar(self.frame, value = False)

        # setup game tk
        self.toggle = Button(self.frame)
        self.toggle["command"] = lambda : do_toggle(self.toggle, self.filling)
        do_toggle(self.toggle, self.filling)

        # start
        self.toggle.pack()
        self.frame.pack()
        self.start_time = time()
        self.update()

        # mainloop (must be last)
        self.window.mainloop()

    def update(self):
        # call the gamerules
        for rule in self.rules:
            rule(self)
        # default movements
        if(self.filling.get() and self.reserve.get() > 0):
            self.current.add(self.fuel)
            self.reserve.add(-self.fuel)
        self.current.add(self.usage)
        # disp
        self.reserve.disp()
        self.current.disp()
        #call again if the game is ongoing
        if(self.current.get() > 0):
            self.window.after(500, self.update)
        else:
            self.splash_text("Game Over; Time : "+str(int((time()-self.start_time)*10)/10)+" Seconds")

    def splash_text(self, text):
        self.splash["text"] = text

# adds random values to the value over time
# increasing delay param will lower the odds of noise happening
# incresing pink param increase how closely noise will stick to the mean
# incresing noise mag param will increase 
def rand_noise(game, delay_param = 10, pink_param = 3, noise_mag_param = 10):
    if not hasattr(game, "time_last_noise"):
        # setup
        game.time_last_noise = time()
    else:
        # chance for noise
        time_since = time() - game.time_last_noise
        if random() < time_since/(delay_param + time_since):
            # apply noise
            sign = -1 if random() < 0.5 else 1
            noise = int((random()**pink_param) * sign * noise_mag_param)
            if noise != 0:
                game.splash_text("Encounted space noise! "+str(noise)+" Energy")
                game.current.add(noise)
                game.time_last_noise = time()

if __name__ == "__main__":
    game = Game([rand_noise])
    game.main()