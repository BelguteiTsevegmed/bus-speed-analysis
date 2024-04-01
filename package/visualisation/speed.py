import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = '../../data/processed/speed_added_afternoon.csv'
data = pd.read_csv(file_path)

speed_limit = 50

plt.figure(figsize=(8, 5))
plt.hist(data['Speed (km/h)'].dropna(), bins=range(0, 101, 10), color='blue', alpha=0.7)
plt.axvline(x=speed_limit, color='red', linestyle='--', label='Speed Limit (50 km/h)')

plt.title('Simplified Distribution of Bus Speeds')
plt.xlabel('Speed (km/h)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
