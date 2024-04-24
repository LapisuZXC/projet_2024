from tkinter import *
from tkinter import messagebox, filedialog


# Фнукция для изменения темы
def change_theme(theme):
    text_fild['bg'] = view_colors[theme]['text_bg']
    text_fild['fg'] = view_colors[theme]['text_fg']
    text_fild['insertbackground'] = view_colors[theme]['cursor']
    text_fild['selectbackground'] = view_colors[theme]['selectbackground']


# Фнукция для изменения шрифта
def change_font(font):
    text_fild['font'] = fonts[font]['font']


# Фнукция для выхода из приложения
def notepad_exit():
    answer = messagebox.askokcancel('Выход', 'Вы точно хотите выйти?')
    if answer:
        root.destroy()


# Фнукция для открытия файла
def open_file():
    file_path = filedialog.askopenfilename(title='Выбор файла',
                                           filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
    if file_path:
        text_fild.delete('1.0', 'end')
        text_fild.insert('1.0', open(file_path, encoding='utf-8').read())


# Фнукция для сохранения файла
def save_file():
    file_path = filedialog.asksaveasfilename(filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
    f = open(file_path, 'w', encoding='utf-8')
    text = text_fild.get('1.0', END)
    f.write(text)
    f.close()


root = Tk() # создание окна
root.title('IDE')
root.geometry('600x700')

f_text = Frame(root) # создание области для записи текста
f_text.pack(fill=BOTH, expand=1)

main_menu = Menu(root)

# Файл
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Открыть', command=open_file)
file_menu.add_command(label='Сохранить', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Закрыть', command=notepad_exit)
root.config(menu=file_menu)

# Вид
# меню темы
view_menu = Menu(main_menu, tearoff=0)
view_menu_sub = Menu(view_menu, tearoff=0)
font_menu_sub = Menu(view_menu, tearoff=0)
view_menu_sub.add_command(label='Темная', command=lambda: change_theme('dark'))
view_menu_sub.add_command(label='Светлая', command=lambda: change_theme('light'))
view_menu.add_cascade(label='Тема', menu=view_menu_sub)

# меню шрифтов
font_menu_sub.add_command(label='Arial', command=lambda: change_font('Arial'))
font_menu_sub.add_command(label='Comic Sans MS', command=lambda: change_font('CSMS'))
font_menu_sub.add_command(label='Times New Roman', command=lambda: change_font('TNR'))
view_menu_sub.add_cascade(label='Шрифт', menu=font_menu_sub)
root.config(menu=view_menu)



# добавление списков меню
main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Вид', menu=view_menu)
root.config(menu=main_menu)

# словарь с темами
view_colors = {
    'dark': {
        'text_bg': 'black', 'text_fg': '#004A13', 'cursor': 'white',
        'selectbackground': '#EDF2B2'
    },
    'light' : {
        'text_bg': 'white', 'text_fg': 'black', 'cursor': 'black',
        'selectbackground': '#C5C5C5'
    }
}

# словарь с шрифтами
fonts = {
    'Arial': {
        'font': 'Arial 10 bold'
    },
    'CSMS': {
        'font': ('Comic Sans MS', 10, 'bold')
    },
    'TNR': {
        'font': ('Times New Roman', 10, 'bold')
    },
}


# настройки поля с текстом
text_fild = Text(f_text,
                 bg='black', # цвет фона
                 fg='#004A13', # цвет текста
                 padx=10, # отступы слева и справа
                 pady=10,
                 wrap=WORD, # перенос строки
                 insertbackground='white', # курсор
                 selectbackground='#EDF2B2', # цвет выделения текста
                 width=30,
                 font='Arial 10 bold'
                 )

text_fild.pack(expand=1, fill=BOTH, side=LEFT)

scroll = Scrollbar(f_text, command=text_fild.yview)
scroll.pack(side=LEFT, fill=Y)
text_fild.config(yscrollcommand=scroll.set)


root.mainloop()
