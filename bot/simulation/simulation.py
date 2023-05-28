import random as rd
import numpy as np
from objects.patient import Patient

class PatientSimulator:
    def __init__(self):
        self.patient = Patient()
        self.BMI_mu = 2.724982891281646
        self.BMI_sigma = 0.35784948829802987
        self.v_lambda = 0.3074085459575776
        self.Age_mu = 31.732
        self.Age_sigma = 12.310977865303798
    
    def generate_patient(self):
        # Presion alta
        high_bp = rd.choices([0, 1], weights=[0.59, 0.41], k=1)[0]
        
        # Colesterol alto
        high_chol = rd.choices([0, 1], weights=[0.542, 0.458], k=1)[0]
        
        # Fumador
        smoker = rd.choices([0, 1], weights=[0.554, 0.446], k=1)[0]
        
        # Diabetes
        diabetes = rd.choices([0, 1, 2], weights=[0.850, 0.015, 0.135], k=1)[0]
        
        # Actividad fisica
        phys_activity = rd.choices([0, 1], weights=[0.249, 0.751], k=1)[0]
        
        # Consumo de alcohol
        alcohol_consumption = rd.choices([0, 1], weights=[0.943, 0.057], k=1)[0]
        
        # Salud general
        general_health = rd.choices([1, 2, 3, 4, 5], weights=[0.182, 0.336, 0.292, 0.134, 0.056], k=1)[0]
        
        # Sexo
        sex = rd.choices([0, 1], weights=[0.574, 0.426], k=1)[0]

        # BMI 
        BMI = np.random.lognormal(mean=self.BMI_mu, sigma=self.BMI_sigma, size=1)[0]

        # Mental health

        mental_health = random_variable = np.random.exponential(1/self.v_lambda, 1)[0]

        # Physical health

        physical_health = random_variable = np.random.exponential(1/self.v_lambda, 1)[0]

        # Age

        age = np.random.normal(loc=self.Age_mu, scale=self.Age_sigma, size=1)[0]

        self.patient.set_high_blood_pressure(high_bp)
        self.patient.set_high_cholesterol(high_chol)
        self.patient.set_BMI(BMI)
        self.patient.set_smoker(smoker)
        self.patient.set_diabetes(diabetes)
        self.patient.set_physical_activity(phys_activity)
        self.patient.set_alcohol(alcohol_consumption)
        self.patient.set_general_health(general_health)
        self.patient.set_mental_health(mental_health)
        self.patient.set_physical_health(physical_health)
        self.patient.set_age(age)
        self.patient.set_sex(sex)

        return self.patient

    
