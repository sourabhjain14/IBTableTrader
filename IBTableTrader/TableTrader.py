#https://www.wintick.com/members/symbolGuide/tda
import time
import pandas as pd
from IPython.display import display
from ipywidgets import widgets
from ipywidgets import interact,interactive, interact_manual, Button, Output, HBox, VBox, Layout
from threading import Thread

import asyncio
import nest_asyncio

import os
import glob
import ast
import json
import csv
import copy
import datetime
import traceback
import functools
import pytz

#import ipyregulartable as rt
import ipysheet
#from ipydatagrid import DataGrid

#import globalvar
#from initialize import g_tick_dict, param, g_param, STRATEGY_LIST
#from trademanager import run_system, run_system_backtester


from ib_insync import *
from ACCOUNT_DETAIL import IP, PORT, CLIENT_ID, MAX_ROW
from IBtrader import get_account_detail, get_ticker
from IBtrader import place_order
from IBtrader import get_open_orders, get_open_trades, get_positions
#from IBtrader import cancel_all_orders, liquidate_all, cancel_order, liquidate_all

from widgetlib import create_button,create_dropdown, create_checkbox



param={}

util.startLoop()  # uncomment this line when in a notebook
global ibprogram
ibprogram = IB()

dl = [{'account':0}]
#dfa  = pd.DataFrame(dl) 
try:
    ibprogram.connect(IP, PORT, clientId=CLIENT_ID)
    #print(ibprogram)
    #acc = ibprogram.accountSummary()
    ibprogram.sleep(2)
    
    print("Connection Established!")
    accdata = get_account_detail(ibprogram)
    #print(accdata)
    #print(type(accdata))
    #print(accdata['accountID'])
    #print("problem")
    dl = [{'AccountID':accdata['accountID'], 'AvailableFunds': accdata['AvailableFunds'], 'BuyingPower': accdata['BuyingPower']}]
    dfa  = pd.DataFrame(dl)
except:
    print("Connection Failed?? Refresh")
    dl = [{'account':0}]
    dfa  = pd.DataFrame(dl)    

account_w = widgets.Textarea(value='',description='Account Details',disabled=False,layout={'width':'100%'},)
account_w.value = dfa.to_string()
    

#symbol_df = pd.read_csv('./nasdaq.csv')
#symbol_list = symbol_df['Symbol'].to_list()


symbol_nasdaq = pd.read_csv('./finvizNASDAQ.csv')
symbol_nasdaq=symbol_nasdaq.dropna()
symbol_nasdaq_list = (symbol_nasdaq['Ticker']).to_list()

symbol_nyse = pd.read_csv('./finvizNYSE.csv')
symbol_nyse=symbol_nyse.dropna()
symbol_nyse_list = symbol_nyse['Ticker'].to_list()

symbol_list_ = symbol_nasdaq_list + symbol_nyse_list

symbol_list = list(set(symbol_list_))



symbol_validity_check_w = create_checkbox(param, "check_symbol_validity", False, tag='check symbol validity')


#print(symbol_list)
    
out_live = widgets.Output()

#out_live.append_stdout(str(dl)+'\n')

MAX_COLUMN = 14
sheet = ipysheet.sheet(rows=MAX_ROW, columns=MAX_COLUMN)
table_w = pd.DataFrame(columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
#table_w.loc = [[None for i in range(MAX_COLUMN)] for j in range(MAX_ROW)]

#table_w_ = pd.DataFrame(columns=['Symbol','Bid','Ask','MaxLoss','EntryPrice','StopPrice','Shares',
#                                '1stTarget','2ndTarget','StopPct','Value','BUY','SELL','Comment'], index=range(30))
#dg = DataGrid(table_w_, editable=True)#,layout={"height": "1000px","width":"100%"})
#table_w = dg.data

MaxLoss_column = 0
EntryPrice_column = 0
StopPrice_column = 0
Shares_column = 0
Target1_column = 0
Target2_column = 0
BUY_column = 0
SELL_column = 0

for i in range(MAX_ROW):
    if i==0:
        j=0
        table_w.loc[i,j] = ipysheet.cell(i, j, 'Symbol',background_color='yellow')
        
        j+=1
        table_w.loc[i,j] = ipysheet.cell(i, j, 'BID',background_color='yellow')
        
        j+=1
        table_w.loc[i,j] = ipysheet.cell(i, j, 'ASK',background_color='yellow')
        
        j+=1
        MaxLoss_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, 'MaxLoss',background_color='yellow')
        
        j+=1
        EntryPrice_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, 'EntryPrice',background_color='yellow')
        
        j+=1
        StopPrice_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, 'StopPrice',background_color='yellow')
        
        j+=1
        Shares_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, 'Shares',background_color='yellow')
        
        j+=1
        Target1_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, '1stTarget',background_color='yellow')
        
        j+=1
        Target2_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, '2ndTarget',background_color='yellow')
        
        j+=1
        table_w.loc[i,j] = ipysheet.cell(i, j, 'StopPct',background_color='yellow')
        j+=1
        table_w.loc[i,j] = ipysheet.cell(i, j, 'Value',background_color='yellow')
        
        j+=1
        BUY_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, 'BUY',background_color='green')
        
        j+=1
        SELL_column = j
        table_w.loc[i,j] = ipysheet.cell(i, j, 'SELL',background_color='red')
        
        j+=1
        table_w.loc[i,j] = ipysheet.cell(i, j, 'Comment',background_color='yellow')
    else:
        for jj in range(MAX_COLUMN):
            if jj==0:
                table_w.loc[i,jj] = ipysheet.cell(i, jj, None,'text',background_color='white')
            elif jj==3:
                table_w.loc[i,jj] = ipysheet.cell(i, jj, 0,'numeric',background_color='red')
            elif jj==4:
                table_w.loc[i,jj] = ipysheet.cell(i, jj, 0,'numeric',background_color='green')
            elif jj==5:
                table_w.loc[i,jj] = ipysheet.cell(i, jj, 0,'numeric',background_color='orange')    
            elif jj==6:
                table_w.loc[i,jj] = ipysheet.cell(i, jj, 0,'numeric',read_only=True)
            else:    
                table_w.loc[i,jj] = ipysheet.cell(i, jj, 0, 'numeric')


                
#print("table built")                






buyt = [None]*MAX_ROW
sellt = [None]*MAX_ROW
for i in range(1,MAX_ROW):
    buyt[i] = create_button(param, "BUY", 0, 'BUY','green')
    sellt[i] = create_button(param, "SELL", 0, 'SELL', 'red')
    table_w.loc[i,11] = ipysheet.cell(i, 11, buyt[i])
    table_w.loc[i,12] = ipysheet.cell(i, 12, sellt[i])

#print("button created")     
    
for i in range(1,MAX_ROW):
    ipysheet.cell(i, 3, 300) # MAX LOSS
    #ipysheet.cell(i, 3, 300) # MAX LOSS

#table_w.loc.loc[1,9]  = 100
#ipysheet.cell(1, 9, b1)
#drp1 = create_dropdown(param, 'symbol_list', symbol_list, 'AAPL', tag='')
#ipysheet.cell(1, 0, drp1)



#out_live_position.clear_output(False)
#with out_live_position:
#    display(sheet)       

#ipysheet.cell(1, 6) = sheet.cell(1, 4) - sheet.cell(1, 5)
def calculate_share(change, i=0):
    try:
        table_w.loc[i,6].value = abs(int(table_w.loc[i,3].value/(table_w.loc[i,EntryPrice_column].value - table_w.loc[i,5].value)))
    except:
        table_w.loc[i,6].value = 0
#table_w.loc.loc[1,4].observe(calculate, 'value')
#table_w.loc.loc[1,5].observe(calculate, 'value')
for r in range(1,MAX_ROW): 
    table_w.loc[r,4].observe(functools.partial(calculate_share, i = r))
    table_w.loc[r,5].observe(functools.partial(calculate_share, i = r))

    
    
def calculate_target1(change, i=0):
    try:
        table_w.loc[i,Target1_column].value = table_w.loc[i,EntryPrice_column].value + (table_w.loc[i,EntryPrice_column].value - table_w.loc[i,5].value)
    except:
        table_w.loc[i,Target1_column].value = 0.0
for r in range(1,MAX_ROW): 
    table_w.loc[r,4].observe(functools.partial(calculate_target1, i = r))
    table_w.loc[r,5].observe(functools.partial(calculate_target1, i = r))

    
    
def calculate_target2(change, i=0):
    try:
        table_w.loc[i,Target2_column].value = table_w.loc[i,EntryPrice_column].value + 2*(table_w.loc[i,EntryPrice_column].value - table_w.loc[i,5].value)
    except:
        table_w.loc[i,Target2_column].value = 0.0
for r in range(1,MAX_ROW): 
    table_w.loc[r,4].observe(functools.partial(calculate_target2, i = r))
    table_w.loc[r,5].observe(functools.partial(calculate_target2, i = r))


    
    
#ipysheet.cell(1, 6) = sheet.cell(1, 4) - sheet.cell(1, 5)
def calculate_stoppct(change, i=0):
    try:
        table_w.loc[i,9].value = 100*(table_w.loc[i,EntryPrice_column].value - table_w.loc[i,5].value)/table_w.loc[i,EntryPrice_column].value
    except:
        table_w.loc[i,9].value = 0
for r in range(1,MAX_ROW): 
    table_w.loc[r,4].observe(functools.partial(calculate_stoppct, i = r))
    table_w.loc[r,5].observe(functools.partial(calculate_stoppct, i = r))


    
    
#ipysheet.cell(1, 6) = sheet.cell(1, 4) - sheet.cell(1, 5)
def calculate_value(change, i=0):
    try:
        table_w.loc[i,10].value = (table_w.loc[i,EntryPrice_column].value * table_w.loc[i,6].value)
    except:
        table_w.loc[i,10].value = 0
for r in range(1,MAX_ROW): 
    table_w.loc[r,4].observe(functools.partial(calculate_value, i = r))
    table_w.loc[r,5].observe(functools.partial(calculate_value, i = r))

    
    

def buy_button(b, i=0):
    b.disabled=True
    b.style.button_color = 'black'
    try:
        symbol = table_w.loc[i,0].value
        price = table_w.loc[i,EntryPrice_column].value
        sl = table_w.loc[i,StopPrice_column].value
        
        size = table_w.loc[i,Shares_column].value
        size1 = int(size/2)
        size2 = int(size - size1)
        
        tp1 = table_w.loc[i,7].value
        tp2 = table_w.loc[i,8].value
        print("BUY1:",symbol,"price:",price,"sl:",sl,"tp:",tp1,"size:",size1)
        place_order(instrument_type='stock',symbol =symbol,orderType='LMT',
                    direction="Buy", size=size1, price=price, TP=tp1, SL=sl,ibprogram=ibprogram)
        print("BUY2:",symbol,"price:",price,"sl:",sl,"tp:",tp2,"size:",size2)
        place_order(instrument_type='stock',symbol =symbol,orderType='LMT',
                    direction="Buy", size=size2, price=price, TP=tp2, SL=sl,ibprogram=ibprogram,adjust=True)
    except:
        print("buy failed for ", table_w.loc[i,0].value)
        out_live.append_stdout("buy failed for "+str(table_w.loc[i,0].value)+'\n')
    b.style.button_color = 'green'
    b.disabled=False


def sell_button(b, i=0):
    b.disabled=True
    b.style.button_color = 'black'
    #time.sleep(5)
    try:
        symbol = table_w.loc[i,0].value
        price = table_w.loc[i,EntryPrice_column].value
        sl = table_w.loc[i,StopPrice_column].value
        
        size = table_w.loc[i,Shares_column].value
        size1 = int(size/2)
        size2 = int(size - size1)

        tp1 = table_w.loc[i,7].value
        tp2 = table_w.loc[i,8].value
        print("SELL1:",symbol,"price:",price,"sl:",sl,"tp:",tp1,"size:",size1)
        place_order(instrument_type='stock',symbol =symbol,orderType='LMT',
                    direction="Sell", size=size1, price=price, TP=tp1, SL=sl,ibprogram=ibprogram)
        print("SELL2:",symbol,"price:",price,"sl:",sl,"tp:",tp2,"size:",size2)
        place_order(instrument_type='stock',symbol =symbol,orderType='LMT',
                    direction="Sell", size=size2, price=price, TP=tp2, SL=sl,ibprogram=ibprogram,adjust=True)
        #print("SELL:",symbol,"price:",price,"sl:",sl,"tp1:",tp1,"tp2:",tp2)
    except:
        print("sell failed for ", table_w.loc[i,0].value)
        out_live.append_stdout("sell failed for "+str(table_w.loc[i,0].value)+'\n')
    b.style.button_color = 'red'
    b.disabled=False

#print("observe method created")



def onTicker(ticker,i):
    table_w.loc[i,1].value = ticker.bid
    table_w.loc[i,2].value = ticker.ask
        
#ipysheet.cell(1, 6) = sheet.cell(1, 4) - sheet.cell(1, 5)
ticker=[None]*30
def calculate_ticker(change, i=0):
    #try:
    symbol = change['new']['value']
    out_live.append_stdout("symbol:"+symbol)
    #symbol = change.new.value
    #out_live.append_stdout("symbol:"+symbol)
    #print(change['new']['value'])
    if symbol_validity_check_w.value==True:
        if symbol not in symbol_list:
            out_live.append_stdout("  not a valid symbol \n")
            #out_live.append_stdout(str(symbol_list))
            return
    #print(change)
    try:
        ticker[i] = get_ticker(ibprogram, symbol)
        #ticker[i].updateEvent += onTicker
        #ticker[i].updateEvent += functools.partial(onTicker, i)
        out_live.append_stdout(str(ticker[i]))
        table_w.loc[i,1].value = ticker[i].bid
        table_w.loc[i,2].value = ticker[i].ask
        table_w.loc[i,13].value = ticker[i].close       
    except:
        out_live.append_stdout("ticker fetch failed for "+str(symbol)+'\n')
        table_w.loc.loc[i,1].value = 0
        table_w.loc.loc[i,2].value = 0
for r in range(1,MAX_ROW): 
    table_w.loc[r,0].observe(functools.partial(calculate_ticker, i = r))

#print("ticker created")
   
    
    
# button creation fails in first attempt sometimes    
try:    
    for r in range(1,MAX_ROW):
        table_w.loc[r,11].value.on_click(functools.partial(buy_button, i = r))
        table_w.loc[r,12].value.on_click(functools.partial(sell_button, i = r))
except:
    for r in range(1,MAX_ROW):
        table_w.loc[r,11].value.on_click(functools.partial(buy_button, i = r))
        table_w.loc[r,12].value.on_click(functools.partial(sell_button, i = r))

#print("button click created")




'''
[Order(orderId=365, clientId=999, permId=20397575, action='SELL', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=198.0, tif='GTC', ocaGroup='20397573', ocaType=3, parentId=363, rule80A='0', trailStopPrice=198.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', deltaNeutralOpenClose='?', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='STP', triggerPrice=200.0, adjustedStopPrice=199.0, cashQty=0.0, dontUseAutoPriceForHedge=True), Order(orderId=364, clientId=999, permId=20397574, action='SELL', totalQuantity=150.0, orderType='LMT', lmtPrice=201.0, auxPrice=0.0, tif='GTC', ocaGroup='20397573', ocaType=3, parentId=363, rule80A='0', openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', deltaNeutralOpenClose='?', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), Order(orderId=363, clientId=999, permId=20397573, action='BUY', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=199.0, tif='GTC', ocaType=3, rule80A='0', trailStopPrice=199.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', deltaNeutralOpenClose='?', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), Order(orderId=361, clientId=999, permId=20397572, action='SELL', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=198.0, tif='GTC', ocaGroup='20397570', ocaType=3, parentId=359, rule80A='0', trailStopPrice=198.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', deltaNeutralOpenClose='?', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), Order(orderId=360, clientId=999, permId=20397571, action='SELL', totalQuantity=150.0, orderType='LMT', lmtPrice=200.0, auxPrice=0.0, tif='GTC', ocaGroup='20397570', ocaType=3, parentId=359, rule80A='0', openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', deltaNeutralOpenClose='?', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), Order(orderId=359, clientId=999, permId=20397570, action='BUY', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=199.0, tif='GTC', ocaType=3, rule80A='0', trailStopPrice=199.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', deltaNeutralOpenClose='?', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True)]
'''




'''
TRADES:[Trade(contract=Stock(conId=76792991, symbol='TSLA', right='?', exchange='SMART', currency='USD', localSymbol='TSLA', tradingClass='NMS'), order=Order(orderId=365, clientId=999, permId=20397575, action='SELL', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=198.0, tif='GTC', ocaGroup='20397573', ocaType=3, parentId=363, rule80A='0', trailStopPrice=198.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='STP', triggerPrice=200.0, adjustedStopPrice=199.0, cashQty=0.0, dontUseAutoPriceForHedge=True), orderStatus=OrderStatus(orderId=365, status='PreSubmitted', filled=0.0, remaining=150.0, avgFillPrice=0.0, permId=20397575, parentId=363, lastFillPrice=0.0, clientId=999, whyHeld='child,trigger', mktCapPrice=0.0), fills=[], log=[TradeLogEntry(time=datetime.datetime(2023, 2, 11, 11, 52, 59, 1507, tzinfo=datetime.timezone.utc), status='PreSubmitted', message='')]), Trade(contract=Stock(conId=76792991, symbol='TSLA', right='?', exchange='SMART', currency='USD', localSymbol='TSLA', tradingClass='NMS'), order=Order(orderId=364, clientId=999, permId=20397574, action='SELL', totalQuantity=150.0, orderType='LMT', lmtPrice=201.0, auxPrice=0.0, tif='GTC', ocaGroup='20397573', ocaType=3, parentId=363, rule80A='0', openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), orderStatus=OrderStatus(orderId=364, status='PreSubmitted', filled=0.0, remaining=150.0, avgFillPrice=0.0, permId=20397574, parentId=363, lastFillPrice=0.0, clientId=999, whyHeld='child', mktCapPrice=0.0), fills=[], log=[TradeLogEntry(time=datetime.datetime(2023, 2, 11, 11, 52, 59, 4510, tzinfo=datetime.timezone.utc), status='PreSubmitted', message='')]), Trade(contract=Stock(conId=76792991, symbol='TSLA', right='?', exchange='SMART', currency='USD', localSymbol='TSLA', tradingClass='NMS'), 0, order=Order(orderId=363, clientId=999, permId=20397573, action='BUY', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=199.0, tif='GTC', ocaType=3, rule80A='0', trailStopPrice=199.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), orderStatus=OrderStatus(orderId=363, status='PreSubmitted', filled=0.0, remaining=150.0, avgFillPrice=0.permId=20397573, parentId=0, lastFillPrice=0.0, clientId=999, whyHeld='trigger', mktCapPrice=0.0), fills=[], log=[TradeLogEntry(time=datetime.datetime(2023, 2, 11, 11, 52, 59, 4510, tzinfo=datetime.timezone.utc), status='PreSubmitted', message='')]), Trade(contract=Stock(conId=76792991, symbol='TSLA', right='?', exchange='SMART', currency='USD', localSymbol='TSLA', tradingClass='NMS'), order=Order(orderId=361, clientId=999, permId=20397572, action='SELL', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=198.0, tif='GTC', ocaGroup='20397570', ocaType=3, parentId=359, rule80A='0', trailStopPrice=198.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), orderStatus=OrderStatus(orderId=361, status='PreSubmitted', filled=0.0, remaining=150.0, avgFillPrice=0.0, permId=20397572, parentId=359, lastFillPrice=0.0, clientId=999, whyHeld='child,trigger', mktCapPrice=0.0), fills=[], log=[TradeLogEntry(time=datetime.datetime(2023, 2, 11, 11, 52, 59, 4510, tzinfo=datetime.timezone.utc), status='PreSubmitted', message='')]), Trade(contract=Stock(conId=76792991, symbol='TSLA', right='?', exchange='SMART', currency='USD', localSymbol='TSLA', tradingClass='NMS'), order=Order(orderId=360, clientId=999, permId=20397571, action='SELL', totalQuantity=150.0, orderType='LMT', lmtPrice=200.0, auxPrice=0.0, tif='GTC', ocaGroup='20397570', ocaType=3, parentId=359, rule80A='0', openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), orderStatus=OrderStatus(orderId=360, status='PreSubmitted', filled=0.0, remaining=150.0, avgFillPrice=0.0, permId=20397571, parentId=359, lastFillPrice=0.0, clientId=999, whyHeld='child', mktCapPrice=0.0), fills=[], log=[TradeLogEntry(time=datetime.datetime(2023, 2, 11, 11, 52, 59, 4510, tzinfo=datetime.timezone.utc), status='PreSubmitted', message='')]), Trade(contract=Stock(conId=76792991, symbol='TSLA', right='?', exchange='SMART', currency='USD', localSymbol='TSLA', tradingClass='NMS'), order=Order(orderId=359, clientId=999, permId=20397570, action='BUY', totalQuantity=150.0, orderType='STP', lmtPrice=0.0, auxPrice=199.0, tif='GTC', ocaType=3, rule80A='0', trailStopPrice=199.0, openClose='', eTradeOnly=False, firmQuoteOnly=False, volatilityType=0, deltaNeutralOrderType='None', referencePriceType=0, account='DU3502935', clearingIntent='IB', adjustedOrderType='None', cashQty=0.0, dontUseAutoPriceForHedge=True), orderStatus=OrderStatus(orderId=359, status='PreSubmitted', filled=0.0, remaining=150.0, avgFillPrice=0.0, permId=20397570, parentId=0, lastFillPrice=0.0, clientId=999, whyHeld='trigger', mktCapPrice=0.0), fills=[], log=[TradeLogEntry(time=datetime.datetime(2023, 2, 11, 11, 52, 59, 4510, tzinfo=datetime.timezone.utc), status='PreSubmitted', message='')])]
'''




'''
try:
    loop = asyncio.get_event_loop()
except RuntimeError as ex:
    if "There is no current event loop in thread" in str(ex):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        nest_asyncio.apply()
        asyncio.get_event_loop()
'''
nest_asyncio.apply()
#util.patchAsyncio()
#util.patchAsyncio()
#openorders = ibprogram.reqAllOpenOrders()
#print(openorders[0].totalQuantity)

#opentrades =  ibprogram.openTrades()
#ibprogram.sleep(2)

TRADETABLE_COLUMN = 8
TRADETABLE_ROW = MAX_ROW*3
tradesheet = ipysheet.sheet(rows=TRADETABLE_ROW, columns=TRADETABLE_COLUMN)
tradetable_w = pd.DataFrame(columns=['A','B','C','D','E','F','G','H'])

for i in range(TRADETABLE_ROW):
    for j in range(TRADETABLE_COLUMN):
        if i==0: tradetable_w.loc[i,j] = ipysheet.cell(i, j, None,background_color='yellow')
        else: tradetable_w.loc[i,j] = ipysheet.cell(i, j, None)
        
        
def fill_tradetable(opentrades):
    k=0
    tradetable_w.loc[k,0].value = "symbol"
    tradetable_w.loc[k,1].value = "action"
    tradetable_w.loc[k,2].value = "orderType"
    tradetable_w.loc[k,3].value = "totalQuantity"
    tradetable_w.loc[k,4].value = "lmtPrice"
    tradetable_w.loc[k,5].value = "auxPrice"
    tradetable_w.loc[k,6].value = "ID"
    tradetable_w.loc[k,7].value = "parentID"
    
    #opentrades_sorted = []
    trade_dict = {}
    trade_id = []
    for trade in opentrades:
        tid = trade.order.orderId
        trade_id.append(tid)
        trade_dict[tid] = trade
    trade_id.sort()
        
    
    for i in range(1,TRADETABLE_ROW):
        for j in range(TRADETABLE_COLUMN):
            tradetable_w.loc[i,j].value = None
    
    #for trade in opentrades:
    for key in trade_id:
        trade = trade_dict[key]
        k+=1
        #print(trade.contract.symbol, trade.order.totalQuantity,
        #trade.order.action,trade.order.orderType,
        #trade.order.lmtPrice, trade.order.auxPrice)
        tradetable_w.loc[k,0].value = trade.contract.symbol
        tradetable_w.loc[k,1].value = trade.order.action
        tradetable_w.loc[k,2].value = trade.order.orderType
        tradetable_w.loc[k,3].value = trade.order.totalQuantity
        tradetable_w.loc[k,4].value = trade.order.lmtPrice
        tradetable_w.loc[k,5].value = trade.order.auxPrice
        tradetable_w.loc[k,6].value = trade.order.orderId
        tradetable_w.loc[k,7].value = 'MAIN' if trade.order.parentId==0 else trade.order.parentId
        #tradetable_w.loc[k,7].background_color='blue'


async def orderTable():
    orders=None
    tz = pytz.timezone('US/Eastern')
    old_minute=-1
    while(True):
        now = datetime.datetime.now()
        nowtz = now.astimezone(tz)
        clocktime = 100*nowtz.hour+nowtz.minute
        new_minute=nowtz.minute
        if new_minute!=old_minute:
            #new_now = nowtz
            #print("EST Time:",nowtz)
            out_live.append_stdout("Time:"+str(nowtz)+'\n')
            #table_w.loc[1,4].value = nowtz.hour 
            #table_w.loc[1,5].value = nowtz.minute 
            old_minute = new_minute
            #try:
            #with await ibprogram.connectAsync():
            #orders = get_open_orders(ibprogram)
            
            #openorders =  ibprogram.reqAllOpenOrders()
            #openorders =  ibprogram.openOrders()
            
            try:
                opentrades = ibprogram.openTrades()
                ibprogram.sleep(2)
                fill_tradetable(opentrades)
            except:
                pass
            #k=1
            #for trade in opentrades:
            #    k+=1
            #    table_w.loc[k,0].value = trade.contract.symbol
            #    table_w.loc[k,6].value = trade.order.totalQuantity
            
            #ibprogram.sleep(2)
            #orders = asyncio.get_event_loop.run_until_complete(get_open_orders(ibprogram))
            #await orders
            #reqtrades = ib.openTrades()
            #ibprogrm.sleep(2)
            
            #orders = asyncio.get_event_loop.run_until_complete(ibprogram.sleep(2))
            #out_live.append_stdout("ORDERS:"+str(openorders)+'\n')
            #out_live.append_stdout("TRADES:"+str(opentrades)+'\n')
            #print("ORDERS: ",openorders)
            #except:
            #    print("orders fetch failed")
        else:
            await asyncio.sleep(1)
#asyncio.get_event_loop().create_task(orderTable())
#asyncio.get_event_loop.create_task(ibprogram.reqAllOpenOrders())

#asyncio.run(orderTable())
#asyncio.ensure_future(orderTable())
#asyncio.ensure_future(secondWorker())
#loop.run_forever()
#loop.run_until_complete(orderTable())
#task = loop.create_task(orderTable())
#await asyncio.sleep(0)

'''
        tasks = [asyncio.ensure_future(client.receiveMessage(connection)),
                 asyncio.ensure_future(client.sendMessage(login_encoded)),
                 asyncio.ensure_future(client.receiveMessage(connection)),
                 asyncio.ensure_future(client.sendMessage(data_encoded)),
                 asyncio.ensure_future(client.receiveMessage(connection))]
        loop.run_until_complete(asyncio.wait(tasks))
'''


#out_live_table.clear_output()
#with out_live_table:
#    display(sheet)



#tabletradesheet
#supertab = widgets.VBox([account_w, symbol_validity_check_w, sheet, out_live])

#global supertab
#supertab=None
async def create_supertab():
    supertab_contents = ['Order Placement','Trades']
    supertab = widgets.Tab()
    supertab.set_title(0, 'Order Placement')
    supertab.set_title(1,'Trades')
    tabletradetab1 = widgets.VBox([account_w, symbol_validity_check_w, sheet, out_live])
    tabletradetab2  = widgets.VBox([tradesheet])
    supertab.children = [tabletradetab1 , tabletradetab2]
    return supertab
            



async def main():
    t1 = asyncio.get_event_loop().create_task(orderTable())
    await asyncio.sleep(0)
    supertab = asyncio.get_event_loop().run_until_complete(create_supertab())
    await asyncio.sleep(0)
    return supertab
    #await t2
    #await asyncio.get_event_loop().run_in_executor()
    #supertab
    #await t
supertab = asyncio.run(main())
#asyncio.get_event_loop().run_until_complete(main())



