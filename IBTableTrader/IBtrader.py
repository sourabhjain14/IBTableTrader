import pandas as pd
from ib_insync import *
#from ib_insync import ib, Contract, MarketOrder, Option, Forex, Stock
from ACCOUNT_DETAIL import IP, PORT, CLIENT_ID
import datetime
#from initialize import g_bar_dict
#import globalvar

def get_access_token():
    return 'xyz'




def get_positions(ibprogram):
    util.startLoop()  # uncomment this line when in a notebook
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
    
    #account: str
    #contract: Contract
    #position: float
    #avgCost: float
    reqpos = ib.positions()
    ib.sleep(2)
    
    #print('REQPOS',reqpos)
    
    
    curPosDictList = []
    for p in reqpos:
        #sym=p.contract.symbol
        #pos = int(p.position)
        curPosDict = {}
        curPosDict['symbol'] = p.contract.localSymbol
        curPosDict['position'] = p.position
        curPosDict['avgCost'] = p.avgCost
        curPosDictList.append(curPosDict)
        #curPosDict['shortQuantity'] = pos if pos < 0 else 0
        #curPosDict['longQuantity'] = pos if pos > 0 else 0            
    
    if already_connected == False:
        ib.disconnect()
        
    return curPosDictList





def get_symbol_positions(symbol, ibprogram):
    util.startLoop()  # uncomment this line when in a notebook
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
    
    #account: str
    #contract: Contract
    #position: float
    #avgCost: float
    reqpos = ib.positions()
    ib.sleep(2)
    print(reqpos)
    
    
    
    curPosDict = {}
    curPosDict['shortQuantity'] = 0
    curPosDict['longQuantity'] = 0
    for p in reqpos:
        sym=p.contract.symbol
        if sym==symbol:
            pos = int(p.position)
            print(symbol, pos)
            curPosDict['shortQuantity'] = pos if pos < 0 else 0
            curPosDict['longQuantity'] = pos if pos > 0 else 0
            break            
    
    if already_connected == False:
        ib.disconnect()
    
    return curPosDict






def get_quote(ibprogram=None, symbol=None, secType=None, exchange=None, expiry=None, strike=None, optionType=None):    
    util.startLoop()  # uncomment this line when in a notebook
    #print('fetchig quote')
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    #print("already_connected:",already_connected)
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
    
    contract = None
    #spx = Index('SPX', 'CBOE')
    if secType=='Index':    
        contract = Index(symbol, exchange)
    elif secType=='Option':
        contract=Option(symbol, expiry, strike, optionType, exchange, tradingClass='SPXW')
           
    #print(contract)
    #ib.sleep(4)
    
    ib.qualifyContracts(contract)
    ib.reqMarketDataType(1)
    [ticker] = ib.reqTickers(contract)
    ib.sleep(2)
    #print(ticker)
    Value = ticker.marketPrice()
    print(Value)
    
    if already_connected == False:
        ib.disconnect()
    
    return Value  
    
    
    
    
    
    
def get_ticker(ibprogram=None, symbol=None, instrument_type='stock'):
    util.startLoop()  # uncomment this line when in a notebook
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    #print("already_connected:",already_connected)
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
    
    
     
    if instrument_type=='stock':
        contract = Contract()
        contract.symbol = symbol
        contract.secType='STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
    else:
        return None
    
    
    ib.qualifyContracts(contract)
    ib.reqMarketDataType(3)
    [ticker] = ib.reqTickers(contract)
    ib.sleep(2)
    #print(tickers)
    
    
    if already_connected == False:
        ib.disconnect()
    
    return ticker   
    
    
        
    
    

def place_order(instrument_type='stock', symbol = 'AAPL', orderType='MKT', direction="Buy", size=1, price=0.0, priceOffset=0.0, TP=0.0, SL=0.0, TSL=0.0, TIF='GTC', outsideRTH=False, ibprogram=None, expiry='20200228', strike=300, optionType='C', tradingClass='',adjust=False,adjustTriggerPrice=0.0, adjustPrice=0.0):
    util.startLoop()  # uncomment this line when in a notebook
    #print("get data connecting IB")
    
    #print("place order ibprogram:",ibprogram)
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print('connection failed, please check whether IB TWS/Gateway is running in background')
            return None
    else:
        ib = ibprogram
    
    
    expiry = expiry.replace('-','')
    
    closedirection = "Sell" if direction=="Buy" else "Buy"
    
    if priceOffset==0 and price==0:
        orderType='MKT'
        
    
    
    
    if instrument_type=='stock':
        contract = Contract()
        contract.symbol = symbol
        contract.secType='STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
    elif instrument_type=='option':
        contract=Option(symbol, expiry, strike, optionType, "CBOE", tradingClass=tradingClass)
        
    
    
    ib.qualifyContracts(contract)
    
    
    if (orderType=='MKT') or (orderType=='LMT' and price==0):
        [ticker] = ib.reqTickers(contract)
        ltp = ticker.marketPrice()
    
    bracket = []
    
    
    if orderType=='MKT':
        price=ltp
        order=MarketOrder(direction, size)
    elif orderType=='LMT':
        if price>0.0:
            #order=LimitOrder(direction, size, price)
            #order=StopLimitOrder(direction, size, price, price)
            #order=StopOrder(direction, size, price)
            order = Order()
            order.action = direction
            order.orderType = "STP"
            order.auxPrice = price
            order.totalQuantity = size
        else:
            price = round(ltp*(1-0.01*priceOffset) if direction=="Buy" else ltp*(1+0.01*priceOffset), 2)
            order=LimitOrder(direction, size, price)
    order.orderId=ib.client.getReqId()
    #order.trailStopPrice = 2.0
    order.tif = TIF
    order.outsideRth = outsideRTH
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    if TP>0 or SL>0 or TSL>0: order.transmit=False
    bracket.append(order)   
    
    
    
    #trade=ib.placeOrder(contract, order)
    #ib.sleep(2)
    #print(trade)    
    
    
    #parentOrderId = ib.client.getReqId()
    #print(parentOrderId)
    
    '''Target Profit'''
    if TP>0:
        TPPrice = round(TP,1) #round(price*(1+0.01*TP) if direction=="Buy" else price*(1-0.01*TP), 2)
        tpOrder=LimitOrder(closedirection, size, TPPrice)
        tpOrder.parentId = order.orderId
        tpOrder.eTradeOnly = False
        tpOrder.firmQuoteOnly = False
        if SL>0 or TSL>0:
            tpOrder.transmit=False
        bracket.append(tpOrder)
    #print(tpOrder)
    
    #tradeTP=ib.placeOrder(contract, tpOrder)
    #ib.sleep(2)
    #print(tradeTP) 
    
    '''Stop Loss'''
    if SL>0 and adjust==False:
        SLPrice = round(SL,1) #round(price*(1-0.01*SL) if direction=="Buy" else price*(1+0.01*SL), 2)
        slOrder=StopOrder(closedirection, size, SLPrice)
        slOrder.parentId = order.orderId
        slOrder.eTradeOnly = False
        slOrder.firmQuoteOnly = False
        if TSL>0:
            slOrder.transmit=False
        bracket.append(slOrder)    
    
    
    '''Adjustable Stop Loss'''
    if SL>0 and adjust==True:
        # Attached order is a conventional STP order in opposite direction
        attachedOrderStopPrice=round(SL,1)
        slOrder = StopOrder(closedirection, size, attachedOrderStopPrice)
        slOrder.parentId = order.orderId
        #When trigger price is penetrated
        triggerPrice= round(0.5*(price + TPPrice),2)
        slOrder.triggerPrice = triggerPrice
        #The parent order will be turned into a STP order
        slOrder.adjustedOrderType = "STP"
        #With the given STP price
        adjustStopPrice=price
        slOrder.adjustedStopPrice = adjustStopPrice
        
        slOrder.eTradeOnly = False
        slOrder.firmQuoteOnly = False
        if TSL>0:
            slOrder.transmit=False
        bracket.append(slOrder) 
    
    
    '''Trailing Stop Loss'''    
    if TSL>0:
        TSLPrice = round(TSL,1) #round(0.01*price*TSL,2) #round(price*(1-0.01*TSL) if direction=="Buy" else price*(1+0.01*TSL), 2)
        tslOrder=StopOrder(closedirection, size, TSLPrice)
        tslOrder.parentId = order.orderId
        tslOrder.orderType = "TRAIL"
        tslOrder.auxPrice = TSLPrice
        tslOrder.eTradeOnly = False
        tslOrder.firmQuoteOnly = False
        tslOrder.transmit=True
        bracket.append(tslOrder)
    
    
    
    #test_order_state = ib.whatIfOrder(bars.contract, test_order)
    #test_trade=[]
    #for ordr in bracket:
    #    test_order_state = ib.whatIfOrder(contract=contract, order=ordr)
    #    print('test_order_state.initMarginAfter: ', test_order_state.initMarginAfter)
        #test_trade.append(order_res)
    
    
    
    trade=[]
    for ordr in bracket:
        order_res = ib.placeOrder(contract=contract, order=ordr)
        print('Order Placed with ID: ',order_res.order.orderId)
        trade.append(order_res)
    
    #print(trade)
    #bkt = BracketOrder(order, tpOrder, slOrder)
    #bktTrade=ib.placeOrder(contract, bkt)
    #ib.sleep(2)
    
    if already_connected == False:
        ib.disconnect()
    
    
    return trade


def place_option_order(symbol = 'NFLX', expiry='20200228', strike=300, optionType="C", direction="Buy", size=1):
    #util.startLoop()  # uncomment this line when in a notebook
    #print("get data connecting IB")
    ib = IB()
    ib.connect(IP, PORT, clientId=CLIENT_ID)
    
    contract=Option(symbol, expiry, strike, optionType,"SMART")
    ib.qualifyContracts(contract)
    
    order=MarketOrder(direction, size)
    trade=ib.placeOrder(contract, order)
    
    ib.disconnect()
    
    return trade


def get_open_orders(ibprogram):
    util.startLoop()  # uncomment this line when in a notebook
    #dacc = pd.read_csv("access.csv")
    #print(dacc)
    #IP = dacc['IP'][0]
    #port=dacc['port'][0]
    #clientId=dacc['clientId'][0]
    #print(IP,port,clientId)
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
    
    #print(df)
    
    openorders =  ib.reqAllOpenOrders()
    #print("Open Orders: ",openorders)
    #return
    
    #reqtrades = ib.openTrades()
    ib.sleep(2)
    if already_connected == False:
        ib.disconnect()
    
    
    #print("Trades: ")
    #print(reqtrades)
    return openorders





def get_open_trades(ibprogram):
    util.startLoop()  # uncomment this line when in a notebook
    #dacc = pd.read_csv("access.csv")
    #print(dacc)
    #IP = dacc['IP'][0]
    #port=dacc['port'][0]
    #clientId=dacc['clientId'][0]
    #print(IP,port,clientId)
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
            #ib.connect(IP, port, clientId=clientId)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
        
    
    reqtrades = ib.openTrades()
    ib.sleep(2)
    
    
    if already_connected == False:
        ib.disconnect()
    
    
    #print("Trades: ")
    #print(reqtrades)
    return reqtrades
    
    
    
    
    
    
def get_account_detail(ibprogram=None):
    util.startLoop()  # uncomment this line when in a notebook
    #dacc = pd.read_csv("access.csv")
    #print(dacc)
    #IP = dacc['IP'][0]
    #port=dacc['port'][0]
    #clientId=dacc['clientId'][0]
    #print(IP,port,clientId)
    #print("In get account detail")
    
    print(ibprogram)
    
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    #print("already_connected:",already_connected)
    
    if already_connected == False:
        #print('oops')
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
            #ib.connect(IP, port, clientId=clientId)
        except:
            print("Connect call failed")
            return
    else:
        #print('here')
        ib = ibprogram
        
    
    
    acc = ib.accountSummary()
    ib.sleep(2)
    #print(acc)
    accdata=dict()
    accdata['accountID'] = acc[0].account
    accountT= [v.tag for v in acc if v.currency == 'USD']
    accountV= [v.value for v in acc if v.currency == 'USD']
    for i in range(len(accountT)): accdata[accountT[i]]=accountV[i]
    
    AvailableFunds = float(accdata['AvailableFunds'])
    BuyingPower = float(accdata['BuyingPower'])
    
    
    if already_connected == False:
        ib.disconnect()
    
    #print(accdata)
    return accdata
    
    
    
    
    
#market, symbol, periodType, period, timeframe, frequency,extended_hours
def get_price_history_OLD(market, symbol, periodType, period, timeframe, frequency, extended_hours, ibprogram=None, end_date=None, liveTrading=False, expiry=None, strike=None, optionType=None, tradingClass=None):
#def get_price_history(market='Stock', symbol = 'AAPL', tf='M1', exthr=False):
    util.startLoop()  # uncomment this line when in a notebook
    
    global g_bar_dict
    g_bar_dict = {}
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    #print("already_connected:",already_connected)
    
    if already_connected == False:
        #print('oops')
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
            #ib.connect(IP, port, clientId=clientId)
        except:
            print("Connect call failed")
            return
    else:
        #print('here')
        ib = ibprogram
    
    
    
    
    
    if timeframe=='minute' and frequency=='1':
        btf = '1 min'
    elif timeframe=='minute' and frequency=='2':
        btf = '2 min'
    elif timeframe=='minute' and frequency=='3':
        btf = '3 min'
    elif timeframe=='minute' and frequency=='5':
        btf = '5 min'
    elif timeframe=='minute' and frequency=='10':
        btf = '10 min'
    elif timeframe=='minute' and frequency=='15':
        btf = '15 min'
    elif timeframe=='minute' and frequency=='20':
        btf = '20 min'
    elif timeframe=='minute' and frequency=='30':
        btf = '30 min'
    elif timeframe=='hour' and frequency=='1':
        btf = '1 hour'
    elif timeframe=='hour' and frequency=='4':
        btf = '4 hours'    
    elif timeframe=='day' and frequency=='1':
        btf = '1 day'
    elif timeframe=='week' and frequency=='1':
        btf = '1 week'
    elif timeframe=='month' and frequency=='1':
        btf = '1 month'
    else:    
        btf = '1 day'
    
    
    if periodType=='day':
        duration = str(period)+' '+'D'
    else:
        duration = '5 D'
    
    #print('duration:',duration)
    
    useRTH = not extended_hours
    
    
    
 

    
    

    #from ib_insync import *
    
    if market=='Forex':
        contract = Forex(symbol)
        whatToShow = 'MIDPOINT'
    elif market=='Option':
        contract=Option(symbol, expiry, strike, optionType, "CBOE", tradingClass=tradingClass)
        whatToShow = 'TRADES'
    elif market=='Index':
        contract = Index(symbol, 'CBOE')
        whatToShow = 'TRADES'
    else:
        contract = Stock(symbol, 'SMART', 'SGD')
        whatToShow = 'TRADES'
    '''
    if tf=='H1':
        btf = '1 hour'
    elif tf=='M1':
        btf = '1 min'
    elif tf=='M2':
        btf = '2 mins'
    elif tf=='M5':
        btf = '5 mins'
    elif tf=='M15':
        btf = '15 mins'
    elif tf=='M30':
        btf = '30 mins'    
    elif tf=='H4':
        btf = '4 hours'    
    elif tf=='H1':
        btf = '1 hour'
    elif tf=='D1':
        btf = '1 day'
    elif tf=='W1':
        btf = '1 week'
    else:
        btf = '1 day'
    '''
    
    #print("get data history request")
    
    #end_date = datetime.datetime(2022, 8, 26).date()
    ib.qualifyContracts(contract)
    
    
    if liveTrading==True:
        end_date = ''
        keepUpToDate=True
        ib.reqMarketDataType(1)
    else:
        keepUpToDate=False
        ib.reqMarketDataType(3)
        
    print(liveTrading, end_date, keepUpToDate)    
    #bars = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf,
    #                        whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
    
    #ib.sleep(1)
    
    #print(bars)
    #ib.reqMarketDataType(4)
    #bars = ib.reqHistoricalData(contract, endDateTime='', durationStr=duration,
    #    barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1)
    
    
    if market=='Index':
        globalvar.g_bar_dict[symbol] = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
        def onBarUpdate(bars, hasNewBar):
            print(bars[-1])

        # Set callback function for streaming bars
        globalvar.g_bar_dict[symbol].updateEvent += onBarUpdate

        bars = globalvar.g_bar_dict[symbol].copy()
    elif market=='Option':
        expy = expiry.replace('-','')[2:]
        prlen = len(str(int(strike)))
        cprlen = 5 - prlen
        zerostr = ''
        zerostr2 = '000'
        for z in range(cprlen):
            zerostr = zerostr+'0'
        optsym = symbol+expy+optionType+zerostr+str(int(strike))+zerostr2
        globalvar.g_bar_dict[optsym] = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
        bars = globalvar.g_bar_dict[optsym].copy()
    
    #print(g_bar_dict)
    #print(g_bar_dict[symbol][-1].close)
    #contract = Forex(symbol)
    #contract = CFD('IBUS30')
    #contract = Stock('FB', 'SMART', 'USD')
    #ib.qualifyContracts(contract)
    #[ticker] = ib.reqTickers(contract)

    # Underlying price
    #undPrice = ticker.last
    #print(undPrice)
    '''
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 Y',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1)

    print(bars)
    '''
    # convert to pandas dataframe:
    df = util.df(bars.copy())
    
    #print(df.head())
    
    
    
    #df.rename(columns={"date": "datetime"}, inplace=True)
    df = df.set_index('date')
    
    # option data
    #option = Option(symbol, exchange='SMART')
    #cds = ib.reqContractDetails(option)
    ##contracts = [cd.summary for cd in cds]
    #for cd in cds: print(cd)

    if already_connected == False:
        ib.disconnect()
    
    return df
#print(df[['date', 'open', 'high', 'low', 'close']])





def cancel_all_orders(ibprogram=None):
    util.startLoop()  # uncomment this line when in a notebook
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    
    
    if already_connected == False:
        ib = IB()
        ib.connect(IP, PORT, clientId=CLIENT_ID)
    else:
        ib = ibprogram
        
        
    reqorders = ib.orders()
    ib.sleep(2)
    for order in reqorders:
        print('cancelling order:',order.orderId)
        ib.cancelOrder(order)
    
    if already_connected == False:
        ib.disconnect()    

    
    
def cancel_order(orderIDStr=None, ibprogram=None):
    util.startLoop()  # uncomment this line when in a notebook
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
        
    if already_connected == False:
        ib = IB()
        ib.connect(IP, PORT, clientId=CLIENT_ID)
    else:
        ib = ibprogram
        
    orderID = int(orderIDStr)
    #print("CANCEL:",orderID, type(orderID))
    
    reqorders = ib.orders()
    ib.sleep(2)
    for order in reqorders:
        #print(order.orderId, type(order.orderId))
        if order.orderId == orderID:
            print('cancelling order:',order.orderId)
            ib.cancelOrder(order)
            ib.sleep(1)
            if already_connected == False:
                ib.disconnect()
            return
    
    if already_connected == False:
        ib.disconnect()
    return
    
    
def liquidate_all(ibprogram=None):
    util.startLoop()  # uncomment this line when in a notebook
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print('connection failed, please check whether IB TWS/Gateway is running in background')
            return None
    else:
        ib = ibprogram
    
    
    reqorders = ib.orders()
    ib.sleep(2)
    for order in reqorders:
        ib.cancelOrder(order)
        
    
    reqpos = ib.reqPositions()
    ib.sleep(2)
    print(reqpos)
    for p in reqpos:
        symbol=p.contract.symbol
        pos = int(p.position)
        print(symbol, pos)
        direction = "BUY" if pos < 0 else "SELL"
        contract = p.contract
        #contract.symbol = symbol
        #contract.secType='STK'
        #contract.exchange = 'SMART'
        #contract.currency = 'USD'
        ib.qualifyContracts(contract)
        
        #ib.cancelOrder(order)
        
        order=MarketOrder(direction, abs(pos))
        ib.sleep(0.2)
        trade = ib.placeOrder(contract, order)
        print(trade)
        ib.sleep(0.2)
    
    reqpos = ib.reqPositions()
    ib.sleep(2)
    print(reqpos)
    for p in reqpos:
        symbol=p.contract.symbol
        pos = int(p.position)
        print(symbol, pos)
    
    if already_connected == False:
        ib.disconnect() 


    
def get_option_chain_data(ibprogram=None, symbol=None, secType=None, exchange=None):
    util.startLoop()  # uncomment this line when in a notebook
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    #print("already_connected:",already_connected)
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
    
    
    contract = None
    if secType=='Index':    
        contract = Index(symbol, exchange)
    
    
    ib.qualifyContracts(contract)
    ib.reqMarketDataType(3)
    [ticker] = ib.reqTickers(contract)
    Value = ticker.marketPrice()
    
    
    chains = ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)
    util.df(chains)
    
    
    
    if secType=='Index' and symbol=='SPX':
        chain = next(c for c in chains if c.tradingClass == 'SPXW' and c.exchange == 'CBOE')
    
    #print(chain)
    
    
    strikes = [strike for strike in chain.strikes if strike % 5 == 0 and Value - 20 < strike < Value + 20]
    expirations = sorted(exp for exp in chain.expirations)[0:1]
    rights = ['P', 'C']

    
    contracts = [Option(symbol, expiration, strike, right, exchange, tradingClass='SPXW')
            for right in rights
            for expiration in expirations
            for strike in strikes]

    contracts = ib.qualifyContracts(*contracts)
    #print(contracts)
    
    if already_connected == False:
        ib.disconnect()
        
    return contracts
       
'''         
def tick_data(instrument_symbl_list, ib):
    global g_tick_dict
    g_tick_dict = {}
    
    global contract_list
    contract_list = []
    
    
    for symbol in instrument_symbol_list:
        contract = Contract()
        contract.symbol = symbol
        contract.secType='STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        ib.qualifyContracts(contract)
        contract_list.append((symbol,contract))
    
    
    try:
        for contract_tuple in contract_list:
            symbol = contract_tuple[0]
            contract = contract_tuple[1]
            ib.reqMktData(contract, "", False, False, [])
    except:
        print('reMktData failed')
        return -1
        
        
    def onPendingTickers(tickers):
        for t in tickers:
            g_tick_dict[t.contract.symbol] = t        

    ib.pendingTickersEvent += onPendingTickers    
            

    #def onPendingTickers(tickers):
    #for t in tickers:
    #    df.loc[t.contract.pair()] = (
    #        t.bidSize, t.bid, t.ask, t.askSize, t.high, t.low, t.close)
    #    clear_output(wait=True)
    #display(df)
    
    return g_tick_dict
                           
'''



def ib_streamer(symbol_dict=None, param=None, ibprogram=None):
    if symbol_dict is None:
        print("symbol data for streaming is None")
        return
    
    #equity_ = symbol_dict['EQUITY']
    #equity = ",".join(equity_)
    #option_ = symbol_dict['OPTION']
    #option = ",".join(option_)
    
    util.startLoop()  # uncomment this line when in a notebook
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    if already_connected == False:
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
        except:
            print("Connect call failed")
            return
    else:
        ib = ibprogram
    
    
    
    #ib.reqHeadTimeStamp(contract, whatToShow='TRADES', useRTH=True)
    index_ = symbol_dict['EQUITY']
    contract = Index(index_, 'CBOE')
    ib.qualifyContracts(contract)
    ib.reqMarketDataType(1)
    index_bars = ib.reqRealTimeBars(contract, 5, 'TRADES', False)
    g_tick_data[index_] = index_bars
    
    
    strike_list = param[index_+'_option_strike_stream']
    expiry = param[index_+'_option_expiry_stream']
    
    print("Streamer Subs:",strike_list, expiry)
    
    option_ = symbol_dict['OPTION']
    contracts = Option(option_, 'CBOE')
    ib.qualifyContracts(contract)
    ib.reqMarketDataType(1)
    option_bars = ib.reqRealTimeBars(*contracts, 5, 'TRADES', False)
    
    for ops in option_:
        g_tick_data[ops] = option_bars[ops]
    
    #while g_streamer_connection==False:
    #    RUN_FOR_MINUTES = param['RUN_FOR_MINUTES']
    #    
    #    #print("g_param['RUN_FOR_MINUTES']=",g_param['RUN_FOR_MINUTES'])
    #    if g_param['RUN_FOR_MINUTES']==0:
    #        break
    
    
    
    
#market, symbol, periodType, period, timeframe, frequency,extended_hours
def get_price_history(market, symbol, periodType, period, timeframe, frequency, extended_hours, ibprogram=None, end_date=None, param=None, expiry=None, strike=None, optionType=None, tradingClass=None):
#def get_price_history(market='Stock', symbol = 'AAPL', tf='M1', exthr=False):
    util.startLoop()  # uncomment this line when in a notebook
    
    ibprogram=param['ibprogram']
    
    liveTrading = param['live_trading']
    
    
    instrument_symbol_list = param['instrument_symbol_list']
    timeframe = param['timeframe']
    frequency = int(param['frequency'])
    extended_hours = param['extended_hours']
    periodType = param['periodType']
    period = param['period']
    
    backtest_date1 = param['backtest_date1']
    backtest_date2 = param['backtest_date2']
    
    
    
    global g_bar_dict
    g_bar_dict = {}
    
    already_connected = False
    if ibprogram!=None:
        already_connected = True
    
    #print("already_connected:",already_connected, ibprogram)
    
    if already_connected == False:
        #print('oops')
        ib = IB()
        try:
            ib.connect(IP, PORT, clientId=CLIENT_ID)
            #ib.connect(IP, port, clientId=clientId)
        except:
            print("Connect call failed")
            return
    else:
        #print('here')
        ib = ibprogram
    
    
    
    
    
    if timeframe=='minute' and frequency=='1':
        btf = '1 min'
    elif timeframe=='minute' and frequency=='2':
        btf = '2 min'
    elif timeframe=='minute' and frequency=='3':
        btf = '3 min'
    elif timeframe=='minute' and frequency=='5':
        btf = '5 min'
    elif timeframe=='minute' and frequency=='10':
        btf = '10 min'
    elif timeframe=='minute' and frequency=='15':
        btf = '15 min'
    elif timeframe=='minute' and frequency=='20':
        btf = '20 min'
    elif timeframe=='minute' and frequency=='30':
        btf = '30 min'
    elif timeframe=='hour' and frequency=='1':
        btf = '1 hour'
    elif timeframe=='hour' and frequency=='4':
        btf = '4 hours'    
    elif timeframe=='day' and frequency=='1':
        btf = '1 day'
    elif timeframe=='week' and frequency=='1':
        btf = '1 week'
    elif timeframe=='month' and frequency=='1':
        btf = '1 month'
    else:    
        btf = '1 day'
    
    
    if param['live_trading']==True:
        period = '1'
    
    if periodType=='day':
        duration = str(period)+' '+'D'
    else:
        duration = '5 D'
    
    #print('duration:',duration)
    
    useRTH = not extended_hours
    

    #from ib_insync import *
    
    if market=='Forex':
        contract = Forex(symbol)
        whatToShow = 'MIDPOINT'
    elif market=='Option':
        contract=Option(symbol, expiry, strike, optionType, "CBOE", tradingClass=tradingClass)
        whatToShow = 'TRADES'
    elif market=='Index':
        contract = Index(symbol, 'CBOE')
        whatToShow = 'TRADES'
    else:
        contract = Stock(symbol, 'SMART', 'USD')
        whatToShow = 'TRADES'
    '''
    if tf=='H1':
        btf = '1 hour'
    elif tf=='M1':
        btf = '1 min'
    elif tf=='M2':
        btf = '2 mins'
    elif tf=='M5':
        btf = '5 mins'
    elif tf=='M15':
        btf = '15 mins'
    elif tf=='M30':
        btf = '30 mins'    
    elif tf=='H4':
        btf = '4 hours'    
    elif tf=='H1':
        btf = '1 hour'
    elif tf=='D1':
        btf = '1 day'
    elif tf=='W1':
        btf = '1 week'
    else:
        btf = '1 day'
    '''
    
    #print("get data history request")
    
    #end_date = datetime.datetime(2022, 8, 26).date()
    ib.qualifyContracts(contract)
    
    
    if liveTrading==True:
        end_date = ''
        keepUpToDate=True
        ib.reqMarketDataType(1)
    else:
        keepUpToDate=False
        ib.reqMarketDataType(3)
        
    #print(liveTrading, end_date, keepUpToDate)    
    #bars = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf,
    #                        whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
    
    
    #print(bars)
    #ib.reqMarketDataType(4)
    #bars = ib.reqHistoricalData(contract, endDateTime='', durationStr=duration,
    #    barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1)
   
    
    if market=='Index':
        param['contract_list'][symbol] = contract
        #print(contract, end_date, duration, btf, whatToShow, useRTH,keepUpToDate)
        globalvar.g_bar_dict[symbol] = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
        #print(globalvar.g_bar_dict[symbol])
        #def onBarUpdate(t, hasNewBar):
        #    print(t[-1])
        ## Set callback function for streaming bars
        #globalvar.g_bar_dict[symbol].updateEvent += onBarUpdate
        ib.sleep(1)
        bars = globalvar.g_bar_dict[symbol].copy()
    elif market=='Option':
        expy = expiry.replace('-','')[2:]
        prlen = len(str(int(strike)))
        cprlen = 5 - prlen
        zerostr = ''
        zerostr2 = '000'
        for z in range(cprlen):
            zerostr = zerostr+'0'
            
        if symbol=='SPX' and tradingClass=='SPXW':
            optsym = tradingClass+expy+optionType+zerostr+str(int(strike))+zerostr2
        else:
            optsym = symbol+expy+optionType+zerostr+str(int(strike))+zerostr2
        param['contract_list'][optsym] = contract
        
        print("duration",duration)
        
        globalvar.g_bar_dict[optsym] = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
        #ib.sleep(3)
        bars = globalvar.g_bar_dict[optsym]#.copy()
        #print(bars)
        #print("see->",len(bars), bars)
        
        if len(bars)==0:
            print(bars, optsym)
            #ib.sleep(3)
            globalvar.g_bar_dict[optsym] = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr='2 D', barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
            bars = globalvar.g_bar_dict[optsym]#.copy()
        
        if len(bars)==0:
            print(bars, optsym)
            globalvar.g_bar_dict[optsym] = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr='3 D', barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
            bars = globalvar.g_bar_dict[optsym]#.copy()
            #ib.sleep(3)
            #globalvar.g_bar_dict[optsym] = [BarData(date=datetime.datetime(2022, 9, 13, 10, 9), open=0.0, high=60.0, low=60.0, close=60.0, volume=0.0, average=60.0, barCount=0)]
            #ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
            #bars = globalvar.g_bar_dict[optsym]#.copy()
    
    #print(g_bar_dict)
    #print(g_bar_dict[symbol][-1].close)
    #contract = Forex(symbol)
    #contract = CFD('IBUS30')
    #contract = Stock('FB', 'SMART', 'USD')
    #ib.qualifyContracts(contract)
    #[ticker] = ib.reqTickers(contract)

    # Underlying price
    #undPrice = ticker.last
    #print(undPrice)
    '''
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 Y',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1)

    print(bars)
    '''
    # convert to pandas dataframe:
    df = util.df(bars)
    
   
    
    #tz = pytz.timezone('US/Eastern')
    #df['date'] = df['date'].dt.tz_localize('GMT').dt.tz_convert('US/Eastern')
    
    #print(df.head())
    #df.rename(columns={"date": "datetime"}, inplace=True)
    try:
        df = df.set_index('date')
    except:
        print('empty dataframe')
        df = pd.DataFrame(columns=['open','high','low','close','volume','average','barCount'])
        #print(df)
        #df = df.set_index('date')
    # option data
    #option = Option(symbol, exchange='SMART')
    #cds = ib.reqContractDetails(option)
    ##contracts = [cd.summary for cd in cds]
    #for cd in cds: print(cd)

    if already_connected == False:
        ib.disconnect()
    
    
    #param['contract_list'].append((symbol,contract))
    
    return df
#print(df[['date', 'open', 'high', 'low', 'close']])




def get_stock_history(ib=None, symbol='TSLA', btf = '5 mins'):
    if ib is None:
        return None
    contract = Stock(symbol, 'SMART', 'USD')
    print(contract)
    whatToShow = 'TRADES'
    ib.qualifyContracts(contract)
    end_date = ''
    duration = '1 D'
    keepUpToDate=True
    ib.reqMarketDataType(1)
    useRTH = True
    bars = ib.reqHistoricalData(contract, endDateTime=end_date, durationStr=duration, barSizeSetting=btf, whatToShow=whatToShow, useRTH=useRTH,formatDate=1,keepUpToDate=keepUpToDate)
    ib.sleep(2)
    print(bars)
    return bars
    


    