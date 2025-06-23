import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

# Muat dataset
data = pd.read_csv('respons.csv')

# Fitur
X = data[['q' + str(i) for i in range(1, 45)]].values

# Bagi data menjadi set pelatihan dan pengujian untuk setiap dimensi
dimensi = ['Processing', 'Perception', 'Input', 'Understanding']
model = {}

# Buat direktori untuk menyimpan model jika belum ada
if not os.path.exists('models'):
    os.makedirs('models')

for dim in dimensi:
    y = data[dim].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Hitung probabilitas prior
    def hitung_prior(y_train):
        kelas = np.unique(y_train)
        prior = {}
        for cls in kelas:
            prior[cls] = np.sum(y_train == cls) / len(y_train)
        return prior

    # Hitung likelihood
    def hitung_likelihood(X_train, y_train):
        n_fitur = X_train.shape[1]
        kelas = np.unique(y_train)
        likelihood = {}
        
        for cls in kelas:
            likelihood[cls] = {}
            X_kelas = X_train[y_train == cls]
            for fitur in range(n_fitur):
                nilai_fitur = np.unique(X_train[:, fitur])
                likelihood[cls][fitur] = {}
                for nilai in nilai_fitur:
                    likeli = np.sum(X_kelas[:, fitur] == nilai) / len(X_kelas)
                    likelihood[cls][fitur][nilai] = likeli
        return likelihood

    # Prediksi
    def prediksi(X_test, prior, likelihood):
        y_pred = []
        for sampel in X_test:
            posteriors = {}
            for cls, prior_cls in prior.items():
                posterior = prior_cls
                for fitur_index in range(len(sampel)):
                    nilai_fitur = sampel[fitur_index]
                    if nilai_fitur in likelihood[cls][fitur_index]:
                        posterior *= likelihood[cls][fitur_index][nilai_fitur]
                    else:
                        posterior *= 1e-6  # nilai smoothing kecil
                posteriors[cls] = posterior
            y_pred.append(max(posteriors, key=posteriors.get))
        return np.array(y_pred)

    # Latih model
    prior = hitung_prior(y_train)
    likelihood = hitung_likelihood(X_train, y_train)

    # Buat prediksi
    y_pred = prediksi(X_test, prior, likelihood)

    # Evaluasi model
    akurasi = accuracy_score(y_test, y_pred)
    matriks_konfusi = confusion_matrix(y_test, y_pred)
    laporan_klasifikasi = classification_report(y_test, y_pred)

    print(f'=== {dim.upper()} ===')
    print(f'Akurasi: {akurasi * 100:.2f}%')
    print('Matriks Konfusi:')
    print(matriks_konfusi)
    print('Laporan Klasifikasi:')
    print(laporan_klasifikasi)

    # Simpan model (prior dan likelihood) untuk setiap dimensi menggunakan joblib
    model[dim] = {
        'prior': prior,
        'likelihood': likelihood
    }
    joblib.dump(model[dim], f'models/model_{dim}.joblib')
