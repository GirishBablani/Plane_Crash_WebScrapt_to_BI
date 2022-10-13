import pandas as pd
from bs4 import BeautifulSoup
import requests
global var 

def request():
    try:
        response = requests.get("http://www.planecrashinfo.com/database.htm")
        parser = BeautifulSoup(response.text,'html.parser')
        return parser
    except Exception as e:
        print("Error : Error in getting error")     

def scrap():
    script = request()
    content_block = script.find("body").find_all("table")
    count = 0
    td_count = 1
    for data in content_block:
        count += 1
        if count==2:
            table_row_data = data.find_all("tr")
            for table_data in table_row_data:
                years = table_data.find_all("td")
                for year in years:
                    value = year.text
                    if value.strip().isdigit()==True :
                        year_wise_data(value.strip()) 


def inside_data(value,link):
    detail_responses = requests.get(f"http://www.planecrashinfo.com/{value}/{link}")
    parser_detail = BeautifulSoup(detail_responses.text,'html.parser')
    detail_data = parser_detail.find("table").find_all("tr")
    count = 0
    detail_data_list = []
    for detail_accident_planes in detail_data:
        detail_table_data = detail_accident_planes.find_all("td")
        cn = 0
        for fields in detail_table_data:
            count +=1
            if count !=1:
                cn +=1
                if cn != 1:
                    detail_data_list.append(fields.text)
    return detail_data_list





        
def year_wise_data(value):
    year_table_request = requests.get(f"http://www.planecrashinfo.com/{value}/{value}.htm")
    parser = BeautifulSoup(year_table_request.text,'html.parser')
    year_table_content = parser.find("table").find_all("tr")
    year_data_df = pd.DataFrame(columns=["col1","col2","col3","col4"])
    detail_data_df = pd.DataFrame(columns=["Date","Time","Location","Operator","Flight","Route","AC Type","Registration","cn/ln","Aboard","Fatalities","Ground","Summary"])
    year_columns_data = []
    for year_table_row in year_table_content:
        year_table_data = year_table_row.find_all("td")
        if len(year_columns_data) > 0:
            year_data_df.loc[len(year_data_df)] = year_columns_data
            year_columns_data = []
        for year_table_info in year_table_data:
            year_columns_data.append(year_table_info.text.strip())
            if year_table_info.find("a") is not None:
                inside_link = year_table_info.find("a").attrs["href"]
                detail_df_list = inside_data(value,inside_link)
                detail_data_df.loc[len(detail_data_df)] = detail_df_list
                
    #for last data
    year_data_df.loc[len(year_data_df)] = year_columns_data
    detail_data_df.to_csv(f"Detaildata/detail-data-{value}.csv")        
    year_data_df.to_csv(f"YearwiseAccidentData/data-year-{value}.csv") 
    print(f"File uploaded of year {value}")       

scrap()



