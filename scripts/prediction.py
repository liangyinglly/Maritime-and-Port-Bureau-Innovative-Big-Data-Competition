import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from statsmodels.tsa.stattools import adfuller

# 讀取處理後的數據
file_path = '/Users/liangying/Desktop/Maritime-and-Port-Bureau-Innovative-Big-Data-Competition/兩岸TEU數:噸數:艘次/processed/8.TEU進出轉口合併.csv'
data = pd.read_csv(file_path)

# 將日期列轉換為datetime格式
data['年月'] = pd.to_datetime(data['年月'])

# 設置日期列為索引
data.set_index('年月', inplace=True)

# 篩選轉口數據
transship_data = data[data['進出轉口'] == '轉口']

# 按日期重采樣，計算每個月的總TEU數
monthly_teu_transship = transship_data['TEU'].resample('M').sum().dropna()

# 轉換數據為數組格式
teu_values = monthly_teu_transship.values.reshape(-1, 1)

# 使用LocalOutlierFactor進行離群值檢測和移除
lof = LocalOutlierFactor(n_neighbors=20)
outliers = lof.fit_predict(teu_values)

# 過濾離群值
cleaned_teu = monthly_teu_transship[outliers == 1]

# 計算每月的累積平均和變異數
size = len(cleaned_teu)
cumulative_mean = np.zeros(size)
cumulative_var = np.zeros(size)

for i in range(size):
    cumulative_mean[i] = cleaned_teu[:i+1].mean()
    cumulative_var[i] = cleaned_teu[:i+1].var()

# 檢查時間序列的穩定性
def adf_test(timeseries):
    adf_result = adfuller(timeseries)
    print('ADF Statistic: %f' % adf_result[0])
    print('p-value: %f' % adf_result[1])
    for key, value in adf_result[4].items():
        print('Critical Values:')
        print(f'   {key}, {value}')

print("ADF Test for Original Data:")
adf_test(monthly_teu_transship)

print("\nADF Test for Cleaned Data:")
adf_test(cleaned_teu)

# 繪製結果
plt.figure(figsize=(14, 10))

# 原始數據
plt.subplot(411)
plt.plot(monthly_teu_transship, label='Original Monthly TEU (Transship)', color='blue')
plt.legend(loc='upper left')
plt.title('Original Monthly TEU (Transship)')

# 移除離群值後的數據
plt.subplot(412)
plt.plot(cleaned_teu, label='Monthly TEU without Outliers (Transship)', color='green')
plt.legend(loc='upper left')
plt.title('Monthly TEU (Transship) without Outliers')

# 累積平均數
plt.subplot(413)
plt.plot(cleaned_teu.index, cumulative_mean, label='Cumulative Mean TEU', color='red')
plt.legend(loc='upper left')
plt.title('Cumulative Mean of Monthly TEU (Transship)')

# 累積變異數
plt.subplot(414)
plt.plot(cleaned_teu.index, cumulative_var, label='Cumulative Variance TEU', color='orange')
plt.legend(loc='upper left')
plt.title('Cumulative Variance of Monthly TEU (Transship)')

plt.tight_layout()
plt.show()
