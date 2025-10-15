Title: MDF Messages Reference

URL Source: https://packages.millistream.com/documents/MDF%20Messages%20Reference.pdf

Published Time: Fri, 04 Jul 2025 21:18:44 GMT

Markdown Content:
MDF Messages Reference 

# Reference Guide 

# 4 July 2025 

Millistream Market Data AB www.millistream.com 

Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117 Introduction 

Since the Millistream Data Feed is a subscriptions based feed, only the instruments and messages that the client has 

issued subscriptions for (and for which the client has authorization for) is sent to the client by the server. Subscribing to 

data is performed by sending requests to the server, requesting either an image request (to see the curent snapshot for 

the instrument(s)/message) or a stream request (subscription to real-time [or delayed, depending upon authorization] 

data as a push based stream of updates). 

Normally clients issue so called full requests wich is a combined image and stream request, this will give a snapshot as 

the staring point and a data stream with updates to that snapshot as there is changes in the market. 

When an update happens in the market, only the modified fields will be sent (messages that creates new records [such 

as trades, news, corporate actions and price history] will be sent as if the previous value for each field was null). 

For example, let's imagine an equity with the following values for it's Quote message: 

Bid Price=22.50, Ask Price = 22.70 

Now there has been a change of the Ask Price in the market, the Quote message will be sent like this: 

Ask Price = 22.80 

And the client has to modify the instrument's state to: 

Bid Price = 22.50, Ask Price = 22.80 

If the Bid Price would be revoced at the market, the Quote message will be sent like this: 

Bid Price = NULL 

And the client thus now have an instrument state of: 

Ask Price = 22.80    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Administrative Messages 

# Login Request 

mref  MDF_M_LOGON #1 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

MDF_F_USERNAME  Username  Y

MDF_F_PASSWORD  Password  Y

MDF_F_S1  Application  N Optionally inform the Millistream server about the 

name (and possible version) of the application. 

MDF_F_EXTRACREDENTIAL  Extra Credentials  N Used to provide extra credentials if the account is setup 

to use two-factor authentication. 

This must be the first message sent by the client. If the account is configured to use two-factor authentication, the 

MDF_F_EXTRACREDENTIAL is required and should contain the data from the smart card (or whatever mechanism is 

used). This data will then be sent to the external authentication service configured for the account. Exactly how this is 

done is dependent upon each specific authentication service used. 

# Log Off 

mref  MDF_M_LOGOFF #2 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

MDF_F_LOGOFFREASON  Logoff reason  N If the server issued the connection to terminate, this 

field will contain the reason. 

The Log Off message can be sent be either the server or the client indicating to the other peer that the connection will be 

terminated. At either end for whatever reason. If the server issued the Log Off message, the 

MDF_F_LOGOFFREASON will be present in the message and it will contain the reason for the termination, the reason 

will be prefixed with a numerical value (401 for authentication failure and 503 if the server is shutting down). 

# Logon Greeting 

mref  MDF_M_LOGONGREETING #3 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

MDF_F_SERVERNAME  Server Name  Y The name of the server the client is connected to 

MDF_F_SERVERTIME  Server Time  Y The current time on the server in UTC 

MDF_F_SERVERDATE  Server Date  Y The current date on the server 

When the client has successfully logged in to the server, the server will send a Logon Greeting message to the client, if 

the logon would fail the client would get a Log Off message instead.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Messages Reference 

mref  MDF_M_MESSAGESREFERENCE #0 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

...  ...  Y

The Messages Reference message will be sent directly after a connection if it detects that the clients version of the 

templates is too old. The message is also sent in realtime whenever the version on the server is changed. It cannot be 

requested and cannot be unsubscribed. 

This message is normally only used by the API internally to synchronize the message templates between the server and 

the API, but it is also exposed to the client since it can be useful for clients wanting to automatically learn about new 

messages and their corresponding fields. 

insref  does not identify any instrument for this message, instead it represents the template version, the API will 

bookkeep this value internally and will send it to the server upon the next connection in order to avoid having to receive 

the templates on every connect if the version has not changed. 

Each field in this message represents a message, I.e the field tag is the  mref  of the message to define and the field 

value will contain a pipe separated ('|') string with the following fields: 

1.  '0' if  insref  represents an instrument, '1' if it does not. 

2.  '0' if each update modifies the message image, I.e a new Bid Price in a Quote message overwrites the old Bid 

Price in the message image. '1' if each update creates a new record, I.e a Trade message creates a new record 

for each received trade and all previously received trade records are still valid (there are a few exceptions to 

this rule in where it is possible to send out corrections for the records). 

3.  The  mclass  of the message 

4.  A space separated list of the field tags defined for the message 

# Instrument Delete 

mref  MDF_M_INSTRUMENTDELETE #17 

mclass  All Message Classes 

Tag  Name  Req'd  Comments 

MDF_F_MARKETPLACE  Marketplace  N Present and with the value of the new marketplace if 

the instrument moved outside of the account's 

entitlements due to change of marketplace. 

A Instrument Delete message will be sent when an instrument is to be deleted. It will only be sent in realtime on stream 

or full requests. If an instrument is deleted prior to an image request, the instrument will not be sent at all.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Request Messages 

# Request 

mref  MDF_M_REQUEST #19 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

MDF_F_REQUESTCLASS  Request Class  Y Can contain a space separated list (use 

mdf_message_add_list()  to add this fields 

efficiently) of the request classes you want to request. 

If it contains the single character " *" the request will be 

for all request classes that the account is entitled for. 

MDF_F_REQUESTTYPE  Request Type  Y If Request Class is  MDF_RC_INSREF , this field 

should be used to inform the server about the number 

of insrefs wanted. If the requested number of insrefs 

cannot be fulfilled, the request fails in full. 

MDF_F_REQUESTID  Request Id  N If present, the value of this field will be sent with a 

Request Finished message when the image request has 

been completed in full. 

MDF_F_INSREFLIST  Insref List  N Can contain a space separated list (use 

mdf_message_add_list()  to add this field 

efficiently) of the insrefs to request. If it contains the 

single character " * the request will be for all 

instruments available for the account. 

This is the message that the client uses to request data from the server. Either realtime streaming data or snapshot image 

data can be requested (or full for a combination request). The current filtering capability is to separate on message type 

using the Request Class and a specified list of instruments with the Insref List. 

# Unsubscribe 

mref  MDF_M_UNSUBSCRIBE #31 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

MDF_F_REQUESTCLASS  Request Class  Y Can cointain a space separated list (use 

mdf_message_add_list()  to add this fields 

efficiently) of the request classes you want to 

unsubscribe. If it contains the single character " *" the 

request will be for all request classes that the account is 

entitled for. 

MDF_F_REQUESTID  Request Id  N If present, the value of this field will be sent in a 

Request Finished message when the unsubscribe 

request has been completed. 

MDF_F_INSREFLIST  Insref List  N Can contain a space separated list (use 

mdf_message_add_list()  to add this field 

efficiently) of the insrefs to unsubscribe. If it contains 

the single character " * the unsubscription will be for all 

instruments available for the account.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

This is the message that the client uses to unsubscribe from the realtime streaming data from the server. 

# Request Finished 

mref  MDF_M_REQUESTFINISHED #20 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

MDF_F_REQUESTID  Request Id  Y The same value that was sent in the 

request/ubsubscribe message. 

MDF_F_REQUESTSTATUS  Request Status  Y ‘100’ The request was completed successfully. 

‘101’ The request was invalid. 

‘102’ The request server is temporarily unavailable. 

‘103’ Internal server error. 

This message will only be sent if a Request Id was present in the Request (only if the request was for an image or full 

request) or Unsubscribe message. 

# Insref 

mref  MDF_M_INSREF #21 

mclass  MDF_MC_UNDEF 

Tag  Name  Req'd  Comments 

MDF_F_INSREFLIST  Insref List  Y

The assigned insrefs as a reply to a  MDF_RC_INSREF  request.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# News Message 

# News Headline 

mref  MDF_M_NEWSHEADLINE #4 

mclass  MDF_MC_NEWSHEADLINE 

Tag  Name  Req'd  Comments 

MDF_F_NEWSID  News Id  Y

MDF_F_NEWSIDREPLACE  Replace Id  N This news item replaces the news item 

that matches this news id. 

MDF_F_LANGUAGE  Language  N

MDF_F_HEADLINE  Headline  N

MDF_F_DATE  Date  N

MDF_F_TIME  Time  N

MDF_F_NEWSCODINGCOMPANY  News Coding Company  N

MDF_F_NEWSCODINGTYPE  News Coding Type  N

MDF_F_NEWSCODINGSUBJECT  News Coding Subject  N

MDF_F_NEWSCODINGCOUNTRY  News Coding Country  N

MDF_F_NEWSCODINGORIGINAL  News Coding Original  N

MDF_F_NEWSCODINGISIN  News Coding ISIN  N

MDF_F_NEWSCODINGREGULATATORY  News Coding Regulatory  N

MDF_F_NEWSCODINGTAGS  News Coding Tags  N

MDF_F_NEWSCODINGIMPACT  News Coding Impact  N

MDF_F_NEWSRANK  News Rank  N

This message will carry the headline and the news coding for the news item. The actual news content will be sent in one 

or several News Content messages, each with the same News Id to identify the news item. 

Several News Headline messages can be sent with the same News Id in order to send corrections or to add fields, for 

example it is very common for the first News Headline message to not include any news coding at all (to keep the 

latency low), with the news coding in a second message. 

# News Content 

mref  MDF_M_NEWSCONTENT #22 

mclass  MDF_MC_NEWSCONTENT 

Tag  Name  Req'd  Comments 

MDF_F_NEWSID  News Id  Y

MDF_F_TEXTBODY  Text Body  Y The news content block to be concatenated 

with the previously sent news blocks. 

MDF_F_NEWSBLOCKNUMBER  News Block Number  Y

MDF_F_NEWSISLASTBLOCK  News Is Last Block  N Present in the last news block    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

This message will carry the actual news content, exceptionally large news content (or when the news source is 

distributing their data segmented) will be split into news blocks that will be sent as individual News Content messages, 

each with the same News Id and with an increasing News Block Number. 

Currently there will be no corrections to the news content, and all news blocks will be sent in order without any gaps. 

The very last news block (which can be the first block for a small news item) will have the News Is Last Block field 

present, currently with the value '1', but that is of less importance since the mere presence of the field marks this as the 

last news block for the news item. 

The news content will be in a special XML format, see the  News Format  document for more information.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Order Book Messages 

The order book in the Millistream Data Feed can be sent using either a Market By Order (MBO) model or a Market By 

Level (MBL) model. 

In the MBO model, each order is sent individually and is usually sourced from a special low latency “total view” feed 

from the exchange which for some exchanges requires an additional exchange license fee. 

In the MBL model, the orders with the same price are aggregated as a single level. The number of levels are usually 

restricted to a max of 5 per side (bid/ask) and rate limiting can be implemented making the MBL the easier but also 

higher latency solution. 

Not all exchanges provides a MBO, but for all that do we will always also present a MBL (the MBL is then created 

from the MBO by us). 

# Order Book Flush 

mref  MDF_M_ORDERBOOKFLUSH #14 

mclass  MDF_MC_ORDER|MDF_MC_MBO|MDF_MC_QUOTEBBO 

Tag  Req'd  Comments 

MDF_F_I1  Y Bitfield that specifies for which type of Order Book messages that should be flushed. Valid 

values: 

## • 1 – Flush  MDF_MC_ORDER  data 

• 2 – Flush  MDF_MC_MBO  data 

• 4 – Flush  MDF_MC_QUOTEBBO  data 

• 8 – The flush was sent as a reply to a Image/Full request just before the image of the order 

is sent. 

The Order Book Flush indicates that the client should clear out (destroy) the whole order book for the instrument 

specified, both the bid and ask sides should be removed and all data received from a QuoteBBO message should be 

discarded, exactly which data that should be cleared/discarded/flushed will be indicated by the  MDF_F_I1  field. 

Will be sent as the first message in reply to a  MDF_RC_ORDER  / MDF_RC_MBO  image or full request to make sure that 

the client will clear out any stale order levels (or orders) before receiving the order book image (which will be sent as a 

series of inserts/adds). For  MDF_RC_MBO  requests from a point in time, a flush will only be sent if there have been 

deletes sent on the instrument in the time between the requested “point in time” and the “time of the request”. 

# Market By Level Messages 

The MBL order book in the Millistream Data Feed uses a insert/update/delete model. Levels are created with the insert 

messages, removed with the delete messages and modified by the update messages. 

When a level is created, all levels equal to and higher than that level will be moved down one level, I.e an insert on 

level #2 will change the existing level #2 to level #3, level #3 to level #4 and so on. Level deletions will remove the 

indicated level and move all levels higher than that level up one level, I.e a delete on level #2 will change the existing 

level #3 to level #2, level #4 to level #3 and so on. 

This means that the client must build the order book in memory and rearrange the levels as it receives insert and delete 

messages. The bid and ask side live in completely separate worlds, so a insert/delete on the bid side will have no impact 

on the ask side. 

It is important that the client stay synchronized with the server, so only image or full requests are recommended. 

Further, the server will always send a  MDF_M_ORDERBOOKFLUSH  message before the actual order book image for a 

instrument to make sure that the client is truly in sync. The order book flush can also be sent out during trading by the    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

market place if a instrument is to resume trading after for example a trade halt. When receiving this message, the client 

should remove all order book levels for the instrument in question. 

Clients requesting order book messages will also receive  MDF_M_INSTRUMENTRESET  messages before trading 

commences on a trading day, this message should be treated like an order book flush and the client should thus remove 

all order book levels for the instrument in question. 

# Bid Level Insert 

mref  MDF_M_BIDLEVELINSERT #7 

mclass  MDF_MC_ORDER 

Tag  Name  Req'd  Comments 

MDF_F_ORDERLEVEL  Order Level  Y

MDF_F_BIDPRICE  Bid Price  N

MDF_F_BIDQUANTITY  Bid Quantity  N

MDF_F_NUMBIDORDERS  Number of Bid Orders  N

MDF_F_BIDCOUNTERPART  Bid Counterpart  N

MDF_F_MMO  Market Maker Order  N

The Bid Level Insert message will create a new order book level on the bid side 

# Bid Level Update 

mref  MDF_M_BIDLEVELUPDATE #11 

mclass  MDF_MC_ORDER 

Tag  Name  Req'd  Comments 

MDF_F_ORDERLEVEL  Order Level  Y

MDF_F_BIDPRICE  Bid Price  N

MDF_F_BIDQUANTITY  Bid Quantity  N

MDF_F_NUMBIDORDERS  Number of Bid Orders  N

MDF_F_BIDCOUNTERPART  Bid Counterpart  N

MDF_F_MMO  Market Maker Order  N

The Bid Level Update modifies the specified bid level in the order book 

# Bid Level Delete 

mref  MDF_M_BIDLEVELDELETE #9 

mclass  MDF_MC_ORDER 

Tag  Name  Req'd  Comments 

MDF_F_ORDERLEVEL  Order Level  Y

The Bid Level Delete message removes the specified bid level in the order book    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Ask Level Insert 

mref  MDF_M_ASKLEVELINSERT #8 

mclass  MDF_MC_ORDER 

Tag  Name  Req'd  Comments 

MDF_F_ORDERLEVEL  Order Level  Y

MDF_F_ASKPRICE  Ask Price  N

MDF_F_ASKQUANTITY  Ask Quantity  N

MDF_F_NUMASKORDERS  Number of Ask Orders  N

MDF_F_ASKCOUNTERPART  Ask Counterpart  N

MDF_F_MMO  Market Maker Order  N

The Ask Level Insert message will create a new order book level on the ask side 

# Ask Level Update 

mref  MDF_M_ASKLEVELUPDATE #12 

mclass  MDF_MC_ORDER 

Tag  Name  Req'd  Comments 

MDF_F_ORDERLEVEL  Order Level  Y

MDF_F_ASKPRICE  Ask Price  N

MDF_F_ASKQUANTITY  Ask Quantity  N

MDF_F_NUMASKORDERS  Number of Ask Orders  N

MDF_F_ASKCOUNTERPART  Ask Counterpart  N

MDF_F_MMO  Market Maker Order  N

The Ask Level Update modifies the specified ask level in the order book 

# Ask Level Delete 

mref  MDF_M_ASKLEVELDELETE #10 

mclass  MDF_MC_ORDER 

Tag  Name  Req'd  Comments 

MDF_F_ORDERLEVEL  Order Level  Y

The Ask Level Delete message removes the specified ask level in the order book    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Market By Order Messages 

# MBO Add Order 

mref  MDF_M_MBOADD #39 

mclass  MDF_MC_MBO 

Tag  Name  Req'd  Comments 

MDF_F_ORDERID  Millistream Order ID  Y The Millistream created id for this order, 

unique in combination with insref. 

MDF_F_ORDERSIDE  Order Side  Y Defines if this is a Bid or Ask order. 

MDF_F_ORDERPRICE  Order Price  Y Can be NULL if the order is a Market Order, 

which is then sent explicitly. 

MDF_F_ORDERQUANTITY  Order Quantity  Y

MDF_F_ORDERPARTICIPANT  Order Participant  N Exchange member if the marketplace does not 

employ pre-trade anonymity. 

MDF_F_MMO  Market Maker Order  N The presence of this field specifies that this 

order is a protected market maker order. 

MDF_F_ORDERPRIORITY  Order Priority  N The priority of this order among orders on the 

same side, lowest value have the highest 

priority. Not all marketplaces uses a priority. 

MDF_F_ORDERIDSOURCE  Source Order ID  N The Order ID used by the marketplace, if 

available. 

# MBO Order Update 

mref  MDF_M_MBOUPDATE #40 

mclass  MDF_MC_MBO 

Tag  Name  Req'd  Comments 

MDF_F_ORDERID  Order ID  Y The Millistream created id for this order, 

unique in combination with insref. 

MDF_F_ORDERPRICE  Order Price  N The new price if the price of the order is to be 

updated, otherwise not present. 

MDF_F_ORDERQUANTITY  Order Quantity  N The new quantity of the quantity of the order is 

to be updated, otherwise not present. 

MDF_F_ORDERPRIORITY  Order Priority  N The new priority if the priority of the order 

have changed, otherwise not present. 

MDF_F_ORDERIDSOURCE  Source Order ID  N The new marketplace Order ID if this update is 

a Cancel-Replace and the marketplace have 

generated a new Order ID for the replace order. 

# MBO Order Delete 

mref  MDF_M_MBODELETE #41    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

mclass  MDF_MC_MBO 

Tag  Name  Req'd  Comments 

MDF_F_ORDERID  Order ID  Y The Millistream created id for this order, 

unique in combination with insref.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Quote Messages 

# Quote Last Sale 

mref  MDF_M_QUOTE #5 

mclass  MDF_MC_QUOTE 

Tag  Name  Req'd  Comments 

MDF_F_BIDPRICE  Bid Price  N Best Bid Price 

MDF_F_ASKPRICE  Ask Price  N Best Ask Price 

MDF_F_BIDQUANTITY  Bid Quantity  N Quantity at Best Bid 

MDF_F_ASKQUANTITY  Ask Quantity  N Quantity at Best Ask 

MDF_F_LASTPRICE  Last Price  N The last paid price today, if there has been no trades 

today, the value is NULL. 

MDF_F_VWAP  VWAP  N Volume Weighted Average Price 

MDF_F_DAYHIGHPRICE  Day High Price  N The highest paid price today 

MDF_F_DAYLOWPRICE  Day Low Price  N The lowest paid price today 

MDF_F_QUANTITY  Quantity  N The total quantity for today 

MDF_F_INTERNALQUANTITY  Internal Quantity  N Part of the total quantity that is for internal trades 

MDF_F_OFFBOOKQUANTITY  Off-Book Quantity  N Part of the total quantity that is for Off-Book trades 

MDF_F_DARKQUANTITY  Dark Pool Quantity  N Part of the total quantity that is for Dark Pool trades 

MDF_F_TURNOVER  Turnover  N The total turnover for today 

MDF_F_INTERNALTURNOVER  Internal Turnover  N Part of the total turnover that is for internal trades 

MDF_F_OFFBOOKTURNOVER  Off-Book Turnover  N Part of the total turnover that is for Off-Book trades 

MDF_F_DARKTURNOVER  Dark Pool Turnover  N Part of the total turnover that is for Dark Pool trades 

MDF_F_NUMTRADES  Number of Trades  N

MDF_F_OPENPRICE  Open Price  N Today's open price 

MDF_F_BIDYIELD  Bid Yield  N Best Bid Yield 

MDF_F_ASKYIELD  Ask Yield  N Best Ask Yield 

MDF_F_LASTYIELD  Last Yield  N

MDF_F_OPENYIELD  Open Yield  N

MDF_F_DAYHIGHYIELD  Day High Yield  N

MDF_F_DAYLOWYIELD  Day Low Yield  N

MDF_F_NAV  NAV  N

MDF_F_TIS  TIS  N

MDF_F_UNCHANGEDPAID  Unchanged Paid  N Sent for market places and lists 

MDF_F_MINUSPAID  Minus Paid  N Sent for market places and lists 

MDF_F_PLUSPAID  Plus Paid  N Sent for market places and lists 

MDF_F_DURATION  Duration  N

MDF_F_SETTLEMENTPRICE  Settlement Price  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_TIME  Time  N Sent if the quote is for another time than 'now' 

MDF_F_DATE  Date  N Sent if the quote is for another date than 'today' 

The Time and Date fields are sent on all image replies and on stream replies if the quote is for another time/date than 

now (I.e if the client is subscribing to delayed data). 

# Quote Best Bid and Offer 

mref  MDF_M_QUOTEBBO #43 

mclass  MDF_MC_QUOTEBBO 

Tag  Name  Req'd  Comments 

MDF_F_BIDPRICE  Bid Price  N Best Bid Price 

MDF_F_ASKPRICE  Ask Price  N Best Ask Price 

MDF_F_BIDYIELD  Bid Yield  N Best Bid Yield 

MDF_F_ASKYIELD  Ask Yield  N Best Ask Yield 

MDF_F_BIDQUANTITY  Bid Quantity  N Quantity at Best Bid 

MDF_F_ASKQUANTITY  Ask Quantity  N Quantity at Best Ask 

MDF_F_TIME  Time  N Sent if the quote is for another time than 'now' 

MDF_F_DATE  Date  N Sent if the quote is for another date than 'today' 

The Time and Date fields are sent on all image replies and on stream replies if the quote is for another time/date than 

now (I.e if the client is subscribing to delayed data). 

# Quote Extra Session 

mref  MDF_M_QUOTEEX #44 

mclass  MDF_MC_QUOTEEX 

Tag  Name  Req'd  Comments 

MDF_F_BIDPRICE  Bid Price  N Best Bid Price 

MDF_F_ASKPRICE  Ask Price  N Best Ask Price 

MDF_F_BIDQUANTITY  Bid Quantity  N Quantity at Best Bid 

MDF_F_ASKQUANTITY  Ask Quantity  N Quantity at Best Ask 

MDF_F_LASTPRICE  Last Price  The last paid price today during the extra session, if 

there has been no trades today, the value is NULL. 

MDF_F_DAYHIGHPRICE  Day High Price  N The highest paid price today during the extra session. 

MDF_F_DAYLOWPRICE  Day Low Price  N The lowest paid price today during the extra session. 

MDF_F_QUANTITY  Quantity  N The total quantity for today during the extra session. 

MDF_F_TURNOVER  Turnover  N The total turnover for today during the extra session. 

MDF_F_NUMTRADES  Number of Trades  N The number of trades for today during the extra 

session. 

MDF_F_TIME  Time  N Sent if the quote is for another time than 'now' 

MDF_F_DATE  Date  N Sent if the quote is for another date than 'today'    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Instrument Reset 

mref  MDF_M_INSTRUMENTRESET #13 

mclass  MDF_MC_QUOTE|MDF_MC_QUOTEBBO|MDF_MC_ORDER|MDF_MC_MBO| 

MDF_MC_NETORDERIMBALANCE|MDF_MC_GREEKS 

Tag  Name  Req'd  Comments 

The Instrument Reset message indicates that the client should reset all quote, netorderimbalance, greeks and order book 

data. All quote and netorderimbalance fields should be set to null, and the order book should be removed in full. Since 

the server will not include fields with a null value in the response to a request, clients are free to implement the reset 

procedure to their choosing, for example not setting Last Price to null could be a need for some clients. 

# Trade State 

mref  MDF_M_TRADESTATE #24 

mclass  MDF_MC_TRADESTATE 

Tag  Name  Req'd  Comments 

MDF_F_TRADESTATE  Trade State  N

MDF_F_TRADESTATEACTIONS  Trade State Actions  N

MDF_F_TIME  Time  N

MDF_F_DATE  Date  N

The Trade State message is sent whenever there is a change in the trade state for a tradable instrument and/or market 

place / list. Examples of use can be to know whether a specific market is open or closed. 

The Time and Date fields are sent on all image replies and on stream replies if the trade state is for another time/date 

than now (I.e if the client is subscribing to delayed data). 

# Net Order Imbalance Indicator 

mref  MDF_M_NETORDERIMBALANCE #30 

mclass  MDF_MC_NETORDERIMBALANCE 

Tag  Name  Req'd  Comments 

MDF_F_BIDPRICE  Best Bid Price  N

MDF_F_ASKPRICE  Best Ask Price  N

MDF_F_BIDQUANTITY  Volume of Best Bid  N

MDF_F_ASKQUANTITY  Volume of Best Ask  N

MDF_F_LASTPRICE  Equilibrium Price  N

MDF_F_QUANTITY  Paired Shares  N

MDF_F_IMBALANCE  Imbalance Shares  N

MDF_F_IMBALANCEDIRECTION  Imbalance Direction  N

MDF_F_CROSSTYPE  Cross Type  N

MDF_F_TIME  Time  N

MDF_F_DATE  Date  N

The Net Order Imbalance Indicator (NOII) message is sent whenever there is a change in the NOII for a tradable 

instrument. The Time and Date fields are sent on all image replies and on stream replies if the NOII is for another    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

time/date than now (I.e if the client is subscribing to delayed data). 

# Trade Messages 

# Trade 

mref  MDF_M_TRADE #6 

mclass  MDF_MC_TRADE 

Tag  Name  Req'd  Comments 

MDF_F_TRADEPRICE  Trade Price  N

MDF_F_TRADEYIELD  Trade Yield  N

MDF_F_TRADEQUANTITY  Trade Quantity  N

MDF_F_TRADEREFERENCE  Trade Reference  Y

MDF_F_TRADECODE  Trade Code  Y

MDF_F_MMT  MMT  N

MDF_F_TRADETIME  Trade Time  N

MDF_F_EXECUTEDSIDE  Executed Side  N

MDF_F_TRADETYPE  Trade Type  N

MDF_F_TRADEBUYER  Trade Buyer  N

MDF_F_TRADESELLER  Trade Seller  N

MDF_F_TRADECANCELTIME  Trade Cancel Time  N

MDF_F_TRADEAGREEMENTTIME  Off-Book Trade 

Agreement Time 

N Only for Off-Book trades 

MDF_F_TRADEAGREEMENTDATE  Off-Book Trade 

Agreement Date 

N Only for Off-Book trades 

MDF_F_MIC  Off-Book Trade 

Execution Venue 

N Only for Off-Book trades 

MDF_F_TRADECURRENCY  Off-Book Trade 

Currency 

N Only for Off-Book trades and if the execution 

currency differs from that of the normal trade 

currency of the instrument. 

Each new trade message creates a new record. The exception to this is when Trade Code has either the 

MDF_TC_CORRECTION  or  MDF_TC_CANCEL  flags set. In this case the intent is to modify a previously sent trade. 

Corrections will carry only the required fields and the fields to modify, this happens normally for exchanges where a 

single trade is distributed in two parts (I.e for an iceberg order where the first part is the public volume and the second 

part is the hidden volume), in these cases the second trade will contain the new correct Trade Quantity. 

Trade Cancellations will only carry the required fields and the Trade Cancel Time indicating the time when the trade 

was canceled, it is up to the client whether to delete the original trade or mark it as canceled.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Basic Data Messages 

# Basic Data 

mref  MDF_M_BASICDATA #15 

mclass  MDF_MC_BASICDATA 

Tag  Name  R

e

q' 

d

Comments 

MDF_F_SYMBOL  Symbol  N

MDF_F_NAME  Name  N

MDF_F_ISIN  ISIN  N

MDF_F_BOARDLOT  Board Lot  N

MDF_F_INSTRUMENTTYPE  Instrument Type  N

MDF_F_INSTRUMENTSUBTYPE  Instrument Sub Type  N

MDF_F_SHARECLASS  Share Class  N

MDF_F_DERIVATIVEINDICATOR  Derivative Indicator  N

MDF_F_EXERCISETYPE  Exercise Type  N

MDF_F_ISSUECURRENCY  Issue Currency  N

MDF_F_TRADECURRENCY  Trade Currency  N

MDF_F_BASECURRENCY  Base Currency  N

MDF_F_QUOTECURRENCY  Quote Currency  N

MDF_F_ISSUEDATE  Issue Date  N

MDF_F_ISSUEPRICE  Issue Price  N

MDF_F_STRIKEDATE  Strike Date  N

MDF_F_STRIKEPRICE  Strike Price  N

MDF_F_MARKETPLACE  Market Place  N

MDF_F_PRIMARYMARKETPLACE  Primary Market Place  N

MDF_F_PRIMARYSHARE  Primary Share  N

MDF_F_SUBMARKET  Sub Market  N

MDF_F_LIST  List  N

MDF_F_COMPANY  Company  N

MDF_F_FUNDPPMCODE  Fund PPM Code  N

MDF_F_UNDERLYINGID  Underlying Id  N

MDF_F_FUNDCOMPANY  Fund Company  N

MDF_F_FUNDPMICODE  Fund PMI Code  N

MDF_F_COUNTRY  Country  N

MDF_F_S1  Comment  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_NUMBEROFSHARES  Number of Shares  N

MDF_F_NOMINALVALUE  Nominal Value  N

MDF_F_MIC  MIC  N

MDF_F_OPERATINGMIC  Operating MIC  N

MDF_F_CHAIRMAN  Chairman  N

MDF_F_CEO  Chief Executive Officer  N

MDF_F_WEBSITE  Website  N

MDF_F_ORGNUM  Organisationsnummer  N Swedish Business ID 

MDF_F_ORGNUMNO  Organisasjonsnummer  N Norwegian Business ID 

MDF_F_CVR  CVR  N Danish Business ID 

MDF_F_YTUNNUS  Y-Tunnus/FO-Nummer  N Finnish Business ID 

MDF_F_KENNITALA  Kennitala  N Icelandic Business ID 

MDF_F_SHORTDESCRIPTION  Short Description  N

MDF_F_DESCRIPTION  Long Description  N

MDF_F_SECTOR  Classification Sector  N

MDF_F_GENDERCEO  The gender of the CEO  N

MDF_F_GENDERCHAIRMAN  The gender of the 

Chairman 

N

MDF_F_BIRTHYEARCEO  The birth year of the CEO  N

MDF_F_BIRTYEARCHAIRMAN  The birt year of the 

Chairman 

N

MDF_F_ADDRESS  Company HQ Address  N

MDF_F_POSTALCODE  Company HQ Postal Code  N

MDF_F_CITY  Company HQ City  N

MDF_F_TELEPHONE  Company Telephone 

Number 

N

MDF_F_FAX  Company Fax Number  N

MDF_F_EMAIL  Company E-Mail  N

MDF_F_IMPORTANTEVENTS  Important Events  N

MDF_F_CONTRACTSIZE  Contract Size  N

MDF_F_CONTRACTVALUE  Contract Value  N

MDF_F_BASERATIO  Base Currency Ratio  N

MDF_F_SOURCEID  Source Id  N

MDF_F_ISSUER  Issuer  N

MDF_F_ISSUERNAME  Issuer Name  N

MDF_F_ONGOINGCHARGE  Ongoing Charge  N

MDF_F_FUNDYEARLYMGMTFEE  Fund Yearly Management 

Fee 

N

MDF_F_FUNDPPMFEE  Fund PPM Fee  N

MDF_F_FUNDPPMTYPE  Fund PPM Type  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_FUNDBENCHMARK  Fund Benchmark  N

MDF_F_FUNDBENCHMARKINSREF  Fund Benchmark Insref  N

MDF_F_FUNDLEVERAGE  Fund Leverage  N

MDF_F_FUNDDIRECTION  Fund Direction  N

MDF_F_FUNDRISK  Fund Risk  N

MDF_F_PROSPECTUS  URL of Prospectus  N

MDF_F_GEOFOCUSREGION  Geofocus Region  N

MDF_F_GEOFOCUSCOUNTRY  Geofocus Country  N

MDF_F_OPENINTEREST  Open Interest  N

MDF_F_CUSIP  CUSIP  N

MDF_F_WKN  WKN  N

MDF_F_UCITS  UCITS  N

MDF_F_INCEPTIONDATE  Fund Inception Date  N

MDF_F_INSTRUMENTCLASS  Instrument Class  N

MDF_F_INSTRUMENTSUBCLASS  Instrument Sub Class  N

MDF_F_INSTRUMENTSUBSUBCLA 

SS 

Instrument SubSub Class  N

MDF_F_CONSTITUENTS  Fund/Index Constituents  N Pipe separated list of the constituents 

MDF_F_COUPONRATE  Coupon Rate  N

MDF_F_COUPONDATE  Coupon Date  N

MDF_F_COUPONFREQUENCY  Coupon Frequency  N

MDF_F_BARRIERPRICE  Barrier Price  N

MDF_F_MORNINGSTARRATING  Morningstar Rating  N

MDF_F_SALESFEE  Sales Fee  N

MDF_F_PURCHASEFEE  Purchase Fee  N

MDF_F_MINSTARTAMOUNT  Min Start Amount  N

MDF_F_MINSUBSCRIPTIONAMOU 

NT 

Min Subscription Amount  N

MDF_F_PERFORMANCEFEE  Perrformance Fee  N

MDF_F_MINADDITIONALAMOUNT  Min Additrional Amount  N

MDF_F_CEOADMISSIONDATE  CEO Admission Date  N

MDF_F_CHAIRMANADMISSIONDA 

TE 

Chairman Admission Date  N

MDF_F_TRADEDTHROUGHDATE  Traded Through Date  N

MDF_F_TOTALFEE  Total Fee  N

MDF_F_DIVIDENDTYPE  Dividend Type  N

MDF_F_DIVIDENDFREQUENCY  Dividend Frequency  N

MDF_F_PRICINGFREQUENCY  Pricing Frequency  N

MDF_F_EUSIPA  EUSIPA Code  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_CONVERTFROMDATE  Convert From Date  N

MDF_F_CONVERTTODATE  Convert To Date  N

MDF_F_CONVERSIONPRICE  Conversion Price  N

MDF_F_SETTLEMENTTYPE  Settlement Type  N

MDF_F_CAP  Cap Level  N

MDF_F_TICKTABLE  Tick Size Table  N

MDF_F_TICKSIZES  Tick Sizes Array  N

MDF_F_PRICETYPE  Price Type  N

MDF_F_VOLUMEDIMENSION  Volume Dimension  N

MDF_F_ASIANTAILSTART  Asian Tail Start  N

MDF_F_ASIANTAILEND  Asian Tail End  N

MDF_F_LOGOTYPE  Company Logotype  N

MDF_F_FINANCINGLEVEL  Financing Level  N

MDF_F_PARTICIPATIONRATE  Participation Rate  N

MDF_F_KIID  URL of the Key Investor 

Information Document 

N

MDF_F_CFI  CFI Code  N

MDF_F_BROKERS  Broker codes  N

MDF_F_MAXLEVEL  Max Level  N

MDF_F_OUTSTANDINGAMOUNT  Outstanding Amount  N

MDF_F_INTERESTRATE  Interest Rate  N

MDF_F_MARKETMAKER  Market Maker  N

MDF_F_MARKETOPENDAYS  Market Open Days  N

MDF_F_MARKETOPEN  Market Open Time  N

MDF_F_MARKETCLOSE  Market Closing Time  N

MDF_F_MARKETEARLYCLOSE  Market Early Closing Time  N

MDF_F_SPECIALCONDITION  Special Condition  N

MDF_F_LEGALSTRUCTURE  Legal Structure  N

MDF_F_PRODUCTCODE  Derivative Product Code  N

MDF_F_QUOTINGTYPE  Quoting Type  N

MDF_F_CIK  Central Index Key  N

MDF_F_CSR  Corporate Sustainability 

Rating 

N

MDF_F_ACTIVESHARE  Active Share  N

MDF_F_TRACKINGERROR  Tracking Error  N

MDF_F_FIGI  FIGI  N

MDF_F_FIGICOMPOSITE  Composite FIGI  N

MDF_F_FIGISHARECLASS  Share Class FIGI  N

MDF_F_FIGISECURITYTYPE  FIGI Security Type  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_DAYCOUNTCONVENTION  Day Count Convention  N

MDF_F_EXPIRATIONTYPE  Expiration Type  N

MDF_F_COMBOLEGS  Combo / Strategy Legs  N

MDF_F_SWINGFACTOR  Swing Factor Redemption  N

MDF_F_SWINGFACTORSUB  Swing Factor Subscription  N

MDF_F_SWINGMETHOD  Swing Method  N

MDF_F_CLEARING  Clearing / Custody data  N

The Basic Data message defines the instrument, and is a required message for all instruments in the Millistream 

universe. 

# Localization 

mref  MDF_M_L10N #32 

mclass  MDF_MC_L10N 

Tag  Name  Req 

'd 

Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that an 

existing Localization entry with the same 

Language as this message should be deleted. 

MDF_F_LANGUAGE  Language  Y 04010_Reference_Language for PRIIPv1, 

00120_Reference_Language for PRIIPv2 

MDF_F_NAME  Name  N

MDF_F_SHORTDESCRIPTION  Short Description  N

MDF_F_DESCRIPTION  Long Description  N

MDF_F_IMPORTANTEVENTS  Important Events  N

MDF_F_PROSPECTUS  URL of Prospectus  N

MDF_F_KIID  URL of the Key Investor 

Information Document 

N 05090_UCITS_KID_Web_Address for 

PRIIPv1, 00075_PRIIPs_KID_Web_Address 

for PRIIPv2 

MDF_F_PRIIP02190  02190_Past_Performance 

_Link 

N

MDF_F_PRIIP02200  02200_Previous_Perform 

ance_Scenarios_Calculati 

on_Link 

N

MDF_F_PRIIP04020  04020_Comprehension_ 

Alert_Portfolio 

N

MDF_F_PRIIP04030  04030_Intended_target_ 

market_retail_investor_P 

ortfolio 

N

MDF_F_PRIIP04040  04040_Investment_objec 

tive_Portfolio 

N

MDF_F_PRIIP04050  04050_Risk_narrative_P 

ortfolio 

N

MDF_F_PRIIP04060  04060_Other_materially 

_relevant_risk_narrative_ 

N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

Portfolio 

MDF_F_PRIIP04070  04070_Type_of_underlyi 

ng_Investment_Option 

N

MDF_F_PRIIP04080  04080_Capital_Guarante 

e

N

MDF_F_PRIIP04081  04081_Capital_Guarante 

e_Level 

N

MDF_F_PRIIP04082  04082_Capital_Guarante 

e_Limitations 

N

MDF_F_PRIIP04083  04083_Capital_Guarante 

e_Early_Exit_Conditions 

N

MDF_F_PRIIP04084  04084_Capital_guarantee 

_Portfolio 

N

MDF_F_PRIIP04085  04085_Possible_maximu 

m_loss_Portfolio 

N

MDF_F_PRIIP04086  04086_Description_Past 

_Interval_Unfavourable_ 

Scenario 

N

MDF_F_PRIIP04087  04087_Description_Past 

_Interval_Moderate_Sce 

nario 

N

MDF_F_PRIIP04088  04088_Description_Past 

_Interval_Favourable_Sc 

enario 

N

MDF_F_PRIIP04089  04089_Was_Benchmark_ 

Used_Performance_Calc 

ulation 

N

MDF_F_PRIIP04100  04100_Portolio_Carried_ 

Interest_Narrative 

N

MDF_F_PRIIP04110  04110_Other_comment  N

MDF_F_PRIIP04120  04120_One_Off_Cost_P 

ortfolio_Entry_Cost_Des 

cription 

N

MDF_F_PRIIP04130  04130_One_Off_Cost_P 

ortfolio_Exit_Cost_Desc 

ription 

N

MDF_F_PRIIP04140  04140_Ongoing_Costs_P 

ortfolio_Management_C 

osts_Description 

N

MDF_F_PRIIP04160  04160_Cost_Dependence 

_Explanation 

N

The Localization message provides language dependent overrides to some of the fields in the Basic Data and PRIIP 

messages. Currently, image requests for Localization messages will be treated like stream requests.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Mappings 

mref  MDF_M_MAPPINGS #38 

mclass  MDF_MC_MAPPINGS 

Tag  Name  Req'd  Comments 

MDF_F_MARKETPLACE  Marketplace  N

MDF_F_SECTORMEMBERS  Sector Members  N

The Mappings message provides mappings between different instruments. Currently, image requests for Mappings 

messages will be treated like stream requests.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# PRIIP/MiFID Messages 

# PRIIP EPT 

mr 

ef 

MDF_M_PRIIP #35 

mc 

las 

s

MDF_MC_PRIIP 

Tag  Name EPTv1  Name EPTv2 

MDF_F_FISN  Financial Instrument Short Name  Financial Instrument Short Name 

MDF_F_LEI  Legal Entity Identifier  Legal Entity Identifier 

MDF_F_PRIIP00001  00001_EPT_Version 

MDF_F_PRIIP00002  00002_EPT_Producer_Name 

MDF_F_PRIIP00004  00004_EPT_Producer_Email 

MDF_F_PRIIP00005  00005_File_Generation_Date_And_Time 

MDF_F_PRIIP00006  00006_EPT_Data_Reporting_Narratives 

MDF_F_PRIIP00007  00007_EPT_Data_Reporting_Costs 

MDF_F_PRIIP00008  00008_EPT_Data_Reporting_Additional_Require 

ments_German_MOPs 

MDF_F_PRIIP00009  00009_EPT_Additional_Information_Structured_ 

Products 

MDF_F_PRIIP00010  00010_Portfolio_Issuer_Name  00010_Portfolio_Manufacturer_Name 

MDF_F_PRIIP00015  00015_Portfolio_Manufacturer_Group_Name 

MDF_F_PRIIP00016  00016_Portfolio_Manufacturer_LEI 

MDF_F_PRIIP00017  00017_Portfolio_Manufacturer_Email 

MDF_F_PRIIP00020  00020_Portfolio_Guarantor_Name  00020_Portfolio_Guarantor_Name 

MDF_F_PRIIP00030  00030_Portfolio_Identifying_Data  00030_Portfolio_Identifying_Data 

MDF_F_PRIIP00040  00040_Type_Of_Identification_Code_F 

or_The_Fund_Share_Or_Portfolio 

00040_Type_Of_Identification_Code_For_The_F 

und_Share_Or_Portfolio 

MDF_F_PRIIP00050  00050_Portfolio_Name  00050_Portfolio_Name 

MDF_F_PRIIP00060  00060_Share_Class_Currency  00060_Portfolio_Or_Share_Class_Currency 

MDF_F_DATE  00070_Reference_Date  00070_PRIIPs_KID_Publication_Date 

MDF_F_PRIIP00075  00075_PRIIPs_KID_Web_Address 

MDF_F_PRIIP00080  00080_Portfolio_PRIIPS_Category  00080_Portfolio_PRIIPs_Category 

MDF_F_PRIIP00090  00090_Fund_CIC_code  00090_Fund_CIC_Code 

MDF_F_PRIIP00100  00100_EOS_portfolio 

MDF_F_PRIIP00110  00110_Is_An_Autocallable_Product 

MDF_F_PRIIP01010  01010_Valuation_Frequency  01010_Valuation_Frequency 

MDF_F_PRIIP01020  01020_Portfolio_VEV_Reference  01020_Portfolio_VEV_Reference    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_PRIIP01030  01030_IS_Flexible  01030_IS_Flexible 

MDF_F_PRIIP01040  01040_Flex_VEV_Historical  01040_Flex_VEV_Historical 

MDF_F_PRIIP01050  01050_Flex_VEV_Ref_Asset_Allocatio 

n

01050_Flex_VEV_Ref_Asset_Allocation 

MDF_F_PRIIP01060  01060_IS_Risk_Limit_Relevant  01060_IS_Risk_Limit_Relevant 

MDF_F_PRIIP01070  01070_Flex_VEV_Risk_Limit  01070_Flex_VEV_Risk_Limit 

MDF_F_PRIIP01080  01080_Existing_Credit_Risk  01080_Existing_Credit_Risk 

MDF_F_PRIIP01090  01090_SRI  01090_SRI 

MDF_F_PRIIP01095  01095_IS_SRI_Adjusted 

MDF_F_PRIIP01100  01100_MRM  01100_MRM 

MDF_F_PRIIP01110  01110_CRM  01110_CRM 

MDF_F_PRIIP01120  01120_Recommended_Holding_Period  01120_Recommended_Holding_Period 

MDF_F_PRIIP01125  01125_Has_A_Contractual_Maturity_Date 

MDF_F_STRIKEDATE  01130_Maturity_Date  01130_Maturity_Date 

MDF_F_PRIIP01140  01140_Liquidity_Risk  01140_Liquidity_Risk 

MDF_F_PRIIP02010  02010_Portfolio_return_unfavorable_sc 

enario_1_year 

02010_Portfolio_Return_Unfavourable_Scenario 

_1_Year 

MDF_F_PRIIP02020  02020_Portfolio_return_unfavorable_sc 

enario_half_RHP 

02020_Portfolio_Return_Unfavourable_Scenario 

_Half_RHP 

MDF_F_PRIIP02030  02030_Portfolio_return_unfavorable_sc 

enario_RHP 

02030_Portfolio_Return_Unfavourable_Scenario 

_RHP_Or_First_Call_Date 

MDF_F_PRIIP02032  02032_Autocall_Applied_Unfavourable_Scenari 

o

MDF_F_PRIIP02035  02035_Autocall_Date_Unfavourable_Scenario 

MDF_F_PRIIP02040  02040_Portfolio_return_moderate_scena 

rio_1_year 

02040_Portfolio_Return_Moderate_Scenario_1_ 

Year 

MDF_F_PRIIP02050  02050_Portfolio_return_moderate_scena 

rio_half_RHP 

02050_Portfolio_Return_Moderate_Scenario_Hal 

f_RHP 

MDF_F_PRIIP02060  02060_Portfolio_return_moderate_scena 

rio_RHP 

02060_Portfolio_Return_Moderate_Scenario_RH 

P_Or_First_Call_Date 

MDF_F_PRIIP02062  02062_Autocall_Applied_Moderate_Scenario 

MDF_F_PRIIP02065  02065_Autocall_Date_Moderate_Scenario 

MDF_F_PRIIP02070  02070_Portfolio_return_favorable_scena 

rio_1_year 

02070_Portfolio_Return_Favourable_Scenario_1 

_Year 

MDF_F_PRIIP02080  02080_Portfolio_return_favorable_scena 

rio_half_RHP 

02080_Portfolio_Return_Favourable_Scenario_H 

alf_RHP 

MDF_F_PRIIP02090  02090_Portfolio_return favorable 

scenario_RHP 

02090_Portfolio_Return_Favourable_Scenario_R 

HP_Or_First_Call_Date 

MDF_F_PRIIP02092  02092_Autocall_Applied_Favourable_Scenario 

MDF_F_PRIIP02095  02095_Autocall_Date_Favourable_Scenario 

MDF_F_PRIIP02100  02100_Portfolio_return_stress_scenario 

_1_year 

02100_Portfolio_Return_Stress_Scenario_1_Year    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_PRIIP02110  02110_Portfolio_return_stress_scenario_ 

half_RHP 

02110_Portfolio_Return_Stress_Scenario_Half_R 

HP 

MDF_F_PRIIP02120  02120_Portfolio_return_stress_scenario 

_RHP 

02120_Portfolio_Return_Stress_Scenario_RHP_ 

Or_First_Call_Date 

MDF_F_PRIIP02122  02122_Autocall_Applied_Stress_Scenario 

MDF_F_PRIIP02125  02125_Autocall_Date_Stress_Scenario 

MDF_F_PRIIP02130  02130_Portfolio_number_of_observed_r 

eturn_M0 

02130_Portfolio_Number_Of_Observed_Return_ 

M0 

MDF_F_PRIIP02140  02140_Portfolio_mean_observed_return 

s_M1 

02140_Portfolio_Mean_Observed_Returns_M1 

MDF_F_PRIIP02150  02150_Portfolio_observed_Sigma  02150_Portfolio_Observed_Sigma 

MDF_F_PRIIP02160  02160_Portfolio_observed_Skewness  02160_Portfolio_Observed_Skewness 

MDF_F_PRIIP02170  02170_Portfolio_observed_Excess_Kurt 

osis 

02170_Portfolio_Observed_Excess_Kurtosis 

MDF_F_PRIIP02180  02180_Portfolio_observed_Stressed_Vol 

atility 

02180_Portfolio_Observed_Stressed_Volatility 

MDF_F_PRIIP02185  02185_Portfolio_Past_Performance_Disclosure_ 

Required 

MDF_F_PRIIP02190  02190_Past_Performance_Link 

MDF_F_PRIIP02200  02200_Previous_Performance_Scenarios_Calcula 

tion_Link 

MDF_F_PRIIP02210  02210_Past_Performance_Number_Of_Years 

MDF_F_PRIIP02220  02220_Reference_Invested_Amount 

MDF_F_PRIIP03010  03010_One_off_cost_Portfolio_entry_c 

ost 

03010_One_Off_Cost_Portfolio_Entry_Cost 

MDF_F_PRIIP03015  03015_One_off_cost_Portfolio_entry_c 

ost_Acquired 

03015_One_Off_Cost_Portfolio_Entry_Cost_Ac 

quired 

MDF_F_PRIIP03020  03020_One_off_costs_Portfolio_exit_co 

st_at_RHP 

03020_One_Off_Costs_Portfolio_Exit_Cost_At_ 

RHP 

MDF_F_PRIIP03030  03030_One_off_costs_Portfolio_exit_co 

st_at_1_year 

03030_One_Off_Costs_Portfolio_Exit_Cost_At_ 

1_Year 

MDF_F_PRIIP03040  03040_One_off_costs_Portfolio_exit_co 

st_at_half_RHP 

03040_One_Off_Costs_Portfolio_Exit_Cost_At_ 

Half_RHP 

MDF_F_PRIIP03050  03050_One_off_costs_Portfolio_sliding 

_exit_cost_Indicator 

03050_One_Off_Costs_Portfolio_Sliding_Exit_C 

ost_Indicator 

MDF_F_PRIIP03060  03060_Ongoing_costs_Portfolio_other_ 

costs 

03060_Ongoing_Costs_Management_Fees_And_ 

Other_Administrative_Or_Operating_Costs 

MDF_F_PRIIP03070  03070_Ongoing_costs_Portfolio_manag 

ement_costs 

MDF_F_PRIIP03080  03080_Ongoing_costs_Portfolio_transac 

tion_costs 

03080_Ongoing_Costs_Portfolio_Transaction_Co 

sts 

MDF_F_PRIIP03090  03090_Existing_performance_fees  03090_Existing_Incidental_Costs_Portfolio 

MDF_F_PRIIP03095  03095_Incidental_costs_Portfolio_perfo 

rmance_fees 

03095_Incidental_Costs    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_PRIIP03100  03100_Existing_carried_interest_fees 

MDF_F_PRIIP03105  03105_Incidental_costs_Portfolio_carrie 

d_interest 

MDF_F_LANGUAGE  04010_Reference_Language  00120_Reference_Language 

MDF_F_PRIIP04020  04020_Comprehension_Alert_Portfolio  04020_Comprehension_Alert_Portfolio 

MDF_F_PRIIP04030  04030_Intended_target_market_retail_in 

vestor_Portfolio 

04030_Intended_Target_Market_Retail_Investor_ 

Portfolio 

MDF_F_PRIIP04040  04040_Investment_objective_Portfolio  04040_Investment_Objective_Portfolio 

MDF_F_PRIIP04050  04050_Risk_narrative_Portfolio  04050_Risk_Narrative_Portfolio 

MDF_F_PRIIP04060  04060_Other_materially_relevant_risk_ 

narrative_Portfolio 

04060_Other_Materially_Relevant_Risk_Narrati 

ve_Portfolio 

MDF_F_PRIIP04070  04070_Type_of_underlying_Investment 

_Option 

04070_Type_Of_Underlying_Investment_Option 

MDF_F_PRIIP04080  04080_Capital_Guarantee  04080_Capital_Guarantee 

MDF_F_PRIIP04081  04081_Capital_Guarantee_Level  04081_Capital_Guarantee_Level 

MDF_F_PRIIP04082  04082_Capital_Guarantee_Limitations  04082_Capital_Guarantee_Limitations 

MDF_F_PRIIP04083  04083_Capital_Guarantee_Early_Exit_ 

Conditions 

04083_Capital_Guarantee_Early_Exit_Condition 

s

MDF_F_PRIIP04084  04084_Capital_guarantee_Portfolio  04084_Capital_Guarantee_Portfolio 

MDF_F_PRIIP04085  04085_Possible_maximum_loss_Portfol 

io 

04085_Possible_Maximum_Loss_Portfolio 

MDF_F_PRIIP04086  04086_Description_Past_Interval_Unfavourable_ 

Scenario 

MDF_F_PRIIP04087  04087_Description_Past_Interval_Moderate_Sce 

nario 

MDF_F_PRIIP04088  04088_Description_Past_Interval_Favourable_Sc 

enario 

MDF_F_PRIIP04089  04089_Was_Benchmark_Used_Performance_Cal 

culation 

MDF_F_PRIIP04090  04090_Portfolio_Performance_Fees_Na 

rrative 

04090_Portfolio_Performance_Fees_Carried_Inte 

rest_Narrative 

MDF_F_PRIIP04100  04100_Portolio_Carried_Interest_Narrat 

ive 

MDF_F_PRIIP04110  04110_Other_comment 

MDF_F_PRIIP04120  04120_One_Off_Cost_Portfolio_Entry_Cost_Des 

cription 

MDF_F_PRIIP04130  04130_One_Off_Cost_Portfolio_Exit_Cost_Desc 

ription 

MDF_F_PRIIP04140  04140_Ongoing_Costs_Portfolio_Management_ 

Costs_Description 

MDF_F_PRIIP04150  04150_Do_Costs_Depend_On_Invested_Amount 

MDF_F_PRIIP04160  04160_Cost_Dependence_Explanation 

MDF_F_PRIIP05010  05010_PRIIP_data_delivery    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_PRIIP05020  05020_UCITS_data_delivery 

MDF_F_PRIIP05030  05030_Portfolio_UCITS_SRRI 

MDF_F_PRIIP05040  05040_Portfolio_UCITS_Vol 

MDF_F_PRIIP05050  05050_Ongoing_costs_Portfolio_other_ 

costs_UCITS 

MDF_F_PRIIP05060  05060_Ongoing_costs_Portfolio_transac 

tion_costs 

MDF_F_PRIIP05065  05065_Transactions_costs_methodology 

MDF_F_PRIIP05070  05070_Incidental_costs_Portfolio_perfo 

rmance_fees_UCITS 

MDF_F_PRIIP05080  05080_Incidental_costs_Portfolio_carrie 

d_interest_UCITS 

MDF_F_KIID  05090_UCITS_KID_Web_Address 

MDF_F_PRIIP06005  06005_German_MOPs_Reference_Date 

MDF_F_PRIIP06010  06010_Bonds_Weight  06010_Bonds_Weight 

MDF_F_PRIIP06020  06020_Annualized_Return_Volatility  06020_Annualized_Return_Volatility 

MDF_F_PRIIP06030  06030_Duration_Bonds  06030_Duration_Bonds 

MDF_F_PRIIP06040  06040_Existing_Capital_Preservation  06040_Existing_Capital_Preservation 

MDF_F_PRIIP06050  06050_Capital_Preservation_Level  06050_Capital_Preservation_Level 

MDF_F_PRIIP06060  06060_Time_Interval_Maximum_Loss  06060_Time_Interval_Maximum_Loss 

MDF_F_PRIIP06070  06070_Uses_PI  06070_Uses_PI 

MDF_F_PRIIP06080  06080_Multiplier_PI  06080_Multiplier_PI 

MDF_F_PRIIP07005  07005_First_Possible_Call_Date 

MDF_F_PRIIP07010  07010_Total_cost_1_year  07010_Total_Cost_1_Year_Or_First_Call 

MDF_F_PRIIP07020  07020_RIY_1_year  07020_RIY_1_Year_Or_First_Call 

MDF_F_PRIIP07030  07030_Total_cost_half_RHP  07030_Total_Cost_Half_RHP 

MDF_F_PRIIP07040  07040_RIY_half_RHP  07040_RIY_Half_RHP 

MDF_F_PRIIP07050  07050_Total_cost_RHP  07050_Total_Cost_RHP 

MDF_F_PRIIP07060  07060_RIY_RHP  07060_RIY_RHP 

MDF_F_PRIIP07070  07070_One_off_costs_Portfolio_entry_c 

ost_RIY 

07070_One_Off_Costs_Portfolio_Entry_Cost 

MDF_F_PRIIP07080  07080_One_off_costs_Portfolio_exit_co 

st_RIY 

07080_One_Off_Costs_Portfolio_Exit_Cost 

MDF_F_PRIIP07090  07090_Ongoing_costs_Portfolio_transac 

tion_costs_RIY 

07090_Ongoing_Costs_Portfolio_Transaction_Co 

sts 

MDF_F_PRIIP07100  07100_Ongoing_costs_Other_ongoing_ 

costs_RIY 

07100_Ongoing_Costs_Management_Fees_And_ 

Other_Administrative_Or_Operating_Costs 

MDF_F_PRIIP07110  07110_Incidental_costs_Portfolio_perfor 

mance_fees_RIY 

07110_Incidental_Costs_Portfolio_Performance_ 

Fees_Carried _Interest 

MDF_F_PRIIP07120  07120_Incidental_costs_Portfolio_carrie 

d_interests_RIY    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# MiFID EMT 

mref  MDF_M_MIFID #36 

mclass  MDF_MC_MIFID 

Tag  Name EMTv1  Name EMTv3 

MDF_F_MIFID00001  00001_EMT_Version 

MDF_F_MIFID00002  00002_EMT_Producer_Name 

MDF_F_MIFID00003  00003_EMT_Producer_LEI 

MDF_F_MIFID00004  00004_EMT_Producer_Email 

MDF_F_MIFID00005  00005_File_Generation_Date_and_Time 

MDF_F_MIFID00006  00006_EMT_Data_Reporting_Target_Mark 

et 

MDF_F_MIFID00007  00007_EMT_Data_Reporting_ExAnte 

MDF_F_MIFID00008  00008_EMT_Data_Reporting_ExPost 

MDF_F_MIFID00010  00010_Financial_Instrument_Identifying_D 

ata 

00010_Financial_Instrument_Identifying_D 

ata 

MDF_F_MIFID00020  00020_Type_Of_Identification_Code_For_ 

The_Financial_Instrument 

00020_Type_Of_Identification_Code_For_ 

The_Financial_Instrument 

MDF_F_MIFID00030  00030_Financial_Instrument_Name  00030_Financial_Instrument_Name 

MDF_F_MIFID00040  00040_Financial_Instrument_Currency  00040_Financial_Instrument_Currency 

MDF_F_MIFID00045  00045_Financial_Instrument_Performance_ 

Fee 

MDF_F_MIFID00047  00047_Financial_Instrument_Distribution_ 

Of_Cash 

MDF_F_DATE  00050_Reporting_Date  00050_General_Reference_Date 

MDF_F_MIFID00060  00060_Financial_Instrument_Legal_Structu 

re 

00060_Financial_Instrument_Product_Type 

MDF_F_STRIKEDATE  00065_Maturity_Date 

MDF_F_MIFID00070  00070_Financial_Instrument_Issuer_Name  00070_Financial_Instrument_Manufacturer_ 

Name 

MDF_F_MIFID00073  00073_Financial_Instrument_Manufacturer_ 

LEI 

MDF_F_MIFID00074  00074_Financial_Instrument_Manufacturer_ 

Email 

MDF_F_MIFID00075  00075_Financial_Instrument_Manufacturer_ 

Product_Governance_Process 

MDF_F_MIFID00080  00080_Financial_Instrument_Guarantor_Na 

me 

00080_Financial_Instrument_Guarantor_Na 

me 

MDF_F_MIFID00085  00085_Financial_Instrument_Type_ 

Notional_or_Item_Based 

MDF_F_MIFID00090  00090_Product_Category_or_Nature  00090_Product_Category_or_Nature_Germ 

any    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_MIFID00095  00095_Structured_Securities_Product_Cate 

gory_or_Nature 

MDF_F_MIFID00100  00100_Leveraged_Financial_Instrument_or 

_Contingent_Liability_Instrument 

00100_Leveraged_Financial_Instrument_or 

_Contingent_Liability_Instrument 

MDF_F_MIFID00110  00110_Fund_Share_Class_Without_Retroce 

ssion 

MDF_F_MIFID00120  00120_Ex_Post_Cost_Calculation_Basis_Ita 

ly 

MDF_F_MIFID01000  01000_Target_Market_Reference_Date 

MDF_F_MIFID01010  01010_Investor_Type_Retail  01010_Investor_Type_Retail 

MDF_F_MIFID01020  01020_Investor_Type_Professional  01020_Investor_Type_Professional 

MDF_F_MIFID01030  01030_Investor_Type_Eligible_Counterpart 

y

01030_Investor_Type_Eligible_Counterpart 

y

MDF_F_MIFID02010  02010_Basic_Investor  02010_Basic_Investor 

MDF_F_MIFID02020  02020_Informed_Investor  02020_Informed_Investor 

MDF_F_MIFID02030  02030_Advanced_Investor  02030_Advanced_Investor 

MDF_F_MIFID02040  02040_Expert_Investor_Germany  02040_Expert_Investor_Germany 

MDF_F_MIFID03010  03010_No_Capital_Loss  03010_Compatible_With_Clients_Who_Can 

_Not_Bear_Capital_Loss 

MDF_F_MIFID03020  03020_Limited_Capital_Loss  03020_Compatible_With_Clients_Who_Can 

_Bear_Limited_Capital_Loss 

MDF_F_MIFID03030  03030_Limited_Capital_Loss_Level  03030_Limited_Capital_Loss_Level 

MDF_F_MIFID03040  03040_No_Capital_Guarantee  03040_Compatible_With_Clients_Who_Do 

_Not_Need_Capital_Guarantee 

MDF_F_MIFID03050  03050_Loss_Beyond_Capital  03050_Compatible_With_Clients_Who_Can 

_Bear_Loss_Beyond_Capital 

MDF_F_MIFID04010  04010_Risk_Tolerance_PRIIPS_Methodolo 

gy 

04010_Risk_Tolerance_PRIIPS_Methodolo 

gy 

MDF_F_MIFID04020  04020_Risk_Tolerance_UCITS_Metholodol 

ogy 

04020_Risk_Tolerance_UCITS_Methodolo 

gy 

MDF_F_MIFID04030  04030_Risk_Tolerance_Internal 

_Methodology_For_Non_PRIIPS_and_Non 

_UCITS 

04030_Risk_Tolerance_Internal_Methodolo 

gy_For_Non_PRIIPS_and_Non_UCITS 

MDF_F_MIFID04040  04040_Risk_Tolerance_For_Non_PRIIPS_a 

nd_Non_UCITS_Spain 

04040_Risk_Tolerance_For_Non_PRIIPS_a 

nd_Non_UCITS_Spain 

MDF_F_MIFID04050  04050_Not_For_Investors_With_The_Lowe 

st_Risk_Tolerance_Germany 

04050_Not_For_Investors_With_The_Lowe 

st_Risk_Tolerance_Germany 

MDF_F_MIFID05010  05010_Return_Profile_Preservation  05010_Return_Profile_Client_looking_for_ 

Preservation 

MDF_F_MIFID05020  05020_Return_Profile_Growth  05020_Return_Profile_Client_looking_for_ 

Capitalized_Growth 

MDF_F_MIFID05030  05030_Return_Profile_Income  05030_Return_Profile_Client_looking_for_I 

ncome 

MDF_F_MIFID05040  05040_Return_Profile_Hedging  05040_Return_Profile_Hedging    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_MIFID05050  05050_Option_or_Leveraged_Return_Profil 

e

05050_Option_or_Leveraged_Return_Profil 

e

MDF_F_MIFID05060  05060_Return_Profile_Other 

MDF_F_MIFID05070  05070_Return_Profile_Pension_Scheme_Ge 

rmany 

05070_Return_Profile_Pension_Scheme_Ge 

rmany 

MDF_F_MIFID05080  05080_Time_Horizon (enums)  05080_Minimum_Recommended_Holding_ 

Period 

MDF_F_MIFID05080N  05080_Time_Horizon (in years)  05080_Minimum_Recommended_Holding_ 

Period 

MDF_F_STRIKEDATE  05090_Maturity_Date  00065_Maturity_Date 

MDF_F_MIFID05100  05100_May_Be_Terminated_Early  00067_May_Be_Terminated_Early 

MDF_F_MIFID05105  05105_Intended_Compatible_With_Clients_ 

Having_ESG_Preferences 

MDF_F_MIFID05110  05110_Specific_Investment_Need 

MDF_F_MIFID05115  05115_Other_Specific_Investment_Need 

MDF_F_MIFID06010  06010_Execution_Only  06010_Execution_Only 

MDF_F_MIFID06020  06020_Execution_With_Appropriateness_T 

est_Or_Non_Advised_Services 

06020_Execution_With_Appropriateness_T 

est_Or_Non_Advised_Services 

MDF_F_MIFID06030  06030_Investment_Advice  06030_Investment_Advice 

MDF_F_MIFID06040  06040_Portfolio_Management  06040_Portfolio_Management 

MDF_F_MIFID07010  07010_Structured_Securities_Quotation  00096_Structured_Securities_Quotation 

MDF_F_MIFID07020  07020_One-

off_cost_Financial_Instrument_entry_cost 

07020_Gross_One-

off_cost_Financial_Instrument_maximum_e 

ntry_cost_non_acquired 

MDF_F_MIFID07025  07025_Net_One-

off_cost_Financial_Instrument_entry_cost_n 

on_acquired 

MDF_F_MIFID07030  07030_One-

off_cost_Financial_Instrument_maximum_e 

ntry_cost_fixed_amount_Italy 

07030_One-

off_cost_Financial_Instrument_maximum_e 

ntry_cost_fixed_amount_Italy 

MDF_F_MIFID07040  07040_One-

off_cost_Financial_Instrument_maximum_e 

ntry_cost_acquired 

07040_One-

off_cost_Financial_Instrument_maximum_e 

ntry_cost_acquired 

MDF_F_MIFID07050  07050_One-

off_costs_Financial_Instrument_maximum_ 

exit_cost 

07050_One-

off_costs_Financial_Instrument_maximum_ 

exit_cost_non_acquired 

MDF_F_MIFID07060  07060_One-

off_costs_Financial_Instrument_maximum_ 

exit_cost_fixed_amount_Italy 

07060_One-

off_costs_Financial_Instrument_maximum_ 

exit_cost_fixed_amount_Italy 

MDF_F_MIFID07070  07070_One-

off_costs_Financial_Instrument_maximum_ 

exit_cost_acquired 

07070_One-

off_costs_Financial_Instrument_maximum_ 

exit_cost_acquired 

MDF_F_MIFID07080  07080_One-

off_costs_Financial_Instrument_Typical_exi 

t_cost 

07080_One-

off_costs_Financial_Instrument_Typical_exi 

t_cost    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_MIFID07090  07090_One-

off_cost_Financial_Instrument_exit_cost_str 

uctured_securities_prior_RHP 

07090_One-

off_Cost_Financial_Instrument_Exit_Cost_ 

Structured_Products_Prior_RHP 

MDF_F_MIFID07100  07100_Financial_Instrument_Ongoing_cost 

s

07100_Financial_Instrument_Gross_Ongoin 

g_costs 

MDF_F_MIFID07105  07105_Financial_Instrument_Gearing_costs 

_ex_ante_UK 

MDF_F_MIFID07110  07110_Financial_Instrument_Management_ 

fee 

07110_Financial_Instrument_Management_ 

fee 

MDF_F_MIFID07120  07120_Financial_Instrument_Distribution_f 

ee 

07120_Financial_Instrument_Distribution_f 

ee 

MDF_F_MIFID07130  07130_Financial_Instrument_Transaction_c 

osts_ex_ante 

07130_Financial_Instrument_Transaction_c 

osts_ex_ante 

MDF_F_MIFID07140  07140_Financial_Instrument_Incidental_cos 

ts_ex_ante 

07140_Financial_Instrument_Incidental_cos 

ts_ex_ante 

MDF_F_MIFID07150  07150_Structured_Securities_Reference_Pri 

ce_ex_ante 

MDF_F_MIFID07155  07155_Structured_Securities_Notional_Refe 

rence_Amount_ex_ante 

MDF_F_MIFID07160  07160_Ex_Ante_Costs_Reference_Date 

MDF_F_MIFID08010  08010_One-

off_cost_Structured_Securities_entry_cost_e 

x_post 

08010_Gross_One-

off_cost_Structured_Securities_entry_cost_e 

x_post 

MDF_F_MIFID08015  08015_Net_One-

off_cost_Structured_Securities_entry_cost_e 

x_post 

MDF_F_MIFID08020  08020_One-

off_costs_Structured_Securities_exit_cost_e 

x_post 

08020_One-

off_costs_Structured_Securities_exit_cost_e 

x_post 

MDF_F_MIFID08025  08025_One-

off_cost_Financial_Instrument_entry_cost_a 

cquired 

MDF_F_MIFID08030  08030_Financial_Instrument_Ongoing_cost 

s_ex_post 

08030_Financial_Instrument_Ongoing_cost 

s_ex_post 

MDF_F_MIFID08040  08040_Structured_Securities_Ongoing_cost 

s_ex_post_accumulated 

08040_Structured_Securities_Ongoing_cost 

s_ex_post_accumulated 

MDF_F_MIFID08045  08045_Financial_Instrument_Borrowing_C 

osts_Ex_Post_UK 

MDF_F_MIFID08050  08050_Financial_Instrument_Management_ 

fee_ex_post 

08050_Financial_Instrument_Management_ 

fee_ex_post 

MDF_F_MIFID08060  08060_Financial_Instrument_Distribution_f 

ee_ex_post 

08060_Financial_Instrument_Distribution_f 

ee_ex_post 

MDF_F_MIFID08070  08070_Financial_Instrument_Transaction_c 

osts_ex_post 

08070_Financial_Instrument_Transaction_c 

osts_ex_post 

MDF_F_MIFID08080  08080_Financial_Instrument_Incidental_cos 

ts_ex_post 

08080_Financial_Instrument_Incidental_cos 

ts_ex_post    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_MIFID08090  08090_Beginning_Of_Calculation_Period  08090_Beginning_Of_Reference_Period 

MDF_F_MIFID08100  08100_End_Of_Calculation_Period  08100_End_Of_Reference_Period 

MDF_F_MIFID08110  08110_Structured_Securities_Reference_Pri 

ce_ex_post 

MDF_F_MIFID08120  08120_Structured 

Securities_Notional_Reference_Amount 

# MiFID EMT History 

mref  MDF_M_MIFIDHISTORY #37 

mclass  MDF_MC_MIFIDHISTORY 

Tag  Name EMTv1  Name EMTv3 

MDF_F_DATE  Date when the Cost & Charges Ex-Post 

Section changed 

Date when the Cost & Charges Ex-Post 

Section changed 

MDF_F_MIFID08010  08010_One-

off_cost_Structured_Securities_entry_cost_e 

x_post 

08010_Gross_One-

off_cost_Structured_Securities_entry_cost_e 

x_post 

MDF_F_MIFID08015  08015_Net_One-

off_cost_Structured_Securities_entry_cost_e 

x_post 

MDF_F_MIFID08020  08020_One-

off_costs_Structured_Securities_exit_cost_e 

x_post 

08020_One-

off_costs_Structured_Securities_exit_cost_e 

x_post 

MDF_F_MIFID08025  08025_One-

off_cost_Financial_Instrument_entry_cost_a 

cquired 

MDF_F_MIFID08030  08030_Financial_Instrument_Ongoing_costs 

_ex_post 

08030_Financial_Instrument_Ongoing_costs 

_ex_post 

MDF_F_MIFID08040  08040_Structured_Securities_Ongoing_costs 

_ex_post_accumulated 

08040_Structured_Securities_Ongoing_costs 

_ex_post_accumulated 

MDF_F_MIFID08045  08045_Financial_Instrument_Borrowing_Co 

sts_Ex_Post_UK 

MDF_F_MIFID08046  08046_Financial_Instrument_Gearing_costs 

_ex_post_UK 

MDF_F_MIFID08050  08050_Financial_Instrument_Management_f 

ee_ex_post 

08050_Financial_Instrument_Management_f 

ee_ex_post 

MDF_F_MIFID08060  08060_Financial_Instrument_Distribution_f 

ee_ex_post 

08060_Financial_Instrument_Distribution_fe 

e_ex_post 

MDF_F_MIFID08070  08070_Financial_Instrument_Transaction_c 

osts_ex_post 

08070_Financial_Instrument_Transaction_c 

osts_ex_post 

MDF_F_MIFID08080  08080_Financial_Instrument_Incidental_cos 

ts_ex_post 

08080_Financial_Instrument_Incidental_cost 

s_ex_post 

MDF_F_MIFID08085  08085_Financial_Instrument_Performance_ 

Fee_costs_ex_post    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_MIFID08090  08090_Beginning_Of_Calculation_Period  08090_Beginning_Of_Reference_Period 

MDF_F_MIFID08100  08100_End_Of_Calculation_Period  08100_End_Of_Reference_Period 

MDF_F_MIFID08110  08110_Structured_Securities_Reference_Pri 

ce_ex_post 

MDF_F_MIFID08120  08120_Structured 

Securities_Notional_Reference_Amount    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# History Messages 

# Price History 

mref  MDF_M_PRICEHISTORY #16 

mclass  MDF_MC_PRICEHISTORY 

Tag  Name  Req'd  Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that 

an existing Price History entry with the 

same Date as this message should be 

deleted. 

MDF_F_DATE  Date  Y

MDF_F_TIME  Time  Y Note that time for PriceHistory is only 

indicative and not meant to be used for 

display purposes, instead the main use 

case for time here is to order events 

between PriceHistory and 

CorporateActions. 

MDF_F_CLOSEPRICETYPE  Close Price Type  N

MDF_F_OPENPRICE  Open Price  N

MDF_F_CLOSEPRICE  Close Price  N

MDF_F_CLOSETRADEPRICE  Close Trade Price  N

MDF_F_CLOSEBIDPRICE  Close Bid Price  N

MDF_F_CLOSEASKPRICE  Close Ask Price  N

MDF_F_CLOSEDAYHIGHPRICE  Close Day High Price  N

MDF_F_CLOSEDAYLOWPRICE  Close Day Low Price  N

MDF_F_CLOSEQUANTITY  Close Quantity  N

MDF_F_CLOSEINTERNALQUANTITY  Close Internal Quantity  N

MDF_F_CLOSEOFFBOOKQUANTITY  Close Off-Book Quantity  N

MDF_F_CLOSEDARKQUANTITY  Close Dark Pool Quantity  N

MDF_F_CLOSETURNOVER  Close Turnover  N

MDF_F_CLOSEINTERNALTURNOVER  Close Internal Turnover  N

MDF_F_CLOSEOFFBOOKTURNOVER  Close Off-Book Turnover  N

MDF_F_CLOSEDARKTURNOVER  Close Dark Pool Turnover  N

MDF_F_CLOSENUMTRADES  Close Number of Trades  N

MDF_F_OPENYIELD  Open Yield  N

MDF_F_CLOSEBIDYIELD  Close Bid Yield  N

MDF_F_CLOSEASKYIELD  Close Ask Yield  N

MDF_F_CLOSEYIELD  Close Yield  N

MDF_F_CLOSEDAYHIGHYIELD  Close Day High Yield  N

MDF_F_CLOSEDAYLOWYIELD  Close Day Low Yield  N

MDF_F_CLOSENAV  Close NAV  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_CLOSETIS  Close TIS  N

MDF_F_CLOSEVWAP  Close VWAP  N

Currently responses to image requests will only send the latest Price History image. Even though the message contains 

the Open Price and Open Yield Price fields, the Price History message will only be sent when the market is closed. 

# Performance 

mref  MDF_M_PERFORMANCE #26 

mclass  MDF_MC_PERFORMANCE 

Tag  Name  Req'd  Comments 

MDF_F_DATE  Date  N

MDF_F_TIME  Time  N

MDF_F_CLOSEBIDPRICE1D  Close Bid Price 1 Day  N

MDF_F_CLOSEBIDPRICE1W  Close Bid Price 1 Week  N

MDF_F_CLOSEPRICE1D  Close Price 1 Day  N

MDF_F_CLOSEPRICE1W  Close Price 1 Week  N

MDF_F_CLOSEPRICE2W  Close Price 2 Weeks  N

MDF_F_CLOSEPRICE1M  Close Price 1 Month  N

MDF_F_CLOSEPRICE3M  Close Price 3 Months  N

MDF_F_CLOSEPRICE6M  Close Price 6 Months  N

MDF_F_CLOSEPRICE9M  Close Price 9 Months  N

MDF_F_CLOSEPRICE1Y  Close Price 1 Year  N

MDF_F_CLOSEPRICE2Y  Close Price 2 Years  N

MDF_F_CLOSEPRICE3Y  Close Price 3 Years  N

MDF_F_CLOSEPRICE4Y  Close Price 4 Years  N

MDF_F_CLOSEPRICE5Y  Close Price 5 Years  N

MDF_F_CLOSEPRICE6Y  Close Price 6 Years  N

MDF_F_CLOSEPRICE7Y  Close Price 7 Years  N

MDF_F_CLOSEPRICE8Y  Close Price 8 Years  N

MDF_F_CLOSEPRICE9Y  Close Price 9 Years  N

MDF_F_CLOSEPRICE10Y  Close Price 10 Years  N

MDF_F_CLOSEPRICEWTD  Close Price Week-To-Date  N

MDF_F_CLOSEPRICEMTD  Close Price Month-To-Date  N

MDF_F_CLOSEPRICEQTD  Close Price Quarter-To-Date  N

MDF_F_CLOSEPRICEYTD  Close Price Year-To-Date  N

MDF_F_CLOSEPRICEPYTD  Close Price Previous Year-To-Date  N

MDF_F_CLOSEPRICELD  Close Price Since Listing Date  N

MDF_F_CLOSEBIDYIELD1D  Close Bid Yield 1 Day  N

MDF_F_CLOSEBIDYIELD1W  Close Bid Yield 1 Week  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_CLOSEYIELD1D  Close Yield 1 Day  N

MDF_F_CLOSEYIELD1W  Close Yield 1 Week  N

MDF_F_CLOSEYIELD2W  Close Yield 2 Weeks  N

MDF_F_CLOSEYIELD1M  Close Yield 1 Month  N

MDF_F_CLOSEYIELD3M  Close Yield 3 Months  N

MDF_F_CLOSEYIELD6M  Close Yield 6 Months  N

MDF_F_CLOSEYIELD9M  Close Yield 9 Months  N

MDF_F_CLOSEYIELD1Y  Close Yield 1 Year  N

MDF_F_CLOSEYIELD2Y  Close Yield 2 Years  N

MDF_F_CLOSEYIELD3Y  Close Yield 3 Years  N

MDF_F_CLOSEYIELD4Y  Close Yield 4 Years  N

MDF_F_CLOSEYIELD5Y  Close Yield 5 Years  N

MDF_F_CLOSEYIELD6Y  Close Yield 6 Years  N

MDF_F_CLOSEYIELD7Y  Close Yield 7 Years  N

MDF_F_CLOSEYIELD8Y  Close Yield 8 Years  N

MDF_F_CLOSEYIELD9Y  Close Yield 9 Years  N

MDF_F_CLOSEYIELD10Y  Close Yield 10 Years  N

MDF_F_CLOSEYIELDWTD  Close Yield Week-To-Date  N

MDF_F_CLOSEYIELDMTD  Close Yield Month-To-Date  N

MDF_F_CLOSEYIELDQTD  Close Yield Quarter-To-Date  N

MDF_F_CLOSEYIELDYTD  Close Yield Year-To-Date  N

MDF_F_CLOSEYIELDPYTD  Close Yield Previous Year-To-Date  N

MDF_F_CLOSEYIELDLD  Close Yield Since Listing Date  N

MDF_F_ATH  All-Time-High  N

MDF_F_ATL  All-Time-Low  N

MDF_F_HIGHPRICE1Y  High Price 1 Year  N

MDF_F_LOWPRICE1Y  Low Price 1 Year  N

MDF_F_HIGHPRICE3Y  High Price 3 Years  N

MDF_F_LOWPRICE3Y  Low Price 3 Years  N

MDF_F_HIGHPRICE5Y  High Price 5 Years  N

MDF_F_LOWPRICE5Y  Low Price 5 Years  N

MDF_F_HIGHPRICE10Y  High Price 10 Years  N

MDF_F_LOWPRICE10Y  Low Price 10 Years  N

MDF_F_ATHDATE  All-Time-High Date  N

MDF_F_ATLDATE  All-Time-Low Date  N

MDF_F_HIGHPRICE1YDATE  High Price 1 Year Date  N

MDF_F_LOWPRICE1YDATE  Low Price 1Year Date  N

MDF_F_HIGHPRICEYTD  High Price Year-To-Date  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_LOWPRICEYTD  Low Price Year-To-Date  N

MDF_F_HIGHPRICEYTDDATE  Date of the HighPriceYTD Price  N

MDF_F_LOWPRICEYTDDATE  Date of the LowPriceYTD Price  N

MDF_F_ATHYIELD  All-Time-High Yield  N

MDF_F_ATLYIELD  All-Time-Low Yield  N

MDF_F_HIGHYIELD1Y  High Yield 1 Year  N

MDF_F_LOWYIELD1Y  Low Yield 1 Year  N

MDF_F_ATHYIELDDATE  All-Time-High Yield Date  N

MDF_F_ATLYIELDDATE  All-Time-Low Yield Date  N

MDF_F_HIGHYIELD1YDATE  High Yield 1 Year Date  N

MDF_F_LOWYIELD1YDATE  Low Yield 1Year Date  N

MDF_F_HIGHYIELDYTD  High Yield Year-To-Date  N

MDF_F_LOWYIELDYTD  Low Yield Year-To-Date  N

MDF_F_HIGHYIELDYTDDATE  Date of the HighYieldYTD value  N

MDF_F_LOWYIELDYTDDATE  Date of the LowYieldYTD value  N

MDF_F_ANNUALIZEDRETURN1Y  Annualized Return 1Y  N

MDF_F_ANNUALIZEDRETURN2Y  Annualized Return 2Y  N

MDF_F_ANNUALIZEDRETURN3Y  Annualized Return 3Y  N

MDF_F_ANNUALIZEDRETURN4Y  Annualized Return 4Y  N

MDF_F_ANNUALIZEDRETURN5Y  Annualized Return 5Y  N

MDF_F_ANNUALIZEDRETURN10Y  Annualized Return 10Y  N

MDF_F_SHARPERATION3Y  Sharpe Ratio 3Y  N

MDF_F_STANDARDDEVIATION3Y  Standard Deviation 3Y  N

MDF_F_NORMANAMOUNT  Norman Amount  N

MDF_F_CLOSEPRICE  Current Close Price  N Difference with ClosePrice1D 

is that this is set immediately 

when the share closes, used to 

calculate the proper net 

change for the QuoteEx data. 

MDF_F_CLOSEPRICEDATE  Date of Current Close Price value  N

MDF_F_CLOSEPRICE1DDATE  Date of Close Price 1 Day  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Corporate Action Messages 

# Corporate Action 

mref  MDF_M_CORPORATEACTION #23 

mclass  MDF_MC_CORPORATEACTION 

Tag  Name  Req'd  Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that an 

existing Corporate Action entry with the 

same Date and Time as this message 

should be deleted. 

MDF_F_DATE  Date  Y

MDF_F_TIME  Time  Y

MDF_F_CATYPE  Corporate Action Type  Y

MDF_F_CASUBTYPE  Corporate Action Sub Type  N

MDF_F_DIVIDEND  Dividend  N

MDF_F_DIVIDENDORIGINAL  Original Dividend  N

MDF_F_ADJUSTMENTFACTOR  Adjustment Factor  N

MDF_F_NUMBEROFSHARES  Number of Shares  N

MDF_F_NUMBEROFSHARESDELTA  Number of Shares Delta  N

MDF_F_NEWSHARES  New Shares  N

MDF_F_OLDSHARES  Old Shares  N

MDF_F_SUBSCRIPTIONPRICE  Subscription Price  N

MDF_F_PERIOD  Period  N

MDF_F_FISCALPERIOD  Fiscal Period  N

MDF_F_NOMINALVALUE  Nominal Value  N

MDF_F_RECORDDATE  Record Date  N

MDF_F_PAYMENTDATE  Payment Date  N

MDF_F_ANNOUNCEMENTDATE  Announcement Date  N

MDF_F_S1  Comment #1  N Used for “position” for insiders 

MDF_F_S2  Comment #2  N Used for “relation” for insiders 

MDF_F_S3  Comment #3  N Used for “equity type” for insiders 

MDF_F_S4  Comment #4  N Used for “equity subtype” for insiders 

MDF_F_S5  Comment #5  N Used for “transaction code” for insiders 

MDF_F_TID  TID  N

MDF_F_CLOSEPRICE  Close Price  N

MDF_F_ISSUECURRENCY  Issue Currency  N

MDF_F_TRADECURRENCY  Trade Currency  N

MDF_F_UNDERLYINGID  Underlying Id  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_SYMBOL  Symbol  N

MDF_F_NAME  Name  N

MDF_F_ISIN  ISIN  N

MDF_F_BOARDLOT  Board Lot  N

MDF_F_MARKETPLACE  Market Place  N

MDF_F_LIST  List  N

MDF_F_REDEMPTIONPRICE  Redemption Price  N

MDF_F_VOTINGPOWERPRC  Percentage of Voting 

Power 

N

MDF_F_CAPITALPRC  Percentage of Capital  N

MDF_F_SHARECLASS  Share Class  N

Currently image requests for Corporate Action messages will be treated like stream requests. 

# Company Information 

mref  MDF_M_CI #33 

mclass  MDF_MC_CI 

Tag  Name  Req'd  Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that 

an existing Company Information entry 

with the same Insref, Type and Sequence 

as this message should be deleted. 

MDF_F_CITYPE  Type  Y

MDF_F_CISUBTYPE  Sub Type  N

MDF_F_SEQUENCE  Sequence  Y

MDF_F_S1  String Value #1  N

MDF_F_S2  String Value #2  N

MDF_F_S3  String Value #3  N

MDF_F_S4  String Value #4  N

MDF_F_S5  String Value #5  N

MDF_F_S6  String Value #6  N

MDF_F_S7  String Value #7  N

MDF_F_S8  String Value #8  N

MDF_F_S9  String Value #9  N

MDF_F_S10  String Value #10  N

MDF_F_S11  String Value #11  N

MDF_F_S12  String Value #12  N

MDF_F_S13  String Value #13  N

MDF_F_S14  String Value #14  N

MDF_F_S15  String Value #15  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_N1  Numeric Value #1  N

MDF_F_N2  Numeric Value #2  N

MDF_F_N3  Numeric Value #3  N

MDF_F_N4  Numeric Value #4  N

MDF_F_N5  Numeric Value #5  N

MDF_F_N6  Numeric Value #6  N

MDF_F_N7  Numeric Value #7  N

MDF_F_N8  Numeric Value #8  N

MDF_F_N9  Numeric Value #9  N

MDF_F_N10  Numeric Value #10  N

MDF_F_I1  Integer Value #1  N

MDF_F_I2  Integer Value #2  N

MDF_F_I3  Integer Value #3  N

MDF_F_I4  Integer Value #4  N

MDF_F_I5  Integer Value #5  N

MDF_F_I6  Integer Value #6  N

MDF_F_I7  Integer Value #7  N

MDF_F_I8  Integer Value #8  N

MDF_F_I9  Integer Value #9  N

MDF_F_I10  Integer Value #10  N

MDF_F_INSREF1  Insref Reference #1  N

MDF_F_INSREF2  Insref Reference #2  N

MDF_F_INSREF3  Insref Reference #3  N

MDF_F_INSREF4  Insref Reference #4  N

MDF_F_INSREF5  Insref Reference #5  N

MDF_F_I5  Intege Value #5  N

MDF_F_D1  Date Value #1  N

MDF_F_D2  Date Value #2  N

MDF_F_D3  Date Value #3  N

Currently image requests for Company Information messages will be treated like stream requests. 

# Company Information History 

mref  MDF_M_CIHISTORY #34 

mclass  MDF_MC_CIHISTORY 

Tag  Name  Req'd  Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that 

an existing Company Information 

History entry with the same Insref, Type, 

Sequence and Date as this message    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

should be deleted. 

MDF_F_CITYPE  Type  Y

MDF_F_CISUBTYPE  Sub Type  N

MDF_F_SEQUENCE  Sequence  Y

MDF_F_DATE  Date  Y

MDF_F_S1  String Value #1  N

MDF_F_S2  String Value #2  N

MDF_F_S3  String Value #3  N

MDF_F_S4  String Value #4  N

MDF_F_S5  String Value #5  N

MDF_F_S6  String Value #6  N

MDF_F_S7  String Value #7  N

MDF_F_S8  String Value #8  N

MDF_F_S9  String Value #9  N

MDF_F_S10  String Value #10  N

MDF_F_S11  String Value #11  N

MDF_F_S12  String Value #12  N

MDF_F_S13  String Value #13  N

MDF_F_S14  String Value #14  N

MDF_F_S15  String Value #15  N

MDF_F_N1  Numeric Value #1  N

MDF_F_N2  Numeric Value #2  N

MDF_F_N3  Numeric Value #3  N

MDF_F_N4  Numeric Value #4  N

MDF_F_N5  Numeric Value #5  N

MDF_F_N6  Numeric Value #6  N

MDF_F_N7  Numeric Value #7  N

MDF_F_N8  Numeric Value #8  N

MDF_F_N9  Numeric Value #9  N

MDF_F_N10  Numeric Value #10  N

MDF_F_I1  Integer Value #1  N

MDF_F_I2  Integer Value #2  N

MDF_F_I3  Integer Value #3  N

MDF_F_I4  Integer Value #4  N

MDF_F_I5  Integer Value #5  N

MDF_F_I6  Integer Value #6  N

MDF_F_I7  Integer Value #7  N

MDF_F_I8  Integer Value #8  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_I9  Integer Value #9  N

MDF_F_I10  Integer Value #10  N

MDF_F_INSREF1  Insref Reference #1  N

MDF_F_INSREF2  Insref Reference #2  N

MDF_F_INSREF3  Insref Reference #3  N

MDF_F_INSREF4  Insref Reference #4  N

MDF_F_INSREF5  Insref Reference #5  N

MDF_F_I5  Intege Value #5  N

MDF_F_D1  Date Value #1  N

MDF_F_D2  Date Value #2  N

MDF_F_D3  Date Value #3  N

Currently image requests for Company Information History messages will be treated like stream requests. 

# Company Fundamentals 

mref  MDF_M_FUNDAMENTALS #25 

mclass  MDF_MC_FUNDAMENTALS 

Tag  Name  Req'd  Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that an 

existing Company Fundamentals entry with the 

same Period, Currency and Source as this 

message should be deleted. 

MDF_F_PERIOD  Period  Y Will be in 'YYYY-Qx' or 'YYYY' format 

MDF_F_SOURCE  Source  Y

MDF_F_ISSUECURRENCY  Currency  Y

MDF_F_DATE  Date  Y

MDF_F_FISCALPERIOD  Fiscal Period  N Will be in “YYYYMMDD – YYYYMMDD” 

format 

MDF_F_SALES  Total Sales  N

MDF_F_EBIT  EBIT  N

MDF_F_EBITA  EBITA  N

MDF_F_EBITDA  EBITDA  N

MDF_F_FINANCIALINCOME  Financial Income  N

MDF_F_FINANCIALCOST  Financial Cost  N

MDF_F_PRETAXPROFIT  Pre-Tax Profit  N

MDF_F_NETPROFIT  Net Profit  N

MDF_F_GROSSPROFIT  Gross Profit (Sales Profit)  N

MDF_F_EPS  Earnings Per Share  N

MDF_F_EPS_TTM  Earnings Per Share  N Trailing Twelve Months 

MDF_F_EPS_LAST  Earnings Per Share  N Annualized    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_DILUTEDEPS  Diluted Earnings Per 

Share 

N

MDF_F_NUMBEROFSHARES  Number of Shares  N

MDF_F_OPERATINGCASHFLOW  Operating Cash Flow  N

MDF_F_INTANGIBLEASSET  Intangible Asset  N

MDF_F_GOODWILL  Goodwill  N

MDF_F_FIXEDASSET  Fixed Asset  N

MDF_F_FINANCIALASSET  Financial Asset  N

MDF_F_NONCURRENTASSETS  Noncurrent Asset  N

MDF_F_INVENTORY  Inventory  N

MDF_F_OTHERCURRENTASSET  Other Current Asset  N

MDF_F_ACCOUNTSRECEIVABLE  Accounts Receivable 

(A/R) 

N

MDF_F_OTHERRECEIVABLES  Other Receivables  N

MDF_F_SHORTTERMINV  Short Term Investments  N

MDF_F_CCE  Cash and Cash 

Equivalents 

N

MDF_F_CURRENTASSETS  Current Assets  N

MDF_F_TOTALASSETS  Total Assets  N

MDF_F_SHEQUITY  Shareholders' Equity  N

MDF_F_PROVISIONS  Provisions  N

MDF_F_LTLIABILITIES  Long Term Liabilities  N

MDF_F_CURLIABILITIES  Current Liabilities  N

MDF_F_TOTSHEQLIABILITIES  Total Shareholder Equity 

Liabilities 

N

MDF_F_NIBL  Non-Interest-Bearing 

Liabilities 

N

MDF_F_TOTLIABILITIES  Total Liabilities  N

MDF_F_IBL  Interest-Bearing 

Liabilities 

N

MDF_F_CASHFLOWBWC  Free Cash Flow  N

MDF_F_CASHFLOWAWC  Operating Cash Flow after 

changes in Working 

Capital 

MDF_F_CASHFLOWIA  Cash Flow from Investing 

Activities 

MDF_F_CASHFLOWFA  Cash Flow from Financial 

Activities 

MDF_F_CASHFLOWTOTAL  Total Cash Flow  N

MDF_F_NUMEPLOYEES  Number of Employees  N

MDF_F_EQUITYRATIO  Equity Ratio  N

MDF_F_DIVIDEND  Dividend  N   

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_INTERESTINCOME  Interest Income  N

MDF_F_OTHERFINANCIALINCOME  Other Financial Income  N

MDF_F_INTERESTEXPENSE  Interest Expense  N

MDF_F_OTHERFINANCIALEXPENS 

E

Other Financial Expense  N

MDF_F_MINORITYINTEREST  Minority Interest  N From the Balance Sheet 

MDF_F_MINORITYINTERESTRES  Minority Interest  N From the Income Statement 

MDF_F_ACCOUNTSPAYABLE  Accounts Payable  N

MDF_F_INCOMEPROPMAN  Income From Property 

Management 

N

MDF_F_EVENTLINK  Event Link  N

MDF_F_EVENTLINGLANGUAGES  Event Link Languages  N Mandatory if MDF_F_EVENTLINK is present 

MDF_F_SPS_TTM  Sales Per Share  N Trailing Twelve Months 

MDF_F_SPS_LAST  Sales Per Share  N Annualized 

MDF_F_BVPS  Book Value Per Share  N

MDF_F_CFPS_TTM  Cash Flow Per Share  N Trailing Twelve Months 

MDF_F_CFPS_LAST  Cash Flow Per Share  N Annualized 

MDF_F_ROE_TTM  Return on Equity  N Trailing Twelve Months 

MDF_F_ROE_LAST  Return on Equity  N Annualized 

MDF_F_ROA_TTM  Return on Assets  N Trailing Twelve Months 

MDF_F_ROA_LAST  Return on Assets  N Annualized 

MDF_F_GM  Gross Margin  N

MDF_F_GM_TTM  Gross Margin  N Trailing Twelve Months 

MDF_F_OM  Operating Margin  N

MDF_F_OM_TTM  Operating Margin  N Trailing Twelve Months 

MDF_F_PM  Profit Margin  N

MDF_F_PM_TTM  Profit Margin  N Trailing Twelve Months 

MDF_F_DER  Debt Ratio  N

MDF_F_ND_EBITDA_TTM  Net Debt to EBITDA 

Ratio 

N Trailing Twelve Months 

MDF_F_ND_EBITDA_LAST  Net Debt to EBITDA 

Ratio 

N Annualized 

MDF_F_DPR  Dividend Payout Ratio  N

MDF_F_ROIC_TTM  Return on Invested 

Capital 

N Trailing Twelve Months 

MDF_F_ROIC_LAST  Return on Invested 

Capital 

N Annualized 

MDF_F_PEG_TTM  Price/Earnings-to-growth 

Ratio 

N Trailing Twelve Months 

MDF_F_PEG_LAST  Price/Earnings-to-growth 

Ratio 

N Annualized    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_CLOSEPRICE  Close Price  N The price used for the Per Price ratios 

MDF_F_DY  Dividend Yield  N

MDF_F_PER_TTM  P/E Ratio  N Trailing Twelve Months 

MDF_F_PER_LAST  P/E Ratio  N Annualized 

MDF_F_PSR_TTM  P/S Ratio  N Trailing Twelve Months 

MDF_F_PSR_LAST  P/S Ratio  N Annualized 

MDF_F_PBR  P/B  N

MDF_F_PCF_TTM  P/CF Ratio  N Trailing Twelve Months 

MDF_F_PCF_LAST  P/CF Ratio  N Annualized 

Currently image requests for Company Fundamentals messages will be treated like stream requests. 

# Company Estimates 

mref  MDF_M_ESTIMATES #28 

mclass  MDF_MC_ESTIMATES 

Tag  Name  Req'd  Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that 

an existing Company Estimates entry 

with the same Source, Period, Field 

Name, Field Aspect, Field Type and 

Currency as this message should be 

deleted. 

MDF_F_PERIOD  Period  Y Will be in 'YYYY', 'YYYY-Qx', 'YYYY-

Hx', 'YYYY-MM' or 'YYYY-9M' format 

MDF_F_FIELDNAME  Field Name  Y

MDF_F_FIELDASPECT  Field Aspect  Y

MDF_F_FIELDTYPE  Field Type  Y

MDF_F_FIELDUNIT  Field Unit  N

MDF_F_AVERAGE  Average Value  N

MDF_F_MIN  Min Value  N The smallest individual value 

MDF_F_MAX  Max Value  N The largest individual value 

MDF_F_COUNT  Number of Values  N The number of individual values 

MDF_F_ISSUECURRENCY  Currency  Y

MDF_F_SOURCE  Source  Y

MDF_F_DATE  Date of Entry  N

MDF_F_TIME  Time of Entry  N

Currently image requests for Company Estimates messages will be treated like stream requests. 

# Company Estimates History 

mref  MDF_M_ESTIMATESHISTORY #29    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

mclass  MDF_MC_ESTIMATESHISTORY 

Tag  Name  Req'd  Comments 

MDF_F_DELETERECORD  Delete Record  N The presence of this field indicates that 

an existing Company Estimates History 

entry with the same Date, Source, Period, 

Field Name, Field Aspect, Field Type and 

Currency as this message should be 

deleted. 

MDF_F_PERIOD  Period  Y Will be in 'YYYY', 'YYYY-Qx', 'YYYY-

Hx', 'YYYY-MM' or 'YYYY-9M' format 

MDF_F_FIELDNAME  Field Name  Y

MDF_F_FIELDASPECT  Field Aspect  Y

MDF_F_FIELDTYPE  Field Type  Y

MDF_F_FIELDUNIT  Field Unit  N

MDF_F_AVERAGE  Average Value  N

MDF_F_MIN  Min Value  N The smallest individual value 

MDF_F_MAX  Max Value  N The largest individual value 

MDF_F_COUNT  Number of Values  N The number of individual values 

MDF_F_ISSUECURRENCY  Currency  Y

MDF_F_SOURCE  Source  Y

MDF_F_DATE  Date of Entry  Y

MDF_F_TIME  Time of Entry  N

Currently image requests for Company Estimates History messages will be treated like stream requests. 

# Key Ratios 

mref  MDF_M_KEYRATIOS #27 

mclass  MDF_MC_KEYRATIOS 

Tag  Name  Req'd  Comments 

MDF_F_DPS  Dividend Per Share. Divide by 

LastPrice and muliply by 100 to 

get the Dividend Yield. 

N From last Annual Report 

MDF_F_EPS  Earnings Per Share. Divide 

LastPrice by value to get P/E. 

N From last Annual Report 

MDF_F_EPS_TTM  Earnings Per Share. Divide 

LastPrice by value to get P/E. 

N Trailing Twelve Months 

MDF_F_EPS_LAST  Earnings Per Share. Divide 

LastPrice by value to get P/E. 

N Annualized from last Interim 

Report 

MDF_F_SPS  Sales Per Share. Divide 

LastPrice by value to get P/S. 

N From last Annual Report 

MDF_F_SPS_TTM  Sales Per Share. Divide 

LastPrice by value to get P/S. 

N Trailing Twelve Months 

MDF_F_SPS_LAST  Sales Per Share. Divide  N Annualized from last Interim    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

LastPrice by value to get P/S.  Report 

MDF_F_BVPS  Book Value of equity Per Share. 

Divide LastPrice by value to 

get P/B. 

N From last Annual Report 

MDF_F_BVPS_LAST  Book Value of equity Per Share. 

Divide LastPrice by value to 

get P/B. 

N Annualized from last Interim 

Report 

MDF_F_CFPS  Cash Flow Per Share. Divide 

LastPrice by value to get P/CF. 

N From last Annual Report 

MDF_F_CFPS_TTM  Cash Flow Per Share. Divide 

LastPrice by value to get P/CF. 

N Trailing Twelve Months 

MDF_F_CFPS_LAST  Cash Flow Per Share. Divide 

LastPrice by value to get P/CF. 

N Annualized from last Interim 

Report 

MDF_F_ROE  Return on Equity  N From last Annual Report 

MDF_F_ROE_TTM  Return on Equity  N Trailing Twelve Months 

MDF_F_ROE_LAST  Return on Equity  N Annualized from last Interim 

Report 

MDF_F_ROA  Return on Assets  N From last Annual Report 

MDF_F_ROA_TTM  Return on Assets  N Trailing Twelve Months 

MDF_F_ROA_LAST  Return on Assets  N Annualized from last Interim 

Report 

MDF_F_GM  Gross Margin  N From last Annual Report 

MDF_F_GM_TTM  Gross Margin  N Trailing Twelve Months 

MDF_F_GM_LAST  Gross Margin  N Annualized from last Interim 

Report 

MDF_F_OM  Operating Margin  N From last Annual Report 

MDF_F_OM_TTM  Operating Margin  N Trailing Twelve Months 

MDF_F_OM_LAST  Operating Margin  N Annualized from last Interim 

Report 

MDF_F_PM  Profit Margin  N From last Annual Report 

MDF_F_PM_TTM  Profit Margin  N Trailing Twelve Months 

MDF_F_PM_LAST  Profit Margin  N Annualized from last Interim 

Report 

MDF_F_DER  Debt Ratio  N From last Annual Report 

MDF_F_DER_LAST  Debt Ratio  N Annualized from last Interim 

Report 

MDF_F_ND_EBITDA  Net Debt to EBITDA Ratio  N From last Annual Report 

MDF_F_ND_EBITDA_TTM  Net Debt to EBITDA Ratio  N Trailing Twelve Months 

MDF_F_ND_EBITDA_LAST  Net Debt to EBITDA Ratio  N Annualized from last Interim 

Report 

MDF_F_DPR  Dividend Payout Ratio  N From last Annual Report 

MDF_F_ROIC  Return on Invested Capital  N From last Annual Report 

MDF_F_ROIC_TTM  Return on Invested Capital  N Trailing Twelve Months    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_ROIC_LAST  Return on Invested Capital  N Annualized from last Interim 

Report 

MDF_F_PEG  Divide LastPrice by value to 

get PEG. 

N From last Annual Report 

MDF_F_PEG_TTM  Divide LastPrice by value to 

get PEG. 

N Trailing Twelve Months 

MDF_F_PEG_LAST  Divide LastPrice by value to 

get PEG. 

N Annualized from last Interim 

Report 

MDF_F_MCAP  Market Cap  N

MDF_F_SMA20  SMA-20  N

MDF_F_SMA50  SMA-50  N

MDF_F_SMA200  SMA-200  N

MDF_F_RSI14  RSI-14  N

MDF_F_MACD  MACD  N

MDF_F_DATE  Date  N

MDF_F_TIME  Time  N

The Time and Date fields are sent on all image replies and on stream replies if the key ratios are for another time/date 

than now (I.e if the client is subscribing to delayed data) 

# Greeks 

mref  MDF_M_GREEKS #42 

mclass  MDF_MC_GREEKS 

Tag  Name  Req'd  Comments 

MDF_F_IV  Implied Volatility on Mid  N

MDF_F_IVBID  Implied Volatility on Bid  N

MDF_F_IVASK  Implied Volatility on Ask  N

MDF_F_DELTA  Delta  N

MDF_F_GAMMA  Gamma  N

MDF_F_RHO  Rho  N

MDF_F_THETA  Theta  N

MDF_F_VEGA  Vega  N

The Time and Date fields are sent on all image replies and on stream replies if the greeks are for another time/date than 

now (I.e if the client is subscribing to delayed data)    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Changelog 

2025-07-04  Added MDF_F_PRIMARYSHARE to MDF_M_BASICDATA. 

2025-05-08  Removed MDF_F_SOURCE from MDF_M_PRICEHISTORY. 

Removed MDF_F_SOURCE from MDF_M_CORPORATEACTION. 

2025-05-05  Added MDF_F_DER, MDF_F_DER_LAST, MDF_F_ND_EBITD, MDF_F_ND_EBITDA_TTM, 

MDF_F_ND_EBITDA_LAST, MDF_F_DPR, MDF_F_ROIC, MDF_F_ROICE_TTM, 

MDF_F_ROIC_LAST, MDF_F_PEG, MDF_F_PEG_TTM and MDF_F_PEG_LAST to 

MDF_M_KEYRATIOS. 

Added MDF_F_DY, MDF_F_PER_TTM, MDF_F_PER_LAST, MDF_F_PSR_TTM, 

MDF_F_PSR_LAST, MDF_F_PBR, MDF_F_PCF_TTM, MDF_F_PCF_LAST, MDF_F_EPS_TTM, 

MDF_F_EPS_LAST, MDF_F_SPS_TTM, MDF_F_SPS_LAST, MDF_F_BVPS, 

MDF_F_CFPS_TTM, MDF_F_CFPS_LAST, MDF_F_ROE_TTM, MDF_F_ROE_LAST, 

MDF_F_ROA_TTM, MDF_F_ROA_LAST, MDF_F_GM_TTM, MDF_F_GM, MDF_F_OM_TTM, 

MDF_F_OM, MDF_F_PM, MDF_F_PM_TTM, MDF_F_DER, MDF_F_ND_EBITDA_TTM, 

MDF_F_ND_EBITDA_LAST, MDF_F_DPR, MDF_F_ROIC_TTM, MDF_F_ROIC_LAST, 

MDF_F_PEG_TTM, MDF_F_PEG_LAST, MDF_F_CLOSEPRICE to MDF_M_FUNDAMENTALS. 

2024-05-19  Extended MDF_F_REQUESTSTATUS. 

2024-02-07  Added MDF_F_SHARECLASS to MDF_M_BASICDATA and MDF_M_CORPORATEACTIONS. 

2023-07-21  Added MDF_F_MCAP, MDF_F_SMA20, MDF_F_SMA50, MDF_F_SMA200, MDF_F_RSI14 and 

MDF_F_MACD to MDF_M_KEYRATIOS. 

2022-11-17  Added MDF_F_CLEARING to MDF_M_BASICDATA. Added MDF_F_CLOSEPRICE4Y, 

MDF_F_CLOSEPRICE6Y, MDF_F_CLOSEPRICE7Y, MDF_F_CLOSEPRICE8Y, 

MDF_F_CLOSEPRICE9Y, MDF_F_CLOSEYIELD4Y, MDF_F_CLOSEYIELD6Y, 

MDF_F_CLOSEYIELD7Y, MDF_F_CLOSEYIELD8Y and MDF_F_CLOSEYIELD9Y to 

MDF_M_PERFORMANCE. 

2022-09-13  Added MDF_F_SWINGFACTORSUB to MDF_M_BASICDATA. 

2022-06-21  Added the localized EPTv2 fields to MDF_M_L10N. 

2022-06-10  Added EPTv2 fields to MDF_M_PRIIP. 

2022-04-29  Added MDF_F_CLOSEPRICEDATE and MDF_F_CLOSEPRICE1DDATE to 

MDF_M_PERFORMANCE. 

2022-01-26  Added MDF_M_QUOTEEX, added MDF_F_CLOSEPRICE to MDF_M_PERFORMANCE, added 

MDF_F_INCOMEPROPMAN to MDF_M_FUNDAMENTALS. 

2021-11-22  Added MDF_F_SWINGFACTOR and MDF_F_SWINGMETHOD to 

MDF_M_BASICDATA. 

2021-11-01  Added MDF_F_SETTLEMENTPRICE to MDF_M_QUOTE. 

Added MDF_F_COMBOLEGS to MDF_M_BASICDATA. 

2021-07-21  Added lots of new fields to MDF_M_CI and MDF_M_CIHISTORY. 

2021-04-23  Altered the values for the MDF_F_I1 in MDF_M_ORDERBOOKFLUSH.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2020-11-29  Added MDF_F_I1 to MDF_M_ORDERBOOKFLUSH. 

2020-11-24  Added MDF_M_QUOTEBBO. 

2020-11-23  Added MDF_F_EXPIRATIONTYPE to MDF_M_BASICDATA. 

2020-11-19  Added MDF_F_DAYCOUNTCONVENTION to MDF_M_BASICDATA. 

2020-11-13  Added MDF_F_IVBID and MDF_F_IVASK to MDF_M_GREEKS. 

2020-10-16  Altered the Market By Order messages. 

2020-10-09  Added MDF_M_GREEKS. 

2020-08-11  Added the Market By Order messages. 

2020-05-29  Added MDF_F_MARKETPLACE to MDF_M_INSTRUMENTDELETE. 

2020-03-03  Added MDF_F_COUPONFREQUENCY to MDF_M_BASICDATA. 

2020-01-16  Added MDF_F_FIGISECURITYTYPE to MDF_M_BASICDATA. 

2019-12-16  The MIFID07090 field changed name in EMTv3 Endorsed (2019-12-10) 

2019-12-04  Changed the name of some new fields in MDF_M_MIFID and MDF_M_MIFIDHISTORY to match 

the latest EMTv3 template (2019-09-20). 

2019-11-15  Added FIGI fields to MDF_M_BASICDATA and MDF_M_CORPORATEACTION. Added the 

MDF_F_MMO field to the Orderbook messages. 

2019-09-23  Added EMTv3 fields to MDF_M_MIFID and MDF_M_MIFIDHISTORY. 

2019-06-20  Clarified some fields for MDF_M_REQUEST. 

2019-06-17  Corrected the new fields to MDF_M_KEYRATIOS. 

2019-06-12  Added lots of new fields to MDF_M_KEYRATIOS while deprecating some. 

2019-05-23  Added MDF_F_SUBMARKET to MDF_M_BASICDATA. 

2019-03-20  Added MDF_M_MAPPINGS. 

2019-01-07  Added MDF_F_HIGHPRICE3Y, MDF_F_HIGHPRICE5Y, MDF_F_HIGHPRICE10Y, 

MDF_F_LOWPRICE3Y, MDF_F_LOWPRICE5Y and MDF_F_LOWPRICE10Y to 

MDF_M_PERFORMANCE. 

2018-12-18  Added MDF_F_ACTIVESHARE and MDF_F_TRACKINGERROR to 

MDF_M_BASICDATA. 

2018-11-22  Added MDF_F_NEWSIDREPLACE to MDF_M_NEWSHEADLINE. 

2018-11-20  Added MDF_M_MIFIDHISTORY. 

2018-10-23  Added MDF_F_NEWSCODINGTAGS and MDF_F_NEWSCODINGIMPACT to 

MDF_F_NEWSHEADLINE. 

2018-07-17  Added MDF_F_CVR, MDF_F_KENNITALA, MDF_F_YTUNNUS and    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_ORGNUMNO to MDF_M_BASICDATA. 

2018-02-23  Added MDF_F_OPERATINGMIC to MDF_M_BASICDATA. 

2017-11-07  Added MDF_M_PRIIP and MDF_M_MIFID. Added some MDF_M_PRIIP fields to 

MDF_M_L10N 

2017-11-03  Added MDF_F_MMT to MDF_M_TRADE. 

2017-02-20  Added MDF_F_CIK to MDF_M_BASICDATA. 

2016-11-18  Added MDF_F_CSR to MDF_M_BASICDATA. 

Added MDF_NORMANAMOUNT to MDF_M_PERFORMANCE. 

Added MDF_S11 to MDF_M_CI and MDF_M_CIHISTORY. 

2016-11-10  Extended the document with the actual MREF values. 

2016-10-06  Added MDF_F_NEWSCODINGREGULATORY to MDF_M_NEWSHEADLINE.. 

2016-06-08  Added MDF_F_VOLUMEDIMENSION to MDF_M_BASICDATA. 

2016-04-20  Added MDF_F_TRADEAGREEMENTTIME, MDF_F_TRADEAGREEMENTDATE, 

MDF_F_MIC and MDF_F_TRADECURRENCY to MDF_M_TRADE. 

2016-02-03  Added MDF_F_PRODUCTCODE and MDF_F_QUOTINGTYPE to 

MDF_M_BASICDATA. 

2015-12-08  Added MDF_F_CLOSEPRICETYPE and MDF_F_CLOSETRADEPRICE to 

MDF_M_PRICEHISTORY. 

2015-11-12  Added MDF_F_MARKETOPENDAYS to MDF_M_BASICDATA. 

2015-11-12  Added MDF_F_LEGALSTRUCTURE, MDF_F_ONGOINGCHARGE and 

MDF_F_PRICINGFREQUENCY to MDF_M_BASICDATA. 

2015-09-21  Added MDF_F_SPECIALCONDITION to MDF_M_BASICDATA. 

2015-09-07  Added MDF_F_MARKETOPEN, MDF_F_MARKETCLOSE and 

MDF_F_MARKETEARLYCLOSE to MDF_M_BASICDATA. 

2014-12-05  Added MDF_F_OUTSTANDINGAMOUNT, MDF_F_INTERESTRATE and 

MDF_F_MARKETMAKER to MDF_M_BASICDATA. 

2014-09-23  Added MDF_M_CI and MDF_M_CIHISTORY. Renamed the 

MDF_F_FREETEXTCOMMENTx tags as MDF_F_Sx. 

2014-08-28  Added MDF_F_ANNUALIZEDRETURN1Y, MDF_F_ANNUALIZEDRETURN2Y and 

MDF_F_ANNUALIZEDRETURN4Y to MDF_M_PERFORMANCE. 

2014-08-06  Added info on how entries for the MDF_M_PRICEHISTORY, 

MDF_M_CORPORATEACTIONS, MDF_M_FUNDAMENTALS, MDF_M_ESTIMATES and 

MDF_M_ESTIMATESHISTORY will be notified for deletion. 

Added the MDF_M_L10N message. 

2014-02-28  Removed MDF_F_DIVIDENDORIGINAL from MDF_M_CORPORATEACTIONS. 

2014-01-24  Added MDF_F_MAXLEVEL to MDF_M_BASICDATA.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2014-01-21  Removed MDF_F_ORDERINTAKE, MDF_F_ORDERBACKLOG, 

MDF_F_NETINTERESTINCOME, MDF_F_NETFEEANDCOMINCOME, 

MDF_F_TOPERATINGEXPENSES, MDF_F_TOPERATINGINCOME, 

MDF_F_PROFITBEFOREWACL, MDF_F_CREDITLOSS, MDF_F_RENTALINCOME, 

MDF_F_PROPERTYMGMTRESULT, MDF_F_REALIZEDCHGPROP, 

MDF_F_UNREALIZEDCHGPROP, MDF_F_RETURNONEQUITY, 

MDF_F_ADJUSTEDEQUITY and MDF_F_TOTLIABILITIES from 

MDF_M_FUNDAMENTALS. 

Added MDF_F_INTERESTINCOME, MDF_F_OTHERFINANCIALINCOME, 

MDF_F_INTERESTEXPENSE, MDF_F_OTHERFINANCIALEXPENSE, 

MDF_F_MINORITYINTERESTRES, MDF_F_ACCOUNTSPAYABLE, 

MDF_F_EVENTLINK and MDF_F_EVENTLINKLANGUAGES to 

MDF_M_FUNDAMENTALS. 

2013-09-11  Added MDF_F_BROKERS to MDF_M_BASICDATA. 

2013-05-10  Added MDF_F_OFFBOOKQUANTITY, MDF_F_DARKQUANTITY, 

MDF_F_OFFBOOKTURNOVER and MDF_F_DARKTURNOVER to MDF_M_QUOTE. 

Added MDF_F_CLOSEOFFBOOKQUANTITY, MDF_F_CLOSEDARKQUANTITY, 

MDF_F_CLOSEOFFBOOKTURNOVER and MDF_F_CLOSEDARKTURNOVER to 

MDF_M_PRICEHISTORY. 

2013-04-12  Added MDF_F_CFI to MDF_M_BASICDATA. 

2013-03-27  Added MDF_F_KIID to MDF_M_BASICDATA. 

2013-01-17  Added MDF_F_FREETEXTCOMMENT1 to MDF_M_LOGON. 

2012-10-08  Added MDF_F_PARTICIPATIONRATE and MDF_F_ISSUEPRICE to 

MDF_M_BASICDATA. 

2012-08-07  Added MDF_F_FINANCINGLEVEL to MDF_M_BASICDATA. 

2012-05-20  Added MDF_F_CLOSEBIDPRICE1D, MDF_F_CLOSEBIDPRICE1W, 

MDF_F_CLOSEBIDYIELD1D and MDF_F_CLOSEBIDYIELD1W to 

MDF_M_PERFORMANCE. 

Added MDF_F_FINANCIALINCOME and MDF_F_FINANCIALCOST to 

MDF_M_FUNDAMENTALS. 

2012-05-03  Added MDF_F_CONTRACTVALUE to MDF_M_BASICDATA. 

2012-02-17  Added MDF_F_LOGOTYPE and MDF_F_ISSUERNAME to MDF_M_BASICDATA. 

2012-01-31  Added MDF_F_ASIANTAILSTART and MDF_F_ASIANTAILEND to MDF_M_BASICDATA. 

2011-12-14  Added MDF_F_PRICETYPE to MDF_M_BASICDATA. 

2011-12-12  Added MDF_M_UNSUBSCRIBE. 

Added MDF_F_TICKTABLE and MDF_F_TICKSIZES to MDF_M_BASICDATA. 

2011-11-18  Added MDF_M_NETORDERIMBALANCE 

2011-11-10  Added MDF_F_CAP to MDF_M_BASICDATA 

2011-09-27  Added MDF_F_SETTLEMENTTYPE to MDF_M_BASICDATA    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2011-06-28  Added MDF_F_CLOSEPRICE2W and MDF_F_CLOSEYIELD2W to 

MDF_M_PERFORMANCE. 

Added MDF_F_CONVERTFROMDATE, MDF_F_CONVERTTODATE and 

MDF_F_CONVERSIONPRICE to MDF_M_BASICDATA. 

Added MDF_F_DURATION to MDF_M_QUOTE. 

2011-04-20  Added MDF_F_FIELDUNIT to MDF_M_ESTIMATES. Added the 

MDF_M_ESTIMATESHISTORY message. 

2011-03-08  Reworked MDF_M_ESTIMATES 

2011-02-18  Added MDF_F_ISSUECURRENCY to MDF_M_FUNDAMENTALS 

2011-02-17  Added MDF_F_SHORTDESCRIPTION, MDF_F_FUNDRISK and MDF_F_EUSIPA to 

MDF_M_BASICDATA. 

Added MDF_F_NEWSRANK to MDF_M_NEWSHEADLINE. 

2010-11-10  Added MDF_F_PRIMARYMARKETPLACE to MDF_M_BASICDATA. 

Added MDF_F_FISCALPERIOD to MDF_M_CORPORATEACTIONS. 

Added MDF_F_PERIOD and MDF_F_FISCALPERIOD to MDF_M_FUNDAMENTALS. 

2010-10-26  Added MDF_F_INSTRUMENTSUBSUBCLASS to MDF_M_BASICDATA 

2010-10-14  Added MDF_F_TRADEDTHROUGHDATE, MDF_F_TOTALFEE, 

MDF_F_DIVIDENDTYPE and MDF_F_DIVIDENDFREQUENCY to 

MDF_M_BASICDATA 

2010-08-10  Added MDF_F_COUPONRATE, MDF_F_COUPONDATE, MDF_F_BARRIERPRICE, 

MDF_F_MORNINGSTARRATING, MDF_F_SALESFEE, MDF_F_PURCHASEFEE, 

MDF_F_MINSTARTAMOUNT, MDF_F_MINSUBSCRIPTIONAMOUNT, 

MDF_F_PERFORMANCEFEE, MDF_F_MINADDITIONALAMOUNT, 

MDF_F_CEOADMISSIONDATE and MDF_F_CHAIRMANADMISSIONDATE to 

MDF_M_BASICDATA. 

Added MDF_F_ANNUALIZEDRETURN3Y, MDF_F_ANNUALIZEDRETURN5Y, 

MDF_F_ANNUALIZEDRETURN10Y, MDF_F_STANDARDDEVIATION3Y and 

MDF_F_SHARPERATIO3Y to MDF_M_PERFORMANCE. 

2010-06-17  Added MDF_F_INSTRUMENTCLASS, MDF_F_INSTRUMENTSUBCLASS and 

MDF_F_CONSTITUENTS to MDF_M_BASICDATA 

2010-06-15  Added MDF_F_FUNDBENCHMARKINSREF to MDF_M_BASICDATA 

2010-06-11  Added MDF_F_CUSIP, MDF_F_WKN, MDF_F_UCITS and MDF_F_INCEPTIONDATE to 

MDF_M_BASICDATA 

2010-06-07  Added MDF_F_ATHYIELD, MDF_F_ATLYIELD, MDF_F_ATHYIELDDATE, 

MDF_F_ATLYIELDDATE, MDF_F_HIGHYIELD1Y, MDF_F_LOWYIELD1Y, 

MDF_F_HIGHYIELDYTD, MDF_F_LOWYIELDYTD, MDF_F_HIGHYIELDYTDDATE, 

MDF_F_LOWYIELDYTDDATE, MDF_F_HIGHYIELD1YDATE, 

MDF_F_LOWYIELD1YDATE 

2010-06-02  Added MDF_F_CLOSEYIELD1D, MDF_F_CLOSEYIELD1W, MDF_F_CLOSEYIELD1M, 

MDF_F_CLOSEYIELD3M, MDF_F_CLOSEYIELD6M, MDF_F_CLOSEYIELD9M, 

MDF_F_CLOSEYIELD1Y, MDF_F_CLOSEYIELD2Y, MDF_F_CLOSEYIELD3Y, 

MDF_F_CLOSEYIELD5Y, MDF_F_CLOSEYIELD10Y, MDF_F_CLOSEYIELDWTD, 

MDF_F_CLOSEYIELDMTD, MDF_F_CLOSEYIELDQTD, MDF_F_CLOSEYIELDYTD, 

MDF_F_CLOSEYIELDPYTD and MDF_F_CLOSEYIELDLD to MDF_M_PERFORMANCE 

2010-05-11  Added MDF_F_FUNDYEARLYMGMTFEE, MDF_F_FUNDPPMFEE, 

MDF_F_FUNDPPMTYPE, MDF_F_FUNDBENCHMARK, MDF_F_FUNDLEVERAGE, 

MDF_F_FUNDDIRECTION, MDF_F_PROSPECTUS, MDF_F_GEOFOCUSREGION,    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_GEOFOCUSCOUNTRY and MDF_F_OPENINTEREST to MDF_M_BASICDATA. 

Added MDF_F_CLOSEPRICE3Y and MDF_F_CLOSEPRICELD to 

MDF_M_PERFORMANCE. 

2010-02-08  Added MDF_F_SOURCEID and MDF_F_ISSUER to MDF_M_BASICDATA 

2010-01-12  Added MDF_F_CONTRACTSIZE and MDF_F_BASERATIO to MDF_M_BASICDATA 

2009-10-30  Added MDF_F_GROSSPROFIT, MDF_F_INTANGIBLEASSET, MDF_F_GOODWILL, 

MDF_F_FIXEDASSET, MDF_F_FINANCIALASSET, MDF_F_NONCURRENTASSET, 

MDF_F_INVENTORY, MDF_F_OTHERCURRENTASSET, 

MDF_F_ACCOUNTSRECEIVABLE, MDF_F_OTHERRECEIVABLES, 

MDF_F_SHORTTERMINV, MDF_F_CCE, MDF_F_CURRENTASSETS, 

MDF_F_TOTALASSETS, MDF_F_SHEQUITY, MDF_F_MINORITYINTEREST, 

MDF_F_PROVISIONS, MDF_F_LTLIABILITIES, MDF_F_CURLIABILITIES, 

MDF_F_TOTSHEQLIABILITIES, MDF_F_NIBL, MDF_F_TOTLIABILITIES, MDF_F_IBL, 

MDF_F_CASHFLOWBWC, MDF_F_CASHFLOWAWC, MDF_F_CASHFLOWIA, 

MDF_F_CASHFLOWFA, MDF_F_CASHFLOWTOTAL, MDF_F_NUMEMPLOYEES and 

MDF_F_DIVIDEND to MDF_M_FUNDAMENTALS. 

2009-10-29  Added MDF_F_VOTINGPOWERPRC and MDF_CAPITALPRC to 

MDF_M_CORPORATEACTION. 

Added MDF_F_GENDERCEO, MDF_F_BIRTHYEARCEO, 

MDF_F_GENDERCHAIRMAN, MDF_F_BIRTHYEARCHAIRMAN, MDF_F_ADDRESS, 

MDF_F_POSTALCODE, MDF_F_CITY, MDF_F_TELEPHONE, MDF_F_FAX, 

MDF_F_EMAIL and MDF_F_IMPORTANTEVENTS to MDF_M_BASICDATA. 

2009-10-15  Added MDF_F_TRADEYIELD to MDF_M_TRADE 

2009-10-12  Added MDF_M_ESTIMATES 

2009-09-02  Added MDF_F_HIGHPRICEYTD, MDF_F_LOWPRICEYTD, 

MDF_F_HIGHPRICEYTDDATE and MDF_F_LOWPRICEYTDDATE to 

MDF_M_PERFORMANCE. 

2009-08-07  Added MDF_F_PRICETOCASHFLOW and MDF_F_PRICETOADJUSTEDEQUITY to 

MDF_M_KEYRATIOS. 

Added MDF_F_OPERATINGCASHFLOW, MDF_F_ADJUSTEDEQUITY and 

MDF_F_NUMBEROFSHARES to MDF_M_FUNDAMENTALS. 

2009-06-11  Added MDF_F_SOURCE to MDF_M_FUNDAMENTALS. 

Changed MDF_F_SOURCE to mandatory for MDF_M_PRICEHISTORY and 

MDF_M_CORPORATEACTION. 

2009-06-01  Added MDF_F_SECTOR to MDF_F_BASICDATA. 

Added MDF_F_REDEMPTIONPRICE, MDF_F_FREETEXTCOMMENT2, 

MDF_F_FREETEXTCOMMENT3, MDF_F_FREETEXTCOMMENT4, 

MDF_F_FREETEXTCOMMENT5 to MDF_M_CORPORATEACTION. 

Added MDF_F_ATHDATE, MDF_F_ATLDATE, MDF_F_HIGHPRICE1YDATE and 

MDF_F_LOWPRICE1YDATE to MDF_M_PERFORMANCE. 

2009-05-13  Moved MDF_F_RETURNONEQUITY to MDF_M_FUNDAMENTALS. Removed 

MDF_F_TOTALNUMBEROFSHARES (MDF_F_NUMBEROFSHARES on a company 

instrument contains the total number of shares so this field was unnecessary). 

2009-04-29  Added MDF_M_KEYRATIOS, MDF_F_CHAIRMAN, MDF_F_CEO, MDF_F_WEBSITE, 

MDF_F_ORGNUM and MDF_F_DESCRIPTION. 

2009-04-27  Added MDF_F_NEWSCODINGISIN 

2009-04-16  Added MDF_M_PERFORMANCE 

2009-04-15  Added MDF_M_FUNDAMENTALS    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2009-04-13  Described when MDF_F_TIME and MDF_F_DATE are sent on MDF_M_QUOTE, also 

added them to MDF_M_TRDAESTATE. 

2009-04-02  Added MDF_M_TRADESTATE 

2009-03-30  Added MDF_F_VWAP and MDF_F_CLOSEVWAP 

2009-03-27  Added MDF_F_UNCHANGEDPAID, MDF_F_MINUSPAID, MDF_F_PLUSPAID to 

MDF_M_QUOTE 

2009-03-23  Initial version