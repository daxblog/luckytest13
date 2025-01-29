import time
import random
import os
from flask_socketio import SocketIO
from flask import Flask
import threading
import json
import ccxt

# Flask setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Trading instellingen
TRADING_SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT']  # Testnet ondersteunde symbolen
TRADE_PERCENTAGE = 0.02  # 2% van het saldo wordt geïnvesteerd
STOP_LOSS_PERCENTAGE = 0.03  # Stop loss op 3% verlies
TAKE_PROFIT_PERCENTAGE = 0.05  # Take profit op 5% winst

# 📌 Verbinding maken met Bybit Testnet API
def connect_to_bybit():
    """Verbind met Bybit Testnet via ccxt"""
    api_key = 'YOUR_TESTNET_API_KEY'  # Vul je eigen Testnet API-key in
    api_secret = 'YOUR_TESTNET_API_SECRET'  # Vul je eigen Testnet API-secret in
    
    exchange = ccxt.bybit({
        'apiKey': api_key,
        'secret': api_secret,
        'options': {'defaultType': 'future'},
        'test': True,  # Gebruik Testnet
    })
    exchange.set_sandbox_mode(True)  # Schakel Testnet in
    return exchange

# 📌 Simulatie van een nep-account balans
def fetch_virtual_balance():
    """Simuleer een virtuele accountbalans."""
    return {'total': {'USDT': 1000.0}}  # Begin met 1000 USDT

# 📌 Plaats een gesimuleerde order op Bybit Testnet
def place_virtual_order(symbol, side, amount):
    """Simuleer een order zonder echt geld."""
    print(f"[TESTNET] {side.upper()} order geplaatst: {amount} {symbol}")
    return {
        'symbol': symbol,
        'side': side,
        'amount': amount,
        'status': 'filled',
        'test_order': True
    }

# 📌 Simulatie van trade winst/verlies en order uitvoeren
def trade_simulation():
    """Simuleer trading op basis van testnet-data."""
    while os.path.exists("bot_running.txt"):
        symbol = random.choice(TRADING_SYMBOLS)
        balance = fetch_virtual_balance()
        amount_to_trade = balance['total']['USDT'] * TRADE_PERCENTAGE / 10000  # Simuleer kleine trade
        profit_or_loss = random.uniform(-STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE)
        
        if profit_or_loss > 0:
            place_virtual_order(symbol, 'buy', amount_to_trade)
            send_notification("notify_profit", f"[TESTNET] Trade op {symbol} - Winst: {profit_or_loss}%")
        else:
            place_virtual_order(symbol, 'sell', amount_to_trade)
            send_notification("notify_loss", f"[TESTNET] Trade op {symbol} - Verlies: {profit_or_loss}%")

        time.sleep(5)

# 📌 Start de bot met Testnet-configuratie
def start():
    """Start de bot op Bybit Testnet."""
    with open("bot_running.txt", "w") as f:
        f.write("running")
    thread = threading.Thread(target=trade_simulation)
    thread.start()

if __name__ == "__main__":
    start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
