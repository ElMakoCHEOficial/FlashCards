from tkinter import *
import pandas
import random
backgColor = "#B1DDC5"
curr_card = {}
W_to_learn = {}
mem_time=3_000
LangDict={"0":"English","1":"Spanish","2":"French","3":"Italian",
          "4":"Portuguese","5":"Greek","6":"German","7":"Norwegian","8":"Dutch",
          "9":"Finnish","9":"Swedish"}
languages="English,Spanish,French,Italian,Portuguese,Greek,German,Norwegian,Dutch,Finnish,Swedish"
# ,Estonian,Croatian,Irish,Polish,Russian,Ukrainian,Hindi,Armenian,Japanese,Korean,Chinese,Arabic
LangList=languages.split(",")
font="Times New Roman"
mode_="ISO-8859-1"
fontSize=28
titleFontSize=32
randomC=False
try:
    data = pandas.read_csv("data/words_to_learn.csv", encoding=mode_)
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv", encoding=mode_)
    W_to_learn = original_data.to_dict(orient="records")
    # print("Initializing...")
else:
    W_to_learn = data.to_dict(orient="records")
from_=LangList[2] # From lang
to_=LangList[1] # To lang
from_=LangDict["0"]
to_=LangDict["1"]

if (randomC):# Random lang
    from_=random.choice(LangList)       
def next_card():
    global W_to_learn, curr_card, flip_timer
    if len(W_to_learn) > 0:
        window.after_cancel(flip_timer)
        curr_card = random.choice(W_to_learn)
        canvas.itemconfig(card_title, text=from_, fill="black")
        canvas.itemconfig(card_word, text=curr_card[from_], fill="black")
        canvas.itemconfig(leftWordsLabel, fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        canvas.itemconfig(leftWordsLabel, text=f"Left: {len(W_to_learn)}")        
        flip_timer = window.after(mem_time, func=flip_card)
    else:
        print("Ganaste / You won / Tu as gagné")
        # player = input("Name: ")
        canvas.itemconfig(card_title, text="The End", fill="white")
        canvas.itemconfig(card_word, text="I see the player you mean\n", fill="white")        
        canvas.itemconfig(card_background, image=card_back_img)        
        original_data = pandas.read_csv("data/french_words.csv", encoding=mode_)
        W_to_learn = original_data.to_dict(orient="records")
        data = pandas.DataFrame(W_to_learn)
        data.to_csv("data/words_to_learn.csv", index=False, encoding=mode_)
        window.after(20000, next_card)
def flip_card():
    canvas.itemconfig(card_title, text=to_, fill="white")
    canvas.itemconfig(card_word, text=curr_card[to_], fill="white")
    canvas.itemconfig(leftWordsLabel, fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
def is_known():
    W_to_learn.remove(curr_card)
    data = pandas.DataFrame(W_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False,encoding=mode_)
    next_card()
window = Tk()
window.title("Languages Flash Card Game")  
window.config(padx=50, pady=50, bg=backgColor)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=(font, titleFontSize, "italic"))
card_word = canvas.create_text(400, 263, text="", font=(font, fontSize, "bold"))
leftWordsLabel = canvas.create_text(620, 463, text=f"Left: {len(W_to_learn)}", font=(font, fontSize, "bold"))
canvas.config(bg=backgColor, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)
next_card()
window.mainloop()