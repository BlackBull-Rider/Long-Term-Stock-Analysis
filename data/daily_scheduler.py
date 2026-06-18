# data/daily_scheduler.py

from datetime import datetime

from data.sync_engine import run_scan
from data.fundamental_sync import run_fundamental_scan


def run_daily_update():

    print("=" * 50)
    print("GREEN BULL RIDER DAILY UPDATE")
    print("=" * 50)

    start_time = datetime.now()

    print(
        f"Started : {start_time}"
    )

    # ==========================
    # TECHNICAL SCAN
    # ==========================

    print(
        "\nRunning Technical Scan..."
    )

    technical_count = run_scan(
        limit=5000
    )

    print(
        f"Technical Updated : {technical_count}"
    )

    # ==========================
    # FUNDAMENTAL SCAN
    # ==========================

    print(
        "\nRunning Fundamental Scan..."
    )

    fundamental_count = (
        run_fundamental_scan(
            limit=5000
        )
    )

    print(
        f"Fundamental Updated : {fundamental_count}"
    )

    end_time = datetime.now()

    print(
        f"\nFinished : {end_time}"
    )

    print(
        f"Duration : {end_time - start_time}"
    )

    print("=" * 50)

    return {

        "technical":
        technical_count,

        "fundamental":
        fundamental_count,

        "started":
        str(start_time),

        "finished":
        str(end_time)

    }


if __name__ == "__main__":

    run_daily_update()
