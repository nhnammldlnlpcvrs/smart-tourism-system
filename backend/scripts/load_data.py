# scripts/load_data.py
import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.create_tables import (
    load_tourism,
    load_foods,
    load_hotels
)


def main():
    parser = argparse.ArgumentParser(description="Load JSONL datasets into PostgreSQL.")

    parser.add_argument(
        "--tourism",
        action="store_true",
        help="Load vietnam_tourism.jsonl into PostgreSQL"
    )

    parser.add_argument(
        "--foods",
        action="store_true",
        help="Load vietnam_foods.jsonl into PostgreSQL"
    )

    parser.add_argument(
        "--hotels",
        action="store_true",
        help="Load vietnam_hotels.jsonl into PostgreSQL"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Load all datasets into PostgreSQL"
    )

    args = parser.parse_args()

    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


    tourism_path = os.path.join(data_dir, "vietnam_tourism.jsonl")
    foods_path   = os.path.join(data_dir, "vietnam_foods.jsonl")
    hotels_path  = os.path.join(data_dir, "vietnam_hotels.jsonl")

    if args.all:
        print("Loading ALL datasets...")
        load_tourism(tourism_path)
        load_foods(foods_path)
        load_hotels(hotels_path)
        print("All datasets loaded successfully.")
        return

    if args.tourism:
        print("Loading tourism data...")
        load_tourism(tourism_path)

    if args.foods:
        print("Loading foods data...")
        load_foods(foods_path)

    if args.hotels:
        print("Loading hotels data...")
        load_hotels(hotels_path)

    if not (args.tourism or args.foods or args.hotels or args.all):
        print("\nBạn chưa chọn dataset để load.")
        print("Ví dụ:")
        print("  python scripts/load_data.py --tourism")
        print("  python scripts/load_data.py --foods")
        print("  python scripts/load_data.py --all\n")


if __name__ == "__main__":
    main()