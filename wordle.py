#imports
from tkinter import messagebox                              
from tkinter import simpledialog
import random
from nltk.corpus import wordnet as wn
from difflib import SequenceMatcher
from tkinter import *


def focus_next_widget(event):
    #for moving automatically to the next text box
    event.widget.tk_focusNext().focus()
    return("break")

def Restrict(e=None):
    #restricts the user to enter only 1 alphabet to one textbox
    string=e.widget.get("1.0","end-1c")
    if len(string)==0:
        focus_next_widget(e)

def focus_back(event):
    #for moving automatically to the previous text box
    event.widget.tk_focusPrev().focus()
    event.widget.focus_get().delete("1.0","end-1c")
    return("break")

def get_word(wordle,n):
    #gets score and accuracy by matching words
    global count,score,accuracy
    score=score-150
    count=count+1
    string=""
    for i in range(n):
        string=string+globals()[f't{count}{i}'].get("1.0","end-1c")
        globals()[f't{count}{i}'].config(state=DISABLED)
        if count<n:
            globals()[f't{count+1}{i}'].config(state="normal")
            globals()[f't{count+1}{0}'].focus_set()
    print(string)
    sm=SequenceMatcher(None,string,wordle)
    score=int(score+sm.ratio()*100)
    #print(sm.ratio())
    
    accuracy=round((accuracy+sm.ratio()*100)/(count+1),2)
    color2(wordle,string,count,n)

def wordlist(n):
    #creates a wordlist of a specified letter count
    words=[w for w in wn.words() if len(w)==n]
    global wordle
    wordle=random.choice(words)
    print(wordle)
    for i in wordle:
        if wordle.count(i)>1 or i.isdigit() or i=="_":
            wordle=wordlist(n)
    else:
        return wordle

def on_click(title,msg):
    #message box
    messagebox.showinfo(title,msg)

def color2(wordle,guess,count,n):
    #coloring of tiles by sequence matching
    if guess==wordle:
        for i in range(n):
            globals()[f't{count}{i}'].config(bg="#538d4e")
        print("\nYou win!")
        on_click("You win","You win\nYour score is: "+str(score)+"\nYour accuracy is: "+str(accuracy)+f"\n {wordle.upper()} means {wn.synsets(wordle)[0].definition()}")
    else:
        for i in range(n):
            if guess[i]==wordle[i]:
                globals()[f't{count}{i}'].config(bg="#538d4e")

            elif guess[i] in wordle:
                if guess[i]==globals()[f't{count}{i}'].get("1.0","end-1c"):
                    globals()[f't{count}{i}'].config(bg="#b59f3b")
                
            else:
                globals()[f't{count}{i}'].config(bg="#292929")
        if count==n:
            on_click("You lose",f"\nThe word was {wordle.upper()} !!\n It means {wn.synsets(wordle)[0].definition()}\nYour Score:{score}\nYour Accuracy:{accuracy}")     

def initiliaze():
    #initializing the game
    global n,score,count,accuracy
    root = Tk()
    root.title("WORDLE")
    root.configure(background='black')
    root.iconphoto(False, PhotoImage(file="logo1.png"))
    n= simpledialog.askinteger("WORDLE","Enter the number of letters in the word:",parent=root,minvalue=4,maxvalue=9)
    wordle=wordlist(n)
    score=n*200
    accuracy=0
    count=-1
    for i in range(n+1):
        for j in range(n):

            globals()[f't{i}{j}']=Text(wrap="none",width=4,height=2,background="black",foreground='#ffffff',font=('Segoe UI',18),padx=5,pady=5)
            globals()[f't{i}{j}'].grid(row=i,column=j)
            globals()[f't{i}{j}'].bind("<Tab>",focus_next_widget)
            globals()[f't{i}{j}'].bind("<Key>",Restrict)
            globals()[f't{i}{j}'].bind("<BackSpace>",focus_back)
            globals()[f't{i}{j}'].insert(END,"")
            if i >=1:
                globals()[f't{i}{j}'].config(state=DISABLED)
        
    b=Button(root,text="Enter",command=lambda: get_word(wordle,n),background="#292929",foreground='#ffffff',font=('Segoe UI',10),padx=8,pady=8)
    b.grid(row=n+4,column=n-1,columnspan=2)
    b.bind("<Return>",lambda event: get_word(wordle,n))
    b.bind("<BackSpace>",focus_back)

    l=Label(root,text="WORDLE",font=("Arial",30),bg="black",fg="white").grid(row=n+3,column=0,columnspan=n)
    root.mainloop()
    return n

if __name__=="__main__":
    #main
    n=initiliaze()
   

