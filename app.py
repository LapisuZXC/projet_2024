import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from tkinter import font
from tkterminal import Terminal
import keyword
import platform
import os
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Whitespace, Punctuation, Other, Literal, Text
from pygments.formatter import Formatter
from pygments import highlight, lex
from pygments.lexers import PythonLexer


class UpperPanel(tk.Frame):

    def __init__(self, master=None, right_panel=None, *args, **kwargs):
        super().__init__(master)
        self.right_panel = right_panel
        self.initUI(master, *args, **kwargs)

    def initUI(self, master, *args, **kwargs):
        self.frame = tk.Frame(master, height=25)
        self.save_b = ctk.CTkButton(self.frame, fg_color="gray", corner_radius=0, width=55, text="save",
                                    command=lambda: self.right_panel.saveFile())
        self.open_b = ctk.CTkButton(self.frame, fg_color="gray", corner_radius=0, width=55, text="open",
                                    command=lambda: self.right_panel.openFile())
        self.new_b = ctk.CTkButton(self.frame, fg_color="gray", corner_radius=0, width=55, text="new",
                                   command=lambda: self.right_panel.newFile())
        # Create a CTkMenuBar widget
        self.new_b.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        self.open_b.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        self.save_b.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        self.frame.pack(expand=False, fill=ctk.BOTH, anchor='n', side=tk.TOP, before=self.right_panel.textPad)

    def attach(self, text_widget):
        self.textwidget = text_widget


class LeftPanel(tk.Frame):
    def __init__(self, master=None, right_panel=None):
        super().__init__(master)
        self.right_panel = right_panel
        self.selected_dir = self.right_panel.selected_dir
        self.initUI(master)

    def initUI(self, master):
        self.file_path = tk.StringVar(master, self.right_panel.selected_dir)
        self.selected_dir = os.path.dirname(self.file_path.get())
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

        self.file_path.trace("w", self.update_file_list(self.file_path))

        self.file_list.pack(expand=True, fill=tk.BOTH)

        self.file_list.bind("<<ListboxSelect>>", self.on_file_select)

    def update_file_list(self, file_path):
        bufer = file_path.get()
        print(bufer)
        if bufer != '':
            self.file_list.delete(0, tk.END)
            for i in os.listdir(bufer):
                self.file_list.insert(tk.END, i)
            print('zhopa')

    def on_file_select(self, event):
        selection = self.file_list.curselection()
        if selection:
            selected_index = selection[0]
            selected_item = self.file_list.get(selected_index)
            self.breadcrumb.set(f"File / {selected_item}")

            # Устанавливаем выбранный файл в правой панели
            self.right_panel.selected_file = os.path.join(self.selected_dir, selected_item)
            self.right_panel.update_text_from_file()


class RightPanel(tk.Frame):
    def __init__(self, master=None, left_panel=None, *args, **kwargs):
        super().__init__(master)
        self.master = master
        self.selected_file = ""  # Initialize selected file
        self.selected_dir = tk.StringVar(self, "")  # Initialize selected directory
        self.initUI(master, *args, **kwargs)
        self.file_list = []

    def initUI(self, master, *args, **kwargs):
        self.textPad = TextPad(master, *args, **kwargs)  # Само поле где пишется текст
        self.textPad.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.tools = UpperPanel(master, self, *args, **kwargs)  # Тут кнопочки всякие
        self.tools.attach(master)  # ?

    def on_selected_file_change(self, *args):
        if self.selected_file:
            self.selected_dir = os.path.dirname(self.selected_file)

    def newFile(self):
        self.textPad.delete('1.0', 'end')

    def saveFile(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.textPad.get('1.0', 'end'))

    def openFile(self):
        file_path = filedialog.askopenfilename(title='Выбор файла',
                                               filetypes=(
                                                   ('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        if file_path:
            self.selected_file = file_path
            self.textPad.delete('1.0', 'end')
            self.textPad.insert('1.0', open(file_path, encoding='utf-8').read())
            self.selected_dir = os.path.dirname(file_path)

    def update_text_from_file(self):
        if self.selected_file:
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                self.textPad.delete('1.0', tk.END)  # Очищаем текстовое поле
                self.textPad.insert(tk.END, file.read())


class TextLineNumbers(ctk.CTkCanvas):
    def __init__(self, *args, **kwargs):
        ctk.CTkCanvas.__init__(self, *args, **kwargs)  # init using parent class initialisation
        self.textwidget = None
        self.configure(bg="#0e003f")
        self.fontSize = 12
        self.configFont()
        self.text_color = "black"

    def configFont(self):  # dont know if needed tbh
        system = platform.system().lower()
        if system == "windows":
            self.font = font.Font(family='monospace', size=self.fontSize)
        elif system == "linux":
            self.font = font.Font(family='monospace', size=self.fontSize)

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete('all')
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(1,y,anchor="nw", font=self.font,text = linenum, fill = "#600061")
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
        self.bind('<KeyRelease>', self.highlight, add='+')

    def highlight(self, event=None, lineNumber=None):
        index = self.index(tk.INSERT).split(".")
        line_no = int(index[0])
        if lineNumber is None:
            line_text = self.get("%d.%d" % (line_no, 0), "%d.end" % (line_no))
            self.mark_set("range_start", str(line_no) + '.0')

        elif lineNumber is not None:
            line_text = self.get("%d.%d" % (lineNumber, 0), "%d.end" % (lineNumber))
            self.mark_set("range_start", str(lineNumber) + '.0')

        for token, content in lex(line_text, PythonLexer()):
            self.tag_configure("Token.Name", foreground="#FFFFFF")
            self.tag_configure("Token.Text", foreground="#FFFFFF")

            self.tag_configure("Token.Keyword", foreground="#CC7A00")
            self.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
            self.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
            self.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
            self.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
            self.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
            self.tag_configure("Token.Keyword.Type", foreground="#CC7A00")

            self.tag_configure("Token.Punctuation", foreground="#2d991d")

            self.tag_configure("Token.Name.Class", foreground="#ddd313")
            self.tag_configure("Token.Name.Exception", foreground="#ddd313")
            self.tag_configure("Token.Name.Function", foreground="#298fb5")
            self.tag_configure("Token.Name.Function.Magic", foreground="#298fb5")
            self.tag_configure("Token.Name.Decorator", foreground="#298fb5")

            self.tag_configure("Token.Name.Builtin", foreground="#CC7A00")
            self.tag_configure("Token.Name.Builtin.Pseudo", foreground="#CC7A00")

            self.tag_configure("Token.Operator.Word", foreground="#CC7A00")
            self.tag_configure("Token.Operator", foreground="#FF0000")

            self.tag_configure("Token.Comment", foreground="#767d87")
            self.tag_configure("Token.Comment.Single", foreground="#767d87")
            self.tag_configure("Token.Comment.Double", foreground="#767d87")

            self.tag_configure("Token.Literal.Number.Integer", foreground="#88daea")
            self.tag_configure("Token.Literal.Number.Float", foreground="#88daea")
            #
            self.tag_configure("Token.Literal.String.Single", foreground="#35c666")
            self.tag_configure("Token.Literal.String.Double", foreground="#35c666")

            self.mark_set("range_end", "range_start + %dc" % len(content))
            self.tag_add(str(token), "range_start", "range_end")
            self.mark_set("range_start", "range_end")

    def highlightall(self, linesInFile, overlord, event=None):

        code = self.get("1.0", "end-1c")
        i = 1
        for line in code.splitlines():
            self.index("%d.0" % i)
            self.highlight(lineNumber=i)
            percent = i / linesInFile * 100
            percent = round(percent, 2)
            overlord.title('Loading ... ' + str(percent) + ' %')
            i += 1


class App(tk.Tk):

    def __init__(self, master=None):
        super().__init__(master)  # again init using parent method
        # self.pack(expand=True,fill=tk.BOTH)
        self.initUI()
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def initUI(self):
        frame1 = tk.Frame(self, bg="#000000")
        frame1.pack(fill=ctk.BOTH, expand=True)

        # textpad
        self.rightPanel = RightPanel(frame1, bg="#331e36", fg='white', font=font.Font(family='monospace', size=14),
                                     padx=5, pady=0)
        self.textline = TextLineNumbers(frame1, width=30)
        self.textline.attach(self.rightPanel.textPad)
        self.textline.pack(side='left', fill='y', before=self.rightPanel.textPad)
        self.leftPanel = LeftPanel(master=frame1, right_panel=self.rightPanel)
        self.leftPanel.pack(side='left', fill='y', before=self.textline)
        self.terminal = Terminal(frame1, height=10,background='#000000',foreground='#00FF00', font=font.Font(family='monospace', size=14), padx=5,
                                  pady=0, insertbackground='#FFFFFF', selectbackground='#FFFFFF', highlightthickness=0)
        self.terminal.shell = True
        self.terminal.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, before=self.rightPanel.textPad)

        # TextLineNumbers

        self.rightPanel.textPad.bind("<<Change>>", self.on_change)
        self.rightPanel.textPad.bind("<Configure>", self.on_change)

    def on_change(self, event):
        self.textline.redraw()
        self.rightPanel.textPad.highlightall(len(self.rightPanel.textPad.get('1.0', 'end-1c').splitlines()), self)


if __name__ == '__main__':
    app = App()

    app.mainloop()
