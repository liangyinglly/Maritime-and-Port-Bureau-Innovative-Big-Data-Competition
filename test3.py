import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

# 步驟 1: 數據準備
# 讀取數據
file_path = '//Users/liangying/Desktop/航港數據競賽/兩岸TEU數:噸數:艘次/8.TEU進出轉口合併.csv'  # 替換為你的實際文件路徑
data = pd.read_csv(file_path)

# 轉換"年月"為日期時間格式並設置為索引
data['年月'] = pd.to_datetime(data['年月'])
data.set_index('年月', inplace=True)

# 篩選進出口類型
# 可以選擇只分析進口或出口，這裡以進口為例
filtered_data = data[data['進出轉口'] == '進口']

# 分組計算每個來源港和目的港在每個月份的TEU總數
grouped_data = filtered_data.groupby(['年月', '來源港', '目的港'])['TEU'].sum().unstack().fillna(0)

# 選擇一個港口進行分析，這裡以"高雄港(TWKHH)"為例
port_data = grouped_data['高雄港(TWKHH)']

# 步驟 2: 應用STL分解
# 應用STL分解
stl = STL(port_data, seasonal=12)
result = stl.fit()

# 可視化分解結果
plt.figure(figsize=(12, 8))

plt.subplot(411)
plt.plot(result.observed)
plt.title('Observed')

plt.subplot(412)
plt.plot(result.trend)
plt.title('Trend')

plt.subplot(413)
plt.plot(result.seasonal)
plt.title('Seasonal')

plt.subplot(414)
plt.plot(result.resid)
plt.title('Residuals')

plt.tight_layout()
plt.show()
