# F1 Telemetry Bot

Automated system that pulls Formula 1 telemetry data daily. Uses FastF1 and GitHub Actions to fetch data, plot fastest lap telemetry, and push it here. No manual work required after setup.

## What this does

- Automatically fetch latest race telemetry (if available)
- Find fastest lap
- Plot Speed, Throttle, Brake data
- Save plots daily to this repo

## How it works

Every day:

1. GitHub Actions runs the bot
2. FastF1 fetches the latest race data
3. Plots are generated and saved
4. Everything is auto-committed to GitHub

## Repo structure

```
telemetry/
├── YYYY-MM-DD/          # Daily telemetry plots
fetch_telemetry.py       # Python script for fetching and plotting
requirements.txt         # Python dependencies
.github/workflows/       # GitHub Actions workflow
```

## Future improvements

- Compare driver laps (delta plots)
- Add sector and timing data
- Improve error handling when race data is missing

## Notes

- Live or recently finished races may not have data → bot will skip or do nothing.
- This is mainly for fun, stats and learning purposes.
- Feel free to fork or adapt.
  
## Run locally

```bash
pip install -r requirements.txt
python fetch_telemetry.py
```

Plots will be saved in `telemetry/YYYY-MM-DD/`.

