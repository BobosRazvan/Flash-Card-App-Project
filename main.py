import random
from tkinter import *
import pandas as pd
import random

# -------------- UI SETUP 1  -------------------


window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50)
window.configure(bg='#8FBFA9')

canvas = Canvas(height=526, width=800)
canvas.configure(bg='#8FBFA9')

image_card_front = PhotoImage(file="images/card_front.png")
image_card_back = PhotoImage(file="images/card_back.png")
image_right = PhotoImage(file="images/right.png")
image_wrong = PhotoImage(file="images/wrong.png")


# -------------- Flip the cards  --------------------
def change_canvas():
    canvas.itemconfig(canvas_image, image=image_card_back)
    canvas.itemconfig(text1, text="English", fill="white")
    canvas.itemconfig(text2, text=current_english_word, fill="white")


window.after(3000, change_canvas)

# -------------- Create new flash Cards  --------------------

df = pd.read_csv('data/french_words.csv')

df_dict = df.to_dict('records')

first_random_index, first_random_word_dict = random.choice(list(enumerate(df_dict)))
current_french_word = first_random_word_dict['French']
current_english_word = first_random_word_dict['English']

words_to_learn = {}


def button_pressed():
    global current_french_word, current_english_word
    random_index, random_word_dict = random.choice(list(enumerate(df_dict)))
    current_french_word = random_word_dict['French']
    current_english_word = random_word_dict['English']

    canvas.itemconfig(canvas_image, image=image_card_front)
    canvas.itemconfig(text1, text="French", fill="black")
    canvas.itemconfig(text2, text=current_french_word, fill="black")
    window.after(3000, change_canvas)


def wrong_pressed():
    button_pressed()
    words_to_learn[current_french_word] = current_english_word


def right_pressed():
    button_pressed()
    global df_dict
    df_dict = [word_dict for word_dict in df_dict if word_dict['French'] != current_french_word]


def save_words_to_learn():
    df_words_to_learn = pd.DataFrame(list(words_to_learn.items()), columns=['French', 'English'])
    df_words_to_learn.to_csv('words_to_learn.csv', index=False)


# -------------- UI SETUP 2 --------------------


button_wrong = Button(window, image=image_wrong, command=wrong_pressed)
button_right = Button(window, image=image_right, command=right_pressed)

canvas_image = canvas.create_image(400, 263, image=image_card_front)
text1 = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"), fill="black")
text2 = canvas.create_text(400, 263, text=current_french_word, font=("Arial", 60, "bold"), fill="black")

canvas.grid(column=0, row=0, columnspan=2)
button_wrong.grid(column=0, row=1)
button_right.grid(column=1, row=1)

window.protocol("WM_DELETE_WINDOW", save_words_to_learn)
window.mainloop()
