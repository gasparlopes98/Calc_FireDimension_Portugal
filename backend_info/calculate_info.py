import json
from backend_info.calculate_indices import FWICLASS
import urllib, json


class Info:
    def __init__(self,city,dsr,fwi,dc,dmc,bui,ffmc):
        self.city = city
        self.dsr = dsr
        self.fwi = fwi
        self.dc = dc
        self.dmc = dmc
        self.bui = bui
        self.ffmc = ffmc
    
    def toJson(self):
        return {
            "city" : self.city,
            "dsr" : self.dsr,
            "fwi" : self.fwi,
            "dc" : self.dc,
            "dmc" : self.dmc,
            "bui" : self.bui,
            "ffmc" : self.ffmc
        }


weather_data = {
"1210702" : "Aveiro",
"1200562" : "Beja",
"1200576" : "Braga",
"1200575" : "Bragança",
"1200570" : "Castelo Branco",
"1200548" : "Coimbra",
"1200558" : "Évora",
"1200554" : "Faro",
"1210683" : "Guarda",
"1210718" : "Leiria",
"1200535" : "Lisboa",
"1200571" : "Portalegre",
"1200545" : "Porto",
"1210734" : "Santarém",
"1210770" : "Setúbal",
"1200551" : "Viana do Castelo",
"1200567" : "Vila Real",
"1240675" : "Viseu",
"1200522" : "Funchal",
"1200524" : "Porto Santo",
"11217165" : "Santa Maria",
"1210932" : "São Miguel",
"11217430" : "Graciosa",
"1200510" : "São Jorge",
"1200504" : "Ilha do Pico",
"11217710" : "Ilha do Faial",
"1200501" : "Ilha das Flores",
"1200502" : "Ilha do Corvo"
}

url = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"
def get_info():
    f=open('./backend_info/dados.json')

    data = json.load(f)
    info_cidades = []
    for cidade in data['cidades']:
        info_cidades.append(
            Info(
                cidade['cidade'],
                cidade['dsr'],
                cidade['fwi'],
                cidade['dc'],
                cidade['dmc'],
                cidade['bui'],
                cidade['ffmc']
            )
        )
  
    return info_cidades 


def calculate_index_for_city(cityName):
    city = None
    for cities in get_info():
        if cities.city == cityName:
            city = cities
            break
    if city ==None:
        return None    
    weather = get_weather_by_city(get_data_from_ipma(),cityName)
    month = 1
    print(weather)
    temp = weather['temperature']
    wind = weather['wind_speed']
    reletativeHumadity = weather['humidity']
    precipitation = weather['precipitation']
    fwisystem= FWICLASS(temp,reletativeHumadity,wind,precipitation)
    ffmc = fwisystem.FFMCcalc(city.ffmc)
    dmc = fwisystem.DMCcalc(city.dmc,month)
    dc = fwisystem.DCcalc(city.dc,month)
    isi = fwisystem.ISIcalc(ffmc)
    bui = fwisystem.BUIcalc(dmc,dc)
    fwi = fwisystem.FWIcalc(isi,bui)
    return {
        ffmc:ffmc,
        dmc:dmc,
        dc:dc,
        isi:isi,
        bui:bui,
        fwi:fwi
    }



def calculate_index():
    info_cidades = get_info()
    weather_list = get_data_from_ipma()
    for city in info_cidades:
        weather = get_weather_by_city(weather_list,city.city)
        month = 12
        temp = weather['temperature']
        wind = weather['wind_speed']
        reletativeHumadity = weather['humidity']
        precipitation = weather['precipitation']
        fwisystem= FWICLASS(temp,reletativeHumadity,wind,precipitation)
        ffmc = fwisystem.FFMCcalc(city.ffmc)
        dmc = fwisystem.DMCcalc(city.dmc,month)
        dc = fwisystem.DCcalc(city.dc,month)
        isi = fwisystem.ISIcalc(ffmc)
        bui = fwisystem.BUIcalc(dmc,dc)
        fwi = fwisystem.FWIcalc(isi,bui)

def get_weather_by_city(weatherList,city):
    for weather in weatherList:
        if (weather['city']==city):
            return weather
    return None        


def get_data_from_ipma():
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    info_list = []
    time = ""
    for hour in data:
        if (hour.endswith('12:00')):
            time = hour

    for estacao in data[time]:
        if estacao in weather_data:
            if data[time][estacao] != None:
                info_list.append({
                    "city" : weather_data.get(estacao),
                    "wind_speed" : data[time][estacao]['intensidadeVentoKM'],
                    "temperature" : data[time][estacao]['temperatura'],
                    "humidity" : data[time][estacao]['humidade'],
                    "precipitation" : data[time][estacao]['precAcumulada']
                })
        

    
    return info_list

