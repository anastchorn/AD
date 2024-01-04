import matplotlib.pyplot as plt
from spyre import server
from datetime import datetime, timedelta
import pandas as pd
import urllib.request
new={1:22,2:24,3:23,4:25,5:3,6:4,7:8,8:19,9:20,10:21,11:9,12:0,13:10,14:11,15:12,16:13,17:14,18:15,19:16,20:-1,21:17,22:18,23:6,24:1,25:2,26:7,27:5}

def newIndex(a):
    a=int(a)
    return new[a]
def oldIndex(a):
    a=int(a)
    for key,value in new.items():
        if value==a:
            return key
def getDataset():

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
        td["Year"] = td["Year"].astype(int)
        td["Week"] = td["Week"].astype(int)
       # print(td)
        print(td.loc[df["area"] != 111, ["VHI", "Week"]])
        return td
df=getDataset()

class MyWebApp(server.App):
    title = "Веб-додаток з випадаючим списком"

    inputs = [
        {
            "type": "dropdown",
            "label": "Виберіть параметр",
            "options": [{"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"},
                        {"label": "VHI", "value": "VHI"}],
            "key": "param"
        },
        {
            "type": "dropdown",
            "label": "Виберіть область",
            "options": [{"label": "Cherkasy", "value":"1"},
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
                                  {"label": "Zhytomyr", "value":"27"}],
            "key": "region"
        },
        {
            "type": "text",
            "label": "Введіть інтервал місяців",
            "key": "months_interval",
            "value": "1-52"
        },
        {
            "type": "dropdown",
            "label": "Виберіть рік",
            "options": [{"label": str(year), "value": str(year)} for year in range(1983, 2024)],
            "key": "year"

        }
    ]

    controls = [
        {
            "type": "button",
            "label": "Оновити",
            "id": "update_button"
        }
    ]

    tabs = ["Таблиця", "Графік"]

    outputs = [
        {
            "type": "table",
            "id": "table_output",
            "tab": "Таблиця",
            "control_id": "update_button"
        },
        {
            "type": "plot",
            "id": "plot_output",
            "tab": "Графік",
            "control_id": "update_button"
        }
    ]


    def getData(self, params):
        global df
        # Отримуємо дані з df за вибраними параметрами
        selected_param = params["param"]
        selected_region = params["region"]
        selected_region = newIndex(selected_region)
        selected_year = int(params["year"])
        week=params["months_interval"]
        week0 = int(week[0:week.find("-")])
        week1 = int(week[week.find("-")+1:])
        tf=df.copy()
        tf = tf[tf["Year"] == selected_year]
        tf = tf[tf["area"] == selected_region]
        if week0>=week1:
            cell=week0
            week0=week1
            week1=cell
        selected_data = tf.loc[ (tf['Week']>=week0)&(tf['Week']<=week1), [selected_param, "Week"]]

        return selected_data

    def getPlot(self, params):
        data = self.getData(params)
        data = data.set_index('Week')
        plt_obj = data.plot(y=params['param'])
        plt_obj.set_xlabel("Week")
        plt_obj.set_ylabel(params['param'])
        fig = plt_obj.get_figure()
        return fig


# Запускаємо веб-додаток
app = MyWebApp()
app.launch()
