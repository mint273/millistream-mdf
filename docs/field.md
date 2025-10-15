Title: MDF Fields Reference

URL Source: https://packages.millistream.com/documents/MDF%20Fields%20Reference.pdf

Published Time: Fri, 04 Jul 2025 21:16:59 GMT

Markdown Content:
MDF Fields Reference 

# Reference Guide 

# 4 July 2025 

Millistream Market Data AB www.millistream.com 

Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117 Regarding Limits 

Defining sizes and limits on fields is a complicated task. From some data sources we get the limits, on other one only 

get to see a maximum message length and on yet some there is no limits stated at all. Also the Millistream Data Feed 

contain a number of calculated fields and determining the limits on these fields is hard guesses at best. 

So if the limit/size numbers might look strange (or very large to be specific), it is because they reflect the largest 

possible size that we currently support for the field in question and has nothing to do with the sizes of the values 

currently being sent in the system. For example some exchanges have sizes on numbers with 20 digits of which 7 can be 

decimals while still only using a maximum of 2 decimals in reality. 

# Data Types 

Type  Description 

string  Free format string in UTF-8 encoding. The size field represents the maximum number of characters and not 

the number of bytes (a UTF-8 character can be encoded with up to four bytes). 

time  Time represented in Universal Time Coordinated (UTC) as HH:MM:SS, HH:MM:SS.mmm or 

HH:MM:SS.nnnnnnnnn. 

date  Date represented in Universal Time Coordinated (UTC) in one of the following formats: 

YYYY-MM-DD 

YYYY-MM 

YYYY 

YYYY-Qx (x is the quarter; 1-4) 

YYYY-Tx (x is the tertiary: 1-3) 

YYYY-Hx (x is the semi-annual; 1-2) 

YYYY-Wxx (x is the ISO-8601 week number; 1-53) 

insref  Unsigned 64-bit integer. Used to uniquely identify a instrument in the Millistream universe. 

list  A space separated list of instrument references (type: insref). The list can be prefixed with the following 

characters: 

• '+' - The supplied list of insrefs should be concatenated to the current value 

• '-' - The supplied list of insrefs should be removed from the current value 

• '=' - The supplied list is the current value, that is it should replace the current value. 

If the list lacks a prefix, it should be treated like it was prefixed with a '=' character. 

tabular  A string of pipe (|) separated rows of space separated columns. I.e: “1 2 3|4 5 6” defines a set of two rows 

with three columns each. If a column contains a space, back-slash or pipe character then it's escaped with a 

back-slash (\). Absent columns are to be decoded as NULL values, I.e here column 2 from the previous 

example is NULL in the first row: “1 3|4 5 6”. 

number  Sequence of digits with optional decimal point and sign character. (ASCII characters '-', '0' – '9' and '.'). 

Trailing zeros after the decimal point are omitted. The size field is 'M,D' where 'M' is the total number of 

digits, of which 'D' digits may be after the decimal point. 

bool  One character containing one of two values: 

• '1' - True/Yes 

• '0' – False/No 

Also if the field is not present in a message, it is to be treated as False/No. 

uint  Unsigned integer. Used to create enumerations lists. 

bitfield  Unsigned integer which forms a binary bit field. For example the value 3 indicates that the flags #1 and #2 

is set while the value 4 indicates that only flag #3 is set. To make it easier we always specify the flag value 

(I.e “4” instead of “flag #3”) in the description.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Message References 

MREF  Define  Description 

0 MDF_M_MESSAGESREFERENCE  Sent by the server on first connection of client or when the message 

templates have been changed. 

1 MDF_M_LOGON  Sent by the client to the server to login to the system 

2 MDF_M_LOGOFF  Sent by the client in order to log off from the system. Also sent by the 

server if the client is kicked out for some reason. 

3 MDF_M_LOGONGREETING  Sent by the server to indicate a successful login by the client 

4 MDF_M_NEWSHEADLINE 

5 MDF_M_QUOTE  Quote Last Sales 

6 MDF_M_TRADE 

7 MDF_M_BIDLEVELINSERT  Order MBL 

8 MDF_M_ASKLEVELINSERT  Order MBL 

9 MDF_M_BIDLEVELDELETE  Order MBL 

10  MDF_M_ASKLEVELDELETE  Order MBL 

11  MDF_M_BIDLEVELUPDATE  Order MBL 

12  MDF_M_ASKLEVELUPDATE  Order MBL 

13  MDF_M_INSTRUMENTRESET 

14  MDF_M_ORDERBOOKFLUSH  Order MBL, Order MBO and QuoteBBO 

15  MDF_M_BASICDATA 

16  MDF_M_PRICEHISTORY 

17  MDF_M_INSTRUMENTDELETE 

18  MDF_M_FIELDSREFERENCE  Currently not used 

19  MDF_M_REQUEST  Sent by the client in order to subscribe to specific messages or insrefs. 

20  MDF_M_REQUESTFINISHED  Sent by the server when a request have been processed in full or there was 

an error with the request. 

21  MDF_M_INSREF  Sent by the client in order to request new insrefs and sent by the server as 

a reply to such a request with the newly created insrefs. 

22  MDF_M_NEWSCONTENT 

23  MDF_M_CORPORATEACTION 

24  MDF_M_TRADESTATE 

25  MDF_M_FUNDAMENTALS 

26  MDF_M_PERFORMANCE 

27  MDF_M_KEYRATIOS 

28  MDF_M_ESTIMATES 

29  MDF_M_ESTIMATESHISTORY 

30  MDF_M_NETORDERIMBALANCE 

31  MDF_M_UNSUBSCRIBE  Sent by the client in order to unsubscribe to a specific message or 

insref(s)    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

32  MDF_M_L10N 

33  MDF_M_CI 

34  MDF_M_CIHISTORY 

35  MDF_M_PRIIP  PRIIP EPT 

36  MDF_M_MIFID  MiFID EMT 

37  MDF_M_MIFIDHISTORY  MiFID EMT History 

38  MDF_M_MAPPINGS  Various Mappings 

39  MDF_M_MBOADD  Order MBO 

40  MDF_M_MBOUPDATE  Order MBO 

41  MDF_M_MBODELETE  Order MBO 

42  MDF_M_GREEKS  Greeks 

43  MDF_M_QUOTEBBO  Quote Best Bid and Offer 

44  MDF_M_QUOTEEX  Quote Extra Session    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

# Field Definitions 

Tag  Define  Type  Size  Description 

381  MDF_F_ACCOUNTSPAYABLE  number  19,7  A balance sheet item: **TODO** 

222  MDF_F_ACCOUNTSRECEIVABLE  number  A balance sheet item: Money owned by customers 

to another entity in exchange for goods or 

services that have been delivered or used, but not 

yet paid for. Also known as Credit Control. 

622  MDF_F_ACTIVESHARE  number  Active Share is a measure of the percentage of 

stock holdings in a manager's portfolio that differs 

from the benchmark index. 

208  MDF_F_ADDRESS  string  255  Postal Address 

200  MDF_F_ADJUSTEDEBITA  number  Adjusted EBITA 

190  MDF_F_ADJUSTEDEQUITY  number  16,8  Reported equity (excluding minority interests) 

less the (proposed) dividend. 

103  MDF_F_ADJUSTMENTFACTOR  number  16,6  The adjustment factor for the instrument when 

adjusting historical values for the corporate 

action. 

Prices should be multiplied with the factor while 

quantities should be divided by the factor. If the 

adjustment is because of change of trading 

currency then the quantities should be left 

untouched while the turnovers and prices should 

be multiplied with the factor. 

113  MDF_F_ANNOUNCEMENTDATE  date  The date on which the dividend where announced 

386  MDF_F_ANNUALIZEDRETURN1Y  number  19,7 

387  MDF_F_ANNUALIZEDRETURN2Y  number  19,7 

302  MDF_F_ANNUALIZEDRETURN3Y  number  19,7 

388  MDF_F_ANNUALIZEDRETURN4Y  number  19,7 

311  MDF_F_ANNUALIZEDRETURN5Y  number  19,7 

312  MDF_F_ANNUALIZEDRETURN10Y  number  19,7 

790  MDF_F_APPLICABLENAV  tabular  Specifies the timing rules for how the Applicable 

NAV is determined in T+/-X format. Each row 

contains this single column and the first row is the 

rules for buying fund units and the second row is 

the rules for selling fund units: 

● rule in T+/-X format 

349  MDF_F_ASIANTAILSTART  date  Start date of the Asian Tail 

350  MDF_F_ASIANTAILEND  date  End date of the Asian Tail 

63  MDF_F_ASKCOUNTERPART  string  Identifies the counter-parties interested in selling 

the instrument on the current level in the order 

book. The counter-parties are sorted from left to 

right in priority order. The list of counter-parties 

will usually be only the top 4 and not all the 

counter-parties. 

6 MDF_F_ASKPRICE  number  19,7  The best ask price on current level. For quotes, 

this is the currently best ask price for all levels.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

20  MDF_F_ASKQUANTITY  number  20,8  The ask quantity on current level. 

75  MDF_F_ASKYIELD  number  The best ask yield on current level. For quotes, 

this is the currently best ask yield for all levels. 

163  MDF_F_ATH  number  19,7  The adjusted all-time-high price 

183  MDF_F_ATHDATE  date  Date for the ATH price 

278  MDF_F_ATHYIELD  number  19,7  The adjusted all-time-high yield 

280  MDF_F_ATHYIELDDATE  date  Date for the ATH yield 

164  MDF_F_ATL  number  19,7  The adjusted all-time-low price 

184  MDF_F_ATLDATE  date  Date for the ATL price 

279  MDF_F_ATLYIELD  number  19,7  The adjusted all-time-low yield 

281  MDF_F_ATLYIELDDATE  date  Date for the ATL yield 

326  MDF_F_AVERAGE  number  19,7  The calculated arithmetic mean 

793  MDF_F_AVGTURNOVER1W  number  20,2  The average turnover over 1 calendar week. 

794  MDF_F_AVGTURNOVER1M  number  20,2  The average turnover over 1 calendar month. 

795  MDF_F_AVGTURNOVER3M  number  20,2  The average turnover over 3 calendar months. 

796  MDF_F_AVGTURNOVER1Y  number  20,2  The average turnover over 1 calendar year. 

797  MDF_F_AVGTURNOVERYTD  number  20,2  The average turnover so far in the current 

calendar year. 

300  MDF_F_BARRIERPRICE  number  19,7 

31  MDF_F_BASECURRENCY  string  4 The first currency in a currency pair 

245  MDF_F_BASERATIO  number  The base currency ratio, a “1:100” currency pair 

is represented with the value “100”. 

62  MDF_F_BIDCOUNTERPART  string  Identifies the counter-parties interested in buying 

the instrument on the current level in the order 

book. The counter-parties are sorted from right to 

rleft in priority order. The list of counter-parties 

will usually be only the top 4 and not all the 

counter-parties. 

5 MDF_F_BIDPRICE  number  19,7  The best bid price on current level. For quotes, 

this is the currently best bid price for all levels. 

19  MDF_F_BIDQUANTITY  number  20,8  The bid quantity on current level 

74  MDF_F_BIDYIELD  number  The best bid yield on current level. For quotes, 

this is the currently best bid yield for all levels. 

206  MDF_F_BIRTHYEARCEO  date  Birth year of the CEO 

207  MDF_F_BIRTHYEARCHAIRMAN  date  Birth year of the Chairman 

24  MDF_F_BOARDLOT  number  10,0  The minimum lot size for round lot trading 

375  MDF_F_BROKERS  tabular  Specifies the brokers for a marketplace. Each row 

contains these columns: 

● symbol (the code used in trades) 

● full name 

639  MDF_F_BVPS  number  Book Value Per Share (BVPS) 

640  MDF_F_BVPS_LAST  number  BVPS (Annualized) 

342  MDF_F_CAP  number  19,7  The cap level for Discount Certificates    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

203  MDF_F_CAPITALPRC  number  5,2  The percentage of the equity's capital that is 

owned by the major holder 

238  MDF_F_CASHFLOWAWC  number  A cash flow item: Operating Cash Flow after 

changes in Working Capital 

237  MDF_F_CASHFLOWBWC  number  A cash flow item: Free Cash Flow 

240  MDF_F_CASHFLOWFA  number  A cash flow item: Cash Flow from Financial 

Activities. Accounts for external activities such as 

issuing cash dividends, adding or changing loans, 

or issuing and selling more stock. 

239  MDF_F_CASHFLOWIA  number  A cash flow item: Cash Flow from Investing 

Activities. The aggregate change in a company's 

cash position resulting from any gains (or losses) 

from investments in the financial markets and 

operating subsidiaries, and changes resulting from 

amounts spent on investments in capital assets 

such as plant and equipment. 

241  MDF_F_CASHFLOWTOTAL  number  A cash flow item: Total Cash Flow 

102  MDF_F_CASUBTYPE  uint  Corporate Action Type = 0 

● 0 – Annual (1x per year) 

● 1 – Bonus 

● 2 – Monthly (12x per year) 

● 3 – Quarterly (4x per year) 

● 4 – Biannual (2x per year) 

● 5 – Triannual (3x per year) 

● 6 – Bimonthly (6x per year) 

Corporate Action Type = 2 

● 1 – Rights Issue Cancelled 

Corporate Action Type = 15 

● 0 – General Meeting 

● 1 – Extraordinary General Meeting 

● 2 – Capital Market Day 

● 3 – Year End Report 

● 4 – Interim Report 

● 5 – Analyst Meeting 

● 6 – Delisting 

● 7 – Company Presentation 

● 8 – Roadshow 

● 9 – Company Update / Interim Update 

● 10 – Business Review 

Corporate Action Type = 16 

● 0 – Buying 

● 1 – Selling 

● 2 – Current Position 

Corporate Action Type = 18 

● 0 – Closed 

● 1 – Early Closing 

● 2 – Extra Open (in case an exchange is 

forced open an a normally closed day) 

Corporate Action Type = 19    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● 0 – Direct Holder 

● 1 – Institutional Holder 

● 2 – Mutual Fund Holder 

99  MDF_F_CATYPE  uint  Defines the corporate action. Valid values: 

● 0 = Dividend 

● 1 = Split 

● 2 = Rights Issue 

● 3 = Bonus Issue 

● 4 = Directed Issue 

● 5 = Share Redemption 

● 6 = Spinoff / De-Merger 

● 7 = Stock Dividend 

● 8 = Stock Dividend of Other Shares 

● 9 = Unknown Event 

● 10 = Initial Public Offer (IPO) 

● 11 = Currency Conversion 

● 12 = Change of Nominal Value 

● 13 = Change in Underlyings 

● 14 = Change of Basic Data 

● 15 = Calendar 

● 16 = Insider Trading 

● 17 = Combined Split and Redemption 

● 18 = Exchange Closed 

● 19 = Major Holders 

● 20 = Share Loans 

● 21 = Internal Use Only 

225  MDF_F_CCE  number  A balance sheet item: The value of a company's 

assets that are cash or can be converted to cash 

immediately 

169  MDF_F_CEO  string  Chief Executive Officer 

313  MDF_F_CEOADMISSIONDATE  date  The CEO Admission date 

366  MDF_F_CFI  string  6 The Classification of Financial Instruments code 

as defined by ISO 10962 

631  MDF_F_CFPS  number  Cash Flow Per Share (CFPS) 

632  MDF_F_CFPS_TTM  number  CFPS (TTM) 

633  MDF_F_CFPS_LAST  number  CFPS (Annualized) 

168  MDF_F_CHAIRMAN  string  60  Chairman of the Board 

314  MDF_F_CHAIRMANADMISSIONDATE  date  The Chairman admission date 

443  MDF_F_CIK  number  10,0  A Central Index Key or CIK number is a number 

given to an individual or company by the United 

States Securities and Exchange Commission. The 

number is used to identify the filings of a 

company, person, or entity in several online 

databases, including EDGAR. 

210  MDF_F_CITY  string  50  City 

408  MDF_F_CISUBTYPE  uint  Company Information Type = 0 

● 0 – Current Insiders / Positions 

● 2 – Current Holdings 

● 3 – Transactions    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

Company Information Type = 1 

● 0 – Lottery Dates 

● 1 – Coupon Dates 

Company Information Type = 2 

● 0 – Short Selling 

Company Information Type = 3 

● 0 – Bond Cash Flow 

● 1 – Debtor Composition 

● 2 – Extra Redemption 

● 3 – Notification Drawing 

● 4 – Notification Drawing Percent 

407  MDF_F_CITYPE  uint  Company Information Type. Valid values: 

● 0 – Insider Trading 

● 1 – Various Dates 

● 2 – Short Selling 

● 3 – Genium GCF Bond Data 

788  MDF_F_CLEARING  tabular  Specifies the clearing/custody data for a 

instrument. Each row contains these columns: 

● BIC 

● Symbol 

● Name 

42  MDF_F_CLOSEASKPRICE  number  19,7  The last ask price when the market closed 

81  MDF_F_CLOSEASKYIELD  number  The last ask yield when the market closed 

41  MDF_F_CLOSEBIDPRICE  number  19,7  The last bid price when the market closed 

354  MDF_F_CLOSEBIDPRICE1D  number  19,7  The adjusted closing price to be used for 

calculating the net change for one day. 

356  MDF_F_CLOSEBIDPRICE1W  number  19,7  The adjusted closing price to be used for 

calculating the net change for one week. 

80  MDF_F_CLOSEBIDYIELD  number  19,7  The last bid yield when the market closed 

355  MDF_F_CLOSEBIDYIELD1D  number  19,7  The adjusted closing yield to be used for 

calculating the net change for one day. 

357  MDF_F_CLOSEBIDYIELD1W  number  19,7  The adjusted closing yield to be used for 

calculating the net change for one week. 

373  MDF_F_CLOSEDARKQUANTITY  number  20,0  The cumulative number of traded shares or 

contracts of shares for Dark Pool trades when the 

market closed. 

374  MDF_F_CLOSEDARKTURNOVER  number  38,7  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency of trades 

for Dark Pool trades when the market closed. 

43  MDF_F_CLOSEDAYHIGHPRICE  number  20,8  The highest paid price when the market closed 

83  MDF_F_CLOSEDAYHIGHYIELD  number  19,7  The highest paid yield when the market closed 

44  MDF_F_CLOSEDAYLOWPRICE  number  20,8  The lowest paid price when the market closed 

84  MDF_F_CLOSEDAYLOWYIELD  number  19,7  The lowest paid yield when the market closed 

58  MDF_F_CLOSEINTERNALQUANTITY  number  20,0  The cumulative number of traded shares or 

contract of shares where buyer and seller is the 

same, when the market closed.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

59  MDF_F_CLOSEINTERNALTURNOVER  number  38,7  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency of trades 

where buyer and seller is the same, when the 

market closed. 

94  MDF_F_CLOSENAV  number  19,4  The Net Asset Value when the market closed 

47  MDF_F_CLOSENUMTRADES  number  20,0  The number of trades when the market closed 

371  MDF_F_CLOSEOFFBOOKQUANTITY  number  20,0  The cumulative number of traded shares or 

contracts of shares for Off-Book trades when the 

market closed. 

372  MDF_F_CLOSEOFFBOOKTURNOVER  number  38,7  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency of trades 

for Off-Book trades when the market closed. 

40  MDF_F_CLOSEPRICE  number  20,8  The official close price. Can be different from the 

actual last paid price. 

737  MDF_F_CLOSEPRICEDATE  date  Date of the ClosePrice field in the Performance 

message. 

148  MDF_F_CLOSEPRICE1D  number  20,8  The adjusted closing price to be used for 

calculating the net change for one day. Sent when 

the market opens. 

736  MDF_F_CLOSEPRICE1DDATE  date  Date of the ClosePrice1D field. 

157  MDF_F_CLOSEPRICE10Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for ten years. 

150  MDF_F_CLOSEPRICE1M  number  20,8  The adjusted closing price to be used for 

calculating the net change for one month. 

149  MDF_F_CLOSEPRICE1W  number  20,8  The adjusted closing price to be used for 

calculating the net change for one week. 

334  MDF_F_CLOSEPRICE2W  number  20,8  The adjusted closing price to be used for 

calculating the net change for two weeks. 

154  MDF_F_CLOSEPRICE1Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for one year. 

155  MDF_F_CLOSEPRICE2Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for two years. 

151  MDF_F_CLOSEPRICE3M  number  20,8  The adjusted closing price to be used for 

calculating the net change for three months. 

249  MDF_F_CLOSEPRICE3Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for three years. 

777  MDF_F_CLOSEPRICE4Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for four years. 

156  MDF_F_CLOSEPRICE5Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for five years. 

152  MDF_F_CLOSEPRICE6M  number  20,8  The adjusted closing price to be used for 

calculating the net change for six months. 

778  MDF_F_CLOSEPRICE6Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for six years. 

779  MDF_F_CLOSEPRICE7Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for seven years.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

780  MDF_F_CLOSEPRICE8Y  number  20,8  The adjusted closing price to be used for 

calculating the net change for eight years. 

153  MDF_F_CLOSEPRICE9M  number  20,8  The adjusted closing price to be used for 

calculating the net change for nine months. 

781  MDF_F_CLOSEPRICE9Y  The adjusted closing price to be used for 

calculating the net change for nine years. 

250  MDF_F_CLOSEPRICELD  number  20,8  The adjusted closing price to be used for 

calculating the net change since listing date. 

159  MDF_F_CLOSEPRICEMTD  number  20,8  The adjusted closing price to be used for 

calculating the net change for month-to-date. 

162  MDF_F_CLOSEPRICEPYTD  number  20,8  The adjusted closing price to be used for 

calculating the net change for previous year-to-

date. 

160  MDF_F_CLOSEPRICEQTD  number  20,8  The adjusted closing price to be used for 

calculating the net change for quarter-to-date. 

431  MDF_F_CLOSEPRICETYPE  uint  Specifies if the value from 

MDF_F_CLOSEPRICE is from an actual trade or 

if it's a theoretical price. Valid values: 

● 0 – Last paid price during the day. 

● 1 – Theoretical price set from Market 

Maker orders. 

● 2 – Mid Price 

● 3 – Theoretical/Valuation price, 

unknown origin. 

● 4 – Volume Weighted Average Price. 

● 5 – Closing price of Reference Market. 

● 6 – Manually set by the Marketplace 

Market Operations. 

● 7 – Last Adjusted Closing Price 

158  MDF_F_CLOSEPRICEWTD  number  20,8  The adjusted closing price to be used for 

calculating the net change for week-to-date. 

161  MDF_F_CLOSEPRICEYTD  number  20,8  The adjusted closing price to be used for 

calculating the net change for year-to-date. 

45  MDF_F_CLOSEQUANTITY  number  20,8  The cumulative number of traded shares or 

contract of shares when the market closed. 

96  MDF_F_CLOSETIS  number  19,7  Taxable Income per Share for the mutual fund 

when the market closed. 

430  MDF_F_CLOSETRADEPRICE  number  20,8  The last paid price (from an actual trade) when 

the market closes. 

46  MDF_F_CLOSETURNOVER  number  38,8  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency of trades, 

when the market closed 

124  MDF_F_CLOSEVWAP  number  19,7  Volume Weighted Average Price when the market 

closed. 

82  MDF_F_CLOSEYIELD  number  Last paid yield when the market closed 

261  MDF_F_CLOSEYIELD1D  number  19,7  The adjusted closing yield to be used for 

calculating the net change for one day. 

271  MDF_F_CLOSEYIELD10Y  number  19,7  The adjusted closing yield to be used for    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

calculating the net change for ten years. 

263  MDF_F_CLOSEYIELD1M  number  19,7  The adjusted closing yield to be used for 

calculating the net change for one month. 

262  MDF_F_CLOSEYIELD1W  number  19,7  The adjusted closing yield to be used for 

calculating the net change for one week. 

335  MDF_F_CLOSEYIELD2W  number  19,7  The adjusted closing yield to be used for 

calculating the net change for two weeks. 

267  MDF_F_CLOSEYIELD1Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for one year. 

268  MDF_F_CLOSEYIELD2Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for two years. 

264  MDF_F_CLOSEYIELD3M  number  19,7  The adjusted closing yield to be used for 

calculating the net change for three months. 

269  MDF_F_CLOSEYIELD3Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for three years. 

782  MDF_F_CLOSEYIELD4Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for four years. 

270  MDF_F_CLOSEYIELD5Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for five years. 

265  MDF_F_CLOSEYIELD6M  number  19,7  The adjusted closing yield to be used for 

calculating the net change for six months. 

783  MDF_F_CLOSEYIELD6Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for six years. 

784  MDF_F_CLOSEYIELD7Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for seven years. 

785  MDF_F_CLOSEYIELD8Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for eight years. 

266  MDF_F_CLOSEYIELD9M  number  19,7  The adjusted closing yield to be used for 

calculating the net change for nine months. 

786  MDF_F_CLOSEYIELD9Y  number  19,7  The adjusted closing yield to be used for 

calculating the net change for nine years. 

277  MDF_F_CLOSEYIELDLD  number  19,7  The adjusted closing yield to be used for 

calculating the net change since listing date. 

273  MDF_F_CLOSEYIELDMTD  number  19,7  The adjusted closing yield to be used for 

calculating the net change for month-to-date. 

276  MDF_F_CLOSEYIELDPYTD  number  19,7  The adjusted closing yield to be used for 

calculating the net change for previous year-to-

date. 

274  MDF_F_CLOSEYIELDQTD  number  19,7  The adjusted closing yield to be used for 

calculating the net change for quarter-to-date. 

272  MDF_F_CLOSEYIELDWTD  number  19,7  The adjusted closing yield to be used for 

calculating the net change for week-to-date. 

275  MDF_F_CLOSEYIELDYTD  number  19,7  The adjusted closing yield to be used for 

calculating the net change for year-to-date. 

732  MDF_F_COMBOLEGS  tabular  Specifies the legs for a Combo or Strategy 

contract. Each row contains these columns:    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● Leg insref 

● Ratio of lots for the leg 

● Leg Side (0 – Buy, 1 – Sell) 

64  MDF_F_COMPANY  insref  Link to the company 

338  MDF_F_CONVERSIONPRICE  number  19,7  The price per share at which a convertible 

security, such as corporate bonds or preferred 

shares, can be converted into common stock. 

336  MDF_F_CONVERTFROMDATE  date  The first date at which a convertible security can 

be converted into common stock. 

337  MDF_F_CONVERTTODATE  date  The last date at thich a convertible security can be 

converted into common stock. 

197  MDF_F_COUNT  number  10  Used to indicate a number of items 

92  MDF_F_COUNTRY  string  2 Specifies country according to ISO 3166-1 alpha 

2

299  MDF_F_COUPONDATE  date 

694  MDF_F_COUPONFREQUENCY  number  1 Specifies the number of coupons per year. 

298  MDF_F_COUPONRATE  number  19,7 

297  MDF_F_CONSTITUENTS  tabular  Specifies the constituents for a index or fund. 

Each row contains these columns: 

● insref 

● weight in percentage (optional) 

● currency (optional) 

● ISIN (optional) 

244  MDF_F_CONTRACTSIZE  number  Specifies the number of underlying shares per 

derivative. For equities it shows the number of 

stocks a Depositary Receipt or Unit represents. 

353  MDF_F_CONTRACTVALUE  number  10  Specifies the monetary value in the underlying 

share of each tick in the derivative. 

143  MDF_F_CREDITLOSS  number  Credit loss 

345  MDF_F_CROSSTYPE  uint  The type of cross for which the Net Order 

Imbalance message is being generated. 

Valid values: 

● 0 – Crossing has Ended 

● 1 – Opening Cross 

● 2 – Closing Cross 

● 3 – Cross for Halted Securities 

● 4 – Scheduled Intraday Auction 

● 5 – Auction on Demand 

441  MDF_F_CSR  number  Corporate Sustainability Rating 

232  MDF_F_CURLIABILITIES  number  A balance sheet item: A company's debts or 

obligations that are due within one year 

226  MDF_F_CURRENTASSETS  number  A balance sheet item: The value of all assets that 

are reasonable expected to be converted into cash 

within one year in the normal course of business. 

290  MDF_F_CUSIP  string  9 The Committee on Uniform Security 

Identification Procedures identifier as assigned 

by Standard & Poor's. CUSIP is the NNA for    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

United States and Canada. 

616  MDF_F_CVR  number  10  Unique identifier for a business in Denmark’s 

Central Business Register (Det Centrale 

Virksomhedsregister). 

https://datacvr.virk.dk/data/ 

404  MDF_F_D1  date  Placeholder for dates. The exact definition is 

dependent upon context. 

405  MDF_F_D2  date 

406  MDF_F_D3  date 

369  MDF_F_DARKQUANTITY  number  20,0  The cumulative number of traded shares or 

contracts of shares for Dark Pool trades. 

370  MDF_F_DARKTURNOVER  number  38,7  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency of trades 

for Dark Pool trades. 

3 MDF_F_DATE  date  Specifies event date 

710  MDF_F_DAYCOUNTCONVENTION  uint  Defines the Day Count Convention used for 

calculating Bonds. 

Valid values: 

● 0 – 30E/360 

● 1 – 30U/360 

● 2 – Actual/360 

● 3 – Actual/365 

● 4 – Actual/Actual 

8 MDF_F_DAYHIGHPRICE  number  20,8  The highest paid price during the current trading 

session 

78  MDF_F_DAYHIGHYIELD  number  The highest paid yield during the current trading 

session 

9 MDF_F_DAYLOWPRICE  number  20,8  The lowest paid price during the current trading 

session 

79  MDF_F_DAYLOWYIELD  number  The lowest paid yield during the current trading 

session 

364  MDF_F_DELETERECORD  The presence of this field indicates that the record 

should be deleted. 

699  MDF_F_DELTA  number  Black–Scholes Delta 

27  MDF_F_DERIVATIVEINDICATOR  uint  Defines the derivative type. Valid values: 

● 0 – Call 

● 1 – Put 

● 2 – Forward 

● 3 – Future 

● 4 – Standard Combination 

● 5 – Tailor Made Combination 

● 6 – Gross Return Forward 

● 7 – Gross Return Future 

810  MDF_F_DER  number  Debt Ratio (DER) 

811  MDF_F_DER_LAST  number  DER (Announcement) 

172  MDF_F_DESCRIPTION  string  65535  Company description, long    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

132  MDF_F_DILUTEDEPS  number  An income statement item: Earnings per share 

that takes account of shares to be issued in the 

future, as well as those currently issued. 

100  MDF_F_DIVIDEND  number  19,4  The gross dividend price expressed in the 

instrument's trading currency 

318  MDF_F_DIVIDENDFREQUENCY  uint  Defines the derivative frequency. Valid values: 

● 0 – Annual 

● 1 – Semi-Annual 

● 2 – Quarterly 

● 3 – Monthly 

101  MDF_F_DIVIDENDORIGINAL  number  19,4  The dividend price expressed in the currency used 

in the announcement 

317  MDF_F_DIVIDENDTYPE  uint  Defines the dividend type. Valid values: 

● 0 – Accumulating 

● 1 – Distributing 

● 2 – None 

815  MDF_F_DPR  number  Dividend Payout Ratio 

630  MDF_F_DPS  number  Dividend Per Share (DPS) 

339  MDF_F_DURATION  number  19,7  Index duration calculated as Macalay's duration. 

175  MDF_F_DY  number  The dividend yield on a company is the 

company's annual dividend divided by its market 

cap. 

128  MDF_F_EBIT  number  An income statement item: Earnings before 

interest and taxes 

134  MDF_F_EBITA  number  An income statement item: Earnings before 

interest, taxes and amortization 

133  MDF_F_EBITDA  number  An income statement item: Earnings Before 

interest, taxes, deprecation and amortization. 

213  MDF_F_EMAIL  string  E-mail address 

131  MDF_F_EPS  number  An income statement item: Earnings per share 

(EPS). The part of the company's profit that is 

attributed to each individual share of stock. 

634  MDF_F_EPS_TTM  number  EPS (TTM) 

635  MDF_F_EPS_LAST  number  EPS (Annualized) 

173  MDF_F_EQUITYRATIO  number  Equity Ratio 

324  MDF_F_EUSIPA  number  4,0  European Structured Investment Products 

Association categorisation code. See 

http://www.eusipa.org/ 

382  MDF_F_EVENTLINK  string  36  A URI for downloading a document linked with 

this event can be constructed by using the value 

from this field as 

“https://documents.millistream.com/ <value>” 

where “<value>” is replaced with the value from 

this field. A specific language of the document 

can be requested with 

“https://documents.millistream.com/ <value>? 

language=<language>”, where “<language>” is a 

language code in ISO 639-1. The languages    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

supported for the document can be derived by the 

MDF_F_EVENTLINKLANGUAGES  field. 

383  MDF_F_EVENTLINGLANGUAGES  string  The languages available for the link described by 

MDF_F_EVENTLINK . Used to construct the 

complete URI of the event link in order to fetch a 

document in a different language than the default. 

The string is comma separated and the language 

codes are according to ISO 639-1. 

792  MDF_F_EVENTSTATUS  uint  Defines the status of the event. Valid values: 

● 0/ NULL  - Confirmed 

● 1 - Unconfirmed 

38  MDF_F_EXECUTEDSIDE  uint  Defines which side in the order book that was 

executed on a trade. Valid values: 

● 0 - Bid Side (the aggressor was the 

seller) 

● 1 - Ask Side (the aggressor was the 

buyer) 

28  MDF_F_EXERCISETYPE  uint  Type of exercise procedure. Valid values: 

● 0 – European 

● 1 – American 

● 2 – Asian 

● 3 – Binary 

● 4 – Bermudan 

711  MDF_F_EXPIRATIONTYPE  uint  Defines how derivatives expire. Valid values: 

● 0 – Quarterly 

● 1 – Monthly 

● 2 – Weekly 

● 3 – Daily 

● 4 – Yearly 

69  MDF_F_EXTRACREDENTIAL  string  Extra login credential to send to a 3d party 

authorization server to perform two-factor 

authentication. 

Currently supported services: 

* Yubikey OTP ( https://www.yubico.com/ )

* OATH-TOTP 

(https://tools.ietf.org/html/rfc6238 )

212  MDF_F_FAX  string  40  Fax number 

330  MDF_F_FIELDASPECT  string  Defines the aspect of the field value for estimates. 

Valid values: 

● Value – The value as such 

● GrPP – The growth in the value, from 

previous period, to the current. 

● GrYY – The growth in the value, from 

the same period, previous year to 

current. 

● Margin – (Margin to Sales) The margin 

between the Variable and the Variable 

Sales. 

329  MDF_F_FIELDNAME  string  30  Contains the name of the field 

331  MDF_F_FIELDTYPE  string  Defines the type of the field value for estimates.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

Describes if the value is an estimate (a consensus 

estimate) or an actual (outcome), and whether 

NRI (Non-Recurring Items) have been included. 

Valid values: 

● EstIEstNri – The estimated value, 

including the estimated NRI. 

● EstXNri – The estimated value excluding 

NRI. 

● EstISmeNri – The estimated value, 

including SME:s judgment of NRI. 

● ActIActNri – The actual value, once it 

has been published, including the actual 

NRI (Proforma if such a value has been 

published later). 

● ActXNri – The actual value, once it has 

been published excluding NRI (Proforma 

if such a value has been published later). 

● ActIActNriAR – The actual value, once 

it has been published, including the 

actual NRI (As originally reported, even 

if a Proforma value has later been 

published). 

● ActXNriAR – The actual value, once it 

has been published, excluding the actual 

NRI (As originally reported, even if a 

Proforma value has later been 

published). 

● SmeNri – SME:s judgment of NRI, 

isolated. 

● ActNri – Actual NRI, isolated (Proforma 

if such a value has been published). 

● ActNriAR – Actual NRI, isolated (As 

originally reported, even if a Proforma 

value has later been published). 

● Dev – Deviation. The percentage 

deviation of the forecast, including 

actual NRI, from the actual value, 

including actual NRI. 

333  MDF_F_FIELDUNIT  string  Defines the unit of the field value. Valid Values: 

● Currency 

● Percentage points 

● Unit 

● Thousand 

● Million 

● Billion 

● Percent 

● UnitCond 

● UnitCond2 

689  MDF_F_FIGI  string  12  Financial Instrument Global Identifier 

690  MDF_F_FIGICOMPOSITE  string  12  Composite Financial Instrument Global Identifier 

693  MDF_F_FIGISECURITYTYPE  string  40  SecurityType according to FIGI. For list of 

definitions see: 

https://www.omg.org/spec/FIGI/20150501/Securit 

yTypes.rdf    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

691  MDF_F_FIGISHARECLASS  string  12  Share Class Financial Instrument Global 

Identifier 

363  MDF_F_FIINSTITUTENUMBER  number  19,0  Identifier assigned by The Swedish Financial 

Supervisory Authority (Finansinspektionen), used 

to identify institutions and mutual funds. 

218  MDF_F_FINANCIALASSET  number  A balance sheet item: An asset that derives value 

because of contractual claim. Stocks, bonds, bank 

deposits, and the like are all examples of financial 

assets. 

359  MDF_F_FINANCIALCOST  number  19,7 

358  MDF_F_FINANCIALINCOME  number  19,7 

360  MDF_F_FINANCINGLEVEL  number  19,7  A loan included in a Minifuture 

321  MDF_F_FISCALPERIOD  char  19  The fiscal period in “YYYYMMDD – 

YYYYMMDD” format. Used for fundamentals 

data and the interim report and quarterly report 

events. 

525  MDF_F_FISN  string  35  Financial Instrument Short Name according to 

ISO 18774 

217  MDF_F_FIXEDASSET  number  A balance sheet item: A long-term tangible piece 

of property that a firm owns and uses in the 

production of its income and is not expected to be 

consumed or converted into cash any sooner than 

at least one year's time. Also known as Plant. 

254  MDF_F_FUNDBENCHMARK  string  Fund benchmark indices. Multiple indices are 

separated with pipe '|'. 

294  MDF_F_FUNDBENCHMARKINSREF  insref  Link to the first benchmark index from the Fund 

Benchmark Index field if available in the 

Millistream universe. 

90  MDF_F_FUNDCOMPANY  insref  Link to the fund company issuing the fund 

791  MDF_F_FUNDCUTOFFTIME  tabular  Specifies the cut-off time for placing orders for 

mutual fund units. Each row contains these 

columns and the first row is the rules for buying 

fund units while the second row is for selling fund 

units: 

● the cut-off time in HH:MM 

● the timezone of the cut-off time 

256  MDF_F_FUNDDIRECTION  string  5 Is either “Long” or “Short” 

255  MDF_F_FUNDLEVERAGE  number  The fund leverage expressed in percent against 

the fund benchmark index. If 

MDF_F_FUNDDIRECTION is not NULL then a 

NULL value for this field indicates that the 

leverage is either +100% or -100%. 

91  MDF_F_FUNDPMICODE  string  11  Identifier assigned by the Swedish Mutual Fund 

Association 

65  MDF_F_FUNDPPMCODE  number  7,0  Identifier assigned by Premie Pensions 

Myndigheten 

252  MDF_F_FUNDPPMFEE  number  The fund yearly management fee if bought as a 

PPM fund    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

253  MDF_F_FUNDPPMTYPE  string 

323  MDF_F_FUNDRISK  number  5

251  MDF_F_FUNDYEARLYMGMTFEE  number  The fund yearly management fee 

700  MDF_F_GAMMA  number  Black–Scholes Gamma 

204  MDF_F_GENDERCEO  string  1 (M)ale or (F)emale 

205  MDF_F_GENDERCHAIRMAN  string  1 (M)ale or (F)emale 

248  MDF_F_GENIUMID  number  10  Identifier used by NASDAQ OMX in their 

Genium Consolidated Feed (GCF) 

259  MDF_F_GEOFOCUSCOUNTRY  string  20  Geographic focus, country 

258  MDF_F_GEOFOCUSREGION  string  20  Geographic focus, region 

647  MDF_F_GM  number  Gross Margin (GM) 

648  MDF_F_GM_TTM  number  GM (TTM) 

649  MDF_F_GM_LAST  number  GM (Annualized) 

216  MDF_F_GOODWILL  number  A balance sheet item: Goodwill typically reflects 

the value of intangible assets such as a strong 

brand name, good customer relations, good 

employee relations and any patents or proprietary 

technology. 

198  MDF_F_GROSSPROFIT  number  An income statement item: The net sales minus 

the cost of goods and services sold. Also known 

as Sales Profit. 

1 MDF_F_HEADLINE  string  The headline of the news item 

165  MDF_F_HIGHPRICE1Y  number  19,7  The adjusted highest price from one year back till 

now. 

624  MDF_F_HIGHPRICE3Y  number  19,7  The adjusted highest price from three years back 

till now. 

626  MDF_F_HIGHPRICE5Y  number  19,7  The adjusted highest price from five years back 

till now. 

628  MDF_F_HIGHPRICE10Y  number  19,7  The adjusted highest price from ten years back till 

now. 

185  MDF_F_HIGHPRICE1YDATE  date  Date of the High Price 1Y price 

193  MDF_F_HIGHPRICEYTD  number  19,7  The adjusted highest price since the previous year 

195  MDF_F_HIGHPRICEYTDDATE  date  Date of the High Price YTD price 

282  MDF_F_HIGHYIELD1Y  number  19,7  The adjusted highest yield from one year back till 

now. 

288  MDF_F_HIGHYIELD1YDATE  date  Date of High Yield 1Y value 

284  MDF_F_HIGHYIELDYTD  number  19,7  The adjusted highest yield since the previous year 

286  MDF_F_HIGHYIELDYTDDATE  date  Date of High Yield YTD value 

399  MDF_F_I1  number  10,0  Placeholder for integers. The exact definition is 

dependent upon context. 

400  MDF_F_I2  number  10,0 

401  MDF_F_I3  number  10,0 

402  MDF_F_I4  number  10,0    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

403  MDF_F_I5  number  10,0 

722  MDF_F_I6  number  10,0 

723  MDF_F_I7  number  10,0 

724  MDF_F_I8  number  10,0 

725  MDF_F_I9  number  10,0 

726  MDF_F_I10  number  10,0 

236  MDF_F_IBL  number  A balance sheet item: Interest-Bearing Liabilities 

343  MDF_F_IMBALANCE  number  20  The number of shares not paired at the current 

equilibrium price. 

344  MDF_F_IMBALANCEDIRECTION  uint  The market side of the order imbalance. 

Valid values: 

● 0 – Imbalance (side not disclosed) 

● 1 – Buy Imbalance 

● 2 – Sell Imbalance 

● 3 – No Imbalance 

● 4 – Insufficient Orders to Calculate 

214  MDF_F_IMPORTANTEVENTS  string  Company description of important events 

293  MDF_F_INCEPTIONDATE  date  The day a fund begins offering shares 

735  MDF_F_INCOMEPROPMAN  number  Income From Property Management 

727  MDF_F_INSREF1  insref 

728  MDF_F_INSREF2  insref 

729  MDF_F_INSREF3  insref 

730  MDF_F_INSREF4  insref 

731  MDF_F_INSREF5  insref 

53  MDF_F_INSREFLIST  list  A list of instrument references. Used as a filter for 

requests or in the reply to a  MDF_RC_INSREF 

request. When used as a filter for request a string 

containing the single character "*" indicates "all 

instruments that I'm entitled to". 

295  MDF_F_INSTRUMENTCLASS  uint  Defines the Instrument Class of the underlying 

instrument. 

Valid values: 

● 0 – Equity 

● 1 – Commodity 

● 2 – Alternative 

● 3 – Currency 

● 4 – Fixed Income 

● 5 – Index 

● 6 – Future 

296  MDF_F_INSTRUMENTSUBCLASS  string  30  Defines the Instrument Sub Class of the 

underlying instrument. 

319  MDF_F_INSTRUMENTSUBSUBCLASS  string  120  Defines the Instrument Subsub Class of the 

underlying instrument. 

26  MDF_F_INSTRUMENTSUBTYPE  uint  Instrument Type = 0    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● 0 – Regulated Marketplace 

● 1 – Multilateral Trading Facility 

● 2 – Over The Counter 

● 3 – Index Calculator 

● 4 – Fund Reporter 

Instrument Type = 1 

● 0 – Exchange List 

● 1 – Custom List (for internal use only) 

Instrument Type = 2 

● 0 – Company 

● 1 – Fund Company 

Instrument Type = 3 

● 0 – News Agency 

● 1 – Press Release Agency 

● 2 – System Messages 

Instrument Type = 4 

● 0 – Common Stock 

● 1 – Preferred Stock 

● 2 – Unit Share 

● 3 – Semi Preferred Stock (Common 

Stock that is functionally equivalent to 

Preferred Stock in many ways). 

● 4 – Special Purpose Aquisition Company 

(SPAC) 

Instrument Type = 5 

● 0 – Standardized Derivative 

● 1 – Certificate 

● 2 – Discount Certificate 

● 3 – Index Certificate 

● 4 – Out-Performance Certificate 

● 5 – Bonus Certificate 

● 6 – Tracker Certificate 

● 7 – Win Win Certificate 

● 8 – Share Basket Certificate 

● 9 – Market Neutral Strategy Linked 

Bond 

● 10 – Mini Future (Knock Out Warrant) 

● 11 – Reversed Convertible 

● 12 – Gearing Certificate 

● 13 – Strategy Linked Bond 

● 14 – Commodities 

● 15 – Booster Certificate 

● 16 – Autocall Certificate 

● 17 – Capital Protected Certificate 

● 18 – Flexible 

● 19 – CBF (Custom Basket Forward) 

Instrument Type = 6 

● 0 – Price Index 

● 1 – Total Return Index, Net 

● 2 – Total Return Index, Gross    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

Instrument Type = 7 

● 0 – Equity 

● 1 – Commodity 

● 2 – Alternative 

● 3 – Currency 

● 4 – Fixed Income 

Instrument Type = 8 

● 0 – Equity Fund 

● 1 – Balanced Fund 

● 2 – Money Market Fund 

● 3 – Bond Fund 

● 4 – Asset Allocation Fund 

● 5 – Hedge Fund 

● 6 – Risk Fund 

● 7 – Short-Term Bond Fund 

● 8 – Index Fund 

● 9 – Unit Link Fund 

● 10 – Income Mixed Fund 

● 11 – Uncategorized Fund 

● 12 – Real Estate Fund 

Instrument Type = 9 

● 0 – Subscription Rights 

● 1 – Bonus Rights 

● 2 – Unit Rights 

● 3 – Share Purchase Right 

● 4 – Interim Share 

● 5 – Redemption Right 

● 6 – Subscription Option 

Instrument Type = 10 

● 0 – Spot 

● 1 – Fixing 

● 2 – Forward 

Instrument Type = 11 

● 0 – Convertible Bond 

● 1 – Premium Bond 

● 2 – Equity Linked Bond 

● 3 – Index Linked Bond 

● 4 – Commodity Linked Bond 

● 5 – Currency Linked Bond 

● 6 – Fund Linked Bond 

● 7 – Multi-Asset Linked Bond 

● 8 – Government Bond 

● 9 – Eurobond 

● 10 – Municipal Bond 

● 11 – Corporate Bond 

● 12 – Mortgage Bond 

● 13 – Bond 

● 14 – Inflation Linked Bond 

● 15 – Loan Debenture 

● 16 – Structured Products 

● 17 – Retail Corporate Bonds 

● 18 – Retail Bonds 

● 19 – Tailor Made Products    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

Instrument Type = 12 

● 0 – Treasury Bill 

● 1 – Treasury Note 

● 2 – Fixings 

● 3 – Certificates 

● 4 – Swaps 

● 5 – Deposits 

● 6 – Forward Rate Agreement (FRA) 

● 7 – Macro Data 

Instrument Type = 13 

● 0 – Tenant Ownership Loan 

● 1 – Detached House Loan 

● 2 – House Loan Average Rate 

Instrument Type = 15 

● 0 – Warrant 

● 1 – Unlimited Turbo (Knock Out) 

● 2 – Digital Warrant 

● 3 – Barrier Warrant 

● 4 – Hit Warrant 

● 5 – Index Warrant 

● 6 – Turbo Warrant (Knock Out) 

● 7 – Knock Out Binary Warrant 

● 8 – Double Knock Out Binary Warrant 

Instrument Type = 20 

● 0 – GICS 

● 1 – ICB 

● 2 – Millistream Open Industry 

Classification (MOIC) 

Instrument Type = 21 

● 0 – Metals 

● 1 – Precious Metals 

● 2 – Energy 

Instrument Type = 22 

● 0 – Bull & Bear 

● 1 – Spread Certificate 

Instrument Type = 25 

● 0 – At The Money (ATM) 

● 1 – -90% of ATM 

● 2 – -95% of ATM 

● 3 – -105% of ATM 

● 4 – -110% of ATM 

25  MDF_F_INSTRUMENTTYPE  uint  The type of the instrument. Value values: 

● 0 – Marketplace 

● 1 – List 

● 2 – Company 

● 3 – News Agency 

● 4 – Equity 

● 5 – Derivative 

● 6 – Index    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● 7 – Exchange Traded Fund 

● 8 – Mutual Fund 

● 9 – Rights 

● 10 – Forex 

● 11 – Fixed Income 

● 12 – Money Market 

● 13 – Real Estate 

● 14 – Structured Product 

● 15 – Warrant 

● 16 – Uncategorized Type 

● 17 – Exchange Traded Commodity 

● 18 – Unit Trust Certificate 

● 19 – Primary Capital Certificate 

● 20 – Classification Sector 

● 21 – Commodity 

● 22 – Exchange Traded Note / Certificate 

● 23 – Tick Table 

● 24 – Submarket 

● 25 – Implied Volatility Instruments 

215  MDF_F_INTANGIBLEASSET  number  19,7  A balance sheet item: An asset that is not physical 

in nature. 

378  MDF_F_INTERESTEXPENSE  number  19,7  An income statement item: **TODO** 

376  MDF_F_INTERESTINCOME  number  19,7  An income statement item: **TODO** 

411  MDF_F_INTERESTRATE  number  19,7  The rate expressed in percentage at which interest 

is paid by a borrower. For Premium/Lottery 

Bonds this is the percentage of the Outstanding 

Amount that is paid out each year in the lottery. 

56  MDF_F_INTERNALQUANTITY  number  20,0  The cumulative number of traded shares or 

contracts of shares where buyer and seller is the 

same. 

57  MDF_F_INTERNALTURNOVER  number  38,7  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency of trades 

where buyer and seller is the same. 

220  MDF_F_INVENTORY  number  A balance sheet item: Value of materials and 

goods held by a firm to support production, for 

support activities, or for sale or customer service. 

23  MDF_F_ISIN  string  12  The International Securities Identification 

Number as assigned to the instrument by the 

National Numbering Agency (NNA). 

29  MDF_F_ISSUECURRENCY  string  4 The issue currency 

33  MDF_F_ISSUEDATE  date  The issue date 

362  MDF_F_ISSUEPRICE  number  19,7  The issue price, can be in percentage for 

structured products. 

247  MDF_F_ISSUER  string  4 The symbol/abbreviated name of the issuer as set 

by the marketplace. 

352  MDF_F_ISSUERNAME  string  255  The non-abbreviated name of the issuer. Set and 

determined by Millistream. 

698  MDF_F_IV  number  Implied Volatility calculated on Mid Price. 

709  MDF_F_IVASK  number  Implied Volatility calculated on Ask Price.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

708  MDF_F_IVBID  number  Implied Volatility calculated on Bid Price. 

617  MDF_F_KENNITALA  number  10  A unique national identification number used by 

the Icelandic government to identify individuals 

and organizations in Iceland, administered by the 

Registers Iceland (Þjóðskrá Íslands). 

https://www.skatturinn.is/fyrirtaekjaskra/ 

365  MDF_F_KIID  string  65535  URL to the UCITS Key Investor Information 

Document (KIID). 

0 MDF_F_LANGUAGE  string  2 Specifies the language according to ISO 639-1 

789  MDF_F_LASTMOD  time_t  UNIX epoch timestamp of when the item was last 

modified 

7 MDF_F_LASTPRICE  number  20,8  The last paid price during the current trading 

session 

76  MDF_F_LASTYIELD  number  The last paid yield during the current trading 

session 

437  MDF_F_LATESTYEARENDREPORT  number  4 The year of the latest Year End report for the 

company as available in the 

MDF_M_FUNDAMENTALS message. 

426  MDF_F_LEGALSTRUCTURE  string  The legal structure of the Mutual Fund 

526  MDF_F_LEI  string  20  Legal Entity Identifier according to ISO 17442 

55  MDF_F_LIST  list  Links to the lists the instrument belongs 

70  MDF_F_LOGOFFREASON  string  The reason the server terminated the connection. 

The value is constructed as a status number 

followed be a free text field. The current status 

numbers are: 

● 503 – The server is shutting down 

● 502 – Lost contact with dbs-node 

● 401 – Authentication Failure 

● 204 – Response to client log off request 

351  MDF_F_LOGOTYPE  string  65535  The URI to a image file representing the company 

logotype. 

166  MDF_F_LOWPRICE1Y  number  19,7  The adjusted lowest price from one year back till 

now. 

625  MDF_F_LOWPRICE3Y  number  19,7  The adjusted lowest price from three yearsback 

till now. 

627  MDF_F_LOWPRICE5Y  number  19,7  The adjusted lowest price from five years back till 

now. 

629  MDF_F_LOWPRICE10Y  number  19,7  The adjusted lowest price from ten years back till 

now. 

186  MDF_F_LOWPRICE1YDATE  date  Date of the Low Price 1Y price 

194  MDF_F_LOWPRICEYTD  number  19,7  The adjusted lowest price since previous year 

196  MDF_F_LOWPRICEYTDDATE  date  Date of the Low Price YTD price 

283  MDF_F_LOWYIELD1Y  number  19,7  The adjusted lowest yield from one year back till 

now. 

289  MDF_F_LOWYIELD1YDATE  date  Date of the Low Yield 1Y value    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

285  MDF_F_LOWYIELDYTD  number  19,7  The adjusted lowest price since previous year 

287  MDF_F_LOWYIELDYTDDATE  date  Date of the Low Yield YTD value 

231  MDF_F_LTLIABILITIES  number  A balance sheet item: A company's liabilities for 

leases, bond repayments and other items due in 

more than one year 

802  MDF_F_MACD  number  Moving Average Convergence/Divergence 

424  MDF_F_MARKETCLOSE  time  The time when the marketplace closes for trading 

on a normal trading day. 

425  MDF_F_MARKETEARLYCLOSE  time  The time when the marketplace closes for trading 

on a early closing day. 

412  MDF_F_MARKETMAKER  string  A broker-dealer firm that accepts the risk of 

holding a certain number of shares of a particular 

security in order to facilitate trading in that 

security. Also called a Liquidity Provider. 

If the name of the Market Maker is unknown then 

a string value of “Y” will be used. 

423  MDF_F_MARKETOPEN  time  The time when the marketplace opens for trading, 

both on normal and early closing days. 

429  MDF_F_MARKETOPENDAYS  bitfield  Tells which days that the marketplace is normally 

open for trading. If the marketplace is forced 

closed or forced open then this information can be 

found in Corporate Action Type = 18. Valid 

values: 

● 64 – Sundays 

● 32 – Saturdays 

● 16 – Fridays 

● 8 – Thursdays 

● 4 – Wednesdays 

● 2 – Tuesdays 

● 1 – Mondays 

54  MDF_F_MARKETPLACE  insref  Link to the marketplace 

328  MDF_F_MAX  number  19,7  The largest number in a range of values 

384  MDF_F_MAXLEVEL  number  13,6  The Max Level for Max Certificates 

243  MDF_F_MCAP  number  19,7  Market Capitalization is a measurement of 

corporate or economic size equal to the share 

price times the number of outstanding shares of a 

public company. 

119  MDF_F_MIC  string  4 Identifier for the Market place according to ISO 

10383 

656  MDF_F_MIFID00001  string  3 00001_EMT_Version. Valid values: 

● V1 – EMTv1 

● V2 – EMTv2 

● V3 - EMTv3 

657  MDF_F_MIFID00005  string  19  00005_File_Generation_Date_and_Time 

658  MDF_F_MIFID00006  string  1 00006_EMT_Data_Reporting_Target_Market. 

Valid values: 

● Y – Yes 

● N - No    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

659  MDF_F_MIFID00007  string  1 00007_EMT_Data_Reporting_ExAnte. Valid 

values: 

● Y – Yes 

● N - No 

660  MDF_F_MIFID00008  string  1 00008_EMT_Data_Reporting_ExPost. Valid 

values: 

● Y – Yes 

● N - No 

548  MDF_F_MIFID00010  string  00010_Financial_Instrument_Identifying_Data 

549  MDF_F_MIFID00020  uint  00020_Type_Of_Identification_Code_For_The_F 

inancial_Instrument. Valid values: 

● 1 – ISIN 

● 2 – CUSIP 

● 3 – SEDOL 

● 4 – WKN 

● 5 – Bloomberg Ticker 

● 6 – BBGID 

● 7 – Reuters RIC 

● 8 – FIGI 

● 9 – Other code by members of the 

Association of National Numbering 

Agencies 

● 99 – Code attributed by the undertaking 

550  MDF_F_MIFID00030  string  255  00030_Financial_Instrument_Name 

551  MDF_F_MIFID00040  string  3 00040_Financial_Instrument_Currency according 

to ISO 4217 

661  MDF_F_MIFID00045  string  1 00045_Financial_Instrument_Performance_Fee. 

Valid values: 

● Y – Yes 

● N – No 

662  MDF_F_MIFID00047  string  1 00047_Financial_Instrument_Distribution_Of_Ca 

sh. Valid values: 

● Y – Yes 

● N – No 

553  MDF_F_MIFID00060  string  2 00060_Financial_Instrument_Legal_Structure. 

Valid values: 

● S – Structured Securities 

● SF – Structured Funds 

● U – UCITS 

● N – Non UCITS 

663  MDF_F_MIFID00068  string  255  00068_EMT_Responsible_Name 

664  MDF_F_MIFID00069  string  20  00069_EMT_Responsible_LEI 

554  MDF_F_MIFID00070  string  255  00070_Financial_Instrument_Issuer_Name 

665  MDF_F_MIFID00073  string  20  00073_Financial_Instrument_Manufacturer_LEI 

666  MDF_F_MIFID00074  string  255  00074_Financial_Instrument_Manufacturer_Emai 

l

667  MDF_F_MIFID00075  string  1 00075_Financial_Instrument_Manufacturer_Prod 

uct_Governance_Process Valid values: 

● A - Product governance procedure 

pursuant to MiFID II    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● B - Product governance procedure 

comparable to MiFID II 

● C - Product governance procedure not in 

accordance with MiFID II 

● D - No information is requested from the 

issuer 

555  MDF_F_MIFID00080  string  255  00080_Financial_Instrument_Guarantor_Name 

668  MDF_F_MIFID00085  string  1 00085_Financial_Instrument_Type_ 

Notional_or_Item_Based. Valid values: 

● N - Notional based instrument 

● I - Item based instrument 

556  MDF_F_MIFID00090  string  255  00090_Product_Category_or_Nature 

669  MDF_F_MIFID00095  number  4,0  00095_Structured_Securities_Product_Category_ 

or_Nature 

557  MDF_F_MIFID00100  string  1 00100_Leveraged_Financial_Instrument_or_Cont 

ingent_Liability_Instrument. Valid values: 

● Y – Yes 

● N – No 

670  MDF_F_MIFID00110  string  1 00110_Fund_Clean_Share_Class Valid values: 

● Y – Yes 

● N - No 

671  MDF_F_MIFID00120  string  1 00120_Ex_Post_Cost_Calculation_Basis_Italy. 

Valid values: 

● R - Rolling based (last 12 months) 

● F - Fixed base (calendar year) 

672  MDF_F_MIFID00130  string  1 00130_ESG_Integration_Level. Valid values: 

● E - Enhanced Integration 

● S - ESG Strategy 

● I - Impact investing 

673  MDF_F_MIFID01000  date  01000_Target_Market_Reference_Date 

558  MDF_F_MIFID01010  string  1 01010_Investor_Type_Retail. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

559  MDF_F_MIFID01020  string  1 01020_Investor_Type_Professional. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

● P – Professional per se 

● E – Elective Professional 

● B – Both 

560  MDF_F_MIFID01030  string  1 01030_Investor_Type_Eligible_Counterparty. 

Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

561  MDF_F_MIFID02010  string  1 02010_Basic_Investor. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

562  MDF_F_MIFID02020  string  1 02020_Informed_Investor. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

563  MDF_F_MIFID02030  string  1 02030_Advanced_Investor. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

564  MDF_F_MIFID02040  string  1 02040_Expert_Investor_Germany. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

565  MDF_F_MIFID03010  string  1 03010_No_Capital_Loss. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

566  MDF_F_MIFID03020  string  1 03020_Limited_Capital_Loss. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

567  MDF_F_MIFID03030  number  03030_Limited_Capital_Loss_Level 

568  MDF_F_MIFID03040  string  1 03040_No_Capital_Guarantee. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

569  MDF_F_MIFID03050  string  1 03050_Loss_Beyond_Capital. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

570  MDF_F_MIFID04010  number  1 04010_Risk_Tolerance_PRIIPS_Methodology. 

Valid values: 1-7 

571  MDF_F_MIFID04020  number  1 04020_Risk_Tolerance_UCITS_Metholodology. 

Valid values: 1-7 

572  MDF_F_MIFID04030  string  1 04030_Risk_Tolerance_Internal 

_Methodology_For_Non_PRIIPS_and_Non_UCI 

TS. Valid values: 

● L – Low 

● M – Medium 

● H – High 

573  MDF_F_MIFID04040  number  1 04040_Risk_Tolerance_For_Non_PRIIPS_and_N 

on_UCITS_Spain. Valid values: 1-6 

574  MDF_F_MIFID04050  string  1 04050_Not_For_Investors_With_The_Lowest_Ri 

sk_Tolerance_Germany. Valid values: 

● Y – Yes 

● ‘-’ - Neutral 

575  MDF_F_MIFID05010  string  1 05010_Return_Profile_Preservation. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

576  MDF_F_MIFID05020  string  1 05020_Return_Profile_Growth. Valid values:    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

577  MDF_F_MIFID05030  string  1 05030_Return_Profile_Income. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

578  MDF_F_MIFID05040  string  1 05040_Return_Profile_Hedging. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

579  MDF_F_MIFID05050  string  1 05050_Option_or_Leveraged_Return_Profile. 

Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

580  MDF_F_MIFID05060  string  1 05060_Return_Profile_Other. Valid values: 

● Y – Yes 

● ‘-’ - Neutral 

581  MDF_F_MIFID05070  string  1 05070_Return_Profile_Pension_Scheme_German 

y. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

582  MDF_F_MIFID05080  string  1 05080_Time_Horizon. Valid values: 

● V – Very short term 

● S – Short term 

● M – Medium term 

● L – Long term 

● ‘-’ – Neutral 

583  MDF_F_MIFID05080N  number  05080_Time_Horizon in years if 

MDF_F_MIFID05080 is NULL or absent 

585  MDF_F_MIFID05100  string  1 05100_May_Be_Terminated_Early. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

674  MDF_F_MIFID05105  string  1 05105_Intended_Compatible_With_Clients_Havi 

ng_ESG_Preferences. Valid values: 

● Y – Yes 

● N – No 

● ‘-’ - Neutral 

586  MDF_F_MIFID05110  string  1 05110_Specific_Investment_Need. Valid values: 

● Y – Yes 

● N -No 

● G – Green Investment 

● E – Ethical Investment 

● I – Islamic Banking 

● S – ESG 

● O – Other 

675  MDF_F_MIFID05115  string  1 05115_Other_Specific_Investment_Need. Valid 

values:    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● N - No 

● I - Islamic banking 

● O - Other 

587  MDF_F_MIFID06010  string  1 06010_Execution_Only. Valid values: 

● R – Retail 

● P – Professional 

● B – Both 

● N – Neither 

588  MDF_F_MIFID06020  string  1 06020_Execution_With_Appropriateness_Test_O 

r_Non_Advised_Services. Valid values: 

● R – Retail 

● P – Professional 

● B – Both 

● N – Neither 

589  MDF_F_MIFID06030  string  1 06030_Investment_Advice. Valid values: 

● R – Retail 

● P – Professional 

● B – Both 

● N – Neither 

590  MDF_F_MIFID06040  string  1 06040_Portfolio_Management. Valid values: 

● R – Retail 

● P – Professional 

● B – Both 

● N – Neither 

591  MDF_F_MIFID07010  string  1 07010_Structured_Securities_Quotation. Valid 

values: 

● U – Unit figures 

● P – Percentage quotation 

592  MDF_F_MIFID07020  number  07020_One-

off_cost_Financial_Instrument_entry_cost 

676  MDF_F_MIFID07025  number  07025_Net_One-

off_cost_Financial_Instrument_entry_cost_non_a 

cquired 

593  MDF_F_MIFID07030  number  07030_One-

off_cost_Financial_Instrument_maximum_entry_ 

cost_fixed_amount_Italy 

594  MDF_F_MIFID07040  number  07040_One-

off_cost_Financial_Instrument_maximum_entry_ 

cost_acquired 

595  MDF_F_MIFID07050  number  07050_One-

off_costs_Financial_Instrument_maximum_exit_ 

cost 

596  MDF_F_MIFID07060  number  07060_One-

off_costs_Financial_Instrument_maximum_exit_ 

cost_fixed_amount_Italy 

597  MDF_F_MIFID07070  number  07070_One-

off_costs_Financial_Instrument_maximum_exit_ 

cost_acquired 

598  MDF_F_MIFID07080  number  07080_One-

off_costs_Financial_Instrument_Typical_exit_cos    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

t

599  MDF_F_MIFID07090  number  07090_One-

off_cost_Financial_Instrument_exit_cost_structur 

ed_securities_prior_RHP 

600  MDF_F_MIFID07100  number  07100_Financial_Instrument_Ongoing_costs 

677  MDF_F_MIFID07101  number  07101_Financial_Instrument_Total_Cost_Of_Un 

derlying_Funds_UK 

678  MDF_F_MIFID07105  number  07105_Financial_Instrument_Gearing_costs_ex_a 

nte_UK 

601  MDF_F_MIFID07110  number  07110_Financial_Instrument_Management_fee 

602  MDF_F_MIFID07120  number  07120_Financial_Instrument_Distribution_fee 

603  MDF_F_MIFID07130  number  07130_Financial_Instrument_Transaction_costs_ 

ex_ante 

604  MDF_F_MIFID07140  number  07140_Financial_Instrument_Incidental_costs_ex 

_ante 

679  MDF_F_MIFID07150  number  07150_Structured_Securities_Reference_Price_ex 

_ante 

680  MDF_F_MIFID07155  number  07155_Structured_Securities_Notional_Reference 

_Amount_ex_ante 

681  MDF_F_MIFID07160  date  07160_Ex_Ante_Costs_Reference_Date 

605  MDF_F_MIFID08010  number  08010_One-

off_cost_Structured_Securities_entry_cost_ex_po 

st 

682  MDF_F_MIFID08015  number  08015_Net_One-

off_cost_Structured_Securities_entry_cost_ex_po 

st 

606  MDF_F_MIFID08020  number  08020_One-

off_costs_Structured_Securities_exit_cost_ex_po 

st 

683  MDF_F_MIFID08025  number  08025_One-

off_cost_Financial_Instrument_entry_cost_acquir 

ed 

607  MDF_F_MIFID08030  number  08030_Financial_Instrument_Ongoing_costs_ex_ 

post 

608  MDF_F_MIFID08040  number  08040_Structured_Securities_Ongoing_costs_ex_ 

post_accumulated 

684  MDF_F_MIFID08045  number  08045_Financial_Instrument_Ongoing_Costs_Un 

derlying_Funds_UK 

685  MDF_F_MIFID08046  number  08046_Financial_Instrument_Gearing_costs_ex_ 

post_UK 

609  MDF_F_MIFID08050  number  08050_Financial_Instrument_Management_fee_e 

x_post 

610  MDF_F_MIFID08060  number  08060_Financial_Instrument_Distribution_fee_ex 

_post 

611  MDF_F_MIFID08070  number  08070_Financial_Instrument_Transaction_costs_ 

ex_post    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

612  MDF_F_MIFID08080  number  08080_Financial_Instrument_Incidental_costs_ex 

_post 

686  MDF_F_MIFID08085  number  08085_Financial_Instrument_Performance_Fee_c 

osts_ex_post 

613  MDF_F_MIFID08090  date  08090_Beginning_Of_Calculation_Period 

614  MDF_F_MIFID08100  date  08100_End_Of_Calculation_Period 

687  MDF_F_MIFID08110  number  08110_Structured_Securities_Reference_Price_ex 

_post 

688  MDF_F_MIFID08120  number  08120_Structured 

Securities_Notional_Reference_Amount 

327  MDF_F_MIN  number  19,7  The smallest number in a range of values 

310  MDF_F_MINADDITIONALAMOUNT  number 

229  MDF_F_MINORITYINTEREST  number  A balance sheet item: A non-current liability that 

represents the proportions of a company's 

subsidiaries owned by minority shareholders 

380  MDF_F_MINORITYINTERESTRES  number  19,7  An income statement item:  The part of the profit 

that belongs to subsidaries partly owned. Also 

know as non-controlling interest. 

307  MDF_F_MINSTARTAMOUNT  number 

308  MDF_F_MINSUBSCRIPTIONAMOUNT  number 

122  MDF_F_MINUSPAID  number  10,0  Total amount of decreased paid prices compared 

with yesterdays closing prices. 

692  MDF_F_MMO  bool  Indicates if this side and level of the orderbook 

contains a protected market maker order. 

524  MDF_F_MMT  string  14  MMT (Market Model Typology) 

304  MDF_F_MORNINGSTARRATING  number  1 Morningstar rating, from 5 (highest rating) to 1 

(lowest rating) 

394  MDF_F_N1  number  19,7  Placeholder for numerical values. The exact 

definition is dependent upon context. 

395  MDF_F_N2  number  19,7 

396  MDF_F_N3  number  19,7 

397  MDF_F_N4  number  19,7 

398  MDF_F_N5  number  19,7 

717  MDF_F_N6  number  19,7 

718  MDF_F_N7  number  19,7 

719  MDF_F_N8  number  19,7 

720  MDF_F_N9  number  19,7 

721  MDF_F_N10  number  19,7 

22  MDF_F_NAME  string  The name 

93  MDF_F_NAV  number  19,4  Net Asset Value. The price set on a fund's units by 

deducting liabilities from assets and dividing by 

the number of outstanding units. 

812  MDF_F_ND_EBITDA  number  Net Debt to EBITDA Ratio    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

813  MDF_F_ND_EBITDA_TTM  number  Net Debt to EBITDA Ratio (TTM) 

814  MDF_F_ND_EBITDA_LAST  number  Net Debt to EBITDA Ratio (Annualized) 

432  MDF_F_NETDIVIDEND  number  19,4  The net dividend price expressed in the 

instrument's trading currency 

139  MDF_F_NETFEEANDCOMINCOME  number  Net fee and commission income 

138  MDF_F_NETFININCOME  number  An income statement item: The income that a 

firm has after subtracting costs and expenses from 

the total revenue. Also known as Net Operating 

Income (NOI) if positive, and Net Operating Loss 

(NOL) if negative. 

137  MDF_F_NETINTERESTINCOME  number  Total interest income less total interest expense 

130  MDF_F_NETPROFIT  number  An income statement item: The gross revenue 

minus all expenses 

199  MDF_F_NETSALES  number  The operating revenues earned by a company 

when it sells it's products. Also knows as 

Revenue. 

73  MDF_F_NEWSBLOCKNUMBER  number  5,0  Number that uniquely identifies this news block 

within this news item. 

85  MDF_F_NEWSCODINGCOMPANY  list  Space separated list of the insref's of the 

companies this news item is coded for 

88  MDF_F_NEWSCODINGCOUNTRY 

621  MDF_F_NEWSCODINGIMPACT  number  5,0  The impact of the news item as determined by the 

news agency. Currently in the range of 0-3 and 

the value is usually set when the news item is 

created and never changed. 

167  MDF_F_NEWSCODINGISIN  string  Space separated list of ISIN codes this news item 

is coded for. 

89  MDF_F_NEWSCODINGORIGINAL  string  Internal use by Millistream 

439  MDF_F_NEWSCODINGREGULATORY  bool  Indicates whether the news item is a Regulatory 

news item or not. 

87  MDF_F_NEWSCODINGSUBJECT  uint  ● 0 – General News (Uncategorized) 

● 1 – Products 

● 2 – Annual Report 

● 3 – Interim Report 

● 4 – Decisions from General Meeting 

● 5 – Prospectus 

● 6 – Marketing 

● 7 – Earnings 

● 8 – Personnel Changes 

● 9 – Stock Activities / Corporate Actions 

● 10 – Newsletter 

● 11 – Notice to convene General Meeting 

620  MDF_F_NEWSCODINGTAGS  tabular  Specifies the tags for a news item, single column 

and each row defines a new tag for the same news 

item. 

For supported values please see the "News 

Format" documentation.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

86  MDF_F_NEWSCODINGTYPE  uint  ● 0 – News Flash 

● 1 – News Article 

● 2 – Press Release 

● 3 – Company Financial Calendar 

● 4 – Report 

● 5 – Market Commentary 

● 6 – Economic Calendar (Today) 

● 7 – Economic Calendar (This Week) 

● 8 – Systems Messages 

106  MDF_F_NEWSHARES  number  The number of new shares for each old share. For 

example for a split or new emission where the 

ratio is 'new:old' 

48  MDF_F_NEWSID  string  36  Unique id for the news id 

552  MDF_F_NEWSIDREPLACE  string  36  The unique news id that this news item replaces, 

either due to correction or amendment. 

115  MDF_F_NEWSISLASTBLOCK  bool  Indicates whether the news block is the last 

325  MDF_F_NEWSRANK  number  2,0  The rank of the news item, currently used by a 

single news source (Marknadskoll Direkt) and the 

rank is in the range of 1-10 

234  MDF_F_NIBL  number  A balance sheet item: Non-Interest-Bearing 

Liabilities 

110  MDF_F_NOMINALVALUE  number  The nominal value 

219  MDF_F_NONCURRENTASSET  number  A balance sheet item: An asset which is not easily 

convertible to cash or not expected to become 

cash within the next year 

440  MDF_F_NORMANAMOUNT  number  The Norman Amount is a calculated prognosis of 

the cumulative cost for investing 1000 monetary 

units per month for 10 consecutive years in a 

Mutual Fund. 

18  MDF_F_NUMASKORDERS  number  5,0  The number of ask orders on the current level 

422  MDF_F_NUMBEROFPREFSHARES  number  The number of issued preference shares 

104  MDF_F_NUMBEROFSHARES  number  The number of issued stem shares 

105  MDF_F_NUMBEROFSHARESDELTA  number  The change of the number of shares, can be 

negative if the number of shares is decreased. 

17  MDF_F_NUMBIDORDERS  number  5,0  The number of bid orders on the current level 

242  MDF_F_NUMEMPLOYEES  number  The number of employees at the company 

37  MDF_F_NUMTRADES  number  20,0  The number of executed trades during the current 

trading session 

367  MDF_F_OFFBOOKQUANTITY  number  20,0  The cumulative number of traded shares or 

contracts of shares for Off-Book trades. 

368  MDF_F_OFFBOOKTURNOVER  number  38,7  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency of trades 

for Off-Book trades. 

107  MDF_F_OLDSHARES  number  The number of old shares needed for each new 

share. I.e for a split or new emission where the 

ratio is 'new:old'. 

427  MDF_F_ONGOINGCHARGE  number  19,7  The Ongoing Charge represents the costs you can    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

reasonably expect to pay as an investor from one 

year to the next,  encompasses the fund’s 

professional fees, management fees, audit fees 

and custody fees. 

650  MDF_F_OM  number  Operating Margin (OM) 

651  MDF_F_OM_TTM  number  OM (TTM) 

652  MDF_F_OM_LAST  number  OM (Annualized) 

260  MDF_F_OPENINTEREST  number  13,6  The Derivative Open Interest 

39  MDF_F_OPENPRICE  number  19,7  First paid price during the current trading session 

77  MDF_F_OPENYIELD  number  First paid yield during the current trading session 

189  MDF_F_OPERATINGCASHFLOW  number  19,7  The cash generated from the operations of a 

company, generally defined as revenues less all 

operating expenses, but calculated through a 

series of adjustments to net income. 

615  MDF_F_OPERATINGMIC  string  4 Identifier for the Market place according to ISO 

10383 

136  MDF_F_ORDERBACKLOG  number  The estimated sales value of unfilled, confirmed 

customer orders for products and services at the 

time of the accounting period. 

695  MDF_F_ORDERID  number  20,0  A reference that in combination with insref 

uniquely identifies this order. 

696  MDF_F_ORDERIDSOURCE  A reference that uniquely identifies this order. The 

value comes directly from the exchange and 

depending upon exchange the value is only 

unique if combined with insref, side and date. 

Also do note that not all exchanges have such a 

identifier so presence of this field is not 

guaranteed. 

135  MDF_F_ORDERINTAKE  number  All orders which where legally concluded during 

the respective accounting period under review and 

also come into effect. 

16  MDF_F_ORDERLEVEL  number  5,0  Current level of the MBL order 

705  MDF_F_ORDERPARTICIPANT  string  4 Exchange member firm that made the MBO order. 

706  MDF_F_ORDERPRICE  number  Price of the MBO order. 

697  MDF_F_ORDERPRIORITY  number  20,0  The order with the lowest value of OrderPriority 

has the highest priority. 

704  MDF_F_ORDERSIDE  enum  Defines the order side for a MBO order: 

• 0 – Bid (Buy) 

• 1 – Ask (Sell/Offer) 

707  MDF_F_ORDERQUANTITY  number  Quantity of the MBO order. 

171  MDF_F_ORGNUM  string  12  A unique identifier for Swedish businesses 

assigned by Bolagsverket. 

https://foretagsfakta.bolagsverket.se/fpl-dft-ext-

web/home.seam 

619  MDF_F_ORGNUMNO  number  9 A unique identifier for Norwegian businesses    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

assigned by Brønnøysundregistrene. 

https://www.brreg.no/home/ 

221  MDF_F_OTHERCURRENTASSET  number  A balance sheet item: A balance sheet item that 

includes the value of non-cash assets due within 

one year 

379  MDF_F_OTHERFINANCIALEXPENSE  number  19,7  An income statement item: **TODO** 

377  MDF_F_OTHERFINANCIALINCOME  number  19,7  An income statement item: **TODO** 

223  MDF_F_OTHERRECEIVABLES  number  A balance sheet item: **TODO** 

410  MDF_F_OUTSTANDINGAMOUNT  number  16,6  The outstanding amount for example 

Premium/Lottery Bonds. 

361  MDF_F_PARTICIPATIONRATE  number  The percentage rate of the performance of the 

underlying asset which will be used to calculate 

the return when a product reaches its maturity. 

68  MDF_F_PASSWORD  string  Client password credential 

112  MDF_F_PAYMENTDATE  date  The date on which the dividend will be paid out 

by the company 

807  MDF_F_PBR  number  P/B Ratio 

808  MDF_F_PCF_TTM  number  P/CF Ratio (TTM) 

809  MDF_F_PCF_LAST  number  P/CF Ratio (Annualized) 

819  MDF_F_PEG  number  Price/Earnings-to-growth Ratio 

820  MDF_F_PEG_TTM  number  Price/Earnings-to-growth Ratio (TTM) 

821  MDF_F_PEG_LAST  number  Price/Earnings-to-growth Ratio (Annualized) 

176  MDF_F_PER_TTM  number  P/E Ratio (TTM) 

805  MDF_F_PER_LAST  number  P/E Ratio (Annualized) 

309  MDF_F_PERFORMANCEFEE  number 

109  MDF_F_PERIOD  string  19  For Fundamentals this is a normal date, i.e it can 

be YYYY, YYYY-Qx, YYYY-Hx, YYYY-Tx and 

YYYY-MM. 

For CorporatActions this is used as the 

Subscription Period and is in the: 'YYYYMMDD 

- YYYYMMDD' format. 

121  MDF_F_PLUSPAID  number  10,0  Total amount of increased paid prices compared 

to yesterdays closing prices. 

209  MDF_F_POSTALCODE  string  Postal Code 

653  MDF_F_PM  number  Profit Margin (PM) 

654  MDF_F_PM_TTM  number  PM (TTM) 

655  MDF_F_PM_LAST  number  PM (Annualized) 

129  MDF_F_PRETAXPROFIT  number  An income statement item: Earnings for the 

period before all tax adjustments. 

701  MDF_F_RHO  number  Black–Scholes Rho 

192  MDF_F_PRICETOADJUSTEDEQUITY  number  The current share price divided by the Adjusted 

Equity    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

191  MDF_F_PRICETOCASHFLOW  number  The current share price divided by the Operating 

Cash Flow 

348  MDF_F_PRICETYPE  uint  Defines how the instrument is traded. Valid 

values: 

● 0 – Price (Monetary) 

● 1 – Yield 

● 2 – Percentage 

● 3 – NAV 

● 4 – Points 

● 5 – Basis Points 

● 6 – Dirty (Percentage including accrued 

interest). 

428  MDF_F_PRICINGFREQUENCY  uint  Defines the pricing frequency. Valid values: 

● 0 – Annual 

● 1 – Semi-Annual 

● 2 – Quarterly 

● 3 – Monthly 

● 4 – Weekly 

● 5 – Daily 

738  MDF_F_PRIIP00001  string  3 00001_EPT_Version. Valid values: 

● V10 – EPTv1.0 

● V20 – EPTv2.0 

739  MDF_F_PRIIP00002  string  255  00002_EPT_Producer_Name 

740  MDF_F_PRIIP00004  string  255  00004_EPT_Producer_Email 

741  MDF_F_PRIIP00005  string  19  00005_File_Generation_Date_And_Time 

742  MDF_F_PRIIP00006  string  1 00006_EPT_Data_Reporting_Narratives. Valid 

values: 

● Y – Yes 

● N – No 

743  MDF_F_PRIIP00007  string  1 00007_EPT_Data_Reporting_Costs. Valid values: 

● Y – Yes 

● N – No 

744  MDF_F_PRIIP00008  string  1 00008_EPT_Data_Reporting_Additional_Require 

ments_German_MOPs. Valid values: 

● Y – Yes 

● N – No 

745  MDF_F_PRIIP00009  string  1 00009_EPT_Additional_Information_Structured_ 

Products. Valid values: 

● Y – Yes 

● N – No 

444  MDF_F_PRIIP00010  string  255  00010_Portfolio_Issuer_Name 

746  MDF_F_PRIIP00015  string  255  00015_Portfolio_Manufacturer_Group_Name 

747  MDF_F_PRIIP00016  string  20  00016_Portfolio_Manufacturer_LEI 

748  MDF_F_PRIIP00017  string  255  00017_Portfolio_Manufacturer_Email 

445  MDF_F_PRIIP00020  string  255  00020_Portfolio_Guarantor_Name 

446  MDF_F_PRIIP00030  string  255  00030_Portfolio_Identifying_Data 

447  MDF_F_PRIIP00040  uint  00040_Type_Of_Identification_Code_For_The_F 

und_Share_Or_Portfolio. Valid values:    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● 1 – ISIN 

● 2 – CUSIP 

● 3 – SEDOL 

● 4 – WKN 

● 5 – Bloomberg Ticker 

● 6 – BBGID 

● 7 – Reuters RIC 

● 8 – FIGI 

● 9 – Other code by members of the 

Association of National Numbering 

Agencies 

● 99 – Code attributed by the undertaking 

448  MDF_F_PRIIP00050  string  255  00050_Portfolio_Name 

449  MDF_F_PRIIP00060  string  3 00060_Share_Class_Currency according to ISO 

4217 

749  MDF_F_PRIIP00075  string  00075_PRIIPs_KID_Web_Address 

451  MDF_F_PRIIP00080  number  1 00080_Portfolio_PRIIPS_Category. Valid values: 

1 to 4 

452  MDF_F_PRIIP00090  string  4 00090_Fund_CIC_code 

453  MDF_F_PRIIP00100  string  1 00100_EOS_portfolio. Valid values: 

● Y – Yes 

● N – No 

750  MDF_F_PRIIP00110  string  1 00110_Is_An_Autocallable_Product. Valid 

values: 

● Y – Yes 

● N – No 

454  MDF_F_PRIIP01010  uint  01010_Valuation_Frequency. Valid values: 

● 0 – Other than 

● 1 – Annual 

● 2 – Biannual 

● 4 – Quarterly 

● 12 – Monthly 

● 24 – Bimonthly 

● 52 – Weekly 

● 104 – Biweekly 

● 252 – Daily 

455  MDF_F_PRIIP01020  number  01020_Portfolio_VEV_Reference 

456  MDF_F_PRIIP01030  string  1 01030_IS_Flexible. Valid values: 

● Y – Yes 

● N – No 

457  MDF_F_PRIIP01040  number  01040_Flex_VEV_Historical 

458  MDF_F_PRIIP01050  number  01050_Flex_VEV_Ref_Asset_Allocation 

459  MDF_F_PRIIP01060  string  1 01060_IS_Risk_Limit_Relevant. Valid values: 

● Y – Yes 

● N – No 

460  MDF_F_PRIIP01070  number  01070_Flex_VEV_Risk_Limit 

461  MDF_F_PRIIP01080  string  1 01080_Existing_Credit_Risk. Valid values: 

● Y – Yes 

● N – No    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

462  MDF_F_PRIIP01090  number  1 01090_SRI. Valid values: 1-7 

751  MDF_F_PRIIP01095  string  1 01095_IS_SRI_Adjusted. Valid values: 

● Y – Yes 

● N – No 

463  MDF_F_PRIIP01100  number  1 01100_MRM. Valid values: 1-7 

464  MDF_F_PRIIP01110  number  1 01110_CRM. Valid values: 1-6 

465  MDF_F_PRIIP01120  number  01120_Recommended_Holding_Period 

752  MDF_F_PRIIP01125  string  1 01125_Has_A_Contractual_Maturity_Date. Valid 

values: 

● Y – Yes 

● N – No 

467  MDF_F_PRIIP01140  string  1 01140_Liquidity_Risk. Valid values: 

● M – Material liquidity risk 

● I – Illiquid 

● L – No liquidity issue 

468  MDF_F_PRIIP02010  number  02010_Portfolio_return_unfavorable_scenario_1_ 

year 

469  MDF_F_PRIIP02020  number  02020_Portfolio_return_unfavorable_scenario_ha 

lf_RHP 

470  MDF_F_PRIIP02030  number  02030_Portfolio_return_unfavorable_scenario_R 

HP 

753  MDF_F_PRIIP02032  string  1 02032_Autocall_Applied_Unfavourable_Scenario 

. Valid values: 

● Y – Yes 

● N – No 

754  MDF_F_PRIIP02035  date  02035_Autocall_Date_Unfavourable_Scenario 

471  MDF_F_PRIIP02040  number  02040_Portfolio_return_moderate_scenario_1_ye 

ar 

472  MDF_F_PRIIP02050  number  02050_Portfolio_return_moderate_scenario_half_ 

RHP 

473  MDF_F_PRIIP02060  number  02060_Portfolio_return_moderate_scenario_RHP 

755  MDF_F_PRIIP02062  string  1 02062_Autocall_Applied_Moderate_Scenario. 

Valid values: 

● Y – Yes 

● N – No 

756  MDF_F_PRIIP02065  date  02065_Autocall_Date_Moderate_Scenario 

474  MDF_F_PRIIP02070  number  02070_Portfolio_return_favorable_scenario_1_ye 

ar 

475  MDF_F_PRIIP02080  number  02080_Portfolio_return_favorable_scenario_half_ 

RHP 

476  MDF_F_PRIIP02090  number  02090_Portfolio_return favorable scenario_RHP 

757  MDF_F_PRIIP02092  string  1 02092_Autocall_Applied_Favourable_Scenario. 

Valid values: 

● Y – Yes 

● N – No 

758  MDF_F_PRIIP02095  date  02095_Autocall_Date_Favourable_Scenario    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

477  MDF_F_PRIIP02100  number  02100_Portfolio_return_stress_scenario_1_year 

478  MDF_F_PRIIP02110  number  02110_Portfolio_return_stress_scenario_half_RH 

P

479  MDF_F_PRIIP02120  number  02120_Portfolio_return_stress_scenario_RHP 

759  MDF_F_PRIIP02122  string  1 02122_Autocall_Applied_Stress_Scenario. Valid 

values: 

● Y – Yes 

● N – No 

760  MDF_F_PRIIP02125  date  02125_Autocall_Date_Stress_Scenario 

480  MDF_F_PRIIP02130  number  02130_Portfolio_number_of_observed_return_M 

0

481  MDF_F_PRIIP02140  number  02140_Portfolio_mean_observed_returns_M1 

482  MDF_F_PRIIP02150  number  02150_Portfolio_observed_Sigma 

483  MDF_F_PRIIP02160  number  02160_Portfolio_observed_Skewness 

484  MDF_F_PRIIP02170  number  02170_Portfolio_observed_Excess_Kurtosis 

485  MDF_F_PRIIP02180  number  02180_Portfolio_observed_Stressed_Volatility 

761  MDF_F_PRIIP02185  string  1 02185_Portfolio_Past_Performance_Disclosure_ 

Required. Valid values: 

● Y – Yes 

● N – No 

762  MDF_F_PRIIP02190  string  02190_Past_Performance_Link 

763  MDF_F_PRIIP02200  string  02200_Previous_Performance_Scenarios_Calcula 

tion_Link 

764  MDF_F_PRIIP02210  number  2 02210_Past_Performance_Number_Of_Years. 

Valid values: 0-10 

765  MDF_F_PRIIP02220  number  02220_Reference_Invested_Amount 

486  MDF_F_PRIIP03010  number  03010_One_off_cost_Portfolio_entry_cost 

487  MDF_F_PRIIP03015  number  03015_One_off_cost_Portfolio_entry_cost_Acqui 

red 

488  MDF_F_PRIIP03020  number  03020_One_off_costs_Portfolio_exit_cost_at_RH 

P

489  MDF_F_PRIIP03030  number  03030_One_off_costs_Portfolio_exit_cost_at_1_ 

year 

490  MDF_F_PRIIP03040  number  03040_One_off_costs_Portfolio_exit_cost_at_hal 

f_RHP 

491  MDF_F_PRIIP03050  string  1 03050_One_off_costs_Portfolio_sliding_exit_cos 

t_Indicator. Valid values: 

● Y – Yes 

● N – No 

492  MDF_F_PRIIP03060  number  03060_Ongoing_costs_Portfolio_other_costs 

493  MDF_F_PRIIP03070  number  03070_Ongoing_costs_Portfolio_management_co 

sts 

494  MDF_F_PRIIP03080  number  03080_Ongoing_costs_Portfolio_transaction_cost 

s

495  MDF_F_PRIIP03090  string  1 03090_Existing_performance_fees. Valid values:    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● Y – Yes 

● N – No 

496  MDF_F_PRIIP03095  number  03095_Incidental_costs_Portfolio_performance_f 

ees 

497  MDF_F_PRIIP03100  string  1 03100_Existing_carried_interest_fees. Valid 

values: 

● Y – Yes 

● N – No 

498  MDF_F_PRIIP03105  number  03105_Incidental_costs_Portfolio_carried_interes 

t

500  MDF_F_PRIIP04020  string  1 04020_Comprehension_Alert_Portfolio. Valid 

values: 

● Y – Yes 

● N – No 

501  MDF_F_PRIIP04030  string  4000  04030_Intended_target_market_retail_investor_P 

ortfolio 

502  MDF_F_PRIIP04040  string  8000  04040_Investment_objective_Portfolio 

503  MDF_F_PRIIP04050  string  300  04050_Risk_narrative_Portfolio 

504  MDF_F_PRIIP04060  string  200  04060_Other_materially_relevant_risk_narrative_ 

Portfolio 

505  MDF_F_PRIIP04070  string  300  04070_Type_of_underlying_Investment_Option 

506  MDF_F_PRIIP04080  string  1 04080_Capital_Guarantee. Valid values: 

● Y – Yes 

● N – No 

507  MDF_F_PRIIP04081  number  04081_Capital_Guarantee_Level 

508  MDF_F_PRIIP04082  string  300  04082_Capital_Guarantee_Limitations 

509  MDF_F_PRIIP04083  date  04083_Capital_Guarantee_Early_Exit_Condition 

s

510  MDF_F_PRIIP04084  string  2500  04084_Capital_guarantee_Portfolio 

511  MDF_F_PRIIP04085  number  04085_Possible_maximum_loss_Portfolio 

766  MDF_F_PRIIP04086  string  300  04086_Description_Past_Interval_Unfavourable_ 

Scenario 

767  MDF_F_PRIIP04087  string  300  04087_Description_Past_Interval_Moderate_Sce 

nario 

768  MDF_F_PRIIP04088  string  300  04088_Description_Past_Interval_Favourable_Sc 

enario 

769  MDF_F_PRIIP04089  string  1 04089_Was_Benchmark_Used_Performance_Cal 

culation. Valid values: 

● Y – Yes 

● N – No 

512  MDF_F_PRIIP04090  string  300  04090_Portfolio_Performance_Fees_Narrative 

513  MDF_F_PRIIP04100  string  300  04100_Portolio_Carried_Interest_Narrative 

514  MDF_F_PRIIP04110  string  04110_Other_comment 

770  MDF_F_PRIIP04120  string  300  04120_One_Off_Cost_Portfolio_Entry_Cost_Des 

cription    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

771  MDF_F_PRIIP04130  string  300  04130_One_Off_Cost_Portfolio_Exit_Cost_Desc 

ription 

772  MDF_F_PRIIP04140  string  150  04140_Ongoing_Costs_Portfolio_Management_ 

Costs_Description 

773  MDF_F_PRIIP04150  string  1 04150_Do_Costs_Depend_On_Invested_Amount 

. Valid values: 

● Y – Yes 

● N – No 

774  MDF_F_PRIIP04160  string  150  04160_Cost_Dependence_Explanation 

515  MDF_F_PRIIP05010  string  1 05010_PRIIP_data_delivery. Valid values: 

● Y – Yes 

● N – No 

516  MDF_F_PRIIP05020  string  1 05020_UCITS_data_delivery. Valid values: 

● Y – Yes 

● N – No 

517  MDF_F_PRIIP05030  number  1 05030_Portfolio_UCITS_SRRI. Valid values: 1-7 

518  MDF_F_PRIIP05040  number  05040_Portfolio_UCITS_Vol 

519  MDF_F_PRIIP05050  number  05050_Ongoing_costs_Portfolio_other_costs_UC 

ITS 

520  MDF_F_PRIIP05060  number  05060_Ongoing_costs_Portfolio_transaction_cost 

s

521  MDF_F_PRIIP05065  string  255  05065_Transactions_costs_methodology 

522  MDF_F_PRIIP05070  number  05070_Incidental_costs_Portfolio_performance_f 

ees_UCITS 

523  MDF_F_PRIIP05080  number  05080_Incidental_costs_Portfolio_carried_interes 

t_UCITS 

775  MDF_F_PRIIP06005  date  06005_German_MOPs_Reference_Date 

528  MDF_F_PRIIP06010  number  06010_Bonds_Weight 

529  MDF_F_PRIIP06020  number  06020_Annualized_Return_Volatility 

530  MDF_F_PRIIP06030  number  06030_Duration_Bonds 

531  MDF_F_PRIIP06040  string  1 06040_Existing_Capital_Preservation. Valid 

values: 

● Y – Yes 

● N – No 

532  MDF_F_PRIIP06050  number  06050_Capital_Preservation_Level 

533  MDF_F_PRIIP06060  string  10  06060_Time_Interval_Maximum_Loss. Valid 

values: 

● 1 – Annual 

● 2 – Biannual 

● 4 – Quarterly 

● 12 – Monthly 

● 24 – Bimonthly 

● 52 – Weekly 

● 104 – Biweekly 

● 252 – Daily 

● YYYY-MM-DD – Fixed date 

534  MDF_F_PRIIP06070  string  1 06070_Uses_PI. Valid values:    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● Y – Yes 

● N – No 

535  MDF_F_PRIIP06080  number  06080_Multiplier_PI 

776  MDF_F_PRIIP07005  date  07005_First_Possible_Call_Date 

536  MDF_F_PRIIP07010  number  07010_Total_cost_1_year 

537  MDF_F_PRIIP07020  number  07020_RIY_1_year 

538  MDF_F_PRIIP07030  number  07030_Total_cost_half_RHP 

539  MDF_F_PRIIP07040  number  07040_RIY_half_RHP 

540  MDF_F_PRIIP07050  number  07050_Total_cost_RHP 

541  MDF_F_PRIIP07060  number  07060_RIY_RHP 

542  MDF_F_PRIIP07070  number  07070_One_off_costs_Portfolio_entry_cost_RIY 

543  MDF_F_PRIIP07080  number  07080_One_off_costs_Portfolio_exit_cost_RIY 

544  MDF_F_PRIIP07090  number  07090_Ongoing_costs_Portfolio_transaction_cost 

s_RIY 

545  MDF_F_PRIIP07100  number  07100_Ongoing_costs_Other_ongoing_costs_RI 

Y

546  MDF_F_PRIIP07110  number  07110_Incidental_costs_Portfolio_performance_f 

ees_RIY 

547  MDF_F_PRIIP07120  number  07120_Incidental_costs_Portfolio_carried_interes 

ts_RIY 

320  MDF_F_PRIMARYMARKETPLACE  insref  Insref of the primary marketplace for the 

company. 

822  MDF_F_PRIMARYSHARE  Insref  Insref of the primary share for the company. 

142  MDF_F_PROFITBEFOREWACL  number  Profit before write-offs and credit losses 

433  MDF_F_PRODUCTCODE  string  20  The product code for derivatives 

145  MDF_F_PROPERTYMGMTRESULT  number  Property management result 

257  MDF_F_PROSPECTUS  string  65535  URL to the prospectus 

230  MDF_F_PROVISIONS  number  A balance sheet item: **TODO** 

177  MDF_F_PSR_TTM  number  P/S Ratio (TTM) 

806  MDF_F_PSR_LAST  number  P/S Ratio (Annualized) 

306  MDF_F_PURCHASEFEE  number  19,7 

10  MDF_F_QUANTITY  number  20,8  The cumulative number of traded shares or 

contracts of shares 

32  MDF_F_QUOTECURRENCY  string  4 The second currency in a currency pair 

434  MDF_F_QUOTINGTYPE  uint  Defines how prices are determined. Valid values: 

● 0 – Order Driven Market (Automatch) 

● 1 – Quote Driven Market (OTC) 

● 2 – Indicative / Calculated 

111  MDF_F_RECORDDATE  date  The date established by an issuer of a security for 

the purpose of determining the holders who are 

entitled to receive a dividend or distribution. 

146  MDF_F_REALIZEDCHGPROP  number  Realized changes in value of properties    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

187  MDF_F_REDEMPTIONPRICE  number  The price with which the instruments shares will 

be redeemed. 

144  MDF_F_RENTALINCOME  number  Income received from rental properties 

174  MDF_F_RETURNONEQUITY  number  Return On Equity (ROE) measures the rate of 

return on the ownership interest of the common 

stock owner. 

52  MDF_F_REQUESTCLASS  uint  Defines the request class. Valid values: 

● 0 – News Headlines 

● 1 – Quotes 

● 2 – Trades 

● 3 – Orders 

● 4 – Basic Data 

● 5 – Price History 

● 6 – Fields Reference 

● 7 – Request Insrefs 

● 8 – News Content 

● 9 – Corporate Actions 

● 10 – Trade State 

● 11 – Fundamentals 

● 12 – Performance 

● 13 – Key Ratios 

● 14 – Estimates 

● 15 – Estimates History 

● 16 – Net Order Imbalance Indicator 

● 17 – Localization (L10N) 

● 18 – Company Information 

● 19 – Company Information History 

● 20 - PRIIP 

● 21 - MIFID 

● 22 - MIFIDHISTORY 

● 23 - Mappings 

It can also contain the single character "*" which 

means "all Request Classes that I'm entitled for", 

which works as a wild card request. 

49  MDF_F_REQUESTID  <any>  If present in a client request message, the value of 

this field will be sent with every image response 

and a Request Finished message will be sent 

when the image request has been completed in 

full. 

50  MDF_F_REQUESTSTATUS  uint  Status of the request. Valid values: 

● 100 – The request succeeded 

● 101 – The request was invalid 

● 102 – dbs-node is unavailable 

● 103 – Internal server error 

51  MDF_F_REQUESTTYPE  uint  Defines the request type. For  MDF_RC_INSREF 

requests, this is the number of insrefs wanted. 

Valid values: 

● 1 – Image request 

● 2 – Stream request 

● 3 – Full request 

644  MDF_F_ROA  number  Return On Assets (ROA) 

645  MDF_F_ROA_TTM  number  ROA (TTM)    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

646  MDF_F_ROA_LAST  number  ROA (Annualized) 

641  MDF_F_ROE  number  Return On Equity (ROE) 

642  MDF_F_ROE_TTM  number  ROE (TTM) 

643  MDF_F_ROE_LAST  number  ROE (Annualized) 

816  MDF_F_ROIC  number  Return on Invested Capital 

817  MDF_F_ROIC_TTM  number  Return on Invested Capital (TTM) 

818  MDF_F_ROIC_LAST  number  Return on Invested Capital (Annualized) 

801  MDF_F_RSI14  number  Relative Strength Index over 14 days. 

98  MDF_F_S1  string  255  Placeholder for strings. The exact definition is 

dependent upon context. 

179  MDF_F_S2  string  255 

180  MDF_F_S3  string  255 

181  MDF_F_S4  string  255 

182  MDF_F_S5  string  255 

389  MDF_F_S6  string  255 

390  MDF_F_S7  string  255 

391  MDF_F_S8  string  255 

392  MDF_F_S9  string  255 

393  MDF_F_S10  string  255 

442  MDF_F_S11  string  255 

713  MDF_F_S12  string  255 

714  MDF_F_S13  string  255 

715  MDF_F_S14  string  255 

716  MDF_F_S15  string  255 

127  MDF_F_SALES  number  An income statement item: Total sales revenue. 

The income generated by the company selling it's 

products and services. 

305  MDF_F_SALESFEE  number  19,7 

188  MDF_F_SECTOR  list  List of links to classification sector instruments 

the instrument belongs to. 

527  MDF_F_SECTORMEMBERS  list  List of the insrefs that are connected with this 

sector instrument. 

409  MDF_F_SEQUENCE  number  10,0  Defines the order of events for multiple events on 

the same date. 

118  MDF_F_SERVERDATE  Date on the server at logon time 

116  MDF_F_SERVERNAME  string  20  Name of the server 

117  MDF_F_SERVERTIME  time  Time on the server at logon time 

385  MDF_F_SETTLEMENTPRICE  number  Settlement price refers to the price at which an 

asset closes or of which a derivatives contract will 

reference at the end of each trading day and/or 

upon its expiration.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

340  MDF_F_SETTLEMENTTYPE  uint  Defines the Settlement Type. Valid values: 

● 1 – Cash 

● 2 – Physical 

● 3 – Any 

804  MDF_F_SHARECLASS  string  4 Classification of common stock for companies 

that has more than one common stock. Different 

share classes within the same entity typically 

confer different rights on their owners. 

303  MDF_F_SHARPERATION3Y  number  19,7 

228  MDF_F_SHEQUITY  number  A balance sheet item: Shareholders Equity. A 

firm's total assets minus its total liabilities 

322  MDF_F_SHORTDESCRIPTION  string  512  Company Description, short 

224  MDF_F_SHORTTERMINV  number  A balance sheet item: Any investments that a 

company has made that will expire within one 

year 

798  MDF_F_SMA20  number  Simple Moving Average over 20 days 

799  MDF_F_SMA50  number  Simple Moving Average over 50 days 

800  MDF_F_SMA200  number  Simple Moving Average over 200 days 

97  MDF_F_SOURCE  string 

246  MDF_F_SOURCEID  string  32  The instrument identifier used by the marketplace 

to uniquely identify the instrument 

125  MDF_F_SPECIALCONDITION  bitfield  Specifies the special condition for the instrument, 

more than one condition can be active at a time. 

Valid values: 

● 1 – Under Observation 

● 2 – Knocked Out 

● 4 – Stressed Market Condition 

● 8 – Exceptional Market Condition 

● 16 – Underlying Not Quoted 

● 32 – Buy-Back 

● 64 – Excluding Dividend 

● 128 – Excluding Rights Issue 

● 256 – Excluding Split 

● 512 – Excluding Financial Reported 

636  MDF_F_SPS  number  Sales Per Share (SPS) 

637  MDF_F_SPS_TTM  number  SPS (TTM) 

638  MDF_F_SPS_LAST  number  SPS (Annualized) 

301  MDF_F_STANDARDDEVIATION3Y  number  19,7 

34  MDF_F_STRIKEDATE  date  The day on which an option or futures contract is 

no longer valid 

35  MDF_F_STRIKEPRICE  number  The stated price per unit for which the underlying 

instrument may be purchased (for a call) or sold 

(for a put) by the option holder upon exercise of 

the option contract. 

499  MDF_F_SUBMARKET  insref  Link to the Submarket instrument 

108  MDF_F_SUBSCRIPTIONPRICE  number  The subscription price 

21  MDF_F_SYMBOL  string  50  The symbol    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

733  MDF_F_SWINGFACTOR  number  The amount a fund’s NAV per share swings up or 

down after swing threshold is exceeded. In 

general the NAV is swung up for net subscription 

and swung down for net redemption. The given 

value is for Redemption of fund units. 

787  MDF_F_SWINGFACTORSUB  number  The amount a fund’s NAV per share swings up or 

down after swing threshold is exceeded. In 

general the NAV is swung up for net subscription 

and swung down for net redemption. The given 

value is for Subscription of fund units. 

734  MDF_F_SWINGMETHOD  uint  Defines the Pricing Swing Method. Valid values: 

● 1 – Full (the NAV is adjusted daily for 

the likely costs of redemptions, 

regardless of the amount of shareholder 

activity) 

● 2 – Partial (the adjustment is triggered 

only when net redemptions exceed some 

pre-determined threshold) 

211  MDF_F_TELEPHONE  string  40  Telephone number 

712  MDF_F_TENOR  string  5 Specifies the time to maturity of the instrument. 

Valid values: 

● 30 – 30 Days 

● 60 – 60 Days 

● 90 – 90 Days 

● 180 – 180 Days 

● 270 – 270 Days 

● 365 – 365 Days 

● 3M – 3 Months 

● 1Y – 1 Year 

● 2Y – 2 Years 

● 3Y – 3 Years 

● 4Y – 4 Years 

● 5Y – 5 Years 

● 6Y – 6 Years 

● 7Y – 7 Years 

● 8Y – 8 Years 

● 9Y – 9 Years 

● 10Y – 10 Years 

2 MDF_F_TEXTBODY  string  The news item text body 

702  MDF_F_THETA  number  Black–Scholes Theta 

347  MDF_F_TICKSIZES  tabular  Specifies the tick sizes for the tick table. Each 

row contains these columns: 

● Threshold 

● Increment 

346  MDF_F_TICKTABLE  insref  Link to the Tick Table instrument 

114  MDF_F_TID  number  19,7  Taxable Incomer per Distribution 

4 MDF_F_TIME  time  The event time 

95  MDF_F_TIS  number  19,7  Taxable Income per Share 

140  MDF_F_TOPERATINGEXPENSES  number  Total operating expenses 

141  MDF_F_TOPERATINGINCOME  number  Total operating income    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

227  MDF_F_TOTALASSETS  number  A balance sheet item: The sum of current and 

long-term assets owned by the company 

316  MDF_F_TOTALFEE  number 

235  MDF_F_TOTLIABILITIES  number  Total Liabilities is the total of all liabilities 

233  MDF_F_TOTSHEQLIABILITIES  number  A balance sheet item: Total Shareholders Equity 

and Liabilities. 

623  MDF_F_TRACKINGERROR  number  Tracking error is the divergence between the price 

behavior of a position or a portfolio and the price 

behavior of a benchmark. Tracking error is 

reported as a standard deviation percentage 

difference, which reports the difference between 

the return an investor receives and that of the 

benchmark he was attempting to imitate. 

436  MDF_F_TRADEAGREEMENTDATE  date  The date of the Agreement Time for off-book 

trades 

435  MDF_F_TRADEAGREEMENTTIME  time  The Agreement Time for off-book trades 

60  MDF_F_TRADEBUYER  string  64  Identifies the counterpart that bought the 

instrument 

72  MDF_F_TRADECANCELTIME  time  Time of when the trade was canceled 

15  MDF_F_TRADECODE  uint  Specifies the trade condition, valid values: 

● 1024 – Dark Pool 

● 512 – Delayed Dissemination 

● 256 – Odd Lot 

● 128 – Trade updates Last Price 

● 64 – Trade updates Quantity and 

Turnover 

● 32 – Trade updates Day High Price and 

Day Low Price 

● 16 – Trade Break (cancelled trade) 

● 8 – Correction 

● 4 – Off-Book 

● 2 – Outside Spread 

● 1 – Off-Hours 

30  MDF_F_TRADECURRENCY  string  4 The currency the instrument trades in 

315  MDF_F_TRADEDTHROUGHDATE  date  The last trading date for the instrument 

12  MDF_F_TRADEPRICE  number  20,8  Trade price 

13  MDF_F_TRADEQUANTITY  number  20,8  The number of shares or contracts traded 

14  MDF_F_TRADEREFERENCE  string  64  A reference that uniquely identifies this trade. The 

string comes directly from the exchange and for 

some exchanges the string is only unique if 

combined with insref. 

61  MDF_F_TRADESELLER  string  64  Identifies the counterpart that sold the instrument 

126  MDF_F_TRADESTATE  uint  Defines the current trade state. Valid values: 

● 0 – Closed 

● 1 – Pre Market Trading 

● 2 – Pre-Open (Order mngmt forbidden) 

● 3 – Call Auction (Opening) 

● 4 – Uncrossing 

● 5 – Continuous Trading    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

● 6 – Post Market Trading 

● 7 – Suspended 

● 8 – Halted 

● 9 – Dead (used by MDA and MWS) 

● 10 – Trading against fixed price 

● 11 – Call Auction (Closing) 

● 12 – Call Auction (Intraday) 

● 13 – Volatility Interruption/Auction 

● 14 – Closing Price Crossing (A trading 

session where orders will be matched at 

an already determined closing price) 

● 15 – Opening Auction Extension 

● 16 – Closing Auction Extension 

● 17 – Trading Pause Static 

● 18 – Trading Pause Dynamic 

● 19 – Pre-Market Trading 

● 20 – After-Market Trading 

● 21 – Static Price Collar Reached 

● 22 – Post-market Crossing 

● 23 – Post Close 

803  MDF_F_TRADESTATEACTIONS  bitfield  Specifies the allowed actions during the current 

trade state, unset bits are disallowed and set bits 

are allowed. Valid values: 

● 1 – Order Add 

● 2 – Order Modify 

● 4 – Order Cancel 

● 8 – Automatch 

● 16 – Off-Book Reporting 

● 32 – Manual Trade 

● 64 – Trade Modify 

● 128 – Trade Cancel 

36  MDF_F_TRADETIME  time  Execution time of the trade 

71  MDF_F_TRADETYPE  string  10  The type of the trade as reported by the market 

place. 

201  MDF_F_TRADEYIELD  number  13,6  Trade Yield 

11  MDF_F_TURNOVER  number  38,7  The cumulative amount traded (e.g. price * 

quantity), expressed in units of currency. 

292  MDF_F_UCITS  uint  Defines the compliance level with the 

Undertakings for Collective Investments in 

Transferable Securities directive. 

NULL indicates no compliance, '1' indicates 

compliance with UCITS I, '2' with UCITS II etc 

120  MDF_F_UNCHANGEDPAID  number  10,0  Total amount of unchanged paid prices compared 

to yesterdays closing prices. 

66  MDF_F_UNDERLYINGID  tabular  Specifices the underlying instruments for a 

instrument. Each row contains these columns: 

● ISIN (matches the value in 

MDF_F_ISIN of the underlying 

instrument) 

● currency (optional) 

147  MDF_F_UNREALIZEDCHGPROP  number  Unrealized change in value of properties 

67  MDF_F_USERNAME  string  Client user name credential    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

703  MDF_F_VEGA  number  Black–Scholes Vega 

438  MDF_F_VOLUMEDIMENSION  uint  Defines the volume dimension. Valid values: 

● 0 – Quantity 

● 1 – Nominal 

341  MDF_F_VOTINGPOWER  number  3 The number of votes per share 

202  MDF_F_VOTINGPOWERPRC  number  5,2  The voting power in percentage controlled by the 

major holder 

123  MDF_F_VWAP  number  19,7  Volume Weighted Average Price 

170  MDF_F_WEBSITE  string  Link to the company web site 

291  MDF_F_WKN  string  6 The Werpapierkennummer as assigned by WM-

Datenservice, the NNA for Germany 

618  MDF_F_YTUNNUS  string  9 Y-Tunnus/FO-Nummer is a unique identifier 

assigned to Finnish businesses by the Finnish 

Patent and Registration Office and the Finnish 

Tax Administration. 

https://tietopalvelu.ytj.fi/yrityshaku.aspx? 

kielikoodi=3 

# Changelog 

2025-07-04  Added MDF_F_PRIMARYSHARE. 

2025-05-05  Added MDF_F_PER_LAST, MDF_F_PSR_LAST, MDF_F_PBR, MDF_F_PCF_TTM, 

MDF_F_PCF_LAST, MDF_F_DER, MDF_F_DER_LAST, MDF_F_ND_EBITDA, 

MDF_F_ND_EBITDA_TTM, MDF_F_ND_EBITDA_LAST, MDF_F_DPR, MDF_F_ROIC, 

MDF_F_ROIC_TTM, MDF_F_ROIC_LAST, MDF_F_PEG, MDF_F_PEG_TTM, 

MDF_F_PEG_LAST, MDF_F_DPS, MDF_F_CFPS, MDF_F_CFPS_TTM, 

MDF_F_CFPS_LAST, MDF_F_EPS_TTM, MDF_F_EPS_LAST, MDF_F_SPS, 

MDF_F_SPS_TTM, MDF_F_SPS_LAST, MDF_F_BVPS, MDF_F_BVPS_LAST, 

MDF_F_ROE, MDF_F_ROE_TTM, MDF_F_ROE_LAST, MDF_F_ROA, 

MDF_F_ROA_TTM, MDF_F_ROA_LAST, MDF_F_GM, MDF_F_GM_TTM, 

MDF_F_GM_LAST, MDF_F_OM, MDF_F_OM_TTM, MDF_F_OM_LAST, MDF_F_PM, 

MDF_F_PM_TTM, MDF_F_PM_LAST. 

2025-03-18  Extended MDF_F_CLOSEPRICETYPE. 

2025-01-02  Extended MDF_F_LOGOFFREASON. 

2024-12-10  Extended MDF_F_SPECIALCONDITION. 

2024-11-18  Extended MDF_F_INSTRUMENTSUBTYPE. 

2024-11-06  Extended MDF_F_IMBALANCEDIRECTION 

2024-07-10  Extended MDF_F_INSTRUMENTSUBTYPE. 

2024-05-30  Extended MDF_F_INSTRUMENTSUBTYPE. 

2024-05-19  Extended MDF_F_REQUESTSTATUS. 

2024-02-07  Added MDF_F_SHARECLASS. 

2023-12-05  Added MDF_F_EVENTSTATUS. 

2023-10-16  Added MDF_F_TRADESTATEACTIONS.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2023-07-21  Added MDF_F_SMA20, MDF_F_SMA50, MDF_F_SMA200, MDF_F_RSI14 and 

MDF_F_MACD. 

2023-03-31  Extended MDF_F_INSTRUMENTSUBTYPE. 

2023-03-27  Extended MDF_M_PRICETYPE. 

2023-02-10  Added MDF_F_AVGTURNOVER1W, MDF_F_AVGTURNOVER1M, 

MDF_F_AVGTURNOVER3M, MDF_F_AVGTURNOVER1Y and 

MDF_F_AVGTURNOVERYTD. 

2023-01-31  Added MDF_F_APPLICABLENAV and MDF_F_FUNDCUTOFFTIME. 

2023-01-26  Added MDF_F_VOTINGPOWER and MDF_F_LASTMOD. 

2022-12-20  Extended MDF_M_DERIVATIVEINDICATOR. 

2022-11-25  Extended MDF_M_SPECIALCONDITION. 

2022-11-17  Added MDF_F_SETTLEMENTPRICE, MDF_F_CLOSEPRICE4Y, 

MDF_F_CLOSEPRICE6Y, MDF_F_CLOSEPRICE7Y, MDF_F_CLOSEPRICE8Y, 

MDF_F_CLOSEPRICE9Y, MDF_CLOSEYIELD4Y, MDF_F_CLOSEYIELD6Y, 

MDF_F_CLOSEYIELD7Y, MDF_F_CLOSEYIELD8Y, MDF_F_CLOSEYIELD9Y and 

MDF_F_CLEARING. 

Extended MDF_F_CASUBTYPE. 

2022-09-13  Added MDF_F_SWINGFACTORSUB. 

2022-06-21  Added the EPTv2.0 fields. 

2022-06-10  Extended MDF_M_INSTRUMENTSUBTYPE. 

2022-04-29  Added MDF_F_CLOSEPRICEDATE and MDF_F_CLOSEPRICE1DDATE. 

2022-04-10  Extended MDF_F_TRADESTATE and MDF_F_CROSSTYPE. 

2022-03-30  Extended MDF_F_EXPIRATIONTYPE. 

2022-03-28  Extended MDF_F_TRADESTATE. 

2022-01-26  Added MDF_F_INCOMEPROPMAN and MDF_M_QUOTEEX. 

2021-12-09  Extended MDF_M_INSTRUMENTSUBTYPE. 

2021-11-22  Added MDF_F_SWINGFACTOR and MDF_F_SWINGMETHOD. 

2021-11-01  Added MDF_F_COMBOLEGS. 

2021-09-22  Extended MDF_M_CASUBTYPE. 

2021-09-17  Extended MDF_M_TENOR. 

2021-07-21  Added MDF_F_S12, MDF_F_S13, MDF_F_S14, MDF_F_S15, MDF_F_N6, 

MDF_F_N7, MDF_F_N8, MDF_F_N9, MDF_F_N10, MDF_F_I6, MDF_F_I7, 

MDF_F_I8, MDF_F_I9, MDF_F_I10, MDF_F_INSREF1, MDF_F_INSREF2, 

MDF_F_INSREF3, MDF_F_INSREF4 and MDF_F_INSREF5. 

2021-04-28  Extended MDF_M_INSTRUMENTSUBTYPE. 

2021-01-14  Extended MDF_F_INSTRUMENTTYPE. Added MDF_F_TENOR. 

2020-11-24  Added MDF_M_QUOTEBBO. 

2020-11-23  Added MDF_F_EXPIRATIONTYPE. 

2020-11-19  Added MDF_F_DAYCOUNTCONVENTION. 

2020-11-13  Extended MDF_F_PRICETYPE. Added MDF_F_IVBID and MDF_F_IVASK. 

2020-10-16  Added MDF_F_ORDERSIDE, MDF_F_ORDERPARTICIPANT, MDF_F_ORDERPRICE    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

and MDF_F_ORDERQUANTITY. 

2020-10-09  Added MDF_F_IV, MDF_F_DELTA, MDF_F_GAMMA, MDF_F_RHO, MDF_F_THETA 

and MDF_F_VEGA. 

2020-09-19  Extended MDF_F_EXERCISETYPE. 

2020-08-11  Added MDF_F_ORDERID, MDF_F_ORDERIDSOURCE and MDF_F_ORDERPRIORITY. 

2020-04-09  Extended MDF_F_SPECIALCONDITION. 

2020-03-18  Extended MDF_F_CASUBTYPE. 

2020-03-04  Extended MDF_F_INSTRUMENTSUBTYPE. 

2020-03-03  Added MDF_F_COUPONFREQUENCY. 

2020-01-16  Added MDF_F_FIGISECURITYTYPE. 

2019-11-27  Changed MDF_F_CASUBTYPE for calendar events from “annual” to “year end”. 

2019-09-23  Added MDF_F_FIGI, MDF_F_FIGICOMPOSITE, MDF_F_FIGISHARECLASS and 

MDF_F_MMO. 

2019-10-22  Extended MDF_F_NEWSCODINGTYPE, MDF_F_INSTRUMENTSUBTYPE. 

2019-09-23  Added MDF_F_MIFID00001, MDF_F_MIFID00005, MDF_F_MIFID00006, 

MDF_F_MIFID00007, MDF_F_MIFID00008, MDF_F_MIFID00045, 

MDF_F_MIFID00047, MDF_F_MIFID00067, MDF_F_MIFID00068, 

MDF_F_MIFID00069, MDF_F_MIFID00073, MDF_F_MIFID00074, 

MDF_F_MIFID00075, MDF_F_MIFID00085, MDF_F_MIFID00095, 

MDF_F_MIFID00096, MDF_F_MIFID00110, MDF_F_MIFID00120, 

MDF_F_MIFID00130, MDF_F_MIFID01000, MDF_F_MIFID05105, 

MDF_F_MIFID05115, MDF_F_MIFID07025, MDF_F_MIFID07101, 

MDF_F_MIFID07105, MDF_F_MIFID07150, MDF_F_MIFID07155, 

MDF_F_MIFID07160, MDF_F_MIFID08015, MDF_F_MIFID08025, 

MDF_F_MIFID08045, MDF_F_MIFID08046, MDF_F_MIFID08085, 

MDF_F_MIFID08110, MDF_F_MIFID08120. 

2019-08-06  Extended MDF_F_TRADESTATE. 

2019-07-31  Extended MDF_F_CROSSTYPE. 

2019-06-20  Extended MDF_F_INSREFLIST and MDF_F_REQUESTCLASS. 

2019-06-18  Clarified the format of MDF_F_PERIOD. 

2019-05-23  Modified the length of MDF_F_ISSUECURENCY, MDF_F_TRADECURRENCY, 

MDF_F_QUOTECURRENCY and MDF_F_BASECURRENCY from 3 to 4 to be able to 

support the new crypto currencies. 

Added MDF_F_SUBMARKET. 

Extended MDF_F_INSTRUMENTTYPE. 

Extended MDF_F_UNDERLYINGID. 

2019-03-20  Added MDF_F_SECTORMEMBERS and MDF_M_MAPPINGS. 

2019-01-07  Added MDF_F_HIGHPRICE3Y, MDF_F_HIGHPRICE5Y, MDF_F_HIGHPRICE10Y, 

MDF_F_LOWPRICE3Y, MDF_F_LOWPRICE5Y and MDF_F_LOWPRICE10Y. 

2018-12-18  Added MDF_F_ACTIVESHARE and MDF_F_TRACKINGERROR. 

2018-11-22  Added MDF_F_NEWSIDREPLACE. 

2018-11-20  Added MDF_M_MIFIDHISTORY. 

2018-10-23  Added MDF_F_NEWSCODINGIMPACT and MDF_F_NEWSCODINGTAGS. 

2018-08-23  Extended MDF_F_TRADESTATE.    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2018-07-17  Added MDF_F_CVR, MDF_F_KENNITALA, MDF_F_YTUNNUS and 

MDF_F_ORGNUMNO. 

2018-02-23  Added MDF_F_OPERATINGMIC. 

2018-01-08  Extended MDF_F_PRICETYPE. 

2017-11-13  Extended MDF_F_CASUBTYPE. 

2017-11-07  Changed MDF_F_UNDERLYINGID to ‘tabular’ from ‘string’. 

Rearranged the MDF_F_PRIIPxxxxx and MDF-F_MIFIDxxxxx fields. 

2017-11-04  Added MDF_F_FISN and MDF_F_LEI. 

2017-11-03  Added MDF_F_MMT. 

2017-11-02  Added 55 MDF_F_PRIIPxxxxx and 25 MDF_F_MIFIDxxxxx fields. 

2017-09-21  Changed description for MDF_F_CASHFLOWBWC. 

2017-08-17  Extended MDF_F_SPECIALCONDITION. 

2017-08-15  Extended MDF_F_TRADESTATE. 

Changed the “time” data type to support nanoseconds resolution as of 2018-01-01. 

2017-04-21  Extended MDF_F_INSTRUMENTSUBTYPE. 

2017-02-20  Added MDF_F_CIK. 

2016-11-18  Added MDF_F_NORMANAMOUNT, MDF_F_CSR and MDF_F_S11. 

2016-11-10  Extended the document with the Message References. 

2016-10-06  Added MDF_F_NEWSCODINGREGULATORY. 

2016-09-06  Extended MDF_F_TRADECODE and MDF_F_SPECIALCONDITION. 

2016-09-05  Extended MDF_F_INSTRUMENTSUBTYPE. 

2016-08-24  Added MDF_F_LATESTYEARENDREPORT, MDF_F_NETDIVIDEND 

and MDF_F_NUMBEROFPREFSHARES. 

2016-08-11  Extended MDF_F_TRADESTATE. 

2016-06-08  Added MDF_F_VOLUMEDIMENSION. 

2016-05-10  Extended MDF_F_TRADESTATE. 

2016-04-25  Extended MDF_F_REQUESTCLASS. 

2016-04-20  Added MDF_F_TRADEAGREEMENTDATE and MDF_F_TRADEAGREEMENTTIME. 

2016-02-03  Added MDF_F_PRODUCTCODE and MDF_F_QUOTINGTYPE. 

2015-12-08  Added MDF_F_CLOSEPRICETYPE and MDF_F_CLOSETRADEPRICE. 

Changed description for MDF_F_CLOSEPRICE. 

Extended MDF_F_CITYPE and MDF_F_CISUBTYPE. 

2015-11-19  Extended MDF_F_INSTRUMENTSUBTYPE. 

2015-11-17  Added MDF_F_MARKETOPENDAYS. 

Added the “bitfield” data type. 

2015-11-12  Added MDF_F_LEGALSTRUCTURE, MDF_F_ONGOINGCHARGE and 

MDF_F_PRICINGFREQUENCY. 

2015-09-21  Added MDF_F_SPECIALCONDITION 

2015-09-07  Added MDF_F_MARKETOPEN, MDF_F_MARKETCLOSE and 

MDF_F_MARKETEARLYCLOSE. 

2015-05-26  ExtendedMDF_F_NEWSCODINSUBJECT    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2014-12-11  Extended MDF_F_NEWSCODINGTYPE 

2014-12-05  Added MDF_F_OUTSTANDINGAMOUNT, MDF_F_INTERESTRATE and 

MDF_F_MARKETMAKER. 

2014-10-23  Extended MDF_F_DERIVATIVEINDICATOR. 

2014-09-23  Added MDF_F_Sx, MDF_F_Nx, MDF_F_Ix, MDF_F_CITYPE, MDF_F_CISUBTYPE and 

MDF_F_SEQUENCE. 

2014-08-28  Added MDF_F_ANNUALIZEDRETURN1Y, MDF_F_ANNUALIZEDRETURN2Y and 

MDF_F_ANNUALIZEDRETURN4Y. 

2014-05-23  Changed the “time” data type to support millisecond resolution. 

2014-05-08  Extended MDF_F_TRADESTATE. 

2014-02-28  Removed MDF_F_DIVIDENDPORIGINAL. 

2014-01-24  Added MDF_F_MAXLEVEL. 

2014-01-21  Removed MDF_F_ORDERINTAKE, MDF_F_ORDERBACKLOG, 

MDF_F_NETINTERESTINCOME, MDF_F_NETFEEANDCOMINCOME, 

MDF_F_TOPERATINGEXPENSES, MDF_F_TOPERATINGINCOME, 

MDF_F_PROFITBEFOREWACL, MDF_F_CREDITLOSS, MDF_F_RENTALINCOME, 

MDF_F_PROPERTYMGMTRESULT, MDF_F_REALIZEDCHGPROP, 

MDF_F_UNREALIZEDCHGPROP, MDF_F_RETURNONEQUITY, 

MDF_F_ADJUSTEDEQUITY and MDF_F_TOTLIABILITIES. 

Added MDF_F_INTERESTINCOME, MDF_F_OTHERFINANCIALINCOME, 

MDF_F_INTERESTEXPENSE, MDF_F_OTHERFINANCIALEXPENSE, 

MDF_F_MINORITYINTERESTRES, MDF_F_ACCOUNTSPAYABLE, 

MDF_F_EVENTLINK, MDF_F_EVENTLINKLANGUAGES. 

2013-12-02  Extended MDF_F_PRICETYPE. 

2013-09-20  Extended MDF_F_INSTRUMENTSUBTYPE. 

2013-09-11  Added MDF_F_BROKERS. 

2013-09-03  Extended MDF_F_CROSSTYPE. 

2013-08-13  Extended MDF_F_FUNDLEVERAGE. 

2013-05-10  Extended MDF_F_TRADECODE. Added MDF_F_OFFBOOKQUANTITY, 

MDF_F_DARKQUANTITY, MDF_F_OFFBOOKTURNOVER, MDF_F_DARKTURNOVER, 

MDF_F_CLOSEOFFBOOKQUANTITY, MDF_F_CLOSEDARKQUANTITY, 

MDF_F_CLOSEOFFBOOKTURNOVER and MDF_F_CLOSEDARKTURNOVER. 

2013-05-02  Extended MDF_F_NEWSCODINGSUBJECT. 

2013-04-12  Added MDF_F_CFI. 

2013-03-27  Added MDF_F_KIID. 

2013-01-30  Extended MDF_F_EXTRACREDENTIAL. 

2013-01-17  Added MDF_F_DELETERECORD. 

2012-10-26  Extended MDF_F_INSTRUMENTCLASS. 

2012-10-19  Added MDF_F_FIINSTITUTENUMBER. Extended the description of the tabular data type. 

2012-10-08  Added MDF_F_PARTICIPATIONRATE and MDF_F_ISSUEPRICE. 

2012-08-07  Added MDF_F_FINANCINGLEVEL. 

2012-06-08  Extended MDF_F_TRADESTATE. 

2012-03-20  Added MDF_F_CLOSEBIDPRICE1D, MDF_F_CLOSEBIDPRICE1W,    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_CLOSEBIDYIELD1D, MDF_F_CLOSEBIDYIELD1W, MDF_F_FINANCIALCOST 

and MDF_F_FINANCIALINCOME. 

2012-03-05  Added MDF_F_CONTRACTVALUE. 

2012-02-17  Added MDF_F_ISSUERNAME and MDF_F_LOGOTYPE. 

2012-01-31  Added MDF_F_ASIANTAILSTART and MDF_F_ASIANTAILEND. 

2011-12-14  Added MDF_F_PRICETYPE. 

2011-12-12  Added MDF_F_TICKTABLE and MDF_F_TICKSIZES. Extended 

MDF_F_INSTRUMENTTYPE. 

2011-11-18  Added MDF_F_IMBALANCE, MDF_F_IMBALANCEDIRECTION and 

MDF_F_CROSSTYPE. 

2011-11-10  Added MDF_F_CAP. 

2011-10-31  Extended MDF_F_CASUBTYPE. 

2011-06-28  Added MDF_F_CLOSEPRICE2W, MDF_F_CLOSEYIELD2W, 

MDF_F_CONVERTFROMDATE, MDF_F_CONVERTTODATE, 

MDF_F_CONVERSIONPRICE and MDF_F_DURATION. 

2011-04-20  Added MDF_F_FIELDUNIT. 

2011-03-24  Extended MDF_F_FIELDTYPE. 

2011-03-08  Added MDF_F_COUNT, MDF_F_AVERAGE, MDF_F_MIN, MDF_F_MAX, 

MDF_F_FIELDNAME, MDF_F_FIELDASPECT and MDF_F_FIELDTYPE. 

Removed MDF_F_SEQUENCENUMBER. 

2011-02-17  Added MDF_F_SHORTDESCRIPTION, MDF_F_FUNDRISK, MDF_F_EUSIPA and 

MDF_F_NEWSRANK. 

2010-11-26  Extended MDF_F_CASUBTYPE. 

2010-11-10  Extended MDF_F_CASUBTYPE. 

Added MDF_F_PRIMARYMARKETPLACE and MDF_F_FISCALPERIOD. 

2010-10-26  Added MDF_F_INSTRUMENTSUBSUBCLASS. 

Extended MDF_F_INSTRUMENTCLASS and MDF_F_INSTRUMENTTYPE.. 

2010-10-14  Added MDF_F_COUPONRATE, MDF_F_COUPONDATE, MDF_F_BARRIERPRICE, 

MDF_F_STANDARDDEVIATION3Y, MDF_F_ANNUALIZEDRETURN3Y, 

MDF_F_ANNUALIZEDRETURN5Y, MDF_F_ANNUALIZEDRETURN10Y, 

MDF_F_STANDARDDEVIATION3Y, MDF_F_MORNINGSTARRATING, 

MDF_F_SALESFEE, MDF_F_PURCHASEFEE, MDF_F_MINSTARTAMOUNT, 

MDF_F_MINSUBSCRIPTIONAMOUNT, MDF_F_PERFORMANCEFEE, 

MDF_F_MINADDITIONALAMOUNT, MDF_F_CEOADMISSIONDATE, 

MDF_F_CHAIRMANADMISSIONDATE, MDF_F_TRADEDTHROUGHDATE, 

MDF_F_TOTALFEE, MDF_F_DIVIDENDTYPE and MDF_F_DIVIDENDFREQUENCY 

2010-09-27  Added MDF_F_SETTLEMENTTYPE 

2010-09-21  Extended MDF_F_INSTRUMENTSUBTYPE 

2010-06-17  Added MDF_F_INSTRUMENTCLASS, MDF_F_INSTRUMENTSUBCLASS and 

MDF_F_CONSTITUENTS 

2010-06-14  Added MDF_F_FUNDBENCHMARKINSREF 

2010-06-11  Added MDF_F_CUSIP, MDF_F_WKN, MDF_F_UCITS and MDF_F_INCEPTIONDATE. 

Extended MDF_F_INSTRUMENTSUBTYPE. 

2010-06-07  Added MDF_F_ATHYIELD, MDF_F_ATHYIELDDATE, MDF_F_ATLYIELD, 

MDF_F_ATLYIELDDATE, MDF_F_HIGHYIELD1Y, MDF_F_HIGHYIELD1YDATE,    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

MDF_F_LOWYIELD1Y, MDF_F_LOWYIELD1YDATE, MDF_F_HIGHYIELDYTD, 

MDF_F_HIGHYIELDYTDDATE, MDF_F_LOWYIELDYTD and 

MDF_F_LOWYIELDYTDDATE 

2010-06-02  Added MDF_F_CLOSEYIELD1D, MDF_F_CLOSEYIELD1W, MDF_F_CLOSEYIELD1M, 

MDF_F_CLOSEYIELD3M, MDF_F_CLOSEYIELD6M, MDF_F_CLOSEYIELD9M, 

MDF_F_CLOSEYIELD1Y, MDF_F_CLOSEYIELD2Y, MDF_F_CLOSEYIELD3Y, 

MDF_F_CLOSEYIELD5Y, MDF_F_CLOSEYIELD10Y, MDF_F_CLOSEYIELDWTD, 

MDF_F_CLOSEYIELDMTD, MDF_F_CLOSEYIELDQTD, MDF_F_CLOSEYIELDYTD, 

MDF_F_CLOSEYIELDPYTD and MDF_F_CLOSEYIELDLD. 

2010-05-11  Added MDF_F_GENIUMID, MDF_F_CLOSEPRICE3Y, MDF_F_CLOSEPRICELD, 

MDF_F_FUNDYEARLYMGMTFEE, MDF_F_FUNDPPMFEE, MDF_F_FUNDPPMTYPE, 

MDF_F_FUNDBENCHMARK, MDF_F_FUNDLEVERAGE, MDF_F_FUNDDIRECTION, 

MDF_F_PROSPECTUS, MDF_F_GEOFOCUSREGION, MDF_F_GEOFOCUSCOUNTRY 

and MDF_F_OPENINTEREST. 

2010-05-06  Extended MDF_F_TRADESTATE 

2010-04-27  Extended MDF_F_INSTRUMENTUBTYPE 

2010-04-19  Defined lengths for MDF_F_TRADETYPE, MDF_F_TRADEBUYER and 

MDF_F_TRADESELLER. 

2010-02-08  Added MDF_F_SOURCEID and MDF_F_ISSUER 

2010-01-12  Added MDF_F_CONTRACTSIZE and MDF_F_BASERATIO 

2009-11-30  Extended MDF_F_CATYPE, MDF_F_INSTRUMENTTYPE and 

MDF_F_INSTRUMENTSUBTYPE. 

Added MDF_F_MCAP. 

2009-10-30  Added MDF_F_INTANGIBLEASSET, MDF_F_GOODWILL, MDF_F_FIXEDASSET, 

MDF_F_FINANCIALASSET, MDF_F_NONCURRENTASSET, MDF_F_INVENTORY, 

MDF_F_OTHERCURRENTASSET, MDF_F_ACCOUNTSRECEIVABLE, 

MDF_F_OTHERRECEIVABLES, MDF_F_SHORTTERMINV, MDF_F_CCE, 

MDF_F_CURRENTASSETS, MDF_F_TOTALASSETS, MDF_F_SHEQUITY, 

MDF_F_MINORITYINTEREST, MDF_F_PROVISIONS, MDF_F_LTLIABILITIES, 

MDF_F_CURLIABILITIES, MDF_F_TOTSHEQLIABILITIES, MDF_F_NIBL, 

MDF_F_TOTLIABILITIES, MDF_F_IBL, MDF_F_CASHFLOWBWC, 

MDF_F_CASHFLOWAWC, MDF_F_CASHFLOWIA, MDF_F_CASHFLOWFA, 

MDF_F_CASHFLOWTOTAL, MDF_F_NUMEPLOYEES. 

2009-10-29  Added MDF_F_VOTINGPOWERPRC, MDF_F_CAPITALPRC, MDF_F_GENDERCEO, 

MDF_F_GENDERCHAIRMAN, MDF_F_BIRTHYEARCEO, 

MDF_F_BIRTHYEARCHAIRMAN, MDF_F_ADDRESS, MDF_F_POSTALCODE, 

MDF_F_CITY, MDF_F_TELEPHONE, MDF_F_FAX, MDF_F_EMAIL, 

MDF_F_IMPORTANTEVENTS 

2009-10-27  Extended MDF_F_CATYPE and MDF_F_CASUBTYPE 

2009-10-15  Added MDF_F_TRADEYIELD 

2009-10-12  Added MDF_F_GROSSPROFIT, MDF_F_NETSALES, MDF_F_ADJUSTEDEBITA and 

MDF_F_SEQUENCENUMBER 

2009-09-22  Extended MDF_F_INSTRUMENTSUBTYPE 

2009-09-21  Extended MDF_F_INSTRUMENTSUBTYPE and MDF_F_EXERCISETYPE 

2009-09-17  Extended MDF_F_INSTRUMENTSUBTYPE 

2009-09-16  Extended MDF_F_CASUBTYPE 

2009-09-15  Extended MDF_F_TRADECODE    

> Millistream Market Data AB www.millistream.com
> Box 5243, 402 24 Göteborg, Sweden Org nr: 556763-4117

2009-09-09  Extended MDF_F_INSTRUMENTSUBTYPE 

2009-09-02  Added MDF_F_HIGHPRICEYTD, MDF_F_HIGHPRICEYTDDATE, 

MDF_F_LOWPRICEYTD and MDF_F_LOWPRICEYTDDATE 

2009-08-07  Added MDF_F_ADJUSTEDEQUITY, MDF_F_OPERATINGCASHFLOW, 

MDF_F_PRICETOADJUSTEDEQUITY and MDF_F_PRICETOCASHFLOW 

2009-08-04  Extended MDF_F_CATYPE with “Combined Split and Redemption” 

2009-05-27  Added MDF_F_SECTOR, MDF_F_REDEMPTIONPRICE, MDF_F_ATHDATE, 

MDF_F_ATLDATE, MDF_F_HIGHPRICE1YDATE, MDF_F_LOWPRICE1YDATE, 

MDF_F_FREETEXTCOMMENT2, MDF_F_FREETEXTCOMMENT3, 

MDF_F_FREETEXTCOMMENT4, MDF_F_FREETEXTCOMMENT5. 

Clarified MDF_F_INSTRUMENTSUBTYPE. 

2009-05-13  Extended MDF_F_CASUBTYPE with more values for dividends. 

Removed MDF_F_TOTALNUMBEROFSHARES. 

2009-04-29  Added MDF_F_CHAIRMAN, MDF_F_CEO, MDF_F_WEBSITE, MDF_F_ORGNUM, 

MDF_F_DESCRIPTION, MDF_F_EQUITYRATIO, MDF_F_RETURNONEQUITY, 

MDF_F_DIVIDENDYIELD, MDF_F_PER, MDF_F_PSR, 

MDF_F_TOTALNUMBEROFSHARES, MDF_F_PERIOD and MDF_F_CASUBTYPE. 

Removed MDF_F_DIVIDENDTYPE and MDF_F_SUBSCRIPTIONPERIOD. 

2009-04-28  Extended MDF_F_NEWSCODINGSUBJECT. 

2009-04-27  Added MDF_F_NEWSCODINGISIN. 

2009-04-23  Clarified MDF_F_NEWSCODINGTYPE and MDF_F_NEWSCODINGSUBJECT. 

2009-04-09  Added “201 Good-Bye” to MDF_F_LOGOFFREASON. 

2009-04-02  Added MDF_F_TRADESTATE. 

2009-04-01  Changed type of MDF_F_UNDERLYINGID to string. 

2009-03-31  Set  size on MDF_F_BOARDLOT. Changed type of MDF_F_TRADEREFERENCE to string. 

Added list to MDF_F_INSTRUMENTTYPE. 

2009-03-30  Added Odd Lot Trade code to MDF_F_TRADECODE. Added MDF_F_VWAP and 

MDF_F_CLOSEVWAP. 

2009-03-27  Added MDF_F_MINUSPAID, MDF_F_PLUSPAID and MDF_F_UNCHANGEDPAID. 

2009-03-24  Initial version.