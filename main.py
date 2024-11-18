from Application import *
from tkinter import Tk

def main():
    root = Tk()
    root.title("Pokemon Game")
    root.geometry("800x600")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()