import requests
from google.transit import gtfs_realtime_pb2
from geopy.distance import geodesic
import time

def fetch_vehicle_positions(url):
    response = requests.get(url)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    return feed

def fetch_trip_updates(url):
    response = requests.get(url)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    return feed

def get_next_stop_info(trip_update):
    # extraire les informations du stop suivant a partir de la mise a jour du voyage
    if trip_update.stop_time_update:
        next_stop = trip_update.stop_time_update[0]
        return next_stop.stop_id, next_stop.arrival.time, next_stop.departure.time, next_stop.schedule_relationship
    return None, None, None, None

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def main():
    vehicle_positions_url = 'https://rmwb-gtfsrt.civilia.ca/pb/vehiclePositions.pb'
    trip_updates_url = 'https://rmwb-gtfsrt.civilia.ca/pb/tripUpdates.pb'
    
    while True:
        vehicle_positions = fetch_vehicle_positions(vehicle_positions_url)
        trip_updates = fetch_trip_updates(trip_updates_url)
        
        for entity in vehicle_positions.entity:
            vehicle = entity.vehicle
            trip_id = vehicle.trip.trip_id
            position = vehicle.position
            
            # chercher le voyage correspondant
            trip_update = next((t for t in trip_updates.entity if t.id == trip_id), None)
            if trip_update:
                next_stop_id, arrival_time, departure_time, relationship = get_next_stop_info(trip_update.trip_update)
                if next_stop_id:
                    # le nom de l'arrêt et ses coordonnées à partir de vos données statiques GTFS
                    stop_name = "Stop name"  # Placeholder
                    stop_coords = (0, 0)  # Placeholder
                    vehicle_coords = (position.latitude, position.longitude)
                    
                    # calcul de la distance entre le vehicule et le prochain stop
                    distance = calculate_distance(vehicle_coords, stop_coords)
                    print(f"Vehicle {vehicle.vehicle.id} -> Next stop: {next_stop_id}, Arrival time: {arrival_time}, Distance: {distance} meters")
        
        time.sleep(30)  # Wait for 1 minute before the next update

if __name__ == '__main__':
    main()
