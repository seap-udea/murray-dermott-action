
from tkinter import *
from customtkinter import *
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

root = Tk()

root.geometry("1000x600")
root.minsize(900, 550)
root.maxsize(1100, 700)
root.title('Function Sin Generator')

main = CTkFrame(root, height=600,fg_color="#9FE2BF", corner_radius=20)
main.pack(fill=Y,  side=RIGHT, pady=20, padx=20)
main.pack_propagate(False)

label = CTkLabel(main, text="w: ")
label.place(x=20, y=230)

entry = CTkEntry(main, width=50, height=20, validate='key')
entry.place(x=100, y=235)

def plot():

    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)

    try:
        w = float(entry.get())
    except:
        messagebox.showerror('Missing Value', 'Some value not well defined')
            

    t = np.linspace(0, 2*np.pi, 200)
    values = np.sin(w*t)     
        
    ax.plot(t, values)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

button = CTkButton(master=main, text="Plot", command=plot)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


root.mainloop()