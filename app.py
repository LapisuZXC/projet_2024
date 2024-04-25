import tkinter as tk 
import customtkinter as ctk 
from tkinter import ttk
from tkinter import font
import keyword
import platform


class TextLineNumbers(ctk.CTkCanvas):
    def __init__(self,*args,**kwargs):
        ctk.CTkCanvas.__init__(self,*args,**kwargs)
        self.textwidget = None
        self.fontSize = 12
        self.configFont()

    def configFont(self):
        system = platform.system().lower()
        if system == "windows":
            self.font = font.Font(family='monospace', size=self.fontSize)
        elif system == "linux":
            self.font = font.Font(family='monospace',size = self.fontSize)

    def attach(self, text_widget):
        self.textwidget=text_widget

    def redraw(self,*args):
        self.delete('all')
        i = self.text_widget.index("@0.0")
        while True :
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(1,y,anchor="nw", font=self.font, text=linenum, fill = "pink")
            i = self.textwidget.index(f"{i}+1line")


class App(ctk.CTkFrame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack(expand=True,fill=tk.BOTH)
        self.initUI()
        self.style=ttk.Style()
        self.style.theme_use("clam")

    def initUI(self):
        frame1 = ctk.CTkFrame(self)
        frame1.pack(fill=ctk.BOTH,expand=True)
        
        #texpad

        self.textpad = ctk.CTkTextbox(frame1, text_color="#FFFFFF", bg_color="#3c003f",fg_color="#4c004f")
        self.textpad.pack(fill=tk.BOTH, expand=True)
        


        #TextLineNumbers
        self.textline = TextLineNumbers(frame1, width=30)
        self.textline.attach(self.textpad)
        self.textline.pack(side='left', fill='y')
        self.textpad.bind("<<Change>>", self.on_change)
    def on_change(self, event):
        self.textline.redraw()
app = App()
app.master.title("temp")
app.master.minsize(width = 800, height=600)
app.mainloop()

