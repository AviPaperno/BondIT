import csv
from datetime import datetime as dt, date, time


class Parser:
    filepath = "data.csv"
    def update(self):
        count = 0
        for key, value in self.data.items():
            if count < 20:
                if value["success"]:
                    count += 1
                    continue
                if value["success"] is None:
                    value["success"] = True
                    count += 1
                    continue
            else:
                value["success"] = False

    def __init__(self):
        data = dict()
        with open(self.filepath, "r") as fi:
            reader = csv.DictReader(fi)
            for flight in reader:
                arrival_time = list(map(int, flight["Arrival"].split(":")))
                departure_time = list(map(int, flight["Departure"].split(":")))
                arrival_time = time(hour=arrival_time[0], minute=arrival_time[1])
                departure_time = time(hour=departure_time[0], minute=departure_time[1])

                flight_time = dt.combine(date.today(), departure_time) - dt.combine(date.today(), arrival_time)
                flight_time = flight_time.seconds / 60
                success = None

                if status := flight["success"].replace("'", ""):
                    success = True if status == "success" else False

                if success is None and flight_time < 180:
                    success = False

                id_ = flight["flight ID"]

                data[id_] = {
                    "arrival_time": arrival_time,
                    "departure_time": departure_time,
                    "fligt_time": flight_time,
                    "success": success
                }

        self.data = dict(sorted(data.items(), key=lambda item: item[1]['arrival_time']))

        self.update()

        self.save_updated_file()

    def save_updated_file(self):
        with open(self.filepath, "w") as fo:
            fieldnames = ["flight ID", "Arrival", "Departure", "success"]
            writer = csv.DictWriter(fo, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in self.data.items():
                elem = {
                    "flight ID": key,
                    "Arrival": f"{value['arrival_time'].strftime('%H:%M')}",
                    "Departure": f"{value['departure_time'].strftime('%H:%M')}",
                    "success": 'success' if value["success"] else 'fail'
                }
                writer.writerow(elem)

    def add_field(self, input_str):
        input_str = input_str.split(",")
        elem = {
            "flight ID": input_str[0],
            "Arrival": input_str[1],
            "Departure": input_str[2],
            "success": input_str[3]
        }
        with open(self.filepath, "a+") as fo:
            fieldnames = ["flight ID", "Arrival", "Departure", "success"]
            writer = csv.DictWriter(fo, fieldnames=fieldnames)
            writer.writerow(elem)
