from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd


class Classifier:
    def __init__(self):
        with open('C:\\Users\\A8\\Documents\\Code\\Python\\Final_proyect_SIST_G5\\bot\\objects\\modelo.pkl', 'rb') as archivo:
            self.classifier = pickle.load(archivo)

    def transform_data(self, data):
        scaler = StandardScaler()
        df = pd.DataFrame(data)
        new_df = scaler.fit_transform(df)
        df = pd.DataFrame(new_df)
        df = scaler.transform(df)
        return df

    def classify(self, data):
        data = self.transform_data(data)
        return self.classifier.predict(data)

