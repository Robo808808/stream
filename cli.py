import argparse
from strategies.moving_average import MovingAverageCrossoverStrategy
from main import stream_gbp_usd_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stream GBPUSD FX rates with strategy")
    parser.add_argument("--short", type=int, default=5)
    parser.add_argument("--long", type=int, default=20)
    parser.add_argument("--interval", type=int, default=10)

    args = parser.parse_args()
    strategy = MovingAverageCrossoverStrategy(short_window=args.short, long_window=args.long)
    stream_gbp_usd_data(strategy, interval=args.interval)
