import pandas as pd
import time
import cProfile
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#завдання у виконанні Pandas
df=pd.read_csv('household_power_consumption.txt',sep=";",low_memory=False)
# print( df.head())
df=df.dropna()
columns_to_convert = ["Global_active_power", "Global_reactive_power", "Voltage",
                      "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]
for column in columns_to_convert:
    df[column] = df[column].astype(float)

#1
start_time = time.time()
Ptask_1=df[df["Global_active_power"]>5]
end_time = time.time()
execution_time = (end_time - start_time)
print("Pandas Task 1 "+str(execution_time))


#2
start_time = time.time()
Ptask_2=df[df["Voltage"]>235]
end_time=time.time()
execution_time = (end_time - start_time)
print("Pandas Task 2 "+str(execution_time))


#3
start_time = time.time()
Ptask_3 = df[(df["Global_intensity"]>=19) & (df["Global_intensity"]<=20)]
Ptask_3 = df[df["Sub_metering_2"]>df["Sub_metering_3"]]
end_time = time.time()
execution_time = (end_time - start_time)
print("Pandas Task 3 "+str(execution_time))


#4
start_time = time.time()
sample=df.sample(5*10**5)
avg_1=sample["Sub_metering_1"].mean()
avg_2=sample["Sub_metering_2"].mean()
avg_3=sample["Sub_metering_3"].mean()
end_time=time.time()
execution_time = (end_time - start_time)
print("Pandas Task 4 "+str(execution_time))


#5
start_time=time.time()
Ptask_5_1 = df[(df["Time"] >= "18:00:00") & (df["Global_active_power"] >= 6)]
Ptask_5_2=Ptask_5_1[(Ptask_5_1["Sub_metering_2"]>Ptask_5_1["Sub_metering_1"])&(Ptask_5_1["Sub_metering_2"]>Ptask_5_1["Sub_metering_3"])]
half_top = Ptask_5_2.head(int(Ptask_5_2.shape[0]/2))
half_bottom = Ptask_5_2.tail(int(Ptask_5_2.shape[0]/2))
half_top_every_3rd = half_top.iloc[::3,:]
half_bottom_every_4th = half_bottom.iloc[::4,:]
end_time=time.time()
execution_time = (end_time - start_time)
print("Pandas Task 5 "+str(execution_time))

#Завдання у виконанні NumPy
array=df.to_numpy()
 #1
start_time=time.time()
numtask1=array[array[:,2]>5]
end_time=time.time()
execution_time = (end_time - start_time)
print("NumPy Task 1 "+str(execution_time))

#2
start_time = time.time()
numtask2=array[array[:,4]>235]
end_time=time.time()
execution_time = (end_time - start_time)
print("NumPy Task 2 "+str(execution_time))

#3
start_time=time.time()
numtask31=array[(array[:,5]>=19) & (array[:,5]<=20)]
numtask3=array[array[:,6]>array[:,7]]
end_time=time.time()
execution_time = (end_time - start_time)
print("NumPy Task 3 "+str(execution_time))

#4
start_time=time.time()
np.random.shuffle(array)
task41 = array[0:500000]
np_avg_1 = np.mean(task41[:,6])
np_avg_2 = np.mean(task41[:,7])
np_avg_3 = np.mean(task41[:,8])
end_time=time.time()
execution_time = (end_time - start_time)
print("NumPy Task 4 "+str(execution_time))

#5
start_time=time.time()
task51 = array[(array[:,1] >= "18:00:00") & (array[:,2]>6)]
task52 = task51[(task51[:,7] > task51[:,6])& (task51[:,7]>task51[:,8])]
array_head=task52[0:int(len(task52)/2):3]
array_tail = task52[int(len(task52)/2)::4]
end_time=time.time()
execution_time = (end_time - start_time)
print("NumPy Task 5 "+str(execution_time))

print(array_head , array_tail)
