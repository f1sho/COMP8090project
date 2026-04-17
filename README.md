# COMP8090 Individual Project

## Task 1 - OOP-based application development

### Overview
A smart parking system that manages parking lots, allocates parking spots, and calculates parking fees using object-oriented principles. The system integrates Dijkstra's algorithm to compute shortest paths from the entrance to parking spots.

### Quick Start

**1. Launch the system:**
Please run the main.py in the task 1 folder of COMP8090project.
Uses ```cd``` according to your file path.
```bash
cd task1
python3 main.py
```

**2. Main menu options:**
```
------------ SMART PARKING SYSTEM ------------
1. Display parking lot status
2. Park a vehicle
3. Checkout and calculate fee
4. Show graphical UI
5. Exit
```

### User Guide

#### Display Parking Lot Status (Option 1)
Shows all parking spots with their current status:
- Spot ID and type
- Occupancy status
- Available spots

#### Park a Vehicle (Option 2)
**Input process:**
1. Enter vehicle type: `car` or `truck`
2. Enter plate number (e.g., `ABC123`)
3. If car: confirm if EV charging is needed (`y` or `n`)

**System processing:**
- Calculates shortest path using Dijkstra algorithm
- Allocates suitable parking spot
- Displays route information
- Generates parking ticket

**Example output:**
```
================================================
Vehicle parked successfully.
Allocated spot: Spot_A_1
Distance: 3
Path: Entry_Gate -> Aisle_1 -> Spot_A_1
Ticket created for plate: ABC123
```

#### Checkout and Calculate Fee (Option 3)
1. Enter vehicle plate number
2. System calculates and displays fee details
3. Vehicle is removed from the system

#### Show Graphical UI (Option 4)
Displays graphical representation of the parking lot with:
- Parking lot structure
- Recently allocated spot highlighted
- Last route path shown

### Core Modules

| Module | Function |
|--------|----------|
| `main.py` | CLI menu and program entry point |
| `parking_lot.py` | Parking lot management system |
| `vehicle.py` | Vehicle class definitions (Car, Truck) |
| `parking_spot.py` | Parking spot classes |
| `fee.py` | Parking fee calculation |
| `mygraph.py` | Graph data structure |
| `mydijkstra.py` | Dijkstra shortest path algorithm |
| `ui.py` | Graphical interface display |

### Example Workflow
```
1. Start system: python3 main.py
2. Option 1: View parking lot status
3. Option 2: Park a car
   - Type: car
   - Plate: ABC123
   - EV charging: y
4. Option 4: View graphical display
5. Option 3: Checkout for plate ABC123
6. Option 5: Exit
```

### Parking System Layout
- Entry Gate
- Main Junction
- 3 Aisles (Aisle_1, Aisle_2, Aisle_3)
- 5 Parking Lanes with various spot types:
  - Regular Car Spots
  - EV Charging Spots
  - Truck Spots


---

## Task 2 - Self Study Data Structure & Algorithm

### Overview
Implementation and testing of Dijkstra's shortest path algorithm to calculate shortest distances from the entrance to all parking lot locations. This is the core algorithm used in Task 1.

### Quick Start

**Run the test:**
Please run the main.py in the task 1 folder of COMP8090project.
Uses ```cd``` according to your file path.
```bash
cd ../task2
python3 test.py
```

### User Guide

#### Test Process

**Step 1: Build test graph**
```
Entry_Gate
  ├─(1)─ Aisle_1
  │      ├─(1)─ Spot_A
  │      ├─(1)─ Spot_B
  │      └─(1)─ Aisle_2
  │             ├─(1)─ Spot_C
  │             └─(1)─ Spot_D
```

**Step 2: Calculate shortest distances**

From `Entry_Gate` to all nodes:
- Entry_Gate: 0.0
- Aisle_1: 1.0
- Aisle_2: 2.0
- Spot_A: 2.0
- Spot_B: 2.0
- Spot_C: 3.0
- Spot_D: 3.0

**Step 3: Reconstruct paths**

Complete paths from entrance to each node:
- Spot_A: [Entry_Gate, Aisle_1, Spot_A]
- Spot_C: [Entry_Gate, Aisle_1, Aisle_2, Spot_C]
- Spot_D: [Entry_Gate, Aisle_1, Aisle_2, Spot_D]

**Step 4: Verify all assertions**

All distances and paths are automatically validated against expected values.

#### Test Output Example
```
=== Shortest Distances from Entry_Gate ===
Entry_Gate: 0.0
Aisle_1: 1.0
Spot_A: 2.0
Spot_B: 2.0
Aisle_2: 2.0
Spot_C: 3.0
Spot_D: 3.0

=== Parent Map ===
Entry_Gate <- None
Aisle_1 <- Entry_Gate
Spot_A <- Aisle_1
Spot_B <- Aisle_1
Aisle_2 <- Aisle_1
Spot_C <- Aisle_2
Spot_D <- Aisle_2

=== Reconstructed Paths ===
Path to Entry_Gate: Entry_Gate
Path to Aisle_1: Entry_Gate -> Aisle_1
Path to Spot_A: Entry_Gate -> Aisle_1 -> Spot_A
Path to Spot_B: Entry_Gate -> Aisle_1 -> Spot_B
Path to Aisle_2: Entry_Gate -> Aisle_1 -> Aisle_2
Path to Spot_C: Entry_Gate -> Aisle_1 -> Aisle_2 -> Spot_C
Path to Spot_D: Entry_Gate -> Aisle_1 -> Aisle_2 -> Spot_D

All tests passed.
```

### Core Modules

| Module | Function |
|--------|----------|
| `test.py` | Main test program entry point |
| `mygraph.py` | Graph data structure implementation |
| `mydijkstra.py` | Dijkstra algorithm implementation |

### Algorithm Details

**Dijkstra's Algorithm Characteristics:**
- Solves single-source shortest path problem
- Works on graphs with non-negative edge weights
- Greedy algorithm: selects node with minimum distance at each step
- Time complexity: O((V + E) log V)

**Key Functions:**

1. **dijkstra_shortest_paths(graph, start)**
   - Input: Graph object and start node
   - Output: Two dictionaries
     - distances: shortest distance from start to each node
     - parent: parent node of each node (for path reconstruction)

2. **reconstruct_path(parent, target, start)**
   - Input: Parent dictionary, target node, start node
   - Output: Complete path from start to target as a list
   - Returns empty list if no path exists


---

## Project Structure
```
COMP8090project/
├── README.md                    # Project documentation
├── task1/                       # Smart Parking System
│   ├── main.py                 # Program entry point
│   ├── parking_lot.py
│   ├── vehicle.py
│   ├── parking_spot.py
│   ├── fee.py
│   ├── mygraph.py
│   ├── mydijkstra.py
│   ├── ui.py
│   └── forfunctiontest.py
└── task2/                       # Dijkstra Algorithm Test
    ├── test.py                  # Test entry point
    ├── mygraph.py
    └── mydijkstra.py
```

## Requirements
- Python 3.6 or higher
- No external dependencies (only standard library)