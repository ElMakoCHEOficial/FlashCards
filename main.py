from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
mem_time=3000
text="English,Spanish,French,Italian,Portuguese,Greek,German,Norwegian,Dutch,Finnish,Swedish,Estonian,Croatian,Irish,Polish,Russian,Ukrainian,Hindi,Armenian,Japanese,Korean,Chinese,Arabic"
LL=text.split(",")
# print(LL)
mode_="ISO-8859-1"
try:
    data = pandas.read_csv("data/words_to_learn.csv", encoding=mode_)
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv", encoding=mode_)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
from_=LL[0] # whatever
# from_=random.choice(LL)  # Random     
to_=LL[1] # spanski/ anglais

fs=32
tfs=30
font="Times New Roman"
def next_card():
    global to_learn, current_card, flip_timer
    if len(to_learn) > 0:
        window.after_cancel(flip_timer)
        current_card = random.choice(to_learn)
        canvas.itemconfig(card_title, text=from_, fill="black")
        canvas.itemconfig(card_word, text=current_card[from_], fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        flip_timer = window.after(mem_time, func=flip_card)
    else:
        print("Ganaste / You won / Tu as gagné")
        player = input("Name: ")
        canvas.itemconfig(card_title, text="The End", fill="white")
        canvas.itemconfig(card_word, text="I see the player you mean\n" + str(player), fill="white")
        canvas.itemconfig(card_background, image=card_back_img)        
        original_data = pandas.read_csv("data/french_words.csv", encoding=mode_)
        to_learn = original_data.to_dict(orient="records")
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False, encoding=mode_)
        window.after(2000, next_card)
def flip_card():
    canvas.itemconfig(card_title, text=to_, fill="white")
    canvas.itemconfig(card_word, text=current_card[to_], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False,encoding=mode_)
    # data = pandas.DataFrame(to_learn)
    # data.to_csv("data/words_to_learn.csv", index=False,encoding=mode_)
    next_card()

window = Tk()
window.title("Flashy")  
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=(font, tfs, "italic"))
card_word = canvas.create_text(400, 263, text="", font=(font, fs, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)
next_card()
window.mainloop()
print(len(to_learn))