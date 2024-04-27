import tkinter as tk 
import customtkinter as ctk 
from tkinter import ttk
from tkinter import font
import keyword
import platform


class ToolTip(ctk.CTkCanvas):
    

    def __init__(self, *args, **kwargs):
        ctk.CTkCanvas.__init__(self, *args, **kwargs)
        

    def attach(self, text_widget):
        self.textwidget = text_widget


    def create_tab(self, name):
        self.tab = tk.Menu()


class LeftPanel(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)

   
    #TODO make leftpanel itself


class RightPanel(ctk.CTkFrame):
    #TODO save new open


class TextLineNumbers(ctk.CTkCanvas):
    

    def __init__(self,*args,**kwargs):
        ctk.CTkCanvas.__init__(self,*args,**kwargs) #init using parent class initialisation
        self.textwidget = None
        self.fontSize = 12
        self.configFont()
        self.text_color = "black"


    def configFont(self): # dont know if needed tbh
        system = platform.system().lower()
        if system == "windows":
            self.font = font.Font(family='monospace', size=self.fontSize)
        elif system == "linux":
            self.font = font.Font(family='monospace',size = self.fontSize)


    def attach(self, text_widget):
        self.textwidget = text_widget


    def redraw(self,*args):
        self.delete('all')
        i = self.textwidget.index("@0,0")
        while True :
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(1,y,anchor="nw", font=self.font,text = linenum, fill = "#003200")
            i = self.textwidget.index("%s+1line" % i)


class TextPad(tk.Text):
    

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs, bg="#331e36",fg='white',font=font.Font(family='monospace',size=14), padx=5)
        # !!!!
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # generate the event for certain types of commands
                if {([lindex $args 0] in {insert replace delete}) ||
                    ([lrange $args 0 2] == {mark set insert}) || 
                    ([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {

                    event generate  $widget <<Change>> -when tail
                }

                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))
        # all of that for real time update of TextLineNumbers
        #basically there is custom tkinted event <<Change>> created 

        self.fontSize = 20

    
    #TODO add functuanality
    def highlight():
        pass
    
    #TODO add everything
    def highlightAll():
        pass


class App(ctk.CTkFrame):


    def __init__(self,master=None):
        super().__init__(master)# again init using parent method    
        self.pack(expand=True,fill=tk.BOTH)
        self.initUI()
        self.style=ttk.Style()
        self.style.theme_use("clam")


    def initUI(self):
        frame1 = ctk.CTkFrame(self)
        frame1.pack(fill=ctk.BOTH,expand=True)
        
        #textpad 
        self.textpad = TextPad(frame1)
        self.textpad.pack(fill=tk.BOTH, expand=True)

        #TextLineNumbers
        self.textline = TextLineNumbers(frame1, width=30)
        self.textline.attach(self.textpad)
        self.textline.pack(side='left', fill='y',before=self.textpad)
        self.textpad.bind("<<Change>>", self.on_change)
        self.textpad.bind("<Configure>", self.on_change)
    def on_change(self, event):
        self.textline.redraw()
        



if __name__ == '__main__':
    app = App()
    app.master.title("temp")
    app.master.minsize(width = 800, height=600)
    app.mainloop()
    
