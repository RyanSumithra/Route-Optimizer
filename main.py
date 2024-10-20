import numpy as np
from scipy.optimize import linear_sum_assignment
import folium
import webbrowser
import tempfile
import os


class RouteOptimizer:
    def __init__(self, num_vehicles, num_locations):
        self.num_vehicles = num_vehicles
        self.num_locations = num_locations
        self.locations = self.generate_random_locations()
        self.distances = self.calculate_distances()

    def generate_random_locations(self):
        return np.random.rand(self.num_locations, 2) * 100  # Random locations in a 100x100 grid

    def calculate_distances(self):
        distances = np.zeros((self.num_locations, self.num_locations))
        for i in range(self.num_locations):
            for j in range(self.num_locations):
                distances[i][j] = np.linalg.norm(self.locations[i] - self.locations[j])
        return distances

    def optimize_routes(self):
        # Use the Hungarian algorithm to assign locations to vehicles
        row_ind, col_ind = linear_sum_assignment(self.distances)

        # Group assignments by vehicle
        routes = [[] for _ in range(self.num_vehicles)]
        for i, j in zip(row_ind, col_ind):
            routes[i % self.num_vehicles].append(j)

        return routes

    def visualize_routes(self, routes):
        # Create a map centered on the mean of all locations
        center = np.mean(self.locations, axis=0)
        m = folium.Map(location=center, zoom_start=10)

        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']

        # Add markers for each location
        for i, loc in enumerate(self.locations):
            folium.Marker(
                loc,
                popup=f'Location {i}',
                icon=folium.Icon(color='gray', icon='info-sign')
            ).add_to(m)

        # Add route lines
        for i, route in enumerate(routes):
            color = colors[i % len(colors)]
            route_coords = [self.locations[loc] for loc in route]
            folium.PolyLine(
                route_coords,
                weight=2,
                color=color,
                opacity=0.8
            ).add_to(m)

        # Save the map to a temporary file and open it in the default web browser
        fd, path = tempfile.mkstemp(suffix='.html')
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(m._repr_html_())
        webbrowser.open('file://' + path)


def main():
    num_vehicles = 3
    num_locations = 15

    optimizer = RouteOptimizer(num_vehicles, num_locations)
    routes = optimizer.optimize_routes()

    print("Optimized Routes:")
    for i, route in enumerate(routes):
        print(f"Vehicle {i + 1}: {route}")

    optimizer.visualize_routes(routes)


if __name__ == "__main__":
    main()