import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

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
monthly_teu_transship = transship_data['TEU'].resample('M').sum()

# 進行時間序列分解
decomposition = sm.tsa.seasonal_decompose(monthly_teu_transship, model='additive')

# 繪製分解結果
plt.figure(figsize=(12, 10))
plt.title('Transship TEU Time Series Decomposition')

plt.subplot(411)
plt.plot(decomposition.observed, label='Observed')
plt.legend(loc='upper left')

plt.subplot(412)
plt.plot(decomposition.trend, label='Trend', color='orange')
plt.legend(loc='upper left')

plt.subplot(413)
plt.plot(decomposition.seasonal, label='Seasonal', color='green')
plt.legend(loc='upper left')

plt.subplot(414)
plt.scatter(decomposition.resid.index, decomposition.resid, label='Residual', color='red', s=10)
plt.axhline(y=0, color='black', linestyle='--')
plt.legend(loc='upper left')

plt.tight_layout()
plt.show()
