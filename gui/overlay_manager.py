import tkinter as tk

class OverlayManager:

    def __init__(self,root):
        self.root=root

    def show_popup(self,text,duration=3000):

        win=tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.geometry("300x120+100+100")
        win.configure(bg="black")

        tk.Label(win,text=text,fg="cyan",bg="black").pack(expand=True)

        win.after(duration,win.destroy)

    def show_image(self,img_path,duration=4000):

        from PIL import Image,ImageTk

        win=tk.Toplevel(self.root)
        win.overrideredirect(True)

        img=ImageTk.PhotoImage(Image.open(img_path))
        tk.Label(win,image=img).pack()

        win.after(duration,win.destroy)