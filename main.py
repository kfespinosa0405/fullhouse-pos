from tkinter import messagebox

from ui.login import LoginWindow


def main():

    try:

        app = LoginWindow()

        app.mainloop()

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Error al iniciar el sistema:\n\n{e}"
        )


if __name__ == "__main__":

    main()