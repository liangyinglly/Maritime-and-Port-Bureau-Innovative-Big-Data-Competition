import pandas as pd
import matplotlib.pyplot as plt

# 讀取CSV文件
file_path = '/Users/liangying/Desktop/123/taiwan_gdp_cpi_ppi.csv'  
taiwan_data = pd.read_csv(file_path)

# 確保數據中沒有缺失值並進行必要的數據清洗
taiwan_data['消費者物價(CPI)'] = taiwan_data['消費者物價(CPI)'].str.rstrip('%').astype('float') / 100.0
taiwan_data['生產者物價(PPI)'] = taiwan_data['生產者物價(PPI)'].str.rstrip('%').astype('float') / 100.0

# 繪製數據圖表
plt.figure(figsize=(12, 8))

# GDP
plt.subplot(3, 1, 1)
plt.plot(taiwan_data['Year'], taiwan_data['GDP(億新臺幣)'], marker='o')
plt.title('Taiwan GDP (億新臺幣)')
plt.xlabel('Year')
plt.ylabel('GDP (億新臺幣)')

# CPI
plt.subplot(3, 1, 2)
plt.plot(taiwan_data['Year'], taiwan_data['消費者物價(CPI)'], marker='o')
plt.title('Taiwan CPI')
plt.xlabel('Year')
plt.ylabel('CPI')

# PPI
plt.subplot(3, 1, 3)
plt.plot(taiwan_data['Year'], taiwan_data['生產者物價(PPI)'], marker='o')
plt.title('Taiwan PPI')
plt.xlabel('Year')
plt.ylabel('PPI')

plt.tight_layout()
plt.show()
