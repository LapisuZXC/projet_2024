import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from tkinter import font
from tkterminal import Terminal
import keyword
import platform
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal, Text
from pygments.formatter import Formatter
from pygments import highlight
from pygments.lexers import PythonLexer
import os

  

class UpperPanel(tk.Frame):
    

    def __init__(self,master=None,right_panel=None,*args,**kwargs):
        super().__init__(master)
        self.right_panel = right_panel
        self.initUI(master,*args,**kwargs)
        
    
    def initUI(self, master, *args, **kwargs):
        self.frame = tk.Frame(master, height=25)
        self.save_b = ctk.CTkButton(self.frame,fg_color="gray",corner_radius=0,width=55,text="save",command=lambda : self.right_panel.saveFile())
        self.open_b = ctk.CTkButton(self.frame,fg_color="gray",corner_radius=0,width=55,text="open",command=lambda : self.right_panel.openFile())
        self.new_b = ctk.CTkButton(self.frame,fg_color="gray",corner_radius=0,width=55,text="new",command=lambda : self.right_panel.newFile())
        # Create a CTkMenuBar widget
        self.new_b.pack(side=tk.LEFT,expand=False, fill=tk.BOTH)
        self.open_b.pack(side=tk.LEFT,expand=False, fill=tk.BOTH)
        self.save_b.pack(side=tk.LEFT,expand=False, fill=tk.BOTH)
        self.frame.pack(expand=False, fill=ctk.BOTH, anchor='n', side=tk.TOP)
        

    def attach(self, text_widget):
        self.textwidget = text_widget


class LeftPanel(tk.Frame): 
    def __init__(self, master=None,right_panel=None): 
        super().__init__(master) 
        self.right_panel = right_panel
        self.selected_dir = None
        self.initUI(master) 
 
    def initUI(self, master):
        self.selected_file = tk.StringVar()
        self.selected_file.trace_add("write", self.on_selected_file_change)
        if self.right_panel.selected_file:
            self.selected_dir = os.path.dirname(self.right_panel.selected_file)

        self.breadcrumb = tk.StringVar(value="File")  # Initialize Breadcrumb 
        self.breadcrumb_label = ctk.CTkLabel( 
            self, textvariable=self.breadcrumb, text_color="white" 
        ) 
        self.breadcrumb_label.pack(pady=5) 
        
        self.file_list = tk.Listbox( 
            self, 
            selectmode=tk.SINGLE, 
            width=20, 
            height=10, 
            highlightthickness=0, 
            activestyle="none", 
            background="#331e36", 
            foreground="white", 
            font=font.Font(family='monospace', size=12), 
        )
        for i in os.listdir(self.selected_dir):
            self.file_list.insert(tk.END, i)
        self.file_list.pack(expand=True, fill=tk.BOTH) 

        self.file_list.bind("<<ListboxSelect>>", self.on_file_select) 
        
 
    def on_file_select(self, event): 
        selection = self.file_list.curselection() 
        if selection: 
            selected_index = selection[0] 
            selected_item = self.file_list.get(selected_index) 
            self.breadcrumb.set(f"File / {selected_item}")
    def on_selected_file_change(self, event):
        self.selected_dir = os.path.dirname(self.right_panel.selected_dir)

class RightPanel(tk.Frame):
    
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master)
        self.master = master
        self.selected_file = ""
        self.initUI(master, *args, **kwargs)

    def initUI(self, master, *args, **kwargs):
        self.textPad = TextPad(master, *args, **kwargs)                 # Само поле где пишется текст
        self.textPad.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)    
        self.tools = UpperPanel(master,self,*args,**kwargs)             # Тут кнопочки всякие
        self.tools.attach(master)#?
        
        
        
    def newFile(self):
        self.textPad.delete('1.0', 'end')


    def saveFile(self):
        file_path = filedialog.asksaveasfilename(filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        self.selected_file = file_path
        if file_path:
            self.textPad.delete('1.0', 'end')
            self.textPad.insert('1.0', open(file_path, encoding='utf-8').read())

    def openFile(self):
        file_path = filedialog.askopenfilename(title='Выбор файла',
                                              filetypes=(
                                              ('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        if file_path:
            self.textPad.delete('1.0', 'end')
            self.textPad.insert('1.0', open(file_path, encoding='utf-8').read())
            

class TextLineNumbers(ctk.CTkCanvas):
    


    def __init__(self,*args,**kwargs):
        ctk.CTkCanvas.__init__(self,*args,**kwargs)  # init using parent class initialisation
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
        tk.Text.__init__(self, *args, **kwargs)
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
        # basically there is custom tkinted event <<Change>> created
        
        self.fontSize = 20
        
        

# TODO associate a function with text directly from the application
class CustomFormatter(Formatter):
    def __init__(self, **options):
        super(CustomFormatter, self).__init__(**options)
        self.styles = {
            Keyword: '\033[94m',  # Blue
            Operator: '\033[91m',  # Red
            Operator.Word: '\033[93m',  # Yellow
            Number.Integer: '\033[91m',  # Red
            Number.Float: '\033[91m',  # Red
            String.Doc: '\033[92m',  # Green
            String.Double: '\033[92m',  # Green (multiline comments)
            Name: '\033[93m',  # Yellow
            Name.Builtin: '\033[95m',  # Purple
            Name.Function.Magic: '\033[95m',  # Purple ex. __init__
            Comment.Single: '\033[92m',  # Green
            Punctuation: '\033[93m',  # Yellow
        }

    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            color = self.styles.get(ttype, '\033[0m')  # Default text without color
            outfile.write(f"{color}{value}\033[0m")  # Reset to default after each token


''' format function test 
code = 'for u in range(10): print("Hello world!") \n#text \nprint(20.2) \nx=5 \n\'\'\'I love \ncoding\'\'\''
formatted_code = highlight(code, PythonLexer(), CustomFormatter())
print(formatted_code)'''


class App(tk.Tk):

    def __init__(self,master=None):
        super().__init__(master)  # again init using parent method
        #self.pack(expand=True,fill=tk.BOTH)
        self.initUI()
        self.style=ttk.Style()
        self.style.theme_use("clam")
        

    def initUI(self):
        frame1 = tk.Frame(self)
        frame1.pack(fill=ctk.BOTH, expand=True)
        
        # textpad 
        self.rightPanel = RightPanel(frame1, bg="#331e36", fg='white', font=font.Font(family='monospace', size=14), padx=5, pady=0)
        self.textline = TextLineNumbers(frame1, width=30)
        self.textline.attach(self.rightPanel.textPad)
        self.textline.pack(side='left', fill='y', before=self.rightPanel.textPad)
        self.leftPanel = LeftPanel(master=frame1,right_panel=self.rightPanel)
        self.leftPanel.pack(side='left', fill='y', before=self.textline)
        self.terminal = Terminal(frame1,height=10,background='black',foreground='white',font=font.Font(family='monospace', size=14),padx=5,
                                  pady=0,insertbackground='white',selectbackground='white',highlightthickness=0)
        self.terminal.shell = True
        self.terminal.pack(side=tk.BOTTOM, expand=True,fill=tk.BOTH,before=self.rightPanel.textPad)
        

        # TextLineNumbers

        self.rightPanel.textPad.bind("<<Change>>", self.on_change)
        self.rightPanel.textPad.bind("<Configure>", self.on_change)

    def on_change(self, event):
        self.textline.redraw()


if __name__ == '__main__':
    app = App()
    
    
    app.mainloop()
    
