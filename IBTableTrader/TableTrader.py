#https://www.wintick.com/members/symbolGuide/tda
import time
import pandas as pd
from IPython.display import display
from ipywidgets import widgets
from ipywidgets import interact,interactive, interact_manual, Button, Output, HBox, VBox, Layout
from threading import Thread
import asyncio
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
from ipydatagrid import DataGrid

#import globalvar
#from initialize import g_tick_dict, param, g_param, STRATEGY_LIST
#from trademanager import run_system, run_system_backtester


from ib_insync import *
from ACCOUNT_DETAIL import IP, PORT, CLIENT_ID, MAX_ROW
from IBtrader import get_account_detail, get_ticker
from IBtrader import place_order
from IBtrader import get_open_orders, get_open_trades
#from IBtrader import cancel_all_orders, liquidate_all, cancel_order, liquidate_all

from widgetlib import create_button,create_dropdown





util.startLoop()  # uncomment this line when in a notebook
global ibprogram
ibprogram = IB()

try:
    ibprogram.connect(IP, PORT, clientId=CLIENT_ID)
    #print(ibprogram)
    #acc = ibprogram.accountSummary()
    ibprogram.sleep(2)
    
    #print("Connection Established!")
    accdata = get_account_detail(ibprogram)
    #print(accdata)
    dl = [{'AccountID':accdata['accountID'], 'AvailableFunds': accdata['AvailableFunds'], 'BuyingPower': accdata['BuyingPower']}]
    dfa  = pd.DataFrame(dl)
except:
    print("Connection Failed? Refresh")
    dl = [{'account':0}]
    dfa  = pd.DataFrame(dl)    


    
param = {}
symbol_df = pd.read_csv('./nasdaq.csv')
symbol_list = symbol_df['Symbol'].to_list()
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
                    direction="Buy", size=size2, price=price, TP=tp2, SL=sl,ibprogram=ibprogram)
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
                    direction="Sell", size=size2, price=price, TP=tp2, SL=sl,ibprogram=ibprogram)
        #print("SELL:",symbol,"price:",price,"sl:",sl,"tp1:",tp1,"tp2:",tp2)
    except:
        print("sell failed for ", table_w.loc[i,0].value)
        out_live.append_stdout("sell failed for "+str(table_w.loc[i,0].value)+'\n')
    b.style.button_color = 'red'
    b.disabled=False

#print("observe method created")

        
#ipysheet.cell(1, 6) = sheet.cell(1, 4) - sheet.cell(1, 5)
ticker=[None]*30
def calculate_ticker(change, i=0):
    #try:
    symbol = change['new']['value']
    out_live.append_stdout("symbol:"+symbol)
    #symbol = change.new.value
    #out_live.append_stdout("symbol:"+symbol)
    #print(change['new']['value'])
    if symbol not in symbol_list:
        out_live.append_stdout("  not a valid symbol \n")
        #out_live.append_stdout(str(symbol_list))
        return
    #print(change)
    try:
        ticker[i] = get_ticker(ibprogram, symbol)
        out_live.append_stdout(str(ticker[i]))
        table_w.loc[i,1].value = ticker[i].bid
    except:
        out_live.append_stdout("ticker fetch failed for "+str(symbol)+'\n')
        table_w.loc.loc[i,10].value = 0
for r in range(1,MAX_ROW): 
    table_w.loc[r,0].observe(functools.partial(calculate_ticker, i = r))

#print("ticker created")
    
try:    
    for r in range(1,MAX_ROW):
        table_w.loc[r,11].value.on_click(functools.partial(buy_button, i = r))
        table_w.loc[r,12].value.on_click(functools.partial(sell_button, i = r))
except:
    for r in range(1,MAX_ROW):
        table_w.loc[r,11].value.on_click(functools.partial(buy_button, i = r))
        table_w.loc[r,12].value.on_click(functools.partial(sell_button, i = r))

#print("button click created")



#out_live_table.clear_output()
#with out_live_table:
#    display(sheet)
account_w = widgets.Textarea(
    value='',
    #placeholder='',
    description='Account Details',
    disabled=False,
    layout={'width':'100%'},)
account_w.value = dfa.to_string()

#tabletradesheet
supertab = widgets.VBox([account_w, sheet, out_live])

#supertab_contents = ['System']
#supertab = widgets.Tab()
#supertab.children = [tabletradesheet]
#supertab.set_title(0, 'System')

