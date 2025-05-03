import json

flights_data = {
    "F101": {
        "flight_number": "BA123",
        "airline": "British Airways",
        "departure_airport": "LHR",
        "arrival_airport": "JFK",
        "departure_time": "2025-06-15T08:30:00",
        "arrival_time": "2025-06-15T16:45:00",
        "departing_date": "2025-06-15",
        "returning_date": "2025-06-30",
        "duration": 8.25,
        "price": 750.00,
        "seats_available": 45,
        "number_of_passengers": 180,
        "class": "Economy",
        "status": "On Time",
        "baggage_allowance": "23kg",
        "gate": "B12",
        "terminal": "5",
        "wifi_available": True,
        "entertainment": ["Movies", "TV Shows", "Music"],
        "check_in_online": True,
        "flight_status": "On Time"
    },
    "F102": {
        "flight_number": "LH456",
        "airline": "Lufthansa",
        "departure_airport": "BER",
        "arrival_airport": "HND",
        "departure_time": "2025-06-16T10:00:00",
        "arrival_time": "2025-06-16T23:30:00",
        "departing_date": "2025-06-16",
        "returning_date": "2025-07-01",
        "duration": 13.5,
        "price": 1200.00,
        "seats_available": 30,
        "number_of_passengers": 220,
        "class": "Business",
        "status": "Delayed",
        "baggage_allowance": "25kg",
        "gate": "C5",
        "terminal": "1",
        "wifi_available": True,
        "entertainment": ["Movies", "Music"],
        "check_in_online": True,
        "flight_status": "Delayed"
    },
    "F103": {
        "flight_number": "EK777",
        "airline": "Emirates",
        "departure_airport": "DXB",
        "arrival_airport": "SYD",
        "departure_time": "2025-06-20T22:00:00",
        "arrival_time": "2025-06-21T15:30:00",
        "departing_date": "2025-06-20",
        "returning_date": "2025-07-10",
        "duration": 14.5,
        "price": 1500.00,
        "seats_available": 20,
        "number_of_passengers": 250,
        "class": "First Class",
        "status": "On Time",
        "baggage_allowance": "32kg",
        "gate": "D1",
        "terminal": "3",
        "wifi_available": True,
        "entertainment": ["Live TV", "Movies", "Games"],
        "check_in_online": True,
        "flight_status": "On Time"
    }
}

# Generating 17 more dummy flights
for i in range(4, 21):
    flights_data[f"F10{i}"] = {
        "flight_number": f"FN{i}",
        "airline": "Air France" if i % 2 == 0 else "Delta Airlines",
        "departure_airport": "CDG" if i % 2 == 0 else "ATL",
        "arrival_airport": "SFO" if i % 2 == 0 else "ORD",
        "departure_time": f"2025-06-{10+i}T{(i%12)+1}:00:00",
        "arrival_time": f"2025-06-{10+i}T{(i%12)+5}:30:00",
        "departing_date": f"2025-06-{10+i}",
        "returning_date": f"2025-07-{10+i}",
        "duration": (i % 12) + 5.5,
        "price": round(600 + (i * 50), 2),
        "seats_available": 40 - (i % 10),
        "number_of_passengers": 200 + (i * 2),
        "class": "Premium Economy" if i % 3 == 0 else "Economy",
        "status": "On Time" if i % 4 != 0 else "Delayed",
        "baggage_allowance": f"{20 + (i%3)}kg",
        "gate": f"A{(i%15)+1}",
        "terminal": str((i % 3) + 1),
        "wifi_available": i % 2 == 0,
        "entertainment": ["Movies", "TV Shows"] if i % 2 == 0 else ["Music", "Live TV"],
        "check_in_online": True,
        "flight_status": "On Time" if i % 4 != 0 else "Delayed"
    }

# Save to JSON file
with open("flights.json", "w") as file:
    json.dump(flights_data, file, indent=4)


