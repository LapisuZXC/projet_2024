from tkinter import *

def change_theme(theme):
    text_fild['bg'] = view_colors[theme]['text_bg']
    text_fild['fg'] = view_colors[theme]['text_fg']
    text_fild['insertbackground'] = view_colors[theme]['cursor']
    text_fild['selectbackground'] = view_colors[theme]['selectbackground']

def change_font(font):
    text_fild['font'] = fonts[font]['font']

def notepad_exit():



root = Tk() # создание окна
root.title('IDE')
root.geometry('600x700')

f_text = Frame(root) # создание области для записи текста
f_text.pack(fill=BOTH, expand=1)

main_menu = Menu(root)

# Файл
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Открыть')
file_menu.add_command(label='Сохранить')
file_menu.add_separator()
file_menu.add_command(label='Закрыть')
root.config(menu=file_menu)

# Вид
view_menu = Menu(main_menu, tearoff=0)
view_menu_sub = Menu(view_menu, tearoff=0)
font_menu_sub = Menu(view_menu, tearoff=0)
view_menu_sub.add_command(label='Темная', command=lambda: change_theme('dark'))
view_menu_sub.add_command(label='Светлая', command=lambda: change_theme('light'))
view_menu.add_cascade(label='Тема', menu=view_menu_sub)

font_menu_sub.add_command(label='Arial', command=lambda: change_font('Arial'))
font_menu_sub.add_command(label='Comic Sans MS', command=lambda: change_font('CSMS'))
font_menu_sub.add_command(label='Times New Roman', command=lambda: change_font('TNR'))
view_menu_sub.add_cascade(label='Шрифт', menu=font_menu_sub)
root.config(menu=view_menu)



# добавление списков меню
main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Вид', menu=view_menu)
root.config(menu=main_menu)

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