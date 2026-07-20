# ето все используемые библиотеки
import cmd
from struct import pack
import tkinter as tk
import re
import sys
import subprocess
from unittest import result
from tkinter import ttk

# название версии (необязательно)
print("стадия разроботки indev")

# добавление понятие tk.tk
root = tk.Tk()

# словарь переводов (не используется просто многие скрипты настроены на старые переводы но тут ничего не нужно трогать)
replacements = {
#   "вывеститекст": "print",
  #  "ввод": "input",
   # "если": "if",
    #"иначе": "else",
    #"пока": "while",
#   "для": "for",
  #  "в": "in",
  #  "диапазон": "range",
  #  "истина": "True",
 #   "ложь": "False",
  #  "импортироватьбиблиотеку": "import",
#    "остановить": "quit",
  #  "импортировать": "import"
     "print": "print",
}

def translate(code):
   for ru, en in replacements.items():
       code = re.sub(rf"\b{ru}\b", en, code)
       return code


# класс для перенаправления print в Text
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)  # автопрокрутка вниз
    def flush(self):  # нужен для совместимости
        pass

# автозаполнение текста
SNIPPETS = {
    'pr': 'print()',
    'pri': 'print()',
    'prin': 'print()',
    'inp': 'input()',
    'inpu': 'input()',
    'for ': 'for # in range():',
    'if': 'if condition:',
    'if c': 'if condition:',
    'if co': 'if condition:',
    'if con': 'if condition:',
    'def': 'def function():',
    'def fu': 'def function():',
    'class': 'class ClassName:',
    'class C': 'class ClassName:',
    'imp': 'import ',
    'try': 'try:\n    pass\nexcept Exception as e:\n    print(e)',
    'wh': 'while True:',
}

def get_word_before_cursor(widget):
    """Получить слово перед курсором"""
    cursor_pos = widget.index("insert")
    line, col = cursor_pos.split('.')
    col = int(col)
    line_text = widget.get(f"{line}.0", f"{line}.end")
    word_start = col - 1
    while word_start >= 0 and (line_text[word_start].isalnum() or line_text[word_start] == '_'):
        word_start -= 1
    word = line_text[word_start + 1:col]
    return word, word_start + 1, col, line


def on_tab_pressed(event):
    """Обработчик нажатия Tab"""
    widget = event.widget
    word, start_pos, end_pos, line = get_word_before_cursor(widget)
    if word in SNIPPETS:
        widget.delete(f"{line}.{start_pos}", f"{line}.{end_pos}")
        widget.insert("insert", SNIPPETS[word])
        return "break"
    return None

def run_code():
    russian_code = text_box.get("1.0", tk.END)   # берём текст из окна
    python_code = translate(russian_code)        # переводим
    output_box.delete("1.0", tk.END)             # очищаем вывод
    try:
        exec(python_code, {"print": print})      # выполняем
    except Exception as e:
        print(f"Ошибка: {e}")

# создаём окно
root.title("IDE")
root.geometry("1280x640")
root.configure(bg="#2b2b2b") # темный фон
tk.Button(root, text="Запуск", bg="#4caf50", fg="white")

# версия в окне
version_label = tk.Label(root, text="версия indev 1.0.0", font=("Arial", 10), fg="gray")
version_label.pack(side="bottom", pady=5)

text_box = tk.Text(root, height=10, width=70, font=("Consolas", 12))
text_box.pack(pady=10)

text_box.bind("<Tab>", on_tab_pressed) # привязываем автодополнение к Tab

# кнопка запуска
run_button = tk.Button(root, text="Запустить", command=run_code, bg="green", fg="white", font=("Arial", 12))
run_button.pack(pady=5)

# поле для вывода результата
output_box = tk.Text(root, height=10, width=70, font=("Consolas", 12))
output_box.pack(pady=10)

# перенаправляем print в output_box
sys.stdout = TextRedirector(output_box)

# выбор пути в приложении
def open_file_by_path():
    path = path_entry.get()  # берём путь из поля ввода
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, content)
        print(f"Файл {path} успешно открыт и загружен.")
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")
        highlight_syntax()
    
    print("Файл успешно открыт.")

# метка для строки пути
path_label = tk.Label(root, text="Введите путь к файлу:", font=("Arial", 12))
path_label.pack(pady=5)

# поле для ввода пути к файлу
path_entry = tk.Entry(root, width=70, font=("Consolas", 12))
path_entry.pack(pady=5)

# сохранение файлов
def save_file():
    path = path_entry.get()
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_box.get("1.0", tk.END))
        print(f"Файл {path} успешно сохранён.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


# кнопка вызывающая функцию сохранение файлов в строках таких как 93 - 101
save_button = tk.Button(root, text="Сохранить файл", command=save_file, bg="orange", fg="white", font=("Arial", 12))
save_button.pack(pady=5)

# кнопка открытие файла по пути к файлу исполнение
open_button = tk.Button(root, text="открыть етот исполняемый файл по пути", command=open_file_by_path, bg="blue", fg="white", font=("Arial", 12))
open_button.pack(pady=5)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")


# вкладка редактирование 
frame_editor = tk.Frame(notebook, bg="#2b2b2b")
editor = tk.Text(frame_editor, font=("Consolas", 12), bg="#1e1e1e", fg="white")
editor.pack(expand=True, fill="both")
notebook.add(frame_editor, text="Редактор")

# menu
menu_bar = tk.Menu(root)

# Меню "Файл"
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Открыть", command=lambda: print("Открыть файл"))
file_menu.add_command(label="Сохранить", command=lambda: print("Сохранить файл"))
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)
menu_bar.add_cascade(label="Файл", menu=file_menu)

# Меню "Правка"
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Копировать", command=lambda: print("Копировать"))
edit_menu.add_command(label="Вставить", command=lambda: print("Вставить"))
edit_menu.add_command(label="Отменить", command=lambda: print("Отменить"))
menu_bar.add_cascade(label="Правка", menu=edit_menu)

# Меню "Справка"
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="О программе", command=lambda: print(
" в версии 1.0.8 была добавлена CMD которая является прототипом "
"       в версии 1.0.6-1.0.7 были исправление багов                                    "
"в версии 1.0.9 была удалена CMD из-за того что она имела              \
множество багов и мы ёе временно закрыли"))
help_menu.add_command(label="доп. информация", command=lambda: print("разроботщик - Vortex Core Labs "
                                                             "программа в стадии разроботки,         "
                                                            "программа временно имеет множество багов"))



menu_bar.add_cascade(label="Справка", menu=help_menu)

# Привязываем меню к окну
root.config(menu=menu_bar)

# ето подсвечивание символов
text_box.tag_configure("keyword", foreground="#d82222")
text_box.tag_configure("builtin", foreground="#1c84c0")

# ето автодополнение закрывающей скобки и других символов

# ето подсвечивание символов
def highlight_syntax(event=None):
    # 1. Списки слов, которые мы хотим красить (стандарт Python)
    # Можно добавлять свои слова в эти списки
    keywords = ["if", "else", "elif", "while", "for", "in", "import", "from", "return", "def", "class", "try", "except", "with", "as"]
    builtins = ["print", "input", "range", "len", "str", "int", "list", "dict", "open", "exec", "type"]

    # 2. Очищаем старую подсветку во всем окне (чтобы цвета не накладывались)
    text_box.tag_remove("keyword", "1.0", tk.END)
    text_box.tag_remove("builtin", "1.0", tk.END)

    # 3. Получаем весь текст из редактора
    content = text_box.get("1.0", tk.END)

    # 4. Магия регулярных выражений: ищем и красим keywords
    # Эта штука ищет слово целиком (\b), чтобы не покрасить "import" внутри слова "important"
    for word in keywords:
        # Ищем все совпадения слова в тексте
        for match in re.finditer(rf"\b{word}\b", content):
            # Определяем точные координаты начала и конца слова в формате Tkinter (строка.символ)
            start_index = f"1.0 + {match.start()} chars"
            end_index = f"1.0 + {match.end()} chars"
            # Накладываем оранжевый тег "keyword"
            text_box.tag_add("keyword", start_index, end_index)

    # 5. То же самое делаем для встроенных функций (красим в голубой)
    for word in builtins:
        for match in re.finditer(rf"\b{word}\b", content):
            start_index = f"1.0 + {match.start()} chars"
            end_index = f"1.0 + {match.end()} chars"
            # Накладываем голубой тег "builtin"
            text_box.tag_add("builtin", start_index, end_index)

# привязываем функцию подсветки 
text_box.pack(expand=True, fill="both")
text_box.bind("<KeyRelease>", highlight_syntax) # Проверь эту строчку!


# Notebook для вкладок
frame_editor = tk.Frame(notebook, bg="#2b2b2b")
editor = tk.Text(frame_editor, font=("Consolas", 12), bg="#1e1e1e", fg="white")
editor.pack(expand=True, fill="both")
notebook.add(frame_editor, text="Редактор")

frame_output = tk.Frame(notebook, bg="#2b2b2b")
output_box = tk.Text(frame_output, font=("Consolas", 12), bg="#1e1e1e", fg="lime")
output_box.pack(expand=True, fill="both")
notebook.add(frame_output, text="Вывод")

root.mainloop()