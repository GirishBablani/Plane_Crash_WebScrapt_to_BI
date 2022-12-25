import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def ScrapAccidentData(parser,year):
    YearsTable = parser.find("table").find_all("tr")
    RecordsList = []
    for dates in YearsTable:
        links = dates.find("td").find("a")
        if links is not None:
            DatesLink = links.attrs["href"]
            DetailData = requests.get(f"http://www.planecrashinfo.com/{year}/{DatesLink}")
            DataHtml = BeautifulSoup(DetailData.text,'html.parser')
            DataTable = DataHtml.find("table").find_all("td")
            count = 1
            DataList = []
            for data in DataTable:
                if count%2==0:
                    DataList.append(data.text)
                    count += 1
                else:
                    count += 1
            DataList.pop(0)        
            RecordsList.append(DataList)        
    PlanesDbData = pd.DataFrame(data=RecordsList,columns=["Date","Time","Location","Operator","Flight","Route","AC Type","Registration","Construction Number/Line or Fuselage Number","Aboard","Fatalities","Ground","Summary"])                
    PlanesDbData.to_csv(f"Planes_Db_Files/{year}.csv")

def YearWiseData():
    for i in range(1920,2023):
        response = requests.get(f"http://www.planecrashinfo.com/{i}/{i}.htm")
        parser = BeautifulSoup(response.text,'html.parser')
        ScrapAccidentData(parser,i)


YearWiseData()