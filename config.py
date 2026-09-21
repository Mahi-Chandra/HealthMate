# 1.DATABASE SETTINGS

DATABASE_FILENAME="healthmate.db"


#2.Health Goals

DAILY_WATER_INTAKE_GOAL=2000  # in milliliters

DAILY_STEP_GOAL=10000  # in steps

#BMI CATEGORIES

BMI_UNDERWEIGHT=18.5
BMI_NORMAL=24.9
BMI_OVERWEIGHT=29.9

BMI_CATEGORIES = {"underweight":"below 18.5", "normal":"18.5-24.9", "overweight":"25-29.9", "obese":"30 and above"}

# 3.APP SETTINGS

APP_TITLE="HealthMate Chatbot"

APP_DESCRIPTION="A chatbot that helps you track your health goals and provides personalized advice."

# HEALTH ADVISORY

HEALTH_ADVISORY_MESSAGES={"underweight":("Your BMI is in underweight range." "Focus on a balanced diet and consult a healthcare professional if you are losing weight unexpectedly."),
                          "normal":("Your BMI is in the normal range." "Maintain your healthy lifestyle and continue to monitor your health." "activity,adequate sleep and good hydration."),
                          "overweight":("Your BMI is in overweight range." "Consider a balanced diet and regular exercise to manage your weight." "Consult a healthcare professional for personalized advice."),
                          "obese":("Your BMI is in obese range." "It's important to consult a healthcare professional for guidance on weight management and overall health." "Focus on a balanced diet, regular physical activity, and lifestyle changes."),
                          "low_water_intake":("Your water intake is below the recommended daily goal." "Increase your water consumption to stay hydrated and support overall health."),
                          "low_steps":("Your step count is below the recommended daily goal." "Consider incorporating more physical activity into your routine to meet your step goal and improve overall fitness.")}


#GENERAL HEALTH DISCLAIMER

HEALTH_DISCLAIMER=("This chatbot provides general health information and is " "not a substitute for professional medical advice, diagnosis, or treatment." "Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition."
                   "consult a healthcare professional before making any changes to your diet, exercise routine, or health regimen." "The information provided by this chatbot is for educational purposes only and should not be relied upon for medical decisions.")
