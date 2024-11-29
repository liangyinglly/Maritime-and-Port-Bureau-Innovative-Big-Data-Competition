import pandas as pd
import matplotlib.pyplot as plt

file_path = '/Users/liangying/Desktop/Maritime-and-Port-Bureau-Innovative-Big-Data-Competition/兩岸TEU數:噸數:艘次/raw/兩岸貿易統計.csv'
data = pd.read_csv(file_path)

data['期間'] = pd.to_numeric(data['期間'], errors='coerce')
data_filtered = data[(data['期間'] >= 2003) & (data['期間'] <= 2023)]

plt.figure(figsize=(12, 8))
plt.plot(data_filtered['期間'], data_filtered['我國對中國大陸及香港-出口(我國海關統計)(百萬美元)'], label='Exports to China and Hong Kong (Taiwan Customs)', marker='o')
plt.plot(data_filtered['期間'], data_filtered['我國自中國大陸及香港-進口(我國海關統計)(百萬美元)'], label='Imports from China and Hong Kong (Taiwan Customs)', marker='o')
plt.plot(data_filtered['期間'], data_filtered['我國對中國大陸及香港-貿易總額(我國海關統計)(百萬美元)'], label='Total Trade with China and Hong Kong (Taiwan Customs)', marker='o')

plt.xlabel('Year')
plt.ylabel('Trade Value (Million USD)')
plt.title('Taiwan Trade with China and Hong Kong (2003-2023)')
plt.legend()
plt.grid(True)
plt.xticks(data_filtered['期間'], rotation=45)
plt.tight_layout()
plt.show()