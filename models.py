WATER_GOAL = 2000
STEPS_GOAL = 8000
BMI_UNDERWEIGHT = 18.5
BMI_NORMAL = 25
BMI_OVERWEIGHT = 30

class HealthAnalyzer:
    def __init__(self,weight,height,water,steps,mood):
        self.weight = weight
        self.height = height
        self.water = water
        self.steps = steps
        self.mood = mood

    def calculate_bmi(self):
        height_m = self.height/100
        return self.weight/(height_m**2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < BMI_UNDERWEIGHT:
            return "Underweight"
        elif bmi < BMI_NORMAL:
            return "Normal"
        elif bmi < BMI_OVERWEIGHT:
            return "Overweight"
        else:
            return "Obese"

    def check_water_intake(self):
        return(self.water/WATER_GOAL)*100
    
    def check_steps(self):
        return (self.steps/STEPS_GOAL)*100

    def check_mood(self):
        mood = self.mood.lower().strip()
        if mood in ("sad","stressed","anxious","angry","tired"):
            return "Take a short break, breathe and talk to someone you trust."
        elif mood in ("happy","excited","calm"):
            return "Great mood! Keep up your good habits."
        else:
            return f"Your mood is {mood}."

    def generate_advisory(self):
        advice = []
        category = self.get_bmi_category()
        if category == "Normal":
            advice.append("Your BMI is healthy.")
        else:
            advice.append(f"Your BMI category is {category}. Consider a balanced diet and regular exercise.")

        if self.check_water_intake() < 80:
            advice.append("Drink more water.")

        if self.check_steps() < 70:
            advice.append("Walk more.") 

        advice.append(self.check_mood())
        return advice
if __name__=="__main__":
    person = HealthAnalyzer(weight=60 ,height=160 ,water=1200 ,steps=4000 ,mood="happy")
    print("BMI:", round(person.calculate_bmi(),1))
    print("Category:", person.get_bmi_category())
    print("Water%:", person.check_water_intake())
    print("Steps%:", person.check_steps()) 
    print("Advice:",person.generate_advisory())

