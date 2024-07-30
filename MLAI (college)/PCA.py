import numpy as np

class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.components = None
        self.mean = None

    def fit(self, X):

        self.mean = np.mean(X, axis=0)
        X = X - self.mean
        cov_matrix = np.cov(X.T)
        
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        eigenvectors = eigenvectors.T
        idxs = np.argsort(eigenvalues)[::-1]
        self.components = eigenvectors[idxs[:self.n_components]]

    def transform(self, X):
        
        X = X - self.mean
        
        return np.dot(X, self.components.T)

    def inverse_transform(self, X):
        return np.dot(X, self.components) + self.mean



data = np.random.randn(100, 5)  

pca = PCA(n_components=2)

pca.fit(data)

transformed_data = pca.transform(data)

print("Transformed Data Shape:", transformed_data.shape)

reconstructed_data = pca.inverse_transform(transformed_data)

print("Reconstructed Data Shape:", reconstructed_data.shape)
