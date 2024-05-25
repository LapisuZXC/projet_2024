import tkinter as tk 
import customtkinter as ctk
import sys, os

class Diolog(tk.Toplevel):
    def __init__(self, parent, title=None):
        super().__init__(parent)
        self.transient(parent)

        if title:
            self.title = title

        self.parent = parent
        self.result = None

