import requests

api_key = '09de91caf3b6d3d1c4739bf430ece1a2'

user_input = input("Enter City: ")

daily= 'current'

# weather_data = requests.get(
#     f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}&exclude={daily}")
 
weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}&exclude={daily}")  
    

weather = weather_data.json()['weather'][0]['main']
rain = round(float(weather_data.json().get('rain', {}).get('1h', 0)), 3)

precipitation = rain * 24

if 70 <= precipitation <= 101 :
    print ("There is a possibility of flooding")
elif precipitation >= 102 :
    print("Floods are sure to happen")
    
else :
    print("Normal")

print(f"The weather in {user_input} is: {weather}")
print(f"The rain in {user_input} is: {precipitation} mm/24h" )

# print(weather_data.json())    