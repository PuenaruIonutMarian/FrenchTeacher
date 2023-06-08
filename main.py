from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    #orient records arange the 2 rows of dictionaries. each word with his dictionary


# -------------- Flash Cards --------------- #
def next_card():
    """ Functia asta alege cuvintele aleatoriu si le imprima pe card """
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(card_img, image=front_image_background)
    flip_timer = window.after(3000, func=flip_card)
    # flip_timer with window after cancel start the recount once i choose validate or cancel



# ------------- Flip the Cards -------------- #
def flip_card():
    """ Functia asta intoarce cardul """
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(card_img, image=back_image_background)


# -------------- Save Progress -------------- #
def is_known():
    if current_card in to_learn:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        next_card()
        # index needs to be false otherwise it will be on each iteration


# ----------- User Interface --------------- #
window = Tk()
window.title("French to English Dictionary")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
front_image_background = PhotoImage(file="images/card_front.png")
back_image_background = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 263, image=front_image_background)

title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

first_image = PhotoImage(file="images/right.png")
right_button = Button(image=first_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

my_second_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=my_second_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
