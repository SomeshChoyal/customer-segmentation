import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
data = pd.read_csv("Mall_Customers.csv")

# Assuming you have features 'Age' and 'Spending Score' for clustering
X = data[['Age', 'Spending Score']].values

# Function to find the optimal k value using the elbow method
def find_optimal_k(X, max_k=6):
    wcss = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)

    # Plot the WCSS against the range of k values
    # plt.plot(range(1, max_k + 1), wcss)
    # plt.title('Elbow Method')
    # plt.xlabel('Number of clusters (k)')
    # plt.ylabel('WCSS')
    # plt.show()

    # Calculate the differences between consecutive WCSS values
    diff_wcss = np.diff(wcss)

    # Find the elbow point (the point with the maximum difference)
    optimal_k_index = np.argmax(diff_wcss) + 1

    return optimal_k_index

# Find the optimal number of clusters using the elbow method
k = find_optimal_k(X, max_k=6)
print("Optimal K value:",k)

kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
clusters = kmeans.fit_predict(X)

# Add the cluster labels to the original DataFrame
data['Cluster'] = clusters


# Create a folder for saving CSV files (replace 'output_folder' with your desired folder path)
output_folder = 'clustered_csv'
os.makedirs(output_folder, exist_ok=True)


# Separate CustomerID for each cluster
cluster_data = {}
for i in range(k):
    cluster_data[i] = data[data['Cluster'] == i]['CustomerID']


# Function to create cluster names based on Age and Spending Score ranges
def create_cluster_name(cluster_df):
    age_range = f"{cluster_df['Age'].min()}-{cluster_df['Age'].max()}"
    spending_range = f"{cluster_df['Spending Score'].min()}-{cluster_df['Spending Score'].max()}"
    return f"Cluster_A_{age_range}_S_{spending_range}"

# Save all cluster data to CSV files in the specified folder
for i in range(k):
    cluster_customers = data[data['Cluster'] == i]
    cluster_name = create_cluster_name(cluster_customers)
    file_name = os.path.join(output_folder, f'{cluster_name}.csv')
    cluster_customers.to_csv(file_name, index=False)
    
# # Save each cluster data to a separate CSV file
# for cluster_id, cluster_customers in cluster_data.items():
#     cluster_customers.to_csv(f'cluster_{cluster_id + 1}.csv', index=False)

# Visualize the clusters
plt.scatter(X[clusters == 0, 0], X[clusters == 0, 1], s=50, c='red', label='Cluster 1')
plt.scatter(X[clusters == 1, 0], X[clusters == 1, 1], s=50, c='blue', label='Cluster 2')
plt.scatter(X[clusters == 2, 0], X[clusters == 2, 1], s=50, c='green', label='Cluster 3')
plt.scatter(X[clusters == 3, 0], X[clusters == 3, 1], s=50, c='cyan', label='Cluster 4')
plt.scatter(X[clusters == 4, 0], X[clusters == 4, 1], s=50, c='magenta', label='Cluster 5')

# Plot the centroids of each cluster
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c='black', label='Centroids')
plt.title('Clusters of Mall Customers')
plt.xlabel('Age')
plt.ylabel('Spending Score')
plt.legend()
plt.show()
