from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
import game
import pygame
import os
import threading
import cv2

pygame.init()
pygame.mixer.init()

SIZE = 5


class myThread(threading.Thread):

    def __init__(self):
        super().__init__(self)

    def run(self):
        pass


class Capture(game.GridWorld):

    def __init__(self, visual=True):
        super().__init__(visual=visual)

    def show_env(self):
        pygame.display.set_caption("GridWorld")
        self.win.fill(game.BLACK)
        self.draw_board()
        pygame.display.flip()
        pygame.image.save(self.win, "img\\env_img.jpg")
        pygame.display.quit()


class Input:

    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.top.title("Enter env size")
        self.top.resizable(False, False)
        self.entry = ttk.Entry(self.top, width=20, font=("default", 15))
        self.entry.pack()
        self.btn = ttk.Button(self.top, text="Create", command=self.set_val)
        self.btn.pack()

    def set_val(self):
        global SIZE
        SIZE = int(self.entry.get())
        self.top.destroy()


class Grid(Tk):

    def __init__(self, screenName=None, baseName=None,
                 useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName,
                         useTk=useTk, sync=sync, use=use)
        try:
            game.Image().process("img\\env_img.jpg", (220, 220))
            img = ImageTk.PhotoImage(Image.open("img\\env_img.jpg"))
        except cv2.error:
            img = ImageTk.PhotoImage(Image.open("img\\default_env_img.jpg"))
        # GUI
        self.title("Grid")
        self.resizable(False, False)
        self.label = ttk.Label(image=img)
        self.label.grid(row=0, column=0, columnspan=3)
        self.play_btn = ttk.Button(self, text="Play", command=self.play)
        self.play_btn.grid(row=1, column=0)
        self.train = ttk.Button(self, text="Train", command=self.train)
        self.train.grid(row=1, column=1)
        self.create = ttk.Button(self, text="Create env",
                                 command=self.create_env)
        self.create.grid(row=1, column=2)
        self.show = ttk.Button(self, text="Show env", command=self.show_env)
        self.show.grid(row=2, column=0)
        self.table = ttk.Button(self, text="Show table",
                                command=self.show_q_table)
        self.table.grid(row=2, column=1)
        self.reset = ttk.Button(self, text="Reset", command=self.reset)
        self.reset.grid(row=2, column=2)
        self.opt = ttk.Button(self, text="Optimize", command=self.optimize)
        self.opt.grid(row=3, column=0)
        self.s = BooleanVar()
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_checkbutton(0, label="Visual", onvalue=1,
                                 offvalue=0, variable=self.s)
        self.menubar.add_cascade(label="Tools", menu=filemenu)
        self.config(menu=self.menubar)
        self.mainloop()

    def play(self):
        g = game.GridWorld(visual=self.s.get())
        g.play()
        del(g)

    def show_env(self):
        g = game.Path()
        del(g)

    def create_env(self):
        inp = Input(self)
        self.wait_window(inp.top)
        g = game.Create(size=SIZE)
        g.create_env()
        del(g, inp)
        game.Image().process("img\\env_img.jpg", (220, 220), save=True)
        self.change()

    def train(self):
        rl = game.Training(visual=False)
        rl.train()
        del(rl)

    def show_q_table(self):
        try:
            env = np.load("q_table.npy")
            env_len = len(env)
            g = game.Create(size=env_len)
            g.show_table()
            del(g)
        except FileNotFoundError:
            env = np.load("def/q_table_default.npy")
            env_len = len(env)
            g = game.Create(size=env_len)
            g.show_table()
            del(g)

    def reset(self):
        try:
            os.remove("q_table.npy")
        except FileNotFoundError:
            self.sound()
        try:
            os.remove("env.npy")
        except FileNotFoundError:
            self.sound()
        try:
            os.remove("img\\env_img.jpg")
        except FileNotFoundError:
            self.sound()
        self.change()

    def change(self):
        try:
            img = ImageTk.PhotoImage(Image.open("img\\env_img.jpg"))
        except FileNotFoundError:
            img = ImageTk.PhotoImage(Image.open("QL_Trainer\\img\\default_env_img.jpg"))
        self.label.configure(image=img)
        self.label.image = img

    def optimize(self):
        o = game.Optimize()
        count = 0
        while count != len(o.action_list)-2:
            o.play()
            print(o.action_list)
            count = o.fix()
            if count == 0:
                break
            continue
        np.save("q_table", o.q_table)
        pygame.display.quit()
        del(o)

    def message(self, msg):
        messagebox.showwarning(title="Error", message=f"{msg}")

    def sound(self):
        pygame.mixer.music.load(r"C:\Windows\Media\Windows Foreground.wav")
        pygame.mixer.music.play(loops=0)


Grid()
