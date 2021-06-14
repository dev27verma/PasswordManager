from tkinter import Tk,Button,PhotoImage,Canvas,Entry,Label
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- Find Password ------------------------------------ #
def click_on_search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title=website, message=f"No details for {website} present")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def click_on_password_generator():
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)
    final_password = "".join(password_list)
    password_entry.insert(0, final_password)
    # this copy the password as clip board, this is not useful, only for learning purpose
    pyperclip.copy(final_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def click_on_add():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title=website, message="Above Entries can't be left empty!!")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the below details entered:\nwebsite: {website}\nEmail: {email}\nIs is OK to save?")
        if is_ok:
            try:
                # Reading old data
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # updating old data with new data
                data.update(new_data)
                # saving updated data
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                clear_field()
        else:
            clear_field()

# to clear the field if we click on cancel/Ok on popup box
def clear_field():
    website_entry.delete(0, END)
    password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.minsize(width=600, height=600)
window.config(padx=20, pady=20, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.config(bg="white")
website_label.grid(column=0, row=1)

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)

email_label = Label(text="Email/Username:")
email_label.config(bg="white")
email_label.grid(column=0, row=2)

email_entry = Entry(width=34)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "devmailbox27@gmail.com")

password_label = Label(text="Password:")
password_label.config(bg="white")
password_label.grid(column=0, row=3)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

search_button = Button(text="Search", bg="white", width=9, highlightthickness=0, command=click_on_search)
search_button.grid(column=2, row=1)

generate_password_button = Button(text="Generate Pass",width=9, bg="white", highlightthickness=0,
                                  command=click_on_password_generator)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=31, bg="white", highlightthickness=0, command=click_on_add)
add_button.grid(column=1, row=4, columnspan=4)

window.mainloop()
