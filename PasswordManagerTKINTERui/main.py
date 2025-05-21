from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
#I DIDNT STORE MY REAL PASSWORDS HERE
def search_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Not Found", message="No data file found.")
    bool=False
    for k,v in data.items(): #note here cuz
        if k==website:
            bool=True
            email = v["email"]
            password = v["password"] #note here cuz
            messagebox.showinfo(title="Password Found!", message=f"Email: {email}\n Password: {password}\n")
    if bool==False:
        messagebox.showerror(title="Not Found", message="No matching data found.")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def storeData():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if (len(website)==0 or len(email)==0 or len(password)==0):
        messagebox.showerror(title="Error", message="Fields cannot be empty!")
    else:
        # is_ok=messagebox.askokcancel(title="Confirm Entries", message=f"Please confirm the entries \n Website: {website} \n Email: {email} \n Do you confirm?" )
        # if is_ok:
        #     with open("data.txt","a") as f:
        #         f.write(f"|   {website}   |   {email}   |   {password}   |\n")
        try:
            with open("data.json", "r") as data_file:
                data=json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0,END)
            password_entry.delete(0,END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


canvas = Canvas(width=200, height=200, highlightthickness=0)

# args and kwargs are paures, caus enow if you have used args how do you tell ki AB STOP!

#Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#Buttons
search_password_button = Button(text="Search",width=16,  command=search_password)
search_password_button.grid(column=2, row=1)

generate_password_button = Button(text="  Generate Password  ", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", highlightthickness=0, width=39, command=storeData)
add_button.grid(column=1, row=4, columnspan=2)

#Entries
website_entry=Entry(width=20)
website_entry.focus()
website_entry.grid(row=1, column=1)
email_entry=Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(END, "mosaif.shaikh20@gmail.com")
password_entry=Entry(width=20)
password_entry.grid(row=3, column=1)
window.mainloop()