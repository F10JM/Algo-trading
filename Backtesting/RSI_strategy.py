import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import matplotlib.pyplot as plt
plt.style.use("seaborn-v0_8")

def test_strategy(stock,period,invest):
    data=yf.download(stock,start = "2010-01-01")
    df=data.Close.to_frame()

    df['MA200'] = ta.sma(df['Close'], length=200)
    df['RSI'] = df.ta.rsi(length=period)
    df= df.dropna()

    df["Buy"]=np.where((df["Close"].shift()>df["MA200"].shift()) & (df["RSI"].shift()<30) ,1,0)
    df["Sell"] = 0
    for i in range(len(df)):
        if df.Buy.iloc[i]:
            for j in range(1,11):
                if (df['RSI'].iloc[i+j]>40):
                    df["Sell"].iloc[i+j+1]=1
                    break
                elif j==10:
                    df["Sell"].iloc[i+j+1]=1
                
    Buy_dates=[]
    Sell_dates=[]
    buys=[]
    sells=[]
    open_pos=False

    for i in range(len(df)):
        if df.Buy.iloc[i]:
            if open_pos==False:
                buys.append(i)
                open_pos=True
                Buy_dates.append(df.iloc[i].name)
        elif df.Sell.iloc[i]:
            if open_pos:
                sells.append(i)
                open_pos=False
                Sell_dates.append(df.iloc[i].name)

    if len(buys)>len(sells):
        buys.pop(-1)
        Buy_dates.pop(-1)
    
    
    check=pd.DataFrame({'buydate':Buy_dates,'selldate':Sell_dates,'buyprice':df.loc[Buy_dates].Close.values,'sellprice':df.loc[Sell_dates].Close.values})
    check["pnl_perc"]=(check.sellprice-check.buyprice)/check.buyprice
    check["cumm+pnl_perc"]=(check["pnl_perc"]+1).cumprod()
    
    profits_perc=(df.loc[check.selldate].Close.values-df.loc[check.buydate].Close.values)/df.loc[check.buydate].Close.values
    list_profits=(profits_perc+1).cumprod()
    net_returns_perc=(list_profits[-1]-1).round(3)*100
    
    inv_ret=invest*(profits_perc+1).cumprod()
    return_inv=inv_ret[-1]
    
    large_loss=profits_perc.min().round(3)*100
    large_profit=profits_perc.max().round(3)*100
    win_rate = ((profits_perc > 0).sum() / len(profits_perc) * 100).round(3)

    
    return print("Returns perc= {}%".format(net_returns_perc)), print("Invested return= {}".format(return_inv)), print("Largest Loss= {}%".format(large_loss)), print("Largest Profit= {}%".format(large_profit)), print("Winrate= {}%".format(win_rate)) 
