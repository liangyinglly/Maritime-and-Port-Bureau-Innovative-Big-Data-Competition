import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import ruptures as rpt

#import matplotlib.font_manager
#a=sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
#for i in a:
    #print(i)

plt.rcParams['font.family'] = 'Heiti TC'

# Load the data
file_path = '/Users/liangying/Desktop/Maritime-and-Port-Bureau-Innovative-Big-Data-Competition/兩岸TEU數:噸數:艘次/processed/8.TEU進出轉口合併.csv'  
data = pd.read_csv(file_path)

# Filter data for "出口" (Export) and "來源港" as "高雄港(TWKHH)"
filtered_data = data[(data['進出轉口'] == '進口') & (data['目的港'] == '高雄港(TWKHH)')]

# Convert the '年月' column to datetime format to extract the year
filtered_data['年月'] = pd.to_datetime(filtered_data['年月'])
filtered_data['年'] = filtered_data['年月'].dt.year

# Group by "目的港" and sum the TEU values, then sort by TEU in descending order
grouped_data = filtered_data.groupby('來源港')['TEU'].sum().reset_index()
sorted_data = grouped_data.sort_values(by='TEU', ascending=False)

# Get the top 4 destinations
top_4_destinations = sorted_data.head(4)
# Filter data for the top 4 destinations
top_4_ports = top_4_destinations['來源港'].tolist()
filtered_top_4 = filtered_data[filtered_data['來源港'].isin(top_4_ports)]

# Group by year and destination port, summing the TEU values
annual_teu_top_4 = filtered_top_4.groupby(['年', '來源港'])['TEU'].sum().unstack().fillna(0)
# Filter the data for the years 2016-2023
annual_teu_top_4_filtered = annual_teu_top_4[(annual_teu_top_4.index >= 2016) & (annual_teu_top_4.index <= 2023)]

# Plotting the line chart for the years 2016-2023
plt.figure(figsize=(12, 8))
for port in top_4_ports:
    plt.plot(annual_teu_top_4_filtered.index, annual_teu_top_4_filtered[port], marker='o', label=port)

plt.title('Annual TEU for Top 4 Destination Ports from Kaohsiung (Export) 2016-2023')
plt.xlabel('Year')
plt.ylabel('TEU (in thousands)')
plt.legend()
plt.grid(True)
plt.xticks(annual_teu_top_4_filtered.index)

# Display the plot
plt.show()