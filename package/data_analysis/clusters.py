import folium
from sklearn.cluster import KMeans
import pandas as pd

# Load the data
file_path = '../../data/processed/speed_added_night.csv'
data = pd.read_csv(file_path)

# Parameters definition
speed_limit = 50  # Define the speed limit (km/h) above which a speed is considered a violation
n_clusters = 200  # Specify the number of clusters to use in KMeans clustering
bus_percentage = 15  # Set the minimum percentage of buses exceeding the speed limit to consider a cluster significant


# Remove records without registered speed
filtered_data = data.dropna(subset=['Speed (km/h)'])

# Prepare data for clustering (latitude and longitude)
X = filtered_data[['Lat', 'Lon']].values

# Clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)

# Adding cluster label to the data
filtered_data['Cluster'] = kmeans.labels_

# Calculating the percentage of speed limit violations for each cluster
clusters_speeding = filtered_data[filtered_data['Speed (km/h)'] > speed_limit].groupby('Cluster').size() / filtered_data.groupby('Cluster').size() * 100

# Filtering clusters where more than bus_percentage of buses exceed the speed limit
significant_speeding_clusters = clusters_speeding[clusters_speeding > bus_percentage]

# Filtering the rows belonging to significant clusters
significant_clusters_data = filtered_data[filtered_data['Cluster'].isin(significant_speeding_clusters.index)]

# Calculating the mean coordinates of these significant clusters
lat_center = significant_clusters_data['Lat'].mean()
lon_center = significant_clusters_data['Lon'].mean()

# Creating the map
map = folium.Map(location=[lat_center, lon_center], zoom_start=12)

# Adding markers for buses in significant speeding clusters
for idx, row in significant_clusters_data.iterrows():
    cluster_number = row['Cluster']
    cluster_percentage = clusters_speeding.loc[row['Cluster']]
    bus_speed = row['Speed (km/h)']
    folium.CircleMarker([row['Lat'], row['Lon']],
                        radius=5,
                        color='red',
                        fill=True,
                        fill_color='red',
                        fill_opacity=0.6,
                        popup=f"Percent: {cluster_percentage:.2f}%\n"
                              f"Cluster: {cluster_number}\n"
                              f"Speed: {bus_speed:.2f} km/h").add_to(map)

map_path = '../../visualisations/significant_speeding_clusters_night.html'
map.save(map_path)
