# Eli Andrew - Feature Reduction using Principal Component Analysis
from testing import *
from sklearn.decomposition import PCA


# Creates, and trains a PCA
# Returns tuple of the PCA object along with the transformed training data
# variance_level is the amount of explained variance desired from the principal components
# variance_level should be given as a decimal between 0 and 1
def train_pca(variance_level, data):
    pca = PCA()
    pca.fit(data)
    explained_variance = 0
    num_components = 0
    for var in pca.explained_variance_ratio_:
        if explained_variance < variance_level:
            explained_variance += var
            num_components += 1
        else:
            break
    trained_pca = PCA(n_components=num_components)
    transformed_data = trained_pca.fit_transform(data)
    return trained_pca, transformed_data


