import tkinter as tk
from tkinter import font, messagebox
import requests
import json
from datetime import datetime

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x600")
        self.root.config(bg="#1a1a1a")
        
        # API endpoint (Open-Meteo - free, no API key needed)
        self.weather_api = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_api = "https://geocoding-api.open-meteo.com/v1/search"
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(
            self.root,
            text="Weather Dashboard",
            font=title_font,
            bg="#1a1a1a",
            fg="#00ccff"
        )
        title.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg="#1a1a1a")
        search_frame.pack(pady=10)
        
        search_label = tk.Label(
            search_frame,
            text="City:",
            font=("Helvetica", 12),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        search_label.pack(side=tk.LEFT, padx=5)
        
        self.city_entry = tk.Entry(search_frame, width=30, font=("Helvetica", 12))
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.insert(0, "New York")
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Helvetica", 12),
            bg="#00ccff",
            fg="#000000",
            command=self.fetch_weather,
            width=10
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Main display frame
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current weather frame
        current_frame = tk.Frame(self.main_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        current_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # City and date
        self.city_label = tk.Label(
            current_frame,
            text="Loading...",
            font=("Helvetica", 20, "bold"),
            bg="#2a2a2a",
            fg="#00ccff"
        )
        self.city_label.pack(pady=10)
        
        # Weather info grid
        info_frame = tk.Frame(current_frame, bg="#2a2a2a")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Temperature
        self.temp_label = tk.Label(
            info_frame,
            text="--°C",
            font=("Helvetica", 60, "bold"),
            bg="#2a2a2a",
            fg="#ff9900"
        )
        self.temp_label.pack()
        
        # Condition and details
        self.condition_label = tk.Label(
            info_frame,
            text="--",
            font=("Helvetica", 16),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        self.condition_label.pack(pady=10)
        
        # Details frame
        details_frame = tk.Frame(current_frame, bg="#2a2a2a")
        details_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.humidity_label = tk.Label(
            details_frame,
            text="Humidity: --%",
            font=("Helvetica", 12),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        self.humidity_label.pack(side=tk.LEFT, padx=10)
        
        self.wind_label = tk.Label(
            details_frame,
            text="Wind: -- km/h",
            font=("Helvetica", 12),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        self.wind_label.pack(side=tk.LEFT, padx=10)
        
        self.pressure_label = tk.Label(
            details_frame,
            text="Pressure: -- hPa",
            font=("Helvetica", 12),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        self.pressure_label.pack(side=tk.LEFT, padx=10)
        
        # Load initial weather
        self.fetch_weather()
    
    def get_coordinates(self, city):
        """Get latitude and longitude from city name"""
        try:
            params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            response = requests.get(self.geocoding_api, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return result["latitude"], result["longitude"], result["name"]
            else:
                messagebox.showerror("Error", "City not found!")
                return None, None, None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get coordinates: {str(e)}")
            return None, None, None
    
    def fetch_weather(self):
        """Fetch weather data from API"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return
        
        # Get coordinates
        lat, lon, city_name = self.get_coordinates(city)
        if lat is None:
            return
        
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,pressure_msl",
                "temperature_unit": "celsius",
                "wind_speed_unit": "kmh"
            }
            
            response = requests.get(self.weather_api, params=params)
            response.raise_for_status()
            data = response.json()
            
            self.display_weather(data, city_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather: {str(e)}")
    
    def get_weather_description(self, code):
        """Get weather description from WMO code"""
        codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail"
        }
        return codes.get(code, "Unknown")
    
    def display_weather(self, data, city_name):
        """Display weather data in UI"""
        current = data["current"]
        
        # Update city label
        self.city_label.config(text=city_name)
        
        # Update temperature
        temp = current["temperature_2m"]
        self.temp_label.config(text=f"{temp}°C")
        
        # Update condition
        weather_code = current["weather_code"]
        condition = self.get_weather_description(weather_code)
        self.condition_label.config(text=condition)
        
        # Update details
        humidity = current["relative_humidity_2m"]
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        
        wind = current["wind_speed_10m"]
        self.wind_label.config(text=f"Wind: {wind} km/h")
        
        pressure = current["pressure_msl"]
        self.pressure_label.config(text=f"Pressure: {pressure} hPa")

if __name__ == "__main__":
    root = tk.Tk()
    dashboard = WeatherDashboard(root)
    root.mainloop()
