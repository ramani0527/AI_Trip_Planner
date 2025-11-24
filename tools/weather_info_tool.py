import os
from utils.weather_info import WeatherForecastTool 
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool

class WeatherIfnoTool:
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHEMAP_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()
        
        
    def _setup_tools(self)-> List:
        # set up al tools for the wather forecast tool
        @tool
        def get_current_weather(city: str) ->List:

            """Get Current weather for city"""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp = weather_data.get('main', {}).get('temp','N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}, {desc}"
            return f"could not fetch forcast for {city}" 
       
    
    
        @tool
        def get_weather_forecast(city: str) ->List:

            """Get weather forecast for city"""
            forecast_data = self.weather_service.get_current_weather(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = [] 
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i] 
                    date = item['dt_txt'].split(' ')[0]      
                    temp = item['main']['temp']
                    desc = item['weather'] [0]['description']
                    forecast_summary.append(f"{date}:{temp} degree celcius, {desc}")
                return f"Weather forecast for {city}\n" + "\n".join(forecast_summary)
            return f"could not fetch forcast for {city}"    
            
        return [get_current_weather, get_weather_forecast]    
            
            
            
            
            
            
            
            
            
            return f"Current weather forecast for  {city}:/n" = "\n".join(forecast_summary)
        return f"could not fetch forcast for {city}"
    
    

