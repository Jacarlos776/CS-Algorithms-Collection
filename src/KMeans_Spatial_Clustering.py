import pandas as pd
import sys, os
import numpy as np

# map plot imports
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt
import contextily as cx

initial_centroids = []
# === || Helper Functions || ===

# Calculates distance between the two points
def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def initialize_centroids(data, k, initial_centroids=None):
    # If initial centroids are given, just use that
    if initial_centroids is not None:
        return initial_centroids
    
    # Else get random centroids from data
    num_samples = data.shape[0]
    random_indices = np.random.choice(num_samples, size=k, replace=False)
    return data[random_indices]

def assign_points_to_clusters(data, centroids):
    cluster_labels = []
    
    for point in data:
        distances = []
        for centroid in centroids:
            # Get distance of point from centroid
            dist = calculate_distance(point, centroid)
            distances.append(dist)
        closest_cluster_index = np.argmin(distances)
        cluster_labels.append(closest_cluster_index)
    
    return cluster_labels

# === || K-Means Clustering Functions || ===

def apply_kmeans(data, k, initial_centroids=None, max_iterations=100):
    current_centroids = initialize_centroids(data, k, initial_centroids)
    
    n_iterations = 0
    
    # Iteration loop
    for i in range(max_iterations):
        n_iterations += 1

        old_centroids = current_centroids.copy() 
        
        # Assign points to clusters
        cluster_labels = assign_points_to_clusters(data, current_centroids)
        
        # Update values
        new_centroids = []
        for cluster_id in range(k):
            # Get all points belonging to this cluster
            points_in_cluster = [
                data[j] for j, label in enumerate(cluster_labels) if label == cluster_id
            ]
            
            # Check for empty clusters
            if len(points_in_cluster) > 0:
                # 3.2: Calculate the mean of these points (the new centroid)
                new_center = np.mean(points_in_cluster, axis=0)
            else:
                # If a cluster is empty, keep the old centroid or re-initialize it
                new_center = old_centroids[cluster_id]

            new_centroids.append(new_center)
            
        current_centroids = new_centroids
        
        # Check for convergence
        # The algorithm stops if the centroids no longer change position significantly.
        if all(np.allclose(old_centroids[j], current_centroids[j], atol=1e-8) for j in range(k)):
            break
            
    # After the loop finishes, re-run the assignment one last time
    # to get the final labels for the final centroids.
    final_labels = assign_points_to_clusters(data, current_centroids)

    return current_centroids, final_labels, n_iterations

# === || Map Plotting Functions || ===
def plot_clusters_on_map(labeled_df, k_clusters):
    geometry = [Point(xy) for xy in zip(labeled_df['Longitude'], labeled_df['Latitude'])]
    gdf = geopandas.GeoDataFrame(labeled_df, geometry=geometry, crs="EPSG:4326")
    gdf_webmercator = gdf.to_crs(epsg=3857)
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    gdf_webmercator.plot(
        ax=ax, 
        column='Cluster_Label', 
        categorical=True, 
        legend=True, 
        markersize=10,
        cmap='viridis',
        alpha=0.6,
        marker='o'
    )
    
    cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
    
    ax.set_title(f'K-Means Clustering on Baltimore Crime Data')
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

# === || Processing & Main || ===
def process_data(file_path):
    k = 0
    data = pd.read_csv(file_path)
    
    # Get first 500 applicable rows
    cleaned_data = data.head(500).dropna(subset=['Longitude', 'Latitude'])
    
    # Separate Longitude and Latitude from data
    features_for_clustering = cleaned_data[['Longitude', 'Latitude']].values
    
    # Get K
    while True:
        k_input = input("Please enter k (integer): ")
        try:
            k = int(k_input)
            if k > 0: break
            else: print("k must be a positive integer.") 
        except ValueError: print("Invalid input. Please try again.")
            
    return cleaned_data, features_for_clustering, k

def output_data(file_name, data_name, k, initial_centroids, final_centroids, final_labels, n_iterations, labeled_df):
    with open(file_name, "w") as out:
        out.write(f"K-Means Clustering Output from {data_name}\n")
        out.write(f"k = {k}\n\n")
        
        out.write("Initial Centroids\n")
        for center in initial_centroids:
            out.write(f"({center[0]:.5f}, {center[1]:.5f})\n")
        out.write("\nFinal Centroids\n")
        for center in final_centroids:
            out.write(f"({center[0]}, {center[1]})\n")
            
        out.write(f"\nIterations: {n_iterations}\n\n")
        
        out.write("Labeled Dataset:\n")
        labeled_df['Cluster_Label'] = final_labels
        
        labeled_df.sort_values(by='Cluster_Label', inplace=True)
        
        crime_description_column = 'Description'
        output_data = labeled_df[['Cluster_Label', crime_description_column, 'Longitude', 'Latitude']]
        for index, row in output_data.iterrows():
            # Format: 0 : AUTO THEFT                     [-76.63217, 39.3136]
            label = int(row['Cluster_Label'])
            # Pad the description to 30 spaces
            description = str(row[crime_description_column]).ljust(30)
            
            # Longitude and Latitude are formatted with 5 decimal places for the data points
            lon = f"{row['Longitude']:.5f}"
            lat = f"{row['Latitude']:.5f}"
            
            out.write(f"{label} : {description}[{lon}, {lat}]\n")

def main():
    # checks if number of arguments is correct
    if len(sys.argv) < 2:
        print("Usage: python carlos_exer8.py 'folder path'")
        sys.exit(1)
        
    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)
    initial_centroids = [[-76.61961, 39.29164], [-76.66073, 39.31828], 
                        [-76.60463, 39.32736], [-76.66799, 39.27466], 
                        [-76.60308, 39.23302]]
    cleaned_data, features, k_clusters = process_data(file_path)
    current_centroids, final_labels, n_iterations = apply_kmeans(features, k_clusters, initial_centroids)
    labeled_df = cleaned_data.copy()
    labeled_df['Cluster_Label'] = final_labels
    
    # Updated output path logic
    output_path = os.path.join("..", "data", "KMeans", "output.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    output_data(output_path, file_name, k_clusters, initial_centroids, current_centroids, final_labels, n_iterations, cleaned_data)
    
    plot_clusters_on_map(labeled_df, k_clusters)
if __name__ == "__main__":
    main()