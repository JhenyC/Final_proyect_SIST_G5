class Patient:
    def __init__(self):
        self.age = 0
        self.sex = None
        self.education = None
        self.income = None
        self.id = None
        self.high_blood_pressure = False
        self.high_cholesterol = False
        self.cholesterol_checked = False
        self.BMI = None
        self.smoker = False
        self.diabetes = False
        self.physical_activity = False
        self.fruits = 0
        self.vegetables = 0
        self.alcohol = False
        self.health_care = False
        self.noDocbcCost = False
        self.general_health = None
        self.mental_health = None
        self.physical_health = None
        self.walking_difficulties = False


    def set_id(self, id):
        self.id = id

    def set_age(self, age):
        self.age = age
    
    def set_sex(self, sex):
        self.sex = sex

    def set_education(self, education):
        self.education = education

    def set_income(self, income):
        self.income = income

    def set_high_blood_pressure(self, high_blood_pressure):
        self.high_blood_pressure = high_blood_pressure

    def set_high_cholesterol(self, high_cholesterol):
        self.high_cholesterol = high_cholesterol

    def set_cholesterol_checked(self, cholesterol_checked):
        self.cholesterol_checked = cholesterol_checked

    def set_BMI(self, BMI):
        self.BMI = BMI

    def set_smoker(self, smoker):
        self.smoker = smoker
    
    def set_diabetes(self, diabetes):
        self.diabetes = diabetes

    def set_physical_activity(self, physical_activity):
        self.physical_activity = physical_activity

    def set_fruits(self, fruits):
        self.fruits = fruits

    def set_vegetables(self, vegetables):
        self.vegetables = vegetables

    def set_alcohol(self, alcohol):
        self.alcohol = alcohol

    def set_health_care(self, health_care):
        self.health_care = health_care

    def set_noDocbcCost(self, noDocbcCost):
        self.noDocbcCost = noDocbcCost

    def set_general_health(self, general_health):
        self.general_health = general_health

    def set_mental_health(self, mental_health):
        self.mental_health = mental_health

    def set_physical_health(self, physical_health):
        self.physical_health = physical_health

    def set_walking_difficulties(self, walking_difficulties):
        self.walking_difficulties = walking_difficulties

    def get_id(self):
        return self.id
    
    def get_age(self):
        return self.age
    
    def get_sex(self):
        return self.sex

    def get_education(self):
        return self.education
    
    def get_income(self):
        return self.income
    
    def get_high_blood_pressure(self):
        return self.high_blood_pressure
    
    def get_high_cholesterol(self):
        return self.high_cholesterol
    
    def get_cholesterol_checked(self):
        return self.cholesterol_checked
    
    def get_BMI(self):
        return self.BMI
    
    def get_smoker(self):
        return self.smoker
    
    def get_diabetes(self):
        return self.diabetes
    
    def get_physical_activity(self):
        return self.physical_activity
    
    def get_fruits(self):
        return self.fruits
    
    def get_vegetables(self):
        return self.vegetables
    
    def get_alcohol(self):
        return self.alcohol
    
    def get_health_care(self):
        return self.health_care
    
    def get_noDocbcCost(self):
        return self.noDocbcCost
    
    def get_general_health(self):
        return self.general_health
    
    def get_mental_health(self):
        return self.mental_health
    
    def get_physical_health(self):
        return self.physical_health
    
    def get_walking_difficulties(self):
        return self.walking_difficulties
    
    def __str__(self):
        return f"Person: age={self.age}, sex={self.sex}, education={self.education}, income={self.income}, id={self.id}, " \
               f"high_blood_pressure={self.high_blood_pressure}, high_cholesterol={self.high_cholesterol}, " \
               f"cholesterol_checked={self.cholesterol_checked}, BMI={self.BMI}, smoker={self.smoker}, " \
               f"diabetes={self.diabetes}, physical_activity={self.physical_activity}, fruits={self.fruits}, " \
               f"vegetables={self.vegetables}, alcohol={self.alcohol}, health_care={self.health_care}, " \
               f"noDocbcCost={self.noDocbcCost}, general_health={self.general_health}, " \
               f"mental_health={self.mental_health}, physical_health={self.physical_health}, " \
               f"difficulty_walking={self.walking_difficulties}"
    