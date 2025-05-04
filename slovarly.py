import customtkinter
import random as rnd

slovar = []

try:
    with open('slovarly.txt', 'r', encoding='utf-8') as f:
        slovar = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    with open('slovarly.txt', 'w', encoding='utf-8') as f:
        pass

app = customtkinter.CTk()
app.title("Словарли")
app.geometry("600x250")


def parse_slovo(slovo_with_definition):
    parts = slovo_with_definition.split(" - ", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return slovo_with_definition.strip(), ""


def new_slovo():
    new_window = customtkinter.CTkToplevel(app)
    new_window.title("Добавить слово")
    new_window.geometry("400x200")

    customtkinter.CTkLabel(new_window, text="Слово:").grid(row=0, column=0, padx=10, pady=5)
    slovo_entry = customtkinter.CTkEntry(new_window)
    slovo_entry.grid(row=0, column=1, padx=10, pady=5)

    customtkinter.CTkLabel(new_window, text="Определение:").grid(row=1, column=0, padx=10, pady=5)
    opredelenie_entry = customtkinter.CTkEntry(new_window)
    opredelenie_entry.grid(row=1, column=1, padx=10, pady=5)

    def save_slovo():
        slovo = slovo_entry.get().strip()
        opredelenie = opredelenie_entry.get().strip()
        if slovo and opredelenie:
            with open('slovarly.txt', 'a', encoding='utf-8') as f:
                entry = f"{slovo} - {opredelenie}\n"
                f.write(entry)
                slovar.append(entry)
            new_window.destroy()

    customtkinter.CTkButton(new_window, text="Сохранить", command=save_slovo).grid(row=2, column=0, columnspan=2,pady=10)


def show_word_quiz(title, num_questions=1):
    if not slovar:
        error_window = customtkinter.CTkToplevel(app)
        error_window.title("Ошибка")
        error_window.geometry("300x100")
        customtkinter.CTkLabel(error_window, text="Словарь пуст! Добавьте слова сначала.").pack(pady=20)
        return

    quiz_window = customtkinter.CTkToplevel(app)
    quiz_window.title(title)
    quiz_window.geometry('400x250')

    current_question = 0
    score = 0
    questions = rnd.sample(slovar, min(num_questions, len(slovar)))

    def show_question():
        nonlocal current_question
        if current_question >= len(questions):
            result_label.configure(text=f"Тест завершен!\nПравильных ответов: {score}/{len(questions)}",
                                   text_color="green")
            check_button.configure(state="disabled")
            strok.configure(state="disabled")
            return

        nonlocal slovo, definition
        slovo, definition = parse_slovo(questions[current_question])
        definition_label.configure(text=f"Определение:\n{definition}")
        strok.delete(0, 'end')
        result_label.configure(text="")

    slovo, definition = "", ""
    definition_label = customtkinter.CTkLabel(quiz_window, text="", wraplength=380)
    definition_label.pack(padx=10, pady=10)

    customtkinter.CTkLabel(quiz_window, text='Введите слово:').pack()
    strok = customtkinter.CTkEntry(quiz_window)
    strok.pack(pady=5)

    result_label = customtkinter.CTkLabel(quiz_window, text="")
    result_label.pack(pady=5)

    def check_answer():
        nonlocal current_question, score
        enter_otvet = strok.get().strip().lower()
        if enter_otvet == slovo.lower():
            result_label.configure(text="Правильно!", text_color="green")
            score += 1
        else:
            result_label.configure(text=f"Неправильно! Правильный ответ: {slovo}", text_color="red")

        current_question += 1
        quiz_window.after(1500, show_question)

    check_button = customtkinter.CTkButton(quiz_window, text='Проверить', command=check_answer)
    check_button.pack(pady=5)

    show_question()


def slovodnya():
    show_word_quiz("Слово дня")


def dificult():
    diff_window = customtkinter.CTkToplevel(app)
    diff_window.title('Выберите сложность')
    diff_window.geometry('400x200')

    customtkinter.CTkButton(diff_window, text="Легко\n5 вопросов",
                            command=lambda: show_word_quiz("Легкий тест", 5)).grid(row=0, column=0, padx=30, pady=50)
    customtkinter.CTkButton(diff_window, text="Сложно\n10 вопросов",
                            command=lambda: show_word_quiz("Сложный тест", 10)).grid(row=0, column=1, padx=30, pady=50)


customtkinter.CTkButton(app, text="Добавить слово", command=new_slovo).grid(row=0, column=0, padx=30, pady=50)
customtkinter.CTkButton(app, text="Слово дня", command=slovodnya).grid(row=0, column=1, padx=30, pady=50)
customtkinter.CTkButton(app, text="Тест", command=dificult).grid(row=0, column=2, padx=30, pady=50)

app.mainloop()