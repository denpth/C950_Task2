# Package Delivery Route Simulator

A Python delivery-routing simulator that assigns packages across multiple trucks, models delivery constraints, and uses a nearest-neighbor routing strategy to complete deliveries while tracking time, mileage, and package status.

## What it demonstrates

- Custom hash-table implementation for package lookup
- Greedy nearest-neighbor route selection
- Constraint handling for delayed packages, address corrections, deadlines, and driver availability
- Time and mileage simulation across multiple delivery vehicles
- CSV ingestion and domain modeling in Python
- Interactive package-status queries at arbitrary times during the simulated day

## How it works

The application loads package, address, and distance data from CSV files into in-memory structures. Packages are assigned to three trucks, and each truck repeatedly selects the nearest valid undelivered package from its current location.

The simulation also accounts for operational constraints. For example, a package with an incorrect address is held until its corrected address becomes available, and the third truck cannot depart until both its earliest allowed departure time and driver availability requirements are satisfied.

## Project structure

- `routing.py` — delivery simulation, route selection, deadline checks, and status UI
- `chainingHash.py` — chained hash table implementation
- `package.py` — package domain model and status behavior
- `load_package.py` — CSV loading and distance/address helpers
- `packages.csv` — package data
- `addresses.csv` — delivery locations
- `distance_table.csv` — pairwise distance data

## Running the simulator

```bash
python main.py
```

The application runs the delivery simulation, verifies delivery deadlines, reports total mileage, and then allows package-status lookups by time using `HH:MM` input.

## Algorithmic notes

The route selection step uses a greedy nearest-neighbor strategy. For each truck, the next destination is selected by scanning the remaining eligible packages and choosing the package with the smallest distance from the truck's current location. With `N` packages on a truck, the routing phase is approximately `O(N²)`.
