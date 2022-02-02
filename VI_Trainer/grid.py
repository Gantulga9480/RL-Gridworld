from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
import pygame
import os
import cv2
# import threading

import game
import game_util as util
import create
import play
import train

pygame.init()
pygame.mixer.init()


class Input:

    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.top.title("Enter env size")
        self.top.resizable(False, False)
        self.entry = ttk.Entry(self.top, width=20, font=("default", 15))
        self.entry.pack()
        self.btn = ttk.Button(self.top, text="Create", command=self.set_val)
        self.btn.pack()
        self.val = 0

    def set_val(self):
        self.val = int(self.entry.get())
        self.top.destroy()


class Grid(Tk):

    def __init__(self, screenName=None, baseName=None,
                 useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName,
                         useTk=useTk, sync=sync, use=use)
        # Load env image
        try:
            self.img = ImageTk.PhotoImage(Image.open(game.ENV))
        except FileNotFoundError:
            self.img = ImageTk.PhotoImage(Image.open(game.DEFAULT_ENV))
        # GUI
        self.title("Grid")
        self.resizable(False, False)
        # Last env img
        self.label = ttk.Label(image=self.img)
        self.label.grid(row=0, column=0, columnspan=3)
        # Play button
        self.play_btn = ttk.Button(self, text="Play", command=self.play)
        self.play_btn.grid(row=1, column=0)
        # self.play_btn["state"] = "disabled"
        # Train button
        self.train = ttk.Button(self, text="Train", command=self.train)
        self.train.grid(row=1, column=1)
        # Create env button
        self.create = ttk.Button(self, text="Create env",
                                 command=self.create_env)
        self.create.grid(row=1, column=2)
        # Env show button
        self.show = ttk.Button(self, text="Show env", command=self.show_env)
        self.show.grid(row=2, column=0)
        # self.show["state"] = "disabled"
        # Table show button
        self.table = ttk.Button(self, text="Show table",
                                command=self.show_v_table)
        # self.table["state"] = "disabled"
        self.table.grid(row=2, column=1)
        # Game reset button
        self.reset = ttk.Button(self, text="Reset", command=self.reset)
        self.reset.grid(row=2, column=2)
        # Path optimize button
        self.opt = ttk.Button(self, text="Optimize", command=self.optimize)
        self.opt.grid(row=3, column=0)
        # self.opt["state"] = "disabled"
        # Insert agent button
        self.age = ttk.Button(self, text="Insert", command=self.inserAgent)
        self.age.grid(row=3, column=1)
        # self.age["state"] = "disabled"
        # Menu section
        self.s = BooleanVar()
        self.s.set(False)
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_checkbutton(label="Visual", onvalue=1,
                                 offvalue=0, variable=self.s)
        filemenu.add_command(label="Refresh", command=self.change)
        filemenu.add_command(label="Reset", command=self.reset)
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="Tools", menu=filemenu)
        self.config(menu=self.menubar)
        # Main loop
        self.mainloop()

    def play(self):
        try:
            ENVI = np.load("env.npy")
        except FileNotFoundError:
            ENVI = np.load(r"def\env.npy")
        try:
            TABLE = np.load("v_table.npy")
        except FileNotFoundError:
            TABLE = np.zeros((len(ENVI), len(ENVI)))
        try:
            g = play.Play(envi=ENVI, table=TABLE, size=len(TABLE))
            g.play(visual=self.s.get())
        except game.NoAgent:
            self.message("Agent not placed!")
        del(g)

    def inserAgent(self):
        try:
            ENVI = np.load("env.npy")
        except FileNotFoundError:
            ENVI = np.load(r"def\env.npy")
        g = create.InsertAgent(envi=ENVI, size=len(ENVI))
        del(g)
        util.Image().process(img_path=game.ENV, dim=(220, 220),
                             save=True, save_path=game.ENV)
        self.change(updata_table=False)

    def show_env(self):
        try:
            ENVI = np.load("env.npy")
        except FileNotFoundError:
            ENVI = np.load(r"def\env.npy")
        try:
            TABLE = np.load("v_table.npy")
        except FileNotFoundError:
            TABLE = np.zeros((len(ENVI), len(ENVI)))
        g = play.Play(envi=ENVI, table=TABLE, size=len(ENVI))
        g.show_env()
        del(g)

    def create_env(self):
        inp = Input(self)
        self.wait_window(inp.top)
        g = create.Create(size=inp.val)
        g.create_env()
        del(g, inp)
        util.Image().process(img_path=game.ENV, dim=(220, 220),
                             save=True, save_path=game.ENV)
        self.change()

    def train(self):
        try:
            TABLE = np.load("v_table.npy")
            ENVI = np.load("env.npy")
        except FileNotFoundError:
            ENVI = np.load("def/env.npy")
            try:
                TABLE = np.load("v_table.npy")
            except FileNotFoundError:
                TABLE = np.zeros((len(ENVI), len(ENVI)))
        rl = train.Train(envi=ENVI, table=TABLE, size=len(TABLE))
        rl.train()
        del(rl)

    def show_v_table(self):
        try:
            TABLE = np.load("v_table.npy")
            try:
                ENVI = np.load("env.npy",)
            except FileNotFoundError:
                ENVI = np.load(r"def\env.npy",)
            env_len = len(TABLE)
            g = train.Train(envi=ENVI, table=TABLE, size=env_len)
            g.show_table()
            pygame.display.quit()
            del(g)
        except FileNotFoundError:
            self.message("No such file found!")

    def reset(self):
        try:
            os.remove("v_table.npy")
        except FileNotFoundError:
            self.sound()
        try:
            os.remove("env.npy")
        except FileNotFoundError:
            self.sound()
        try:
            os.remove(game.ENV)
        except FileNotFoundError:
            self.sound()
        self.change()

    def optimize(self):
        o = game.Optimize()
        count = 0
        while count != len(o.action_list) - 2:
            o.play()
            print(o.action_list)
            count = o.fix()
            if count == 0:
                break
            continue
        np.save("q_table", o.q_table)
        pygame.display.quit()
        del(o)

    def change(self, updata_table=True):
        try:
            ENVI = np.load("env.npy",)
        except FileNotFoundError:
            ENVI = np.load(r"def\env.npy",)
        if updata_table:
            np.save("v_table", np.zeros((len(ENVI), len(ENVI))))
        try:
            self.img = ImageTk.PhotoImage(Image.open(game.ENV))
        except FileNotFoundError:
            self.img = ImageTk.PhotoImage(Image.open(game.DEFAULT_ENV))
        self.label.configure(image=self.img)
        self.label.image = self.img

    def message(self, msg):
        messagebox.showwarning(title="Error", message=f"{msg}")

    def sound(self):
        pygame.mixer.music.load(r"C:\Windows\Media\Windows Foreground.wav")
        pygame.mixer.music.play(loops=0)


Grid()
