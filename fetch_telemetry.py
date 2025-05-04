import fastf1
from datetime import datetime
import matplotlib.pyplot as plt
import os

fastf1.Cache.enable_cache("./cache")

def get_last_race():
    schedule = fastf1.get_event_schedule(2025)
    past_events = schedule[schedule['EventDate'] < datetime.utcnow()]
    last_event = past_events.iloc[-1]
    return last_event['RoundNumber'], last_event['EventName']

def fetch_telemetry(round_number):
    session = fastf1.get_session(2025, round_number, 'R')
    session.load()
    fastest_lap = session.laps.pick_fastest()
    car_data = fastest_lap.get_car_data()
    return car_data

def plot_telemetry(car_data, event_name, date_str):
    os.makedirs(f"telemetry/{date_str}", exist_ok=True)
    fig, ax = plt.subplots()
    ax.plot(car_data['Time'].dt.total_seconds(), car_data['Speed'], label='Speed (km/h)')
    ax.plot(car_data['Time'].dt.total_seconds(), car_data['Throttle']*100, label='Throttle (%)')
    ax.plot(car_data['Time'].dt.total_seconds(), car_data['Brake']*100, label='Brake (%)')
    ax.set_title(f"{event_name} Fastest Lap Telemetry")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Values")
    ax.legend()
    plt.savefig(f"telemetry/{date_str}/telemetry_plot.png")
    plt.close()

def main():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    round_number, event_name = get_last_race()
    car_data = fetch_telemetry(round_number)
    plot_telemetry(car_data, event_name, today)
    print(f"Saved telemetry plot for {event_name} on {today}")

if __name__ == "__main__":
    main()
