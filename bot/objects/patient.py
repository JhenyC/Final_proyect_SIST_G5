import pandas as pd
class Patient:
    def __init__(self):
        self.high_blood_pressure = None
        self.high_cholesterol = None
        self.BMI = None
        self.smoker = None
        self.diabetes = None
        self.physical_activity = None
        self.alcohol = None
        self.general_health = None
        self.mental_health = None
        self.physical_health = None
        self.age = None
        self.sex = None

    def data_frame_format(self):
        data = {
        'HighBP': [self.high_blood_pressure],
        'HighChol': [self.high_cholesterol],
        'BMI': [self.BMI],
        'Smoker': [self.smoker],
        'Diabetes': [self.diabetes],
        'PhysActivity': [self.physical_activity],
        'HvyAlcoholConsump': [self.alcohol],
        'GenHlth': [self.general_health],
        'MentHlth': [self.mental_health],
        'PhysHlth': [self.physical_health],
        'Age': [self.age],
        'Sex': [self.sex]
        }

        df = pd.DataFrame(data)
        print(df.head())
        return df

    def set_age(self, age):
        self.age = age
    
    def set_sex(self, sex):
        self.sex = sex

    def set_high_blood_pressure(self, high_blood_pressure):
        self.high_blood_pressure = high_blood_pressure

    def set_high_cholesterol(self, high_cholesterol):
        self.high_cholesterol = high_cholesterol

    def set_BMI(self, BMI):
        self.BMI = BMI

    def set_smoker(self, smoker):
        self.smoker = smoker
    
    def set_diabetes(self, diabetes):
        self.diabetes = diabetes

    def set_physical_activity(self, physical_activity):
        self.physical_activity = physical_activity

    def set_alcohol(self, alcohol):
        self.alcohol = alcohol

    def set_general_health(self, general_health):
        self.general_health = general_health

    def set_mental_health(self, mental_health):
        self.mental_health = mental_health

    def set_physical_health(self, physical_health):
        self.physical_health = physical_health

    def get_age(self):
        return self.age
    
    def get_sex(self):
        return self.sex
    
    def get_high_blood_pressure(self):
        return self.high_blood_pressure
    
    def get_high_cholesterol(self):
        return self.high_cholesterol
    
    def get_BMI(self):
        return self.BMI
    
    def get_smoker(self):
        return self.smoker
    
    def get_diabetes(self):
        return self.diabetes
    
    def get_physical_activity(self):
        return self.physical_activity

    def get_alcohol(self):
        return self.alcohol

    def get_general_health(self):
        return self.general_health
    
    def get_mental_health(self):
        return self.mental_health
    
    def get_physical_health(self):
        return self.physical_health

    def __str__(self):
        return f"Person: age={self.age}, sex={self.sex}," \
               f"high_blood_pressure={self.high_blood_pressure}, high_cholesterol={self.high_cholesterol}, " \
               f"BMI={self.BMI}, smoker={self.smoker}, " \
               f"diabetes={self.diabetes}, physical_activity={self.physical_activity}," \
               f"alcohol={self.alcohol}, health_care={self.health_care}, " \
               f"general_health={self.general_health}, " \
               f"mental_health={self.mental_health}, physical_health={self.physical_health}, "