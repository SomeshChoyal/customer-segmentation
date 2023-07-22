import pandas as pd
from sklearn.cluster import KMeans

def perform_kmeans(data):
    df = pd.read_csv(data)

    # Select columns for K-Means clustering
    X = df[['spend_in_one_year', 'purchase_history']]

    # Initialize KMeans with 2 clusters (based on gender: male and female)
    kmeans = KMeans(n_clusters=2)
    df['cluster'] = kmeans.fit_predict(X)

    return df.to_csv(index=False)
