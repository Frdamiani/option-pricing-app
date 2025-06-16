import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    if T == 0 or sigma == 0:
        if option_type == 'call':
            return max(0, S - K)
        else:
            return max(0, K - S)

    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def update_pricing():
    try:
        S = float(entry_S.get())
        K = float(entry_K.get())
        T = float(entry_T.get())
        r = float(entry_r.get())
        sigma = float(entry_sigma.get())
        option_type_selected = option_type.get()

        price = black_scholes_price(S, K, T, r, sigma, option_type_selected)
        result_label.config(text="Option price")

        ax.clear()
        S_values = [s for s in range(int(S * 0.5), int(S * 1.5))]
        option_prices = []

        for s in S_values:
            option_prices.append(black_scholes_price(s, K, T, r, sigma, option_type_selected))

        ax.plot(S_values, option_prices)
        ax.set_title("Option Price vs Underlying Price")
        ax.set_xlabel("Underlying Price (S)")
        ax.set_ylabel("Option Price")
        ax.grid(True)

        canvas.draw()

    except Exception as e:
        result_label.config(text="Error")

root = tk.Tk()
root.title("Calcul d'options européennes avec Black-Scholes")

params = [
    ("Prix de l'actif sous-jacent (S)", "100"),
    ("Strike (K)", "100"),
    ("Maturité (T, en années)", "1"),
    ("Taux sans risque (r)", "0.05"),
    ("Volatilité (σ)", "0.2")
]

entries = []
for texte, valeur in params:
    label = tk.Label(root, text=texte)
    label.pack()
    entry = tk.Entry(root)
    entry.insert(0, valeur)
    entry.pack()
    entries.append(entry)

entry_S, entry_K, entry_T, entry_r, entry_sigma = entries

option_type = tk.StringVar(value="call")
frame_type = tk.Frame(root)
frame_type.pack()
ttk.Radiobutton(frame_type, text="Call", variable=option_type, value="call").pack(side=tk.LEFT)
ttk.Radiobutton(frame_type, text="Put", variable=option_type, value="put").pack(side=tk.LEFT)

tk.Button(root, text="Calculer", command=update_pricing).pack(pady=5)

result_label = tk.Label(root, text="Option price :")
result_label.pack()

fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
