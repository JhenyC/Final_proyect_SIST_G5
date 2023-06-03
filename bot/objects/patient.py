import pandas as pd
class Patient:
    def __init__(self):
        self.high_blood_pressure = None
        self.high_cholesterol = None
        self.cholesterol_checked = None
        self.BMI = None
        self.smoker = None
        self.stroke = None
        self.diabetes = None
        self.physical_activity = None
        self.fruits= None
        self.veggies = None
        self.alcohol = None
        self.health_care = None
        self.noDocbcCost = None
        self.general_health = None
        self.mental_health = None
        self.physical_health = None
        self.walking_difficulty = None
        self.age = None
        self.sex = None

    def data_frame_format(self):
        data = {
        'HighBP': [self.high_blood_pressure],
        'HighChol': [self.high_cholesterol],
        'CholCheck': [self.cholesterol_checked],
        'BMI': [self.BMI],
        'Smoker': [self.smoker],
        'Stroke': [self.stroke],
        'Diabetes': [self.diabetes],
        'PhysActivity': [self.physical_activity],
        'Fruits': [self.fruits],
        'Veggies': [self.veggies],
        'HvyAlcoholConsump': [self.alcohol],
        'AnyHealthCare': [self.health_care],
        'NoDocbcCost': [self.noDocbcCost],
        'GenHlth': [self.general_health],
        'MentHlth': [self.mental_health],
        'PhysHlth': [self.physical_health],
        'DiffWalk': [self.walking_difficulty],
        'Age': [self.age],
        'Sex': [self.sex],
        }

        df = pd.DataFrame(data)
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

    def set_walking_difficulty(self, walking_difficulty):
        self.walking_difficulty = walking_difficulty

    def set_fruits(self, fruits):
        self.fruits = fruits

    def set_veggies(self, veggies):
        self.veggies = veggies

    def set_health_care(self, health_care):
        self.health_care = health_care
    
    def set_noDocbcCost(self, noDocbcCost):
        self.noDocbcCost = noDocbcCost

    def set_chol_checked(self, cholesterol_checked):
        self.cholesterol_checked = cholesterol_checked
    
    def set_stroke(self, stroke):
        self.stroke = stroke

    def get_stroke(self):
        return self.stroke
    
    def get_chol_checked(self):
        return self.cholesterol_checked
    
    def get_noDocbcCost(self):
        return self.noDocbcCost
    
    def get_health_care(self):
        return self.health_care
    
    def get_fruits(self):
        return self.fruits
    
    def get_veggies(self):
        return self.veggies
    
    def get_walking_difficulty(self):
        return self.walking_difficulty

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
               f"mental_health={self.mental_health}, physical_health={self.physical_health}, "\
               f"walking_difficulty={self.walking_difficulty}, fruits={self.fruits}, veggies={self.veggies}, "\
               f"noDocbcCost={self.noDocbcCost}, chol_checked={self.cholesterol_checked}, stroke={self.stroke}"
