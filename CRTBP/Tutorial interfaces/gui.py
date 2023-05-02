from tkinter import messagebox
from tkinter import *
from customtkinter import *

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import odeint

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import warnings
warnings.filterwarnings("error")

root = CTk()

root.geometry("1000x600")
root.minsize(900, 550)
root.maxsize(1100, 700)

main = CTkFrame(root, width=650, fg_color="#2B76B0", corner_radius=20)
main.pack(fill=Y, side=LEFT, pady=10, padx=20)

# Primero sin propagate y mostrar que pasa, que no conserva el tamaño
main.pack_propagate(False)

label = CTkLabel(
    main, text=' Circular Restricted Three Body Problem', height=200, bg_color='#3C9AE3',
    font=('Georgia', 30))

label.pack(fill=X, side=TOP)

buttons_frame = CTkFrame(main, height=200, fg_color="transparent")
buttons_frame.pack(fill=X)
buttons_frame.grid_propagate(False)

# Esto los centra, poner el weight
for i in range(3):
    buttons_frame.grid_columnconfigure(i, weight=1)
buttons_frame.grid_rowconfigure(0, weight=1)


def graph():

    global systemsvalues, systemsvaluesnum, systemvariable

    win = CTkToplevel()
    win.grab_set()
    win.geometry("1000x600")
    validation = win.register(lambda val: val.isdigit()
                              or val == '.' or val == "-" or val == 'e' or val == 'E')
    options_graph = CTkFrame(win, height=100, fg_color='transparent')
    options_graph.pack(side=TOP, fill=X, pady=20)

    Settings = CTkFrame(win, width=300, fg_color="#2B76B0", corner_radius=0)
    Settings.pack(fill=Y, side=RIGHT, pady=10, padx=20)

    Settings.grid_propagate(False)
    Settings.grid_columnconfigure(0, weight=1)

    lagrangevar = IntVar()
    lagrangevar.set(0)
    LagrangeCheck = CTkCheckBox(
        Settings, text='Lagrange', variable=lagrangevar, onvalue=1, offvalue=0)
    LagrangeCheck.grid(row=0, column=0, pady=50)

    surfacevar = IntVar()
    surfacevar.set(0)
    surfaceCheck = CTkSwitch(
        Settings, text='Surface', variable=surfacevar, onvalue=1, offvalue=0)
    surfaceCheck.grid(row=1, column=0, pady=50)

    lmu = CTkLabel(
        options_graph, text=r'mu')
    lmu.grid(row=0, column=0, padx=10)

    if systemvariable.get() != 'Select System':
        mu = CTkEntry(options_graph, width=70)
        index = systemsvalues.index(systemvariable.get())
        mu.insert(-1, str(systemsvaluesnum[index]))
        mu.configure(state=DISABLED)
    else:
        mu = CTkEntry(options_graph, width=70,  validate='key',
                      validatecommand=(validation, '%S'))
    mu.grid(row=0, column=1, padx=5)

    lx = CTkLabel(options_graph, text=r"x")
    lx.grid(row=0, column=2, padx=10)
    x = CTkEntry(options_graph, width=70, validate='key',
                 validatecommand=(validation, '%S'))
    x.grid(row=0, column=3, padx=5)

    ly = CTkLabel(options_graph, text=r"y")
    ly.grid(row=0, column=4, padx=10)
    y = CTkEntry(options_graph, width=70, validate='key',
                 validatecommand=(validation, '%S'))
    y.grid(row=0, column=5, padx=5)

    lvx = CTkLabel(options_graph, text=r"vx")
    lvx.grid(row=0, column=6, padx=10)
    vx = CTkEntry(options_graph, width=70, validate='key',
                  validatecommand=(validation, '%S'))
    vx.grid(row=0, column=7, padx=5)

    lvy = CTkLabel(options_graph, text=r"vy")
    lvy.grid(row=0, column=8, padx=10)
    vy = CTkEntry(options_graph, width=70, validate='key',
                  validatecommand=(validation, '%S'))
    vy.grid(row=0, column=9, padx=5)

    lt = CTkLabel(options_graph, text=r"t")
    lt.grid(row=0, column=10, padx=10)
    te = CTkEntry(options_graph, width=70, validate='key',
                  validatecommand=(validation, '%S'))
    te.grid(row=0, column=11, padx=5)

    def CRTBP(te, x, y, vx, vy, mu, canvas, ax):
        ax.clear()
        try:
            t = float(te.get())
            x = float(x.get())
            y = float(y.get())
            vx = float(vx.get())
            vy = float(vy.get())
            mu = float(mu.get())
            Y0 = np.array([x, y, 0, vx, vy, 0])
        except:
            messagebox.showerror(
                'Missing Value', 'Some value not well defined')

        def equation(Y, t, mu):

            x, y, z, vx, vy, vz = Y
            mu1 = 1-mu
            mu2 = mu
            r1 = np.sqrt((x+mu2)**2 + y**2+z**2)
            r2 = np.sqrt((x-mu1)**2 + y**2+z**2)

            mu_r1 = mu1/(r1**3)
            mu_r2 = mu2/(r2**3)

            ax = 2*vy+x-(x+mu2)*mu_r1-(x-mu1)*mu_r2
            ay = -2*vx+y - (mu_r1+mu_r2)*y
            az = -(mu_r1+mu_r2)*z

            return [vx, vy, vz, ax, ay, az]

        ts = np.linspace(0, t, int(1e5))

        Y_rotational = odeint(equation, y0=Y0, t=ts,
                              atol=1e-10, rtol=1e-10, mxstep=1000, args=(mu,))

        mu1 = 1-mu
        mu2 = mu

        r1 = np.sqrt((x+mu2)**2+y**2)
        r2 = np.sqrt((x-mu1)**2+y**2)

        cj = x**2+y**2+2*(mu1/r1+mu2/r2)-vx**2-vy**2
        if surfacevar.get():

            x = np.linspace(-2, 2, 100)
            y = np.linspace(-2, 2, 100)

            X, Y = np.meshgrid(x, y)
            r1 = np.sqrt((X+mu2)**2+Y**2)
            r2 = np.sqrt((X-mu1)**2+Y**2)

            Cj = X**2+Y**2+2*(mu1/r1+mu2/r2)
            try:
                ax.contour(X, Y, Cj, levels=[cj], colors='gray')
            except:
                messagebox.showinfo('Orbit Info', 'The Orbit is Unbounded')
        if lagrangevar.get():
            alpha = (mu2/(3*mu1))**(1/3)
            L1 = mu1 - (alpha - (alpha**2)/3 -
                        (alpha**3)/9-(alpha**4)*(23/81))
            L2 = mu1 + (alpha + (alpha**2)/3 -
                        (alpha**3)/9-(alpha**4)*(31/81))
            ax.plot(L1, 0, 'b+')
            ax.plot(L2, 0, 'b+')
            if Y_rotational[:, 0].min() < 0:
                mu2mu1 = mu2/mu1
                L3 = -mu2 - 1 - (-(7/12)*(mu2mu1)+(7/12) *
                                 ((mu2mu1)**2) - (13223/20736)*((mu2mu1)**3))
                ax.plot(L3, 0, 'b+')
        ax.plot(Y_rotational[:, 0], Y_rotational[:, 1])
        ax.plot(-mu, 0, 'ro')
        ax.plot(1-mu, 0, 'bo')
        ax.axis('equal')
        canvas.draw()
        return Y_rotational

    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=win)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, win)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    plotbutton = CTkButton(options_graph, text='PLOT',
                           command=lambda x=x, y=y, vx=vx, vy=vy, te=te, mu=mu: CRTBP(te, x, y, vx, vy, mu, canvas, ax))
    plotbutton.grid(row=0, column=12, padx=5)


orbits_button = CTkButton(buttons_frame, width=200, height=80, text='Graph orbit', command=graph,
                          corner_radius=10, bg_color="transparent", fg_color="#3CC2E3")
orbits_button.grid(row=0, column=0)

lagrange_button = CTkButton(buttons_frame, width=200, height=80, text='Find Equilibrium Points',
                            corner_radius=10, bg_color="transparent", fg_color="#3CC2E3")
lagrange_button.grid(row=0, column=1)

orbits_button = CTkButton(buttons_frame, width=200, height=80, text='Stability of orbits',
                          corner_radius=10, bg_color="transparent", fg_color="#3CC2E3")
orbits_button.grid(row=0, column=2)

widgetsframe = CTkFrame(root, width=500, fg_color='#424242')
widgetsframe.pack(side=RIGHT, fill=Y, pady=20, padx=20)

sliderlabel = CTkLabel(widgetsframe, text="Slider Value")
sliderlabel.pack(pady=20)


def slider_event(value):
    sliderlabel.configure(text=round(value))


slider = CTkSlider(widgetsframe, width=400,
                   command=slider_event, from_=1, to=100)
slider.pack(pady=20)

systemslabel = CTkLabel(widgetsframe, text='Pre made systems')
systemslabel.pack(pady=20)

systemvariable = StringVar()
systemvariable.set('Select System')

systemsvalues = ['Earth Moon', 'Jupiter Europa', 'Sun Earth', 'Sun Jupiter']
systemsvaluesnum = [0.0121437, 0.0000252801, 0.00000304043, 0.000953886]

systems = CTkOptionMenu(
    widgetsframe, values=systemsvalues, variable=systemvariable)
systems.pack(pady=20)

root.mainloop()
