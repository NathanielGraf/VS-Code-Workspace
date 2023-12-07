'''
Checks for the time to be less than the time we want to start selling off by
Once a message comes through with a symbol, we check to see if we are above our risk threshhold for that symbol, and if so, we sell off our volume to the highest bids
We repeat this for each symbol that comes through until the end of the game
Stuff needed: 
volume_held being specified for each specific symbol we have 
The time needs to be defined
The risk percent needs to be defined 
All these are variables which can be easily changed 

'''
while time < timetoselloff:  

    if message["symbol"] == "BOND":

        #Runs the following loop while we are above our risk threshold, selling to the highest bidder until we get below it. 
        while (volume_held(BOND) / 100) > riskpercent: 

            def best_bid():
                if message["buy"]:
                    return message["buy"][0][0] # , message["buy"][0][1]

            exchange.send_add_message(order_id=nextid, symbol="BOND", dir=Dir.SELL, price=best_bid(), size=1)

    if message["symbol"] == "VALE":

        #Runs the following loop while we are above our risk threshold, selling to the highest bidder until we get below it. 
        while (volume_held(VALE) / 10) > riskpercent: 

            def best_bid():
                if message["buy"]:
                    return message["buy"][0][0] # , message["buy"][0][1]

            exchange.send_add_message(order_id=nextid, symbol="VALE", dir=Dir.SELL, price=best_bid(), size=1)

    if message["symbol"] == "VALBZ":

        #Runs the following loop while we are above our risk threshold, selling to the highest bidder until we get below it. 
        while (volume_held(VALBZ) / 10) > riskpercent: 

            def best_bid():
                if message["buy"]:
                    return message["buy"][0][0] # , message["buy"][0][1]

            exchange.send_add_message(order_id=nextid, symbol="VALBZ", dir=Dir.SELL, price=best_bid(), size=1)

    if message["symbol"] == "GS":

        #Runs the following loop while we are above our risk threshold, selling to the highest bidder until we get below it. 
        while (volume_held(GS) / 100) > riskpercent: 

            def best_bid():
                if message["buy"]:
                    return message["buy"][0][0] # , message["buy"][0][1]

            exchange.send_add_message(order_id=nextid, symbol="GS", dir=Dir.SELL, price=best_bid(), size=1)

    if message["symbol"] == "MS":

        #Runs the following loop while we are above our risk threshold, selling to the highest bidder until we get below it. 
        while (volume_held(MS) / 100) > riskpercent: 

            def best_bid():
                if message["buy"]:
                    return message["buy"][0][0] # , message["buy"][0][1]

            exchange.send_add_message(order_id=nextid, symbol="MS", dir=Dir.SELL, price=best_bid(), size=1)

    if message["symbol"] == "WFC":

        #Runs the following loop while we are above our risk threshold, selling to the highest bidder until we get below it. 
        while (volume_held(WFC) / 100) > riskpercent: 

            def best_bid():
                if message["buy"]:
                    return message["buy"][0][0] # , message["buy"][0][1]

            exchange.send_add_message(order_id=nextid, symbol="WFC", dir=Dir.SELL, price=best_bid(), size=1)
