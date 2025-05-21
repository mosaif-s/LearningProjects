import pandas
from numpy.ma.core import filled

BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas as pd


try:
    #Converting csv to a usable item like list , so csvs are useful!
    data = pd.read_csv("data/words_to_learn.csv")
    word_list = data.to_dict(orient="records")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    word_list = data.to_dict(orient="records")

if (len(word_list) == 0):
    data = pd.read_csv("data/french_words.csv")
    word_list = data.to_dict(orient="records")

#talk abut th ebeauty of data we were given (that is csv)
index=0
def removeCurrentCard():
    print(len(word_list))
    print(index)
    word_list.remove(word_list[index])
    #To write to csv or read csv we need datafrae, thats what pandas does to list.
    data=pandas.DataFrame(word_list)
    data.to_csv("data/words_to_learn.csv", index=False)
    #print(len(word_list))
def flip_card():
    global index
    card = word_list[index-1]
    #Itemconfig use and synatx
    canvas.itemconfig(mainCard_canvas, image=backCard)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=card["English"], fill="white")


# def switchCard():
#     global index, flip_timer
#     window.after_cancel(flip_timer)
#     canvas.itemconfig(mainCard_canvas, image=frontCard)
#     if index < len(word_list):
#         card = word_list[index]
#         index += 1
#         canvas.itemconfig(card_title, text="French", fill="black")
#         canvas.itemconfig(card_word, text=card["French"], fill="black")
#         flip_timer=window.after(3000, flip_card)
#     else:
#         return
#         #messagebox.showinfo(title="Done!", message="You've gone through all the flashcards.")

def switchCard():
    global index, flip_timer
    if index >= len(word_list):
        canvas.itemconfig(card_title, text="Done!", fill="black")
        canvas.itemconfig(card_word, text="You've gone through all cards.", fill="black")
        canvas.itemconfig(mainCard_canvas, image=frontCard)
        return
    #After cancel needed here because for every switch card we need to reset or atart a nww timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(mainCard_canvas, image=frontCard)
    card = word_list[index]
    index += 1
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=card["French"], fill="black")
    #Why we cant use sleep here (idk you answer, maybe because there is a main loop running, and that would stop running, you dont want to stop running program, you want to make a callback function, if not then your card might flip before 3000 because of asynchrony ig?)
    flip_timer = window.after(3000, flip_card)

def tick():
    switchCard()
    removeCurrentCard()
def cross():
    switchCard()

#_______________________ui setup
window=Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashcard for French")
flip_timer = window.after(3000, flip_card)


canvas=Canvas(width=800,height=526)
frontCard=PhotoImage(file="images/card_front.png")
backCard=PhotoImage(file="images/card_back.png")
mainCard_canvas=canvas.create_image(400, 263, image=frontCard)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.grid(row=0,column=0, columnspan=2)

rightButtonImg = PhotoImage(file="images/right.png")
rightButton = Button(image=rightButtonImg, highlightthickness=0, command=tick)
rightButton.grid(column=1, row=1)

wrongButtonImg = PhotoImage(file="images/wrong.png")
wrongButton = Button(image=wrongButtonImg, highlightthickness=0, command=cross)
wrongButton.grid(column=0, row=1)

#write one line about toolbox whc=ich you hae for ui= label, createtexr, button(image, htihglight thinckcness, command), canvas,config, create_image



window.mainloop()
#_______________________________________________________