def execute_trade(action: str, price: float, quantity: float = 1000):
    # Mock integration: print a pretend order structure
    order = {
        "symbol": "GBPUSD",
        "action": action,
        "quantity": quantity,
        "price": price,
        "strategy": "MA_Crossover"
    }
    print(f"📤 Placing Order: {order}")
    # Simulate order response
    return {"status": "submitted", "order_id": "FX123456"}
