import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    if T == 0 or sigma == 0:
        return max(0, S - K) if option_type == 'call' else max(0, K - S)

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
        result_label.config(text=f"Option price")

        # Plotting
        ax.clear()
        S_values = [s for s in range(int(S * 0.5), int(S * 1.5))]
        option_prices = [black_scholes_price(s, K, T, r, sigma, option_type_selected) for s in S_values]

        ax.plot(S_values, option_prices)
        ax.set_title("Option Price vs Underlying Price")
        ax.set_xlabel("Underlying Price (S)")
        ax.set_ylabel("Option Price")
        ax.grid(True)
        canvas.draw()

    except Exception as e:
        result_label.config(text="Error")


root = tk.Tk()
root.title("European Option Pricing with Black-Scholes equations")


params = [
    ("Underlying price(S)", "100"),
    ("Strike(K)", "100"),
    ("Maturity (T, in years)", "1"),
    ("Risk-free rate (r)", "0.05"),
    ("Vol (σ)", "0.2")
]

entries = []
for label_text, default_val in params:
    label = tk.Label(root, text=label_text)
    label.pack()
    entry = tk.Entry(root)
    entry.insert(0, default_val)
    entry.pack()
    entries.append(entry)

entry_S, entry_K, entry_T, entry_r, entry_sigma = entries

option_type = tk.StringVar(value="call")
type_frame = tk.Frame(root)
type_frame.pack()
ttk.Radiobutton(type_frame, text="Call", variable=option_type, value="call").pack(side=tk.LEFT)
ttk.Radiobutton(type_frame, text="Put", variable=option_type, value="put").pack(side=tk.LEFT)

tk.Button(root, text="Calculate", command=update_pricing).pack(pady=5)


result_label = tk.Label(root, text="Option price: ")
result_label.pack()


fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()


root.mainloop()
