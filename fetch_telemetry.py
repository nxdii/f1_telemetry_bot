import os
import fastf1
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from datetime import datetime


os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

def get_last_race():
    schedule = fastf1.get_event_schedule(2025)
    past_events = schedule[schedule['EventDate'] < datetime.utcnow()]
    last_event = past_events.iloc[-1]
    return last_event['RoundNumber'], last_event['EventName']

def fetch_telemetry(round_number):
    print("Loading session...")
    session = fastf1.get_session(2025, round_number, 'R')
    session.load()
    print("Session loaded.")

    fastest_lap = session.laps.pick_fastest()
    car_data = fastest_lap.get_car_data()
    return car_data, session.event['EventName']

def plot_telemetry(car_data, event_name, date_str):
    output_dir = f"telemetry/{date_str}"
    os.makedirs(output_dir, exist_ok=True)

    print("Plotting telemetry...")
    fig, ax = plt.subplots()
    ax.plot(car_data['Time'].dt.total_seconds(), car_data['Speed'], label='Speed (km/h)')
    ax.plot(car_data['Time'].dt.total_seconds(), car_data['Throttle'] * 100, label='Throttle (%)')
    ax.plot(car_data['Time'].dt.total_seconds(), car_data['Brake'] * 100, label='Brake (%)')
    ax.set_title(f"{event_name} - Fastest Lap Telemetry")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/telemetry_plot.png")
    plt.close()
    print(f"Saved plot to {output_dir}/telemetry_plot.png")

def main():
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        round_number, event_name = get_last_race()
        car_data, event_name = fetch_telemetry(round_number)

        if car_data.empty:
            print("No telemetry data available.")
            return

        plot_telemetry(car_data, event_name, today)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
