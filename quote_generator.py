import tkinter as tk
from tkinter import messagebox
import json
import random
import os

# Создаём функции
def load_quotes():
    # Загрузка коллекции цитат
    try:
        with open("quotes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файла нет или он повреждён — возвращаем встроенный список
        return [
            {"text": "Человек есть тайна. Её надо разгадать, и ежели будешь её разгадывать всю жизнь, то не говори, что потерял время.", "author": "Ф.М. Достоевский", "theme": "жизнь"},
            {"text": "Делай, что должно, и будь что будет.", "author": "Л.Н. Толстой", "theme": "мотивация"},
            {"text": "Светить всегда, светить везде, до дней последних донца, светить — и никаких гвоздей!", "author": "В.В. Маяковский", "theme": "вдохновение"},
            {"text": "Человек — это звучит гордо.", "author": "М. Горький", "theme": "самоценность"},
            {"text": "Идеального времени не существует. Есть только время, и ты должен использовать его наилучшим образом.", "author": "Харуки Мураками", "theme": "время"},
            {"text": "Будь собой, прочие роли уже заняты.", "author": "Оскар Уайльд", "theme": "индивидуальность"},
            {"text": "Воображение важнее, чем знания.", "author": "Альберт Эйнштейн", "theme": "творчество"},
        ]

def save_quotes(quotes):
    # Сохранение коллекции цитат в JSON
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

def load_history():
    # Загрузка истории показанных цитат
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    # Сохранение истории в JSON
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def add_quote():
    # Добавление новой цитаты с проверкой на пустые поля
    text = entry_text.get().strip()
    author = entry_author.get().strip()
    theme = entry_theme.get().strip()
    if not text or not author or not theme:
        messagebox.showwarning("Ошибка", "Все поля (текст, автор, тема) должны быть заполнены")
        return
    quotes = load_quotes()
    quotes.append({"text": text, "author": author, "theme": theme})
    save_quotes(quotes)
    # Очищаем поля ввода
    entry_text.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_theme.delete(0, tk.END)

def generate_quote():
    # Случайная цитата из коллекции, запись в историю
    quotes = load_quotes()
    if not quotes:
        messagebox.showwarning("Ошибка", "Коллекция цитат пуста")
        return
    quote = random.choice(quotes)
    history = load_history()
    history.append(quote)
    save_history(history)
    update_history_view()

def update_history_view():
    # Отображение истории с учётом фильтров
    filter_author = entry_filter_author.get().strip().lower()
    filter_theme = entry_filter_theme.get().strip().lower()
    history = load_history()
    filtered = []
    for q in history:
        if filter_author and filter_author not in q["author"].lower():
            continue
        if filter_theme and filter_theme not in q["theme"].lower():
            continue
        filtered.append(q)
    listbox_history.delete(0, tk.END)
    for q in filtered:
        listbox_history.insert(tk.END, f"«{q['text']}» — {q['author']} [{q['theme']}]")

def reset_filter():
    # Сброс фильтров и показ всей истории
    entry_filter_author.delete(0, tk.END)
    entry_filter_theme.delete(0, tk.END)
    update_history_view()

# Создаём интерфейс
window = tk.Tk()
window.title("Генератор случайных цитат")
window.geometry("1000x700")
window.resizable(False, False)
window.config(bg="lightgrey")

# Верхний фрейм (добавление цитат)
input_frame = tk.Frame(window, bg="lightgrey", bd=5)
input_frame.pack(side="top", fill="x", padx=10, pady=10)
# Текст цитаты
label_text = tk.Label(input_frame, text="Текст:", bg="lightgrey")
label_text.grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_text = tk.Entry(input_frame, width=70)  # чуть шире поле ввода
entry_text.grid(row=0, column=1, padx=5, pady=2)

# Автор
label_author = tk.Label(input_frame, text="Автор:", bg="lightgrey")
label_author.grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_author = tk.Entry(input_frame, width=70)
entry_author.grid(row=1, column=1, padx=5, pady=2)

# Тема
label_theme = tk.Label(input_frame, text="Тема:", bg="lightgrey")
label_theme.grid(row=2, column=0, sticky="w", padx=5, pady=2)
entry_theme = tk.Entry(input_frame, width=70)
entry_theme.grid(row=2, column=1, padx=5, pady=2)

# Кнопка добавления цитаты
btn_add = tk.Button(window, text="Добавить цитату", command=add_quote, bg="white")
btn_add.pack(pady=5)

# Кнопка генерации случайной цитаты
btn_generate = tk.Button(window, text="Сгенерировать случайную цитату", command=generate_quote, bg="white", font=("Arial", 10, "bold"))
btn_generate.pack(pady=10)

# Фрейм для фильтров
filter_frame = tk.Frame(window, bg="lightgrey")
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Автор:", bg="lightgrey").grid(row=0, column=0, padx=5)
entry_filter_author = tk.Entry(filter_frame, width=30)
entry_filter_author.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Тема:", bg="lightgrey").grid(row=0, column=2, padx=5)
entry_filter_theme = tk.Entry(filter_frame, width=30)
entry_filter_theme.grid(row=0, column=3, padx=5)

btn_apply = tk.Button(filter_frame, text="Фильтровать", command=update_history_view, bg="white")
btn_apply.grid(row=0, column=4, padx=5)

btn_reset = tk.Button(filter_frame, text="Сбросить", command=reset_filter, bg="white")
btn_reset.grid(row=0, column=5, padx=5)

# Список истории
listbox_history = tk.Listbox(window, width=150, height=20, bg="white")
listbox_history.pack(pady=10)

# Инициализация файлов при первом запуске
if not os.path.exists("quotes.json"):
    save_quotes(load_quotes())
if not os.path.exists("history.json"):
    save_history([])

# Показываем историю (с учётом пустых фильтров)
update_history_view()

window.mainloop()