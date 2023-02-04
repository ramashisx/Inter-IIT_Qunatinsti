import pandas as pd
import numpy as np
import os

x = os.listdir('15m')

for t in x:
    try:
        aa = pd.read_csv("15m/"+t)
        xx = []
        for i in range(len(aa)):
            if aa.Date[i][-5:-3] == '00':
                xx.append([aa.Date[i],
                          aa.Open[i-3],
                          max(aa.High[i-3:i+1]),
                          min(aa.Low[i-3:i+1]),
                          aa.Close[i],
                          sum(aa.Volume[i-3:i+1])])
        Frame = pd.DataFrame(xx, columns = aa.columns)
        Frame.to_csv("1hr/"+t,index=False)
        print(t)
    except:
        pass