import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 讀取處理後的數據
file_path = '/Users/liangying/Desktop/Maritime-and-Port-Bureau-Innovative-Big-Data-Competition/兩岸TEU數:噸數:艘次/processed/8.TEU進出轉口合併.csv'
data = pd.read_csv(file_path)

# 篩選進口數據
data = data[(data['進出轉口'] == '進口') & (data['目的港'] == '高雄港(TWKHH)')]


# 轉換日期欄位
data['年月'] = pd.to_datetime(data['年月'])

# 按月聚合TEU數據
monthly_teu = data.groupby(data['年月'].dt.to_period('M'))['TEU'].sum().reset_index()
monthly_teu['年月'] = monthly_teu['年月'].dt.to_timestamp()

# 分割訓練集和測試集
train_data = monthly_teu[monthly_teu['年月'] < '2022-01-01']
test_data = monthly_teu[(monthly_teu['年月'] >= '2022-01-01') & (monthly_teu['年月'] <= '2022-12-01')]

# 訓練SARIMA模型
sarima_model = SARIMAX(train_data['TEU'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
sarima_result = sarima_model.fit()

# 預測TEU
pred = sarima_result.get_forecast(steps=len(test_data))
pred_ci = pred.conf_int()
test_data['Predicted_TEU'] = pred.predicted_mean.values

# 計算RMSE
mse = mean_squared_error(test_data['TEU'], test_data['Predicted_TEU'])
rmse = mse ** 0.5
print(f'RMSE: {rmse}')

# 繪製實際值與預測值的比較圖
plt.figure(figsize=(12, 6))
plt.plot(train_data['年月'], train_data['TEU'], label='Training Data')
plt.plot(test_data['年月'], test_data['TEU'], label='Actual TEU', color='blue')
plt.plot(test_data['年月'], test_data['Predicted_TEU'], label='Predicted TEU', color='red', linestyle='--')
plt.title('SARIMA Forecast vs Actuals')
plt.xlabel('Month')
plt.ylabel('TEU')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

test_data['Predicted_TEU'] = test_data['Predicted_TEU'].round().astype(int)
test_data['TEU'] = test_data['TEU'].round().astype(int)

# 列出預測的每月TEU數與實際每月TEU數
predicted_vs_actual = test_data[['年月', 'TEU', 'Predicted_TEU']]

# 計算MAE (Mean Absolute Error)
mae = mean_absolute_error(test_data['TEU'], test_data['Predicted_TEU'])

# 計算MAPE (Mean Absolute Percentage Error)
mape = (abs((test_data['TEU'] - test_data['Predicted_TEU']) / test_data['TEU']).mean()) * 100

# 計算RMSE (Root Mean Squared Error)
rmse = mean_squared_error(test_data['TEU'], test_data['Predicted_TEU'], squared=False)



print(predicted_vs_actual , 'mae = {mae}, mape = {mape}, rmse = {rmse}' .format(mae=mae, mape=mape, rmse=rmse))
# 顯示圖表
plt.show()