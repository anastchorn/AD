from spyre import server
from datetime import datetime, timedelta
import pandas as pd
import urllib.request
import cherrypy
import json
import sys


new={1:22,2:24,3:23,4:25,5:3,6:4,7:8,8:19,9:20,10:21,11:9,12:0,13:10,14:11,15:12,16:13,17:14,18:15,19:16,20:-1,21:17,22:18,23:6,24:1,25:2,26:7,27:5}

def newIndex(a):
    a=int(a)
    return new[a]
def oldIndex(a):
    a=int(a)
    for key,value in new.items():
        if value==a:
            return key
def getData():
       
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
        cont = []
        a=1
        b=28
        
        for i in range(a,b):
            url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID="+str(i)+"&year1=1981&year2=2023&type=Mean"
            wp = urllib.request.urlopen(url)
            text = wp.read()
            now = datetime.now()
            date_and_time_time = now.strftime("%d%m%Y%H%M%S")
            out = open('NOAA_ID'+str(i)+'_'+date_and_time_time+'.csv','wb')
            out.write(text)
            out.close()
   
        
            df = pd.read_csv('NOAA_ID'+str(i)+'_'+date_and_time_time+'.csv', header = 1, names = headers)
            df.at[0, 'Year'] = df.at[1, 'Year']
            df = df.drop([len(df)-1])
            df = df.drop(df.loc[df['VHI'] == -1].index)
        
            df['area'] = i
            df["area"].replace({i:newIndex(i)}, inplace = True)
            cont.append(df)
        td = pd.concat(cont)
        print(td)
        print(td.loc[df["area"] != 111, ["VHI", "Year"]])
        return td
td=getData()
class StockExample(server.App):
    title = "NOAA_data visualisation"
    inputs = [{        "type":'dropdown',
                    "label": 'NOAA_data dropdown',
                    "options" : [ {"label": "VCI", "value":"VCI"},
                                  {"label": "TCI", "value":"TCI"},
                                  {"label": "VHI", "value":"VHI"}],
                    "key": 'ticker',
                    "action_id": "update_data"},
                {        "type":'dropdown',
                    "label": 'Obl',
                    "options" : [ {"label": "Cherkasy", "value":"1"},
                                  {"label": "Chernihiv", "value":"2"},
                                  {"label": "Chernivtsi", "value":"3"},
                                  {"label": "Crimea", "value":"4"},
                                  {"label": "Dnipropetrovs'k", "value":"5"},
                                  {"label": "Donets'k", "value":"6"},
                                  {"label": "Ivano-Frankivs'k", "value":"7"},
                                  {"label": "Kharkiv", "value":"8"},
                                  {"label": "Kherson", "value":"9"},
                                  {"label": "Khmel'nyts'kyy", "value":"10"},
                                  {"label": "Kiev", "value":"11"},
                                  {"label": "Kiev City", "value":"12"},
                                  {"label": "Kirovohrad", "value":"13"},
                                  {"label": "Luhans'k", "value":"14"},
                                  {"label": "L'viv", "value":"15"},
                                  {"label": "Mykolayiv", "value":"16"},
                                  {"label": "Odessa", "value":"17"},
                                  {"label": "Poltava", "value":"18"},
                                  {"label": "Rivne", "value":"19"},
                                  {"label": "Sevastopol", "value":"20"},
                                  {"label": "Sumy", "value":"21"},
                                  {"label": "Ternopil", "value":"22"},
                                  {"label": "Transcarpathia", "value":"23"},
                                  {"label": "Vinnytsya", "value":"24"},
                                  {"label": "Volyn", "value":"25"},
                                  {"label": "Zaporizhzhya", "value":"26"},
                                  {"label": "Zhytomyr", "value":"27"},
                                   {
            "type": 'dropdown',
            "label": 'Select Year',
            "options": [{"label": year, "value": year} for year in range(1981, 2023)],
            "key": 'selected_year',
            "action_id": "update_data"
                                        }


                                  ],
                    "action_id": "update_data"},
              dict( type='text',
                    key='words',
                    label='діапазон тижнів',
                    value='',
                    action_id='simple_html_output')
                



              ]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True },
                dict( type='html',
                     tab= "range",
                     id='simple_html_output')]
    def getHTML(self, params):
        words = params["words"]
        return words
    def getData(self, params):
        global td
        t=td
        ticker = params['ticker']
        obl=params['obl']
        obl=newIndex(obl)
        selected_year = int(params['selected_year'])


        rangeS=params['words']
        parts = rangeS.split('-')
        part1 = int(parts[0])  
        part2 = int(parts[1])
        if part2<part1:
            part2=part1+1
       t = t.loc[(t['area']==obl)&]
     return t


        

    def getPlot(self, params,):
        global td
        t=td
        ticker = params['ticker']
        obl=params['obl']
        obl=newIndex(obl)

        
        rangeS=params['words']
        parts = rangeS.split('-')
        part1 = int(parts[0])  
        part2 = int(parts[1])
        if part2<part1:
            t=[(t["area"] == obl) & (t["Week"] >= part1) & (t["Week"] <= part2) & (t["Year"] == selected_year),[ticker, "Year"]
         ]

        t = t.set_index('Year')
        plt_obj = t.plot()
        
        
        plt_obj.set_xlabel("Year")
        plt_obj.set_ylabel(ticker)

        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch(port=8080)
