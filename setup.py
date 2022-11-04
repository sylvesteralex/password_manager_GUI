import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os


class PasswordManager:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 200, 200
        self.MAIN_BACKGROUND = "white"

        self.window = tk.Tk()
        self.window.minsize(self.WIDTH, self.HEIGHT)
        self.window.title("Password manager")
        self.window.config(padx=20, pady=20, bg=self.MAIN_BACKGROUND)

        self.canvas = tk.Canvas(width=self.WIDTH, height=self.HEIGHT, bg=self.MAIN_BACKGROUND, highlightthickness=0)
        self.lock_img = tk.PhotoImage(file="logo.png")
        self.canvas.create_image(self.WIDTH/2, self.HEIGHT/2, image=self.lock_img)
        self.canvas.grid(column=1, row=0)

        self.website_lbl = tk.Label(text="Website:", bg=self.MAIN_BACKGROUND)
        self.website_lbl.grid(column=0, row=1)
        self.website_input = tk.Entry()
        self.website_input.focus()
        self.website_input.grid(column=1, row=1, sticky="we")

        self.username_lbl = tk.Label(text="Email/Username:", bg=self.MAIN_BACKGROUND)
        self.username_lbl.grid(column=0, row=2)
        self.username_input = tk.Entry()
        self.username_input.insert(0, "email@email.pl")
        self.username_input.grid(column=1, row=2, sticky="we")

        self.password_lbl = tk.Label(text="Password:", bg=self.MAIN_BACKGROUND)
        self.password_lbl.grid(column=0, row=3)
        self.password_input = tk.Entry()
        self.password_input.grid(column=1, row=3, sticky="we")

        self.search_btn = tk.Button(text="Search", command=lambda: search_data(self))
        self.search_btn.grid(column=2, row=1, sticky="we")

        self.gen_pass_btn = tk.Button(text="Generate Password", command=lambda: generate_password(self))
        self.gen_pass_btn.grid(column=2, row=3)

        self.add_btn = tk.Button(text="Add", command=lambda: add_to_file(self))
        self.add_btn.grid(column=1, row=4, columnspan=2, sticky="we")

        # window.grid_columnconfigure(0, weight=1)
        # window.mainloop()

        # ==================== PASSWORD GENERATOR ====================
        def generate_password(cls):
            def random_character():
                letters = random.choice(string.ascii_letters)
                digits = random.choice(string.digits)
                special = random.choice(string.punctuation)
                char = random.choice([letters, digits, special])
                return char

            password = "".join([random_character() for _ in range(9)])
            self.password_input.delete(0, "end")
            self.password_input.insert(0, f"{password}")
            save_to_clipboard(self)

        # ==================== SAVE PASSWORD ====================
        # save to clipboard
        def save_to_clipboard(cls):
            clipboard = tk.Tk()
            clipboard.withdraw()
            clipboard.clipboard_clear()
            clipboard_pass = self.password_input.get()
            clipboard.clipboard_append(clipboard_pass)
            clipboard.update()  # now it stays on the clipboard after the window is closed
            clipboard.destroy()

        # create dataframe
        def save_to_dict(website, username, password):
            pass_data = {
                website: {
                    "username": username,
                    "password": password,
                }
            }

            return pass_data

        def add_to_file(cls):

            # read fields data
            website = self.website_input.get()
            username = self.username_input.get()
            password = self.password_input.get()

            if len(website) < 2 or len(username) < 2 or len(password) < 2:
                tk.messagebox.showwarning(
                    title="No data",
                    message="Fields are empty or too short! You must fill in the fields."
                )
            else:
                is_ok = tk.messagebox.askokcancel(
                    title=website,
                    message=f"Are the details correct? \nUsername: {username} \nPassword: {password}"
                )

                # save df to file
                if is_ok:
                    new_data = save_to_dict(website, username, password)
                    try:
                        if os.stat("saved_passwords.json").st_size > 0:
                            with open("saved_passwords.json", "r") as existing_data_file:
                                data = json.load(existing_data_file)
                        else:
                            raise FileNotFoundError
                    except FileNotFoundError:
                        with open("saved_passwords.json", "w") as new_data_file:
                            json.dump(new_data, new_data_file, indent=4)
                    else:
                        data.update(new_data)

                        with open("saved_passwords.json", "w") as data_file:
                            json.dump(data, data_file, indent=4)
                    finally:
                        # clear fields data
                        self.website_input.delete(0, "end")
                        self.password_input.delete(0, "end")

        # ==================== SEARCH ====================
        def search_data(cls):
            try:
                if os.stat("saved_passwords.json").st_size > 0:
                    with open("saved_passwords.json", "r") as existing_data_file:
                        data = json.load(existing_data_file)
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                tk.messagebox.showinfo(
                    title="No data",
                    message="There are no saved passwords yet"
                )
            else:
                website_inquiry = self.website_input.get()

                if len(website_inquiry) > 0:
                    if website_inquiry in data:
                        website = data[website_inquiry]
                        tk.messagebox.showinfo(
                            title=website_inquiry,
                            message=f"Username: {website['username']} \nPassword: {website['password']}"
                        )
                    else:
                        tk.messagebox.showinfo(
                            title="No such entry",
                            message=f"There is no saved password for {website_inquiry} yet"
                        )
                else:
                    tk.messagebox.showerror(
                        title="Empty field",
                        message="Fill in the searched website!"
                    )
