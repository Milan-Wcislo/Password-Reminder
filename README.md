# Secure Password Reminder

This is a simple Secure Password Reminder web application built with `Flask`, `SQLAlchemy`, and `Bootstrap5`. It allows users to register, log in, add, edit, delete, and copy passwords securely.

## Getting Started

1. Make sure you have [Python](https://pages.github.com/](https://www.python.org/downloads/). installed.
  
2. Clone the repository:
```console
git clone https://github.com/Milan-Wcislo/Password-Reminder.git
```
3. Navigate to the project directory:
```console
cd Password-Reminder
```
4. Install the required dependencies:
```console
pip install -r requirements.txt
```

## Features:

- Registration and Login: Users can register for an account and log in securely.
- Dashboard: View, search, and manage your stored passwords.
- Add Password: Add new passwords with website details securely.
- Edit Password: Modify existing passwords, including email, website name, and password.
- Delete Password: Remove passwords you no longer need.
- Copy Password: Quickly copy a password to the clipboard for easy use.

## Technologies Used:

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Bootstrap5
- Werkzeug
- Pyperclip

## Database

The application uses `SQLite` as the database, and the database file is named `secure.db`. It is automatically created when the application is run for the first time. 
Security Passwords are securely hashed using the `PBKDF2` algorithm. This ensures that passwords are stored securely. 

## Contributing

If you would like to contribute to this project, feel free to open an issue or create a pull request. 
