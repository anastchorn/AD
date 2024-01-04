import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import seaborn as sns
df = pd.read_csv('chronic_kidney_disease.txt',sep=",", names= ['age','bp', 'sg','al','su','rbc','pc','pcc','ba','bgr','bu','sc',
                'sod','pot','hemo','pcv','wbcc','rbcc','htn','dm','cad','appet','pe','ane','class'], on_bad_lines='skip')
print(df.head(10))
count=0
df.replace("?", pd.NA, inplace=True)
print(df.isnull().sum())

df.dropna(inplace=True)
print(df)
columns_to_convert = ['sg','bgr','bu','sc','sod','pot','hemo','pcv','wbcc','rbcc']
for column in columns_to_convert:
    df[column] = df[column].astype(float)


columns_to_convert = ['age', 'bp','al','su']
for column in columns_to_convert:
    df[column] = df[column].astype(int)


# plt.scatter(df['age'], df['hemo'])
# plt.title('Scatter Plot: Age vs Blood Pressure')
# plt.xlabel('Age')
# plt.ylabel('Blood Pressure')
# plt.show()



def standardize_columns(df, columns):

    df_std = df.copy()

    for column in columns:
        mean_val = df[column].mean()
        std_val = df[column].std()

        new_col_name = f"{column}_std"
        df_std[new_col_name] = (df[column] - mean_val) / std_val

    return df_std

columns_to_standardize = ['age', 'bp','sg','al','su','bgr','bu','sc','sod','pot','hemo','pcv','wbcc','rbcc']
df_standardized = standardize_columns(df, columns_to_standardize)
print(df_standardized)
# plt.scatter(df_standardized['age_std'], df_standardized['hemo_std'])
# plt.title('Scatter Plot: Age vs Blood Preasure Standart')
# plt.xlabel('Age')
# plt.ylabel('Blood Pressure')
# plt.show()




custom_bins = [-2,-1.75,-1.5,-1,0,0.25,0.5,0.75,1,2]
plt.hist(df_standardized['bp_std'], bins=custom_bins, edgecolor='black')

# plt.xlabel('Значення')
# plt.ylabel('Кількість елементів')
# plt.title('Гістограма з 10 діапазонами')
# plt.show()


attribute1 = 'age'
attribute2 = 'bp'


correlation_coefficient_pearson, _ = pearsonr(df[attribute1], df[attribute2])
print(f"Коефіцієнт Пірсона між {attribute1} та {attribute2}: {correlation_coefficient_pearson}")


correlation_coefficient_spearman, _ = spearmanr(df[attribute1], df[attribute2])
print(f"Коефіцієнт Спірмена між {attribute1} та {attribute2}: {correlation_coefficient_spearman}")

df_encoded = pd.get_dummies(df, columns=['appet'], prefix=['appet'])
df_encoded['appet_good'] = df_encoded['appet_good'].astype(int)
df_encoded['appet_poor'] = df_encoded['appet_poor'].astype(int)
print(df_encoded)
g = sns.PairGrid(df, vars=['bp','sg','al','su'],
                 hue='age', palette='RdBu_r')
g.map(plt.scatter, alpha=0.8)
g.add_legend();

plt.show()

