import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import os
import sys
import argparse


def load_data(csv_file_path):
    print("Loading data from:", csv_file_path)
    # Load the data from the CSV file
    data = pd.read_csv(csv_file_path)
    print("available coulmns:", data.columns)


    # Assuming you have features 'Age', 'Annual Income', and 'Spending Score' for clustering
    X = data[['Age', 'Annual Income ', 'Spending Score ']].values

    return data, X


def find_optimal_k(X, max_k=6):
    print("Finding optimal K value...")
    wcss = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, init='k-means++',
                        max_iter=300, n_init=10, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)

    # Calculate the differences between consecutive WCSS values
    diff_wcss = np.diff(wcss)

    # Find the elbow point (the point with the maximum difference)
    optimal_k_index = np.argmax(diff_wcss) + 1

    print("Optimal K value:", optimal_k_index)
    return optimal_k_index


def create_clusters(data, X, k):
    print("Performing K-means clustering...")
    # Find the optimal number of clusters using the elbow method
    kmeans = KMeans(n_clusters=k, init='k-means++',
                    max_iter=300, n_init=10, random_state=0)
    clusters = kmeans.fit_predict(X)

    # Add the cluster labels to the original DataFrame
    data['Cluster'] = clusters

    return data


def save_clusters_to_csv(data, output_folder):
    print("Saving clusters to CSV files...")
    # Create a folder for saving CSV files
    os.makedirs(output_folder, exist_ok=True)

    # Save all cluster data to CSV files in the specified folder
    for cluster_id in data['Cluster'].unique():
        cluster_customers = data[data['Cluster'] == cluster_id]
        cluster_name = f"Cluster_{cluster_id}"
        file_name = os.path.join(output_folder, f'{cluster_name}.csv')
        cluster_customers.to_csv(file_name, index=False)


def main(csv_file_path, output_folder):
    print("Starting K-means clustering process...")
    # Load the data
    print(csv_file_path)
    data, X = load_data(csv_file_path)

    # Find the optimal K value
    k = find_optimal_k(X, max_k=6)

    # Perform K-means clustering
    data = create_clusters(data, X, k)

    # Save the clustered data to CSV files
    save_clusters_to_csv(data, output_folder)

    print("Clustering process completed!")


if __name__ == "__main__":
    print("enters in kmeans code")
    # import sys
    print("Received command-line arguments:", sys.argv)

    if len(sys.argv) != 3:
        print("Usage: python kmeans.py <csv_file_path> <output_folder>")
        sys.exit(1)
    else:
        csv_file_path = sys.argv[1]
        output_folder = sys.argv[2]
        main(csv_file_path, output_folder)
