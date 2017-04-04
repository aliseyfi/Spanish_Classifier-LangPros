# Eli Andrew - Feature Reduction using Principal Component Analysis
from testing import *
from sklearn.decomposition import PCA

# Creates, and trains a PCA
# Returns tuple of the PCA object along with the transformed training data
def train_pca(num_components, data):
    pca = PCA(n_components=num_components)
    transformed_data = pca.fit_transform(data)
    return pca, transformed_data


