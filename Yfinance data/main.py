import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Apple = yf.download("AAPL", start = "2010-01-01",end ="2021-01-01")


def test_strategy(stock,start,end,SMA):
    df=yf.download(stock,start=start,end=end)
    data=df.Close.to_frame()
    data["returns"]=np.log(data.Close.div(data.Close.shift(1)))
    data["SMA_S"]=data.Close.rolling(int(SMA[0])).mean()
    data["SMA_L"]=data.Close.rolling(int(SMA[1])).mean()
    data.dropna(inplace=True)
    
    data["position"]=np.where(data["SMA_S"]>data["SMA_L"],1,-1)
    data["strategy"]=data["returns"]*data.position.shift(1)
    data.dropna(inplace=True)
    ret=np.exp(data["strategy"].sum())
    std= data["strategy"].std()*np.sqrt(252)
    
    return ret,std
