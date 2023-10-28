import tkinter as tk
from enum import Enum
from time import strftime, localtime
from tkintermapview import TkinterMapView
from run_model import run_model

route_id_option = ["300025", "100104", "100118", "100138", "100156", "100165", "1100315", "1100337", "1100338", "1100339", "1400441", "1400454",
                   "1200750", "2800827", "1200859", "800504", "100144", "1400486", "1200857", "1400267", "1400457", "1700978", "1600263",
                   "1100307", "1700950", "1700969", "1600286", "2200876", "1700921", "1100273", "1200842", "1700962", "1700990", "2200866",
                   "1700970", "1300081", "1300810", "1700935", "1700960", "1700905", "1400419", "1200818", "1600270", "2300711", "2400702",
                   "2200872", "2200875", "1100306", "1300869", "1600258", "1700975", "1200800", "1300829", "2400704", "1100304", "1200749",
                   "1100318", "1600264", "1100348", "1100671", "2400701", "1300834", "1200856", "2800897", "1700976", "1300824", "800510",
                   "6301933", "1100321", "1100335", "1200751", "1200881", "301555", "1300899", "1300774", "300284", "800522", "100055",
                   "1100312", "1100336", "100013", "1100349", "1200813", "1700931", "100131", "1600261", "1200747", "300481", "300482",
                   "300483", "300484", "800506", "1100303", "1100316", "800056", "1300837", "1700915", "800511", "800523", "1300767", "2800868",
                   "100018", "100124", "100135", "1100310", "1200741", "1300838", "1300984", "100142", "100007", "100192", "1100344", "1400425",
                   "100143", "1100325", "1400440", "100145", "100154", "300285", "800508", "300283", "300282", "100166", "1600265", "800519",
                   "2200732", "1300806", "1300809", "1300823", "2200877", "1100308", "1100343", "1200812", "1700092", "300281", "1300814",
                   "1200882", "1300985", "1300082", "2200860", "1400456", "1300770", "1600260", "1700949", "1200855", "1600273", "300273",
                   "300201", "1600252", "1300815", "1700093", "1600278", "100016", "300202", "300203", "300204", "300205", "1700941", "300206",
                   "300207", "300208", "300209", "1100314", "800051", "800513", "1700091", "300280", "301501", "300211", "300212", "300213",
                   "1300807", "300214", "100133", "300217", "300218", "1600271", "1100345", "1400422", "1200752", "1300986", "301502", "300222",
                   "300227", "300229", "1600274", "1100332", "1700922", "1700971", "2200870", "300232", "800163", "300235", "300236", "1300772",
                   "300238", "800501", "301503", "100148", "800505", "2400703", "1700980", "301504", "300244", "301505", "300251", "300253",
                   "13001026", "300255", "300257", "300258", "100160", "1100340", "301506", "1200845", "100121", "1100333", "1200740", "100127",
                   "100139", "300278", "1700920", "800520", "2200873", "100136", "2400706", "1300768", "301509", "2400705", "2400709",
                   "1300802", "1300830", "1300833", "2800893", "100172", "800053", "1300769", "100126", "100017", "100193", "100153", "1100366",
                   "1200843", "1700961", "100150", "100141", "1600240", "100155", "100147", "1300766", "1100331", "1700965", "1300801",
                   "1200884", "1300763", "2200874", "1100362", "1400040", "100001", "100106", "1100323", "2400707", "1300819", "1300836",
                   "2200865", "1200880", "2800898", "1700927", "1700945", "1100317", "300403", "100120", "100132", "1200753", "1100301",
                   "1300820", "301511", "301512", "300426", "1100426", "1100427", "300427", "300429", "1100429", "300430", "300431", "300432",
                   "300433", "300434", "300435", "300437", "300438", "300439", "100157", "100015", "800512", "300451", "1100319", "2300712",
                   "1700955", "1100302", "800515", "1400420", "100159", "1300808", "100109", "1600268", "1400421", "1400485", "1400487",
                   "2200731", "1200745", "2800826", "100151", "100196", "301522", "301529", "1300885", "301535", "1100626", "2300714", "301532",
                   "301537", "301539", "100162", "1100363", "2300720", "1200858", "301570", "301541", "301572", "301573", "301549", "100123",
                   "800507", "800518", "301550", "600540", "100146", "1100346", "1400455", "800503", "301591", "301553", "100152", "100005",
                   "800517", "1300764", "1100364", "1400400", "100125", "100140", "100003", "1100365", "1100375", "800502", "2200733",
                   "1300762", "1300822", "1300828", "1300831", "1300832", "2800867", "1300886", "600600", "600601", "600602", "600603",
                   "600604", "600605", "600606", "600607", "600608", "1300891", "600610", "600061", "600611", "600612", "600613", "600614",
                   "1700924", "15101090", "100122", "1300821", "600062", "301567", "301569", "600630", "600063", "600631", "600632", "600633",
                   "600634", "600635", "600636", "600637", "600638", "600640", "600641", "600642", "600645", "2200871", "600065", "301557",
                   "600066", "600666", "1200817", "600067", "100195", "1100361", "600068", "600681", "600682", "600683", "600684", "600685",
                   "600686", "600687", "600688", "600689", "100134", "600690", "600069", "100167", "1600288", "1100311", "1300835", "1300839",
                   "1700977", "800521", "1100347", "2900721", "1700937", "1700968", "1700944", "1700987", "1700910", "1700933", "1700979",
                   "1600266", "1700972", "1700930", "1700957", "100101", "1700911", "1700964", "1700967", "1300761", "300020", "300021",
                   "300022", "1700988", "6300023", "300023", "300024", "1700966", "100161", "2200736", "2200737", "2200738", "800516",
                   "1700974", "2400779", "1100324", "1400423", "1300825", "1400453", "1700923", "100149", "100191", "1100320", "100004",
                   "100158", "1100334", "1100398", "800054", "2400708", "2200878", "2800896", "14101021", "14101028", "1300760", "100012",
                   "2900723", "100164", "100009", "2300713", "1900379"]
direction_id_option = ["0", "1"]
curr_time = strftime("%Y-%m-%d %H:%M:%S", localtime())


class CongestionLevel(Enum):
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
        self.route_id_value = tk.StringVar(input_frame)
        self.route_id_value.set("Select")
        self.route_id_entry = tk.OptionMenu(input_frame, self.route_id_value, *route_id_option)
        self.route_id_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Enter Direction ID:").grid(row=1, column=0, sticky="w")
        self.direction_id_value = tk.StringVar(input_frame)
        self.direction_id_value.set("Select")
        self.direction_id_entry = tk.OptionMenu(input_frame, self.direction_id_value, *direction_id_option)
        self.direction_id_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Enter Time:").grid(row=2, column=0, sticky="w")
        self.future_time_entry = tk.Entry(input_frame, textvariable=tk.StringVar(input_frame, value=curr_time))
        self.future_time_entry.grid(row=2, column=1)

        # Run Model button
        run_button = tk.Button(input_frame, text="Run Model", command=self.run_model_from_gui)
        run_button.grid(row=3, columnspan=2)

        # Map widget
        self.map_widget = TkinterMapView(self, width=1000, height=1000, corner_radius=0)
        self.map_widget.pack(fill="both")
        self.map_widget.set_address("Cologne")

    def run_model_from_gui(self):

        self.map_widget.delete_all_marker()
        self.map_widget.delete_all_path()

        # Get the input values from the GUI entry fields
        route_id = int(self.route_id_value.get())
        direction_id = int(self.direction_id_value.get())
        future_time = self.future_time_entry.get()

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
                level = CongestionLevel.FREE
            elif 1 < color <= 2:
                level = CongestionLevel.BASICALLY_FREE
            elif 2 < color <= 3:
                level = CongestionLevel.MILD_CONGESTED
            elif 3 < color <= 4:
                level = CongestionLevel.MODERATE_CONGESTED
            else:
                level = CongestionLevel.HEAVILY_CONGESTED

            self.map_widget.set_path([start[:2], end[:2]], color=level.value)

        first_marker = location_list[0]
        self.map_widget.set_position(first_marker[0], first_marker[1])

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
