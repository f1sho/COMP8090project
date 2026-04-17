import tkinter as tk
from parking_spot import RegularCarSpot, EVChargingSpot, TruckSpot


class ParkingLotUI:
    """
    GUI for visualising the parking lot layout.

    Correct physical layout:
    - 5 horizontal rows
    - 6 spots in each row
    - Row 1: EV
    - Row 2-4: Regular
    - Row 5: Truck
    - Aisle 1 is between Row 1 and Row 2
    - NO aisle between Row 2 and Row 3
    - Aisle 2 is between Row 3 and Row 4
    - Aisle 3 is between Row 4 and Row 5

    Internal graph nodes such as Aisle_1 / Lane_1 are NOT drawn as nodes.
    The UI shows a physical parking-lot style layout instead.
    """

    def __init__(self, parking_lot):
        self.parking_lot = parking_lot

        self.window = tk.Tk()
        self.window.title("Smart Parking System")

        self.canvas_width = 1320
        self.canvas_height = 820
        self.canvas = tk.Canvas(
            self.window,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white"
        )
        self.canvas.pack()

        self.node_positions = {}
        self.spot_centers = {}

        # Title / legend
        self.title_y = 35
        self.legend_y = 760

        # Gate
        self.gate_x = 110
        self.gate_y = 270
        self.gate_w = 130
        self.gate_h = 60

        # Parking block
        self.spot_start_x = 390
        self.spot_width = 112
        self.spot_height = 68
        self.spot_gap_x = 18

        # 5 horizontal rows
        self.row_y = {
            "Lane_1": 120,   # EV
            "Lane_2": 300,   # Regular row 1
            "Lane_3": 385,   # Regular row 2
            "Lane_4": 560,   # Regular row 3
            "Lane_5": 680,   # Truck
        }

        # 3 horizontal aisles
        self.aisle_y = {
            "Aisle_1": 210,  # between Lane_1 and Lane_2
            "Aisle_2": 470,  # between Lane_3 and Lane_4
            "Aisle_3": 620,  # between Lane_4 and Lane_5
        }

        self.row_spots = {
            "Lane_1": [f"EV{i}" for i in range(1, 7)],
            "Lane_2": [f"R1_{i}" for i in range(1, 7)],
            "Lane_3": [f"R2_{i}" for i in range(1, 7)],
            "Lane_4": [f"R3_{i}" for i in range(1, 7)],
            "Lane_5": [f"T{i}" for i in range(1, 7)],
        }

        self.lane_display_name = {
            "Lane_1": "EV Row",
            "Lane_2": "Regular Row 1",
            "Lane_3": "Regular Row 2",
            "Lane_4": "Regular Row 3",
            "Lane_5": "Truck Row",
        }

    # Helper methods
    
    def _get_spot_color(self, spot):
        if isinstance(spot, EVChargingSpot):
            return "#CDEAC0"
        if isinstance(spot, TruckSpot):
            return "#F6D6A8"
        if isinstance(spot, RegularCarSpot):
            return "#BFDDF6"
        return "#DDDDDD"

    def _short_display_id(self, spot_id):
        if spot_id.startswith("R1_"):
            return spot_id.replace("R1_", "R1-")
        if spot_id.startswith("R2_"):
            return spot_id.replace("R2_", "R2-")
        if spot_id.startswith("R3_"):
            return spot_id.replace("R3_", "R3-")
        return spot_id

    def _draw_title(self):
        self.canvas.create_text(
            self.canvas_width / 2,
            self.title_y,
            text="Smart Parking Lot Layout",
            font=("Arial", 18, "bold")
        )

    def _draw_legend(self):
        items = [
            ("Regular Spot", "#BFDDF6"),
            ("EV Charging Spot", "#CDEAC0"),
            ("Truck Spot", "#F6D6A8"),
            ("Occupied", "#F4B3B3"),
            ("Assigned Spot", "#FFD166"),
            ("Path", "#FF0000"),
        ]

        start_x = 30
        gap = 205

        for i, (label, color) in enumerate(items):
            x = start_x + i * gap
            self.canvas.create_rectangle(
                x, self.legend_y, x + 26, self.legend_y + 26,
                fill=color, outline="black"
            )
            self.canvas.create_text(
                x + 34, self.legend_y + 13,
                text=label,
                anchor="w",
                font=("Arial", 10)
            )

    def _draw_gate(self):
        x1 = self.gate_x - self.gate_w / 2
        y1 = self.gate_y - self.gate_h / 2
        x2 = self.gate_x + self.gate_w / 2
        y2 = self.gate_y + self.gate_h / 2

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#F1F1F1", outline="black", width=2
        )
        self.canvas.create_text(
            self.gate_x, self.gate_y,
            text="Gate",
            font=("Arial", 16, "bold")
        )

        self.node_positions["Gate"] = (self.gate_x, self.gate_y)

    def _draw_roads_and_rows(self):
        road_start_x = self.gate_x + self.gate_w / 2
        road_turn_x = 280

        # Gate -> vertical main road
        self.canvas.create_line(
            road_start_x, self.gate_y,
            road_turn_x, self.gate_y,
            width=6, fill="#8A8A8A"
        )

        self.canvas.create_line(
            road_turn_x, self.aisle_y["Aisle_1"],
            road_turn_x, self.aisle_y["Aisle_3"],
            width=6, fill="#8A8A8A"
        )

        # horizontal aisles
        end_x = self.spot_start_x + 6 * self.spot_width + 5 * self.spot_gap_x + 30

        for aisle_name, y in self.aisle_y.items():
            self.canvas.create_line(
                road_turn_x, y,
                end_x, y,
                width=6, fill="#8A8A8A"
            )

        # row labels on left
        label_x = 370
        for lane_name, y in self.row_y.items():
            self.canvas.create_text(
                label_x, y,
                text=self.lane_display_name[lane_name],
                font=("Arial", 11, "bold"),
                anchor="e"
            )

    def _get_spot_rect(self, lane_name, index_in_row):
        x1 = self.spot_start_x + index_in_row * (self.spot_width + self.spot_gap_x)
        y1 = self.row_y[lane_name] - self.spot_height / 2
        x2 = x1 + self.spot_width
        y2 = y1 + self.spot_height
        return x1, y1, x2, y2

    def _draw_spots(self, assigned_spot_id=None):
        for lane_name, spot_ids in self.row_spots.items():
            for i, spot_id in enumerate(spot_ids):
                spot = self.parking_lot.get_spot(spot_id)
                x1, y1, x2, y2 = self._get_spot_rect(lane_name, i)

                fill_color = self._get_spot_color(spot)

                if spot.is_occupied:
                    fill_color = "#F4B3B3"

                if assigned_spot_id == spot_id:
                    fill_color = "#FFD166"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color, outline="black", width=2
                )

                self.canvas.create_text(
                    (x1 + x2) / 2,
                    y1 + 24,
                    text=self._short_display_id(spot_id),
                    font=("Arial", 10, "bold")
                )

                status = "X" if spot.is_occupied else "O"
                self.canvas.create_text(
                    (x1 + x2) / 2,
                    y1 + 48,
                    text=status,
                    font=("Arial", 11)
                )

                center = ((x1 + x2) / 2, (y1 + y2) / 2)
                self.spot_centers[spot_id] = center
                self.node_positions[spot_id] = center

    def _spot_lane_name(self, spot_id):
        if spot_id.startswith("EV"):
            return "Lane_1"
        if spot_id.startswith("R1_"):
            return "Lane_2"
        if spot_id.startswith("R2_"):
            return "Lane_3"
        if spot_id.startswith("R3_"):
            return "Lane_4"
        if spot_id.startswith("T"):
            return "Lane_5"
        return None

    def _choose_access_aisle(self, path, target_spot_id):
        for node in path:
            if node in self.aisle_y:
                return node

        # fallback
        if target_spot_id.startswith("EV"):
            return "Aisle_1"
        if target_spot_id.startswith("R1_"):
            return "Aisle_1"
        if target_spot_id.startswith("R2_"):
            return "Aisle_2"
        if target_spot_id.startswith("R3_"):
            return "Aisle_2"
        if target_spot_id.startswith("T"):
            return "Aisle_3"

        return "Aisle_1"

    def _draw_path(self, path):
        if not path:
            return

        target_spot_id = None
        for node in reversed(path):
            if node in self.spot_centers:
                target_spot_id = node
                break

        if not target_spot_id:
            return

        lane_name = self._spot_lane_name(target_spot_id)
        if not lane_name:
            return

        aisle_name = self._choose_access_aisle(path, target_spot_id)
        aisle_y = self.aisle_y[aisle_name]
        spot_x, spot_y = self.spot_centers[target_spot_id]

        road_turn_x = 280
        gate_exit_x = self.gate_x + self.gate_w / 2

        # Gate -> main vertical road -> selected aisle -> target spot
        points = [
            (self.gate_x, self.gate_y),
            (gate_exit_x, self.gate_y),
            (road_turn_x, self.gate_y),
            (road_turn_x, aisle_y),
            (spot_x, aisle_y),
            (spot_x, spot_y),
        ]

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="red", width=5,
                capstyle=tk.ROUND, joinstyle=tk.ROUND
            )

        # dots
        self.canvas.create_oval(
            self.gate_x - 5, self.gate_y - 5,
            self.gate_x + 5, self.gate_y + 5,
            fill="red", outline="red"
        )
        self.canvas.create_oval(
            spot_x - 5, spot_y - 5,
            spot_x + 5, spot_y + 5,
            fill="red", outline="red"
        )

    
    # Public method to draw the entire layout
    def draw_layout(self, path=None, assigned_spot_id=None):
        self.canvas.delete("all")
        self.node_positions.clear()
        self.spot_centers.clear()

        self._draw_title()
        self._draw_gate()
        self._draw_roads_and_rows()
        self._draw_spots(assigned_spot_id=assigned_spot_id)
        self._draw_path(path)
        self._draw_legend()

    def run(self, path=None, assigned_spot_id=None):
        self.draw_layout(path=path, assigned_spot_id=assigned_spot_id)
        self.window.mainloop()