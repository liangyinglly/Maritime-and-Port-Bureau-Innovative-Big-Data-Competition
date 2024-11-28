import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Step 1: Data Preparation
# Load the data
file_path = '/Users/liangying/Desktop/航港數據競賽/code/兩岸TEU數:噸數:艘次/8.TEU進出轉口合併.csv'  
data = pd.read_csv(file_path)

# 將日期欄位轉換為datetime格式
data['年月'] = pd.to_datetime(data['年月'])

# 設置日期欄位為索引
data.set_index('年月', inplace=True)

# 创建一个新的列，以便按月份分组
data['Month'] = data.index.month

# 按年份和月份分组，计算每月的总TEU数
monthly_teu_by_year = data.groupby([data.index.year, data['Month']])['TEU'].sum().unstack(level=0)

# 绘制每年的时间序列图（叠图）
plt.figure(figsize=(14, 8))

for year in monthly_teu_by_year.columns:
    plt.plot(monthly_teu_by_year.index, monthly_teu_by_year[year], label=f'{year}')

plt.title('Monthly TEU Over Years')
plt.xlabel('Month')
plt.ylabel('TEU')
plt.xticks(monthly_teu_by_year.index, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Year')
plt.show()