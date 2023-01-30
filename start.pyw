import tkinter as tk
import images
import ctypes

screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)


class Menu(tk.Toplevel):
    def __init__(self, serval):
        tk.Toplevel.__init__(self, bg="#e8cb75")
        self.geometry(f"+{serval.winfo_pointerx()}+{serval.winfo_pointery()}")
        self.wm_attributes("-topmost", True)
        self.lift()
        self.serval = serval

        self.desc = tk.Label(self, bg="#e8cb75", font=("Arial", 10), text="Enter Commands")
        self.desc.grid(row=0, columnspan=2, column=0)

        self.exitButton = tk.Button(self, bg="#fcad03", fg="#ffffff", text="Dismiss", font=("Arial", 10),
                                    width=10, command=self.serval.leave)
        self.exitButton.grid(row=2, column=1, padx=10, pady=10)

        self.entry = tk.Entry(self, width=30, font=("Arial", 10))
        self.entry.grid(row=1, column=0, columnspan=2, pady=(5, 10), padx=10)
        self.entry.focus()

        self.submit = tk.Button(self, text="Chat", font=("Arial", 10), bg="#fcad03", fg="#ffffff",
                                command=self.execute)
        self.submit.grid(row=2, column=0)

        self.response = tk.Label(self, bg="#e8cb75", font=("Arial", 10), text="Response: ")
        self.response.grid(row=3, columnspan=2)

        self.bind("<Return>", self.execute)

    # deals with the command entered by the user
    def execute(self, *args):
        text = self.entry.get().lower()
        if text in ("leave", "go away", "close"):
            self.serval.leave()
            self.destroy()
        elif text in ("hide", "lower"):
            self.serval.wm_attributes("-topmost", False)
            self.response.config(text="Response: Ok, no longer displaying over apps")
        elif text in ("show", "raise"):
            self.serval.wm_attributes("-topmost", True)
            self.response.config(text="Response: Ok, now displaying over apps")
        else:
            return
        self.entry.delete(0, tk.END)  # clear text only if command successful


# the main window
class Serval(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.overrideredirect(True)

        self.x = 50
        self.y = 50
        self.geometry(f"+{self.x}+{self.y}")

        self.wm_attributes("-transparentcolor", "#000000")
        self.wm_attributes("-topmost", True)
        self.lift()
        self.display = tk.Label(self, bg="#000000")
        self.display.pack()
        self.idleMotion = [tk.PhotoImage(data=x, format="png") for x in images.idle]
        self.leaveMotion = [tk.PhotoImage(data=x, format="png") for x in images.leave]
        self.currentMotion = self.idleMotion
        self.frame = 0
        self.leaving = False
        self.counter = 0
        self.menu = None
        self.dragOffsetX = 0
        self.dragOffsetY = 0
        self.dragging = False
        self.bind("<Button-1>", self.drag_initiate)
        self.bind("<Button-3>", self.right_click)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)

    # open the menu on right lcick
    def right_click(self, event):
        # do not create a menu if one already exists, or if the program is preparing to close
        if not [x for x in self.winfo_children() if isinstance(x, Menu)] and not self.leaving:
            self.menu = Menu(self)
            self.menu.mainloop()

    # prepare to close the program (first display leaving animation)
    def leave(self):
        self.counter = 0
        self.menu.destroy()
        self.currentMotion = self.leaveMotion
        self.frame = 0
        self.leaving = True

    # start dragging, recording where the mouse starts
    def drag_initiate(self, event):
        self.dragging = True
        self.dragOffsetX = self.winfo_pointerx() - self.x
        self.dragOffsetY = self.winfo_pointery() - self.y

    # update window position to the mouse position (taking into account initial offset)
    def drag(self, event):
        self.x = self.winfo_pointerx() - self.dragOffsetX
        self.y = self.winfo_pointery() - self.dragOffsetY
        self.geometry(f"+{self.x}+{self.y}")

    def stop_drag(self, event):
        self.dragging = False

    # cycle through frames at 30FPS
    def animate(self):
        self.frame = round(self.frame + 1)
        if self.frame >= len(self.currentMotion):
            self.frame = 0
        self.display.config(image=self.currentMotion[self.frame])

    # main loop
    def update(self):
        self.animate()

        if self.leaving:
            self.counter += 1
            if self.counter >= 60:
                self.destroy()

        self.after(33, self.update)


if __name__ == "__main__":
    s = Serval()
    s.update()
    s.mainloop()
