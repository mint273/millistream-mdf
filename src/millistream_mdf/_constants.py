"""
Internal constants mapping for libmdf field and message names.
This module provides IntEnum classes that match the C API integer values.

IMPORTANT DISTINCTION:

1. MessageReference (MDF_M_): Message type identifiers
   - These identify the TYPE of message being sent or received
   - Used when:
     * Sending messages (e.g., MessageReference.LOGON to log in)
     * Receiving messages (messages arrive with a MessageReference type)
     * Identifying what message you're working with
   - Examples:
     * MessageReference.LOGON - for authentication
     * MessageReference.REQUEST - for subscription requests
     * MessageReference.QUOTE - when sending/receiving quote data
     * MessageReference.TRADE - when sending/receiving trade data

2. RequestClass (MDF_RC_): Data class identifiers for subscriptions
   - These specify WHAT DATA you want to subscribe to
   - Used when:
     * Making subscription requests (goes in the REQUESTCLASS field)
     * Specifying which data streams you want to receive
   - Examples:
     * RequestClass.QUOTE - to subscribe to quote data
     * RequestClass.TRADE - to subscribe to trade data
     * RequestClass.BASICDATA - to subscribe to basic instrument data

PRACTICAL EXAMPLE:
  To subscribe to quotes and trades:
    1. Send a MessageReference.REQUEST message
    2. With Field.REQUESTCLASS = [RequestClass.QUOTE, RequestClass.TRADE]
    3. You'll receive messages with MessageReference.QUOTE and MessageReference.TRADE

  To send a quote:
    1. Send a message with MessageReference.QUOTE
    2. Add fields like Field.BIDPRICE, Field.ASKPRICE, etc.

Note that MessageReference and RequestClass have overlapping names (e.g., both have 
QUOTE, TRADE, etc.) but serve different purposes and have different integer values.
"""

from enum import IntEnum


# =============================================================================
# MESSAGE TYPE ENUMS (MREF)
# =============================================================================

class MessageReference(IntEnum):
    """
    Message type identifiers (MDF_M_ in C API).
    
    These identify the TYPE of message being sent or received.
    Values match libmdf C API message reference numbers.
    
    Use these when:
    - Sending any message to the server (login, request, data, etc.)
    - Checking the type of received messages
    - Identifying what kind of message you're working with
    """
    MESSAGESREFERENCE = 0
    LOGON = 1
    LOGOFF = 2
    LOGONGREETING = 3
    NEWSHEADLINE = 4
    QUOTE = 5
    TRADE = 6
    BIDLEVELINSERT = 7
    ASKLEVELINSERT = 8
    BIDLEVELDELETE = 9
    ASKLEVELDELETE = 10
    BIDLEVELUPDATE = 11
    ASKLEVELUPDATE = 12
    INSTRUMENTRESET = 13
    ORDERBOOKFLUSH = 14
    BASICDATA = 15
    PRICEHISTORY = 16
    INSTRUMENTDELETE = 17
    FIELDSREFERENCE = 18
    REQUEST = 19
    REQUESTFINISHED = 20
    INSREF = 21
    NEWSCONTENT = 22
    CORPORATEACTION = 23
    TRADESTATE = 24
    FUNDAMENTALS = 25
    PERFORMANCE = 26
    KEYRATIOS = 27
    ESTIMATES = 28
    ESTIMATESHISTORY = 29
    NETORDERIMBALANCE = 30
    UNSUBSCRIBE = 31
    L10N = 32
    CI = 33
    CIHISTORY = 34
    PRIIP = 35
    MIFID = 36
    MIFIDHISTORY = 37
    MAPPINGS = 38
    MBOADD = 39
    MBOUPDATE = 40
    MBODELETE = 41
    GREEKS = 42
    QUOTEBBO = 43
    QUOTEEX = 44


# =============================================================================
# FIELD ENUMS (TAG)
# =============================================================================

class Field(IntEnum):
    """
    Field identifiers (TAG).
    Values match libmdf C API field tag numbers.
    """
    LANGUAGE = 0
    HEADLINE = 1
    TEXTBODY = 2
    DATE = 3
    TIME = 4
    BIDPRICE = 5
    ASKPRICE = 6
    LASTPRICE = 7
    DAYHIGHPRICE = 8
    DAYLOWPRICE = 9
    QUANTITY = 10
    TURNOVER = 11
    TRADEPRICE = 12
    TRADEQUANTITY = 13
    TRADEREFERENCE = 14
    TRADECODE = 15
    ORDERLEVEL = 16
    NUMBIDORDERS = 17
    NUMASKORDERS = 18
    BIDQUANTITY = 19
    ASKQUANTITY = 20
    SYMBOL = 21
    NAME = 22
    ISIN = 23
    BOARDLOT = 24
    INSTRUMENTTYPE = 25
    INSTRUMENTSUBTYPE = 26
    DERIVATIVEINDICATOR = 27
    EXERCISETYPE = 28
    ISSUECURRENCY = 29
    TRADECURRENCY = 30
    BASECURRENCY = 31
    QUOTECURRENCY = 32
    ISSUEDATE = 33
    STRIKEDATE = 34
    STRIKEPRICE = 35
    TRADETIME = 36
    NUMTRADES = 37
    EXECUTEDSIDE = 38
    OPENPRICE = 39
    CLOSEPRICE = 40
    CLOSEBIDPRICE = 41
    CLOSEASKPRICE = 42
    CLOSEDAYHIGHPRICE = 43
    CLOSEDAYLOWPRICE = 44
    CLOSEQUANTITY = 45
    CLOSETURNOVER = 46
    CLOSENUMTRADES = 47
    NEWSID = 48
    REQUESTID = 49
    REQUESTSTATUS = 50
    REQUESTTYPE = 51
    REQUESTCLASS = 52
    INSREFLIST = 53
    MARKETPLACE = 54
    LIST = 55
    INTERNALQUANTITY = 56
    INTERNALTURNOVER = 57
    CLOSEINTERNALQUANTITY = 58
    CLOSEINTERNALTURNOVER = 59
    TRADEBUYER = 60
    TRADESELLER = 61
    BIDCOUNTERPART = 62
    ASKCOUNTERPART = 63
    COMPANY = 64
    FUNDPPMCODE = 65
    UNDERLYINGID = 66
    USERNAME = 67
    PASSWORD = 68
    EXTRACREDENTIAL = 69
    LOGOFFREASON = 70
    TRADETYPE = 71
    TRADECANCELTIME = 72
    NEWSBLOCKNUMBER = 73
    BIDYIELD = 74
    ASKYIELD = 75
    LASTYIELD = 76
    OPENYIELD = 77
    DAYHIGHYIELD = 78
    DAYLOWYIELD = 79
    CLOSEBIDYIELD = 80
    CLOSEASKYIELD = 81
    CLOSEYIELD = 82
    CLOSEDAYHIGHYIELD = 83
    CLOSEDAYLOWYIELD = 84
    NEWSCODINGCOMPANY = 85
    NEWSCODINGTYPE = 86
    NEWSCODINGSUBJECT = 87
    NEWSCODINGCOUNTRY = 88
    NEWSCODINGORIGINAL = 89
    FUNDCOMPANY = 90
    FUNDPMICODE = 91
    COUNTRY = 92
    NAV = 93
    CLOSENAV = 94
    TIS = 95
    CLOSETIS = 96
    SOURCE = 97
    S1 = 98
    CATYPE = 99
    DIVIDEND = 100
    CASUBTYPE = 102
    ADJUSTMENTFACTOR = 103
    NUMBEROFSHARES = 104
    NUMBEROFSHARESDELTA = 105
    NEWSHARES = 106
    OLDSHARES = 107
    SUBSCRIPTIONPRICE = 108
    PERIOD = 109
    NOMINALVALUE = 110
    RECORDDATE = 111
    PAYMENTDATE = 112
    ANNOUNCEMENTDATE = 113
    TID = 114
    NEWSISLASTBLOCK = 115
    SERVERNAME = 116
    SERVERTIME = 117
    SERVERDATE = 118
    MIC = 119
    UNCHANGEDPAID = 120
    PLUSPAID = 121
    MINUSPAID = 122
    VWAP = 123
    CLOSEVWAP = 124
    SPECIALCONDITION = 125
    TRADESTATE = 126
    SALES = 127
    EBIT = 128
    PRETAXPROFIT = 129
    NETPROFIT = 130
    EPS = 131
    DILUTEDEPS = 132
    EBITDA = 133
    EBITA = 134
    NETFININCOME = 138
    CLOSEPRICE1D = 148
    CLOSEPRICE1W = 149
    CLOSEPRICE1M = 150
    CLOSEPRICE3M = 151
    CLOSEPRICE6M = 152
    CLOSEPRICE9M = 153
    CLOSEPRICE1Y = 154
    CLOSEPRICE2Y = 155
    CLOSEPRICE5Y = 156
    CLOSEPRICE10Y = 157
    CLOSEPRICEWTD = 158
    CLOSEPRICEMTD = 159
    CLOSEPRICEQTD = 160
    CLOSEPRICEYTD = 161
    CLOSEPRICEPYTD = 162
    ATH = 163
    ATL = 164
    HIGHPRICE1Y = 165
    LOWPRICE1Y = 166
    NEWSCODINGISIN = 167
    CHAIRMAN = 168
    CEO = 169
    WEBSITE = 170
    ORGNUM = 171
    DESCRIPTION = 172
    EQUITYRATIO = 173
    S2 = 179
    S3 = 180
    S4 = 181
    S5 = 182
    ATHDATE = 183
    ATLDATE = 184
    HIGHPRICE1YDATE = 185
    LOWPRICE1YDATE = 186
    REDEMPTIONPRICE = 187
    SECTOR = 188
    OPERATINGCASHFLOW = 189
    HIGHPRICEYTD = 193
    LOWPRICEYTD = 194
    HIGHPRICEYTDDATE = 195
    LOWPRICEYTDDATE = 196
    COUNT = 197
    GROSSPROFIT = 198
    NETSALES = 199
    ADJUSTEDEBITA = 200
    TRADEYIELD = 201
    VOTINGPOWERPRC = 202
    CAPITALPRC = 203
    GENDERCEO = 204
    GENDERCHAIRMAN = 205
    BIRTHYEARCEO = 206
    BIRTHYEARCHAIRMAN = 207
    ADDRESS = 208
    POSTALCODE = 209
    CITY = 210
    TELEPHONE = 211
    FAX = 212
    EMAIL = 213
    IMPORTANTEVENTS = 214
    INTANGIBLEASSET = 215
    GOODWILL = 216
    FIXEDASSET = 217
    FINANCIALASSET = 218
    NONCURRENTASSET = 219
    INVENTORY = 220
    OTHERCURRENTASSET = 221
    ACCOUNTSRECEIVABLE = 222
    OTHERRECEIVABLES = 223
    SHORTTERMINV = 224
    CCE = 225
    CURRENTASSETS = 226
    TOTALASSETS = 227
    SHEQUITY = 228
    MINORITYINTEREST = 229
    PROVISIONS = 230
    LTLIABILITIES = 231
    CURLIABILITIES = 232
    TOTSHEQLIABILITIES = 233
    NIBL = 234
    IBL = 236
    CASHFLOWBWC = 237
    CASHFLOWAWC = 238
    CASHFLOWIA = 239
    CASHFLOWFA = 240
    CASHFLOWTOTAL = 241
    NUMEMPLOYEES = 242
    MCAP = 243
    CONTRACTSIZE = 244
    BASERATIO = 245
    SOURCEID = 246
    ISSUER = 247
    GENIUMID = 248
    CLOSEPRICE3Y = 249
    CLOSEPRICELD = 250
    FUNDYEARLYMGMTFEE = 251
    FUNDPPMFEE = 252
    FUNDPPMTYPE = 253
    FUNDBENCHMARK = 254
    FUNDLEVERAGE = 255
    FUNDDIRECTION = 256
    PROSPECTUS = 257
    GEOFOCUSREGION = 258
    GEOFOCUSCOUNTRY = 259
    OPENINTEREST = 260
    CLOSEYIELD1D = 261
    CLOSEYIELD1W = 262
    CLOSEYIELD1M = 263
    CLOSEYIELD3M = 264
    CLOSEYIELD6M = 265
    CLOSEYIELD9M = 266
    CLOSEYIELD1Y = 267
    CLOSEYIELD2Y = 268
    CLOSEYIELD3Y = 269
    CLOSEYIELD5Y = 270
    CLOSEYIELD10Y = 271
    CLOSEYIELDWTD = 272
    CLOSEYIELDMTD = 273
    CLOSEYIELDQTD = 274
    CLOSEYIELDYTD = 275
    CLOSEYIELDPYTD = 276
    CLOSEYIELDLD = 277
    ATHYIELD = 278
    ATLYIELD = 279
    ATHYIELDDATE = 280
    ATLYIELDDATE = 281
    HIGHYIELD1Y = 282
    LOWYIELD1Y = 283
    HIGHYIELDYTD = 284
    LOWYIELDYTD = 285
    HIGHYIELDYTDDATE = 286
    LOWYIELDYTDDATE = 287
    HIGHYIELD1YDATE = 288
    LOWYIELD1YDATE = 289
    CUSIP = 290
    WKN = 291
    UCITS = 292
    INCEPTIONDATE = 293
    FUNDBENCHMARKINSREF = 294
    INSTRUMENTCLASS = 295
    INSTRUMENTSUBCLASS = 296
    CONSTITUENTS = 297
    COUPONRATE = 298
    COUPONDATE = 299
    BARRIERPRICE = 300
    STANDARDDEVIATION3Y = 301
    ANNUALIZEDRETURN3Y = 302
    SHARPERATIO3Y = 303
    MORNINGSTARATING = 304
    SALESFEE = 305
    PURCHASEFEE = 306
    MINSTARTAMOUNT = 307
    MINSUBSCRIPTIONAMOUNT = 308
    PERFORMANCEFEE = 309
    MINADDITIONALAMOUNT = 310
    ANNUALIZEDRETURN5Y = 311
    ANNUALIZEDRETURN10Y = 312
    CEOADMISSIONDATE = 313
    CHAIRMANADMISSIONDATE = 314
    TRADEDTHROUGHDATE = 315
    TOTALFEE = 316
    DIVIDENDTYPE = 317
    DIVIDENDFREQUENCY = 318
    INSTRUMENTSUBSUBCLASS = 319
    PRIMARYMARKETPLACE = 320
    FISCALPERIOD = 321
    SHORTDESCRIPTION = 322
    FUNDRISK = 323
    EUSIPA = 324
    NEWSRANK = 325
    AVERAGE = 326
    MIN = 327
    MAX = 328
    FIELDNAME = 329
    FIELDASPECT = 330
    FIELDTYPE = 331
    FUNDCOMPANY2 = 332
    FIELDUNIT = 333
    CLOSEPRICE2W = 334
    CLOSEYIELD2W = 335
    CONVERTFROMDATE = 336
    CONVERTTODATE = 337
    CONVERSIONPRICE = 338
    DURATION = 339
    SETTLEMENTTYPE = 340
    VOTINGPOWER = 341
    CAP = 342
    IMBALANCE = 343
    IMBALANCEDIRECTION = 344
    CROSSTYPE = 345
    TICKTABLE = 346
    TICKSIZES = 347
    PRICETYPE = 348
    ASIANTAILSTART = 349
    ASIANTAILEND = 350
    LOGOTYPE = 351
    ISSUERNAME = 352
    CONTRACTVALUE = 353
    CLOSEBIDPRICE1D = 354
    CLOSEBIDYIELD1D = 355
    CLOSEBIDPRICE1W = 356
    CLOSEBIDYIELD1W = 357
    FINANCIALINCOME = 358
    FINANCIALCOST = 359
    FINANCINGLEVEL = 360
    PARTICIPATIONRATE = 361
    ISSUEPRICE = 362
    FIINSTITUTENUMBER = 363
    DELETERECORD = 364
    KIID = 365
    CFI = 366
    OFFBOOKQUANTITY = 367
    OFFBOOKTURNOVER = 368
    DARKQUANTITY = 369
    DARKTURNOVER = 370
    CLOSEOFFBOOKQUANTITY = 371
    CLOSEOFFBOOKTURNOVER = 372
    CLOSEDARKQUANTITY = 373
    CLOSEDARKTURNOVER = 374
    BROKERS = 375
    INTERESTINCOME = 376
    OTHERFINANCIALINCOME = 377
    INTERESTEXPENSE = 378
    OTHERFINANCIALEXPENSE = 379
    MINORITYINTERESTRES = 380
    ACCOUNTSPAYABLE = 381
    EVENTLINK = 382
    EVENTLINKLANGUAGES = 383
    MAXLEVEL = 384
    SETTLEMENTPRICE = 385
    ANNUALIZEDRETURN1Y = 386
    ANNUALIZEDRETURN2Y = 387
    ANNUALIZEDRETURN4Y = 388
    S6 = 389
    S7 = 390
    S8 = 391
    S9 = 392
    S10 = 393
    N1 = 394
    N2 = 395
    N3 = 396
    N4 = 397
    N5 = 398
    I1 = 399
    I2 = 400
    I3 = 401
    I4 = 402
    I5 = 403
    D1 = 404


# =============================================================================
# REQUEST CLASS ENUMS
# =============================================================================

class RequestClass(IntEnum):
    """
    Request class identifiers (MDF_RC_ in C API).
    
    These specify WHAT DATA you want to subscribe to in a subscription request.
    Values match libmdf C API request class codes.
    
    Use these when:
    - Making subscription requests (in the Field.REQUESTCLASS field)
    - Specifying which data streams you want to receive
    - Unsubscribing from data streams
    
    Example:
        To subscribe to quote and trade data:
        client.subscribe(
            request_classes=[RequestClass.QUOTE, RequestClass.TRADE],
            instruments='*'
        )
        
        This sends a MessageReference.REQUEST message with:
        - Field.REQUESTCLASS = "1 2" (space-separated RequestClass values)
        - Field.INSREFLIST = "*"
        
        You'll then receive:
        - MessageReference.QUOTE messages with quote data
        - MessageReference.TRADE messages with trade data
    """
    NEWSHEADLINE = 0
    QUOTE = 1
    TRADE = 2
    ORDER = 3
    BASICDATA = 4
    PRICEHISTORY = 5
    FIELDSREFERENCE = 6
    INSREF = 7
    NEWSCONTENT = 8
    CORPORATEACTION = 9
    TRADESTATE = 10
    FUNDAMENTALS = 11
    PERFORMANCE = 12
    KEYRATIOS = 13
    ESTIMATES = 14
    ESTIMATESHISTORY = 15
    NETORDERIMBALANCE = 16
    L10N = 17
    CI = 18
    CIHISTORY = 19
    PRIIP = 20
    MIFID = 21
    MIFIDHISTORY = 22
    MAPPINGS = 23
    MBO = 24
    GREEKS = 25
    QUOTEBBO = 26
    QUOTEEX = 27


# =============================================================================
# REQUEST TYPE ENUMS
# =============================================================================

class RequestType(IntEnum):
    """
    Request type identifiers.
    Values match libmdf C API request type codes.
    """
    IMAGE = 1
    STREAM = 2
    FULL = 3


# =============================================================================
# DELAY TYPE ENUMS
# =============================================================================

class DelayType(IntEnum):
    """
    Delay type identifiers.
    Values match libmdf C API delay type codes.
    """
    REALTIME = 0
    DELAY = 1
    EOD = 2
    NEXTDAY = 3
    T1 = 4
    ANY = 14
    BEST = 15


# =============================================================================
# TRADE CODE FLAGS
# =============================================================================

class TradeCodeFlag(IntEnum):
    """
    Trade code flag identifiers (bit field).
    Values match libmdf C API trade code flags.
    """
    OFFHOURS = 1
    OUTSIDESPREAD = 2
    REPORTED = 4
    CORRECTION = 8
    CANCEL = 16
    UPDATEHIGHLOW = 32
    UPDATEVOLUME = 64
    UPDATELAST = 128
    ODDLOT = 256
    DELAYED = 512
    DARKPOOL = 1024


# =============================================================================
# CORPORATE ACTION TYPE ENUMS
# =============================================================================

class CorporateActionType(IntEnum):
    """
    Corporate action type identifiers.
    Values match libmdf C API corporate action type codes.
    """
    DIVIDEND = 0
    SPLIT = 1
    RIGHTSISSUE = 2
    BONUSISSUE = 3
    DIRECTEDISSUE = 4
    SHAREREDEMPTION = 5
    SPINOFF = 6
    STOCKDIVIDEND = 7
    STOCKDIVIDENDEX = 8
    UNKNOWN = 9
    IPO = 10
    CURRENCYCONVERSION = 11
    NOMINALVALUE = 12
    CHANGEINUNDERLYING = 13
    CHANGEOFBASICDATA = 14
    CALENDAR = 15
    INSIDERTRADING = 16
    SPLITANDREDEMPTION = 17
    EXCHANGECLOSED = 18
    MAJORHOLDERS = 19
    SHARELOAN = 20



