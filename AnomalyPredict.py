from typing_extensions import runtime
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
from joblib import dump, load
import numpy as np
import time
from tensorflow.keras.models import load_model


CENTROID = (9.821855933229172e-18, -8.620621754345029e-19)
PCA_MODEL = 'model/pca_model.pickle'
PCA_THRESHOLD =  0.14
AU_MODEL = 'model/lstm_encoder.h5'
AU_THRESHOLD = 0.04


def get_euclidean_distance(x, centroids):
    centroids = np.array(centroids)
    return euclidean_distances([x], [centroids])[0][0]


if __name__ == '__main__':
    xi = input('Input bearing values ex = 0.1 0.5 0.6 0.7 : ')
    xi = np.array([float(i) for i in xi.split()])

    toc = time.time()
    pca_model = load(PCA_MODEL)
    x = xi.reshape(1, len(xi))
    x = pca_model.transform(x)
    d = get_euclidean_distance(x[0], CENTROID)
    t1 = time.time() - toc

    toc = time.time()
    tf_model = load_model(AU_MODEL)
    x = xi.reshape(1, 1, 4)
    pred = tf_model.predict(x)
    loss = np.mean(np.abs(pred-x))
    t2 = time.time() - toc

    print(f'result for : {xi}')
    print('PCA')
    if d < PCA_THRESHOLD:
        print(f'distance for the data {d} < {PCA_THRESHOLD} -> NORMAL')
    elif d >= PCA_THRESHOLD:
        print(f'distance for the data {d} >= {PCA_THRESHOLD} -> ANOMALY')
    print(f'runtime {t1} s')
    
    print('Autoencoder')
    if loss < AU_THRESHOLD:
        print(f'loss for the data {loss} < {AU_THRESHOLD} -> NORMAL')
    elif loss >= AU_THRESHOLD:
        print(f'loss for the data {loss} >= {AU_THRESHOLD} -> ANOMALY')
    print(f'runtime {t2} s')