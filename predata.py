import pandas as pd
from sklearn.impute import KNNImputer

# 讀取原始數據
file_path = '/Users/liangying/Desktop/航港數據競賽/code/兩岸TEU數:噸數:艘次/8.TEU進出轉口合併.csv'
data = pd.read_csv(file_path)

# 查看缺失值情況
print(data.isnull().sum())

# 創建KNNImputer對象
imputer = KNNImputer(n_neighbors=5)

# 對TEU列進行缺失值填補
data[['TEU']] = imputer.fit_transform(data[['TEU']])

# 查看缺失值情況
print(data.isnull().sum())

# 保存處理後的數據到新的CSV文件
data.to_csv('/Users/liangying/Desktop/航港數據競賽/code/兩岸TEU數:噸數:艘次/8.TEU進出轉口合併.csv', index=False)

# 確認處理後的數據
print(data.head())
