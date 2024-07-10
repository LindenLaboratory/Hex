from googlesearch import search
import requests
from bs4 import BeautifulSoup

def search_web(query):
    text,n,txt = [],3,""
    for link in search(query, num_results=n):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text.append([paragraph.get_text() for paragraph in paragraphs[:2]])
    for t in text:
        txt = txt + "\n".join(t)
    return txt
def summarise_data(link):
    text,txt = [],""
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text.append([paragraph.get_text() for paragraph in paragraphs[:6]])
    for t in text:
        txt = txt + "\n".join(t)
    return txt
def get_current_weather(location, format):
    api_key = '67003984a95c4d3886c53240231806'
    base_url = 'http://api.weatherapi.com/v1/current.json'
    params = {'key': api_key,'q': location,'format': format}
    response = requests.get(base_url, params=params);data = response.json();temperature,info = data['current']['temp_' + format[0]],data['current']['condition']['text']
    return [str(temperature), str(info)]
def get_n_day_weather_forecast(location, format, num_days):
    api_key,base_url = '67003984a95c4d3886c53240231806','http://api.weatherapi.com/v1/forecast.json';params = {'key': api_key,'q': location,'format': format,'days': num_days};response = requests.get(base_url, params=params);data,forecast = response.json(),[]
    for day in data['forecast']['forecastday']:
        date,temperature,weather_info = day['date'],day['day']['avgtemp_' + format[0]],day['day']['condition']['text'];forecast.append(f"Date: {str(date)} Temperature: {str(temperature)} Weather: {str(weather_info)}")
    return forecast
