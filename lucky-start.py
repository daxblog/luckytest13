import tkinter as tk
from tkinter import messagebox
import requests
import threading

# URL van de Flask-server
FLASK_SERVER_URL = "http://127.0.0.1:5000"

# Functie om de bot te starten
def start_bot():
    try:
        response = requests.post(f"{FLASK_SERVER_URL}/start-bot")
        if response.status_code == 200:
            messagebox.showinfo("Succes", "Bot gestart!")
        else:
            messagebox.showerror("Fout", "Er is iets mis gegaan met het starten van de bot.")
    except Exception as e:
        messagebox.showerror("Fout", f"Fout bij het verbinden met de server: {str(e)}")

# Functie om de bot te stoppen
def stop_bot():
    try:
        response = requests.post(f"{FLASK_SERVER_URL}/stop-bot")
        if response.status_code == 200:
            messagebox.showinfo("Succes", "Bot gestopt!")
        else:
            messagebox.showerror("Fout", "Er is iets mis gegaan met het stoppen van de bot.")
    except Exception as e:
        messagebox.showerror("Fout", f"Fout bij het verbinden met de server: {str(e)}")

# Functie voor het ophalen van de accountbalans
def fetch_balance():
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/get-balance")
        if response.status_code == 200:
            balance = response.json().get("balance", 0)
            balance_label.config(text=f"Saldo: ${balance}")
        else:
            messagebox.showerror("Fout", "Er is iets mis gegaan met het ophalen van de balans.")
    except Exception as e:
        messagebox.showerror("Fout", f"Fout bij het verbinden met de server: {str(e)}")

# Functie voor het ophalen van actieve trades
def fetch_trades():
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/get-trades")
        if response.status_code == 200:
            trades = response.json().get("trades", [])
            trades_text = "\n".join([f"Symbol: {trade['symbol']} | Winst/Verlies: {trade['current_profit']}%" for trade in trades])
            trades_label.config(text=f"Actieve Trades:\n{trades_text}")
        else:
            messagebox.showerror("Fout", "Er is iets mis gegaan met het ophalen van de trades.")
    except Exception as e:
        messagebox.showerror("Fout", f"Fout bij het verbinden met de server: {str(e)}")

# Hoofdapplicatie voor de Windows GUI
def create_window():
    window = tk.Tk()
    window.title("Lucky13 Trading Bot")
    window.geometry("400x300")

    # Knoppen om de bot te starten en stoppen
    start_button = tk.Button(window, text="Start Bot", command=start_bot, width=20)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop Bot", command=stop_bot, width=20)
    stop_button.pack(pady=10)

    # Label om de saldo weer te geven
    balance_label = tk.Label(window, text="Saldo: $0", font=("Arial", 14))
    balance_label.pack(pady=10)

    # Label om de actieve trades weer te geven
    trades_label = tk.Label(window, text="Actieve Trades:\nGeen actieve trades", font=("Arial", 12), justify=tk.LEFT)
    trades_label.pack(pady=10)

    # Knoppen om de gegevens van de bot op te halen
    fetch_balance_button = tk.Button(window, text="Haal Saldo Op", command=fetch_balance, width=20)
    fetch_balance_button.pack(pady=10)

    fetch_trades_button = tk.Button(window, text="Haal Trades Op", command=fetch_trades, width=20)
    fetch_trades_button.pack(pady=10)

    # Start de GUI
    window.mainloop()

# Start de app in een aparte thread zodat de GUI draait
if __name__ == "__main__":
    threading.Thread(target=create_window).start()
