import tkinter as tk
from tkinter import Checkbutton, Entry, messagebox

#define a class Person
class Person:
    def __init__(self, user_id, password, name):
        self.user_id = user_id
        self.password = password
        self.name = name

# Teacher has subject as an additional attribute
class Teacher(Person):
    def __init__(self, user_id, password, name, subject):
        super().__init__(user_id, password, name)
        self.subject = subject

# Student has department as an additional attribute
class Student(Person):
    def __init__(self, user_id, password, name, department):
        super().__init__(user_id, password, name)
        self.department = department

# Undergraduate Student and Postgraduate Student inherit from Student
class UGStudent(Student):
    pass

class PGStudent(Student):
    pass

font_style = ('Calibri', 16)

class RegistrationGUI:
    def __init__(self, master, user_database, main_app):
        # Initialization of RegistrationGUI
        self.master = master
        self.main_app = main_app
        self.user_database = user_database
        self.master.title("New User Registration")
        self.master.configure(bg="#FFD700")  # Set background color to gold
        # GUI elements for user registration form
        self.name_label = tk.Label(master, text="Name:", foreground="blue", bg="#FFD700",font=font_style)
        self.name_entry = tk.Entry(master)
        self.user_id_label = tk.Label(master, text="User ID:", foreground="blue", bg="#FFD700",font=font_style)
        self.user_id_entry = tk.Entry(master)
        self.password_label = tk.Label(master, text="Password:", foreground="blue", bg="#FFD700",font=font_style)
        self.password_entry = tk.Entry(master, show="*")
        self.check_button = Checkbutton(master, text="Show Password", command=self.show_password, bg="#FFD700")
        self.role_var = tk.StringVar(master)
        self.role_var.set("Role")
        self.role_menu = tk.OptionMenu(master, self.role_var, "Teacher", "UG_Student", "PG_Student")
        self.subject_label = tk.Label(master, text="Department:", foreground="blue", bg="#FFD700",font=font_style)
        self.subject_entry = tk.Entry(master)
        self.register_button = tk.Button(master, text="Register", command=self.register_user, background="green", foreground="white")
        self.cancel_button = tk.Button(master, text="Cancel", command=self.on_cancel, background="red", foreground="white")

        # Packing GUI elements
        self.name_label.pack(pady=5)
        self.name_entry.pack(pady=5)
        self.user_id_label.pack(pady=5)
        self.user_id_entry.pack(pady=5)
        self.password_label.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.check_button.pack()
        self.role_menu.pack(pady=5)
        self.subject_label.pack(pady=5)
        self.subject_entry.pack(pady=5)
        self.register_button.pack(pady=10)
        self.cancel_button.pack(pady=10)
        master.update_idletasks()

        self.master.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_cancel(self):
        # Handle cancel button click
        self.master.destroy()
        self.main_app.show_main_application()

    # To hide password
    def show_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    # To check password
    def password_check(self, password):
        lower, upper, special, digit = 0, 0, 0, 0
        special_char = ["!", "@", "#", "%", "&", "$", "*"]
        if (len(password) >= 8 and len(password) <= 50):
            for i in password:
                if (i.islower()):
                    lower += 1
                if (i.isupper()):
                    upper += 1
                if (i.isdigit()):
                    digit += 1
                if (i in special_char):
                    special += 1
        if (lower < 1 or upper < 1 or special < 1 or digit < 1 or lower + special + upper + digit != len(password)):
            # Show error if password does not meet criteria
            messagebox.showerror("Invalid Password", "Password must contain atleast -\n 1) one uppercase alphabet\n 2) one lowercase alphabet\n 3) one special character\n 4) one number")
            return False
        else:
            return True

    def register_user(self):
        # Handle user registration
        name = self.name_entry.get()
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        subject_or_department = self.subject_entry.get()
        # Check if the password meets the criteria
        if self.password_check(password):
            # Check if the user ID already exists
            if user_id in self.user_database:
                messagebox.showinfo(title="error",message="User with this ID already exists. Choose another User ID")
                return False
            else:
                # Show the main application and add user to the database
                self.main_app.show_main_application()
                if role == "Teacher":
                    self.user_database[user_id] = {"Password": password, "Name": name, "Phone": "", "Role": role, "Subject": subject_or_department}
                else:
                    self.user_database[user_id] = {"Password": password, "Name": name, "Phone": "", "Role": role, "Department": subject_or_department}
                self.master.destroy()
                messagebox.showinfo("Message","Registration Sucessfull")
                return True

class AcademicSystemGUI:
    def __init__(self, master):
        # Initialization of AcademicSystemGUI
        self.master = master
        self.master.title("Academic System")
        self.master.configure(bg="#6495ED")  # Set background color to cornflower blue
        self.user_database = {}
        self.load_user_data()
        # GUI elements for login form
        self.user_id_label = tk.Label(master, text="User ID:", foreground="black", bg="#6495ED",font=font_style)
        self.user_id_entry = tk.Entry(master)
        self.password_label = tk.Label(master, text="Password:", foreground="black", bg="#6495ED",font=font_style)
        self.password_entry = tk.Entry(master, show="*")
        self.check_button = Checkbutton(master, text="Show Password", command=self.show_password, bg="#6495ED")
        self.login_button = tk.Button(master, text="Login", command=self.login, background="green", foreground="white")
        self.login_attempts = 3
        self.btn = tk.Button(root, text="Sign Up", command=self.open_regi_window, background="blue", foreground="white")

        # Packing GUI elements
        self.user_id_label.pack(pady=5)
        self.user_id_entry.pack(pady=5)
        self.password_label.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.check_button.pack()
        self.login_button.pack(pady=10)
        self.btn.pack()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Handle closing of the main window
        self.save_user_data()
        self.master.destroy()

    def save_user_data(self):
        # Save user data to a file
        with open("user_data.txt", "w") as file:
            for user_id, user_data in self.user_database.items():
                user_line = f"{user_id} {user_data['Password']} {user_data['Name']} {user_data['Role']} {user_data.get('Subject', '')} {user_data.get('Department', '')}\n"
                file.write(user_line)

    def load_user_data(self):
        # Load user data from a file
        try:
            with open("user_data.txt", "r") as file:
                for line in file:
                    data = line.strip().split()
                    user_id = data[0]
                    password = data[1]
                    name = data[2]
                    role = data[3]
                    dept = data[4]  

                    if role == 'Teacher':
                        self.user_database[user_id] = {"User ID": user_id,"Password": password, "Name": name, "Role": role, "Subject": dept}
                    else:
                        self.user_database[user_id] = {"User ID": user_id,"Password": password, "Name": name, "Role": role, "Department": dept}

        except FileNotFoundError:
            pass

    def show_password(self):
        # Toggle password visibility
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def login(self):
        # Handle user login
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()

        authenticated_user = self.authenticate_user(user_id, password)

        if authenticated_user:
            self.open_user_window(user_id)
        else:
            if user_id in self.user_database:
                self.login_attempts -= 1
                if self.login_attempts > 0:
                    messagebox.showwarning(title="Login Failed", message="Invalid credentials. {} attempts left.".format(self.login_attempts))
                else:
                    messagebox.showerror(title="Account Deactivated",message= "Too many unsuccessful attempts.")
                    self.master.destroy()

    def authenticate_user(self, user_id, password):
        # Authenticate user credentials
        if user_id in self.user_database:
            return self.user_database.get(user_id, {}).get("Password") == password
        else:
            messagebox.showerror("Error","User ID doesn't exist")
            return False

    def open_user_window(self, user_id):
        # Open the user window after successful login
        self.hide_main_application()
        new_window = tk.Toplevel(self.master)
        new_window.geometry("500x500")
        user_app = UserGUI(new_window, user_id, self.user_database, self)

    def open_regi_window(self):
        # Open the user registration window
        self.hide_main_application()
        new_window = tk.Toplevel(self.master)
        new_window.geometry("500x500")
        registration_app = RegistrationGUI(new_window, self.user_database, self)

    def hide_main_application(self):
        # Hide the main application window
        self.master.iconify()

    def show_main_application(self):
        # Show the main application window
        self.master.deiconify()

class EditProfileGUI:
    def __init__(self, master, user_id, user_database, main_app):
        # Initialization of EditProfileGUI
        self.master = master
        self.user_database = user_database
        self.user_id = user_id
        self.main_app = main_app
        self.master.title("Edit Profile")
        self.master.configure(bg="#FF6347")  # Set background color to tomato
        # GUI elements for editing user profile
        self.name_label = tk.Label(master, text="Name:", foreground="blue", bg="#FF6347",font=font_style)
        self.name_entry = tk.Entry(master)
        self.name_entry.insert(0, user_database.get(user_id, {}).get("Name", ""))

        self.userid_label = tk.Label(master, text="User ID:", foreground="blue", bg="#FF6347",font=font_style)
        self.userID_entry = tk.Entry(master)
        self.userID_entry.insert(0, self.user_id)

        # self.phone_label = tk.Label(master, text="Phone Number:", foreground="blue", bg="#FF6347",font=font_style)
        # self.phone_entry = tk.Entry(master)
        # self.phone_entry.insert(0, user_database.get(user_id, {}).get("Phone", ""))

        self.password_label = tk.Label(master, text="Password:", foreground="blue", bg="#FF6347",font=font_style)
        self.password_entry = tk.Entry(master)
        self.password_entry.insert(0, user_database.get(user_id, {}).get("Password", ""))

        self.role_label = tk.Label(master, text="Role:", foreground="blue", bg="#FF6347",font=font_style)
        self.role_entry = tk.Entry(master)
        self.role_entry.insert(0, user_database.get(user_id, {}).get("Role", ""))

        save_button = tk.Button(master, text="Save Changes", command=self.save_changes, background="green", foreground="white")
        cancel_button = tk.Button(master, text="Cancel", command=self.on_cancel, background="red", foreground="white")

        # Packing GUI elements
        self.name_label.pack()
        self.name_entry.pack(pady=10)
        self.userid_label.pack()
        self.userID_entry.pack(pady=10)
        # self.phone_label.pack()
        # self.phone_entry.pack(pady=10)
        self.password_label.pack()
        self.password_entry.pack(pady=10)
        self.role_label.pack()
        self.role_entry.pack(pady=10)

        save_button.pack(pady=10)
        cancel_button.pack(pady=10)
        self.master.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def save_changes(self):
        # Save changes to the user profile
        new_name = self.name_entry.get()
        # new_phone = self.phone_entry.get()
        new_password = self.password_entry.get()
        new_userID = self.userID_entry.get()
        new_role = self.role_entry.get()
        self.user_database[self.user_id]["Name"] = new_name
        # self.user_database[self.user_id]["Phone"] = new_phone
        self.user_database[self.user_id]["Password"] = new_password
        self.user_database[self.user_id]["Role"] = new_role
        if new_userID != self.user_id:
            self.user_database[new_userID] = self.user_database[self.user_id].copy()
            del self.user_database[self.user_id]
        messagebox.showinfo(title="Changes Saved",message= "Profile updated successfully!")
        self.master.destroy()
        self.main_app.show_main_application()

    def on_cancel(self):
        # Handle cancel button click
        self.master.destroy()
        self.main_app.show_main_application()

class UserGUI:
    def __init__(self, master, user_id, user_database, main_app):
        # Initialization of UserGUI
        self.master = master
        self.main_app = main_app
        self.user_database = user_database
        self.user_id = user_id
        name = self.user_database.get(user_id, {}).get("Name")
        self.master.title(name)
        self.text = tk.Message(master, text="Welcome {}".format(name), width=500, font='500', bg="white")
        self.text.pack()
        self.text2 = tk.Message(master, text="", width=100, font='100',bg='white')
        self.text2.pack()
        self.my_profile = tk.Button(master, text="My Profile", bg="White")
        for key, value in user_database[user_id].items():
            if value:
                self.label_text = f"{key}: {value}"
                self.label = tk.Label(master, text=self.label_text, padx=10, pady=5, bg="White",font=font_style)
                self.label.pack()
       
        self.my_profile.place(x=50, y=150)
        self.edit_profile = tk.Button(master, text="Edit Profile", command=lambda: self.open_edit_profile(user_id), background="blue", foreground="white")
        self.delete = tk.Button(master, text="Delete Account", command=lambda: self.on_delete_account(user_id), background="red", foreground="white")

        self.my_profile.place(x=50, y=150)
        self.edit_profile.place(x=50, y=190)
        self.delete.place(x=50, y=270)
        self.logout = tk.Button(master, text="Logout", command=self.on_logout, background="red", foreground="white")
        self.logout.place(x=50, y=230)

    def open_edit_profile(self, user_id):
        # Open the Edit Profile window
        self.master.withdraw()
        edit_profile_window = tk.Toplevel(self.main_app.master)
        edit_profile_window.geometry("500x500")
        edit_profile_app = EditProfileGUI(edit_profile_window, user_id, self.user_database, self)

    def on_delete_account(self, user_id):
        # Confirm account deletion
        answer = messagebox.askyesno(title='Confirmation', message='Are you sure that you want to Delete?')
        if answer:
            # Delete the user account
            del self.user_database[user_id]
            messagebox.showinfo("Deletion Successful","Your account has been deleted")
            self.master.destroy()    

    def on_logout(self):
        # Confirm logout
        answer = messagebox.askyesno(title='Confirmation', message='Are you sure that you want to Logout?')
        if answer:
            # Close the user window and show the main application
            self.master.destroy()
            self.main_app.show_main_application()

if __name__ == "__main__":
    # Run the application
    root = tk.Tk()
    root.geometry("500x500")
    root.configure(bg="#F0E68C")  # Set background color to khaki
    app = AcademicSystemGUI(root)
    root.mainloop()

