import datetime
import double_top_bottom as dtb
# date,open,close,high,low,volume
data = [[],[],[],[],[]]
with open('data/tcs.txt') as file:
    for line in file:
        items = line.strip().split(',')
        date = datetime.datetime.strptime(items[0], '%Y-%m-%d %H:%M:%S%z')
        values = [float(item) for item in items[1:]]

        data[0].append(date)
        data[1].append(values[0])
        data[2].append(values[1])
        data[3].append(values[2])
        data[4].append(values[3])
        # data[5].append(values[4])

# print(data)

import plotly.graph_objects as go

data1 = go.Ohlc(x=data[0],
                   open=data[1],
                   high=data[3],
                   low=data[4],
                   close=data[2])

layout = dict(title="tcs")
fig = go.Figure(data=data1, layout=layout)
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()

double_top_bottom_calculator = dtb.double_top_bottom(5)
for i in range(data[0].__len__()):
    double_top_bottom_calculator.zigzag(i, {'low': data[4][i], 'high': data[3][i], 'date': data[0][i]})
    double_top, double_bottom = double_top_bottom_calculator.calculate_double_pattern()
    if(double_top or double_bottom):
        print('detected')