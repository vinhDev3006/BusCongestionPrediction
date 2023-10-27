import tkinter as tk
from enum import Enum

from tkintermapview import TkinterMapView
from run_model import run_model

class congestion_level(Enum):
    FREE = "gray"
    BASICALLY_FREE = "green"
    MILD_CONGESTED = "yellow"
    MODERATE_CONGESTED = "red"
    HEAVILY_CONGESTED = "brown"
class App(tk.Tk):
    APP_NAME = "Simple Map"
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []
        self.marker_path = None


        # Create a frame for input fields
        input_frame = tk.Frame(self)
        input_frame.pack(padx=10, pady=10)

        # Input fields and labels
        tk.Label(input_frame, text="Enter Route ID:").grid(row=0, column=0, sticky="w")
        self.route_id_entry = tk.Entry(input_frame)
        self.route_id_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Enter Direction ID:").grid(row=1, column=0, sticky="w")
        self.direction_id_entry = tk.Entry(input_frame)
        self.direction_id_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Enter Future Time:").grid(row=2, column=0, sticky="w")
        self.future_time_entry = tk.Entry(input_frame)
        self.future_time_entry.grid(row=2, column=1)

        # Run Model button
        run_button = tk.Button(input_frame, text="Run Model", command=self.run_model_from_gui)
        run_button.grid(row=3, columnspan=2)

        # Map widget
        self.map_widget = TkinterMapView(self, width=1000, height=1000, corner_radius=0)
        self.map_widget.pack(fill="both")
        self.map_widget.set_address("Cologne")

    def run_model_from_gui(self):
        # Get the input values from the GUI entry fields
        route_id = int(self.route_id_entry.get())
        direction_id = int(self.direction_id_entry.get())
        future_time = self.future_time_entry.get()

        # Call the run_model function with the provided input
        # self.marker_list = run_model(route_id, direction_id, future_time)
        # path_positions = [marker.position for marker in self.marker_list]
        # self.marker_path = self.map_widget.set_path(path_positions, color=congestion_level.MODERATE_CONGESTED.value)
        df = run_model(route_id, direction_id, future_time)
        location_list = list(zip(df['stop_lat'], df['stop_lon'], df['congestion_level']))
        self.marker_list = location_list

        # Add markers for each coordinate in self.marker_list
        for marker in self.marker_list:
            lat, lon, _ = marker
            self.map_widget.set_marker(lat, lon)

        # Create paths with different colors
        for i in range(len(location_list) - 1):
            start = location_list[i]
            end = location_list[i + 1]
            _, _, color = start  # Extract the congestion level as the color

            if color <= 1:
                level = congestion_level.FREE
            elif 1 < color <= 2:
                level = congestion_level.BASICALLY_FREE
            elif 2 < color <= 3:
                level = congestion_level.MILD_CONGESTED
            elif 3 < color <= 4:
                level = congestion_level.MODERATE_CONGESTED
            else:
                level = congestion_level.HEAVILY_CONGESTED

            self.map_widget.set_path([start[:2], end[:2]], color=level.value)  # Use color= to specify the color





    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()
        self.map_widget.delete_all_path()

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()
