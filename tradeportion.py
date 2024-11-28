import pandas as pd
import chardet
from io import StringIO

# Step 1: Detect the file encoding
file_path = '/Users/liangying/Downloads/9bce0729-14f1-433c-bb57-f176d488746f.csv'

with open(file_path, 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f'The file encoding is: {encoding}')

# Step 2: Decode the content with the detected encoding
decoded_content = raw_data.decode(encoding, errors='ignore')

# Step 3: Use StringIO to read the decoded content into a pandas DataFrame
data = pd.read_csv(StringIO(decoded_content))


# 選擇可能影響TEU數與貿易量的變量
relevant_columns = [
    '國內生產毛額(GDP) 年(月)別',  # GDP in different currencies and time periods
    'GDP(億新臺幣)', 
    'GDP(億人民幣)', 
    'GDP(億美元)', 
    '經濟成長率', 
    '消費者物價(CPI)', 
    '生產者物價(PPI)', 
    '居民消費價格(CPI)', 
    '外匯存底(億美元)', 
    '  匯率(新臺幣兌1美元)', 
    '   匯率(人民幣兌1美元)', 
    '實際利用金額(億美元)', 
    '實際利用金額成長率(億美元)', 
    '實際利用金額(億人民幣)', 
    '實際利用金額成長率(億人民幣)'
]

filtered_data = data[relevant_columns].dropna()

# Print the first five rows of the DataFrame
print(filtered_data.head())