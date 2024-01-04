
import urllib.request
import pandas as pd
from datetime import datetime, timedelta
new={1:22,2:24,3:23,4:25,5:3,6:4,7:8,8:19,9:20,10:21,11:9,12:0,13:10,14:11,15:12,16:13,17:14,18:15,19:16,20:-1,21:17,22:18,23:6,24:1,25:2,26:7,27:5}


def start(a=1,b=28,c=1,c1=3,d=2023):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    cont = []
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
    for i in range(c,c1):
        print("VHI")
        VHI(newIndex(i),d,td)
        print("VHIAll")
        VHIAll(newIndex(i),td)
    drought(td)
        
    
    
   
    
    
 
        
def newIndex(a):
    return new[a];
def oldIndex(a):
    for key,value in new.items():
        if value==a:
            return key;

def VHI(index,year,dd):
    
    
    
    print(dd[(dd["area"] == index) & (dd["Year"] == str(year))]['VHI'])
    min_v = dd[(dd.Year.astype(str)==str(year)) ]['VHI'].min()
    max_v = dd[(dd.Year.astype(str)==str(year)) ]['VHI'].max()
    print(min_v,max_v)
def VHIAll(index,dd):
    print(dd.loc[dd["area"] == index, ["VHI", "Year"]])
    
def drought(df):
    df_drought = df[(df.VHI <= 15)]
    print("Посуха, інтенсивність якої від середньої до надзвичайної:")
    print(df_drought)
    df_drought2 = df[(df.VHI <= 35)]
    print("Посуха, інтенсивність якої від помірної до надзвичайної:")
    print(df_drought2)
    df_drought3 = df[(df.VHI <= 40)]
    print("Стресові умови:")
    print(df_drought3)
    df_ndrought = df[(df.VHI > 60)]
    print("Сприятливі умови:")
    print(df_ndrought)
start()

