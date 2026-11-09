# EVEQuant

**A market-data engine that finds profitable trade routes in EVE Online's player-driven economy.**

EVE Online has a real, player-run economy with millions of live buy and sell orders spread across thousands of star systems. EVEQuant pulls that order book from the official API, works out which trades are profitable along a chosen route after tax and cargo limits, and ranks the best opportunities.

It's a hobby project, but the problems it solves are the same ones found in real market analysis: ingesting large, paginated API data efficiently, cleaning out anomalous prices, modelling a network, and calculating margins net of fees.

## What it does

1. **Plans the route.** Builds a graph of the whole EVE universe (every stargate connection) with NetworkX, finds the shortest path between two systems, and expands it into a "bubble" of every system within *N* jumps of that path.
2. **Fetches live market orders.** Pulls every buy and sell order for the regions the bubble touches from the EVE ESI API, fetching pages in parallel with `concurrent.futures`. Conditional requests (`If-Modified-Since`) skip data that hasn't changed since the last run.
3. **Cleans the data.** Filters out manipulated or outlier prices using the interquartile range (IQR) method.
4. **Finds the trades.** For every item, compares the cheapest sell order with the highest buy order inside the bubble, calculates the margin after sales tax, and limits quantities to what fits in the ship's cargo hold.
5. **Ranks the results.** Outputs the top opportunities with item, quantity, buy and sell stations, and margin.

## Tech

Python · pandas · NumPy · NetworkX · Requests · SQLite · `concurrent.futures`

## Project structure

```
main.py                    # entry point: set start/end systems, jump radius, cargo volume
config.py                  # trade hubs, regions, tax and broker fee settings
controllers/
  route_manager.py         # route → bubble → fetch → group orders by item
services/
  fetcher.py               # parallel, cached ESI market order fetching
  router.py                # universe graph, shortest path, systems within N jumps
  analyzer.py              # margin calculation and ranking
  filters.py               # IQR outlier filtering
  sde.py                   # item names, volumes, jumps and regions from the SDE database
  converters.py, storage.py
```

## Running it

```bash
pip install -r requirements.txt
```

It also needs the EVE **Static Data Export (SDE)** as a SQLite database (`eve.db`, set by `DB_PATH` in `config.py`). This provides item names, item volumes and the map of stargate connections. Community-maintained SQLite conversions of the SDE are widely available.

Set your start and end systems, jump radius and cargo volume in `main.py`, then run:

```bash
python main.py
```

## Possible next steps

- Factor in broker fees and order competition (how quickly an order would actually fill)
- Track price history over time to spot trends and avoid short-lived spikes
- A simple web dashboard for the results
