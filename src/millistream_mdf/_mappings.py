"""
Mapping utilities for MDF constants.
Provides type mappings and name conversions for Field enums.
"""

from ._constants import RequestType, Field
from datetime import date, time


# =============================================================================
# REQUEST TYPE MAPPINGS
# =============================================================================

SUB_TYPES = {
    'image': RequestType.IMAGE,
    'stream': RequestType.STREAM,
    'full': RequestType.FULL
}


# =============================================================================
# FIELD NAME MAPPINGS
# =============================================================================

def _create_field_name_mapping():
    """Generate lowercase field names from Field enum."""
    return {field: field.name.lower() for field in Field}


# Auto-generated field name mapping
FIELD_TO_NAME = _create_field_name_mapping()

# Reverse mapping for convenience
NAME_TO_FIELD = {name: field for field, name in FIELD_TO_NAME.items()}


# =============================================================================
# FIELD TYPE MAPPINGS
# =============================================================================
# Based on MDF Fields Reference Document
# Only non-string types need to be specified; defaults to str

FIELD_TYPES = {
    # -------------------------------------------------------------------------
    # Date Fields
    # -------------------------------------------------------------------------
    Field.DATE: date,
    Field.ISSUEDATE: date,
    Field.STRIKEDATE: date,
    Field.RECORDDATE: date,
    Field.PAYMENTDATE: date,
    Field.ANNOUNCEMENTDATE: date,
    Field.ATHDATE: date,
    Field.ATLDATE: date,
    Field.HIGHPRICE1YDATE: date,
    Field.LOWPRICE1YDATE: date,
    Field.HIGHPRICEYTDDATE: date,
    Field.LOWPRICEYTDDATE: date,
    Field.ATHYIELDDATE: date,
    Field.ATLYIELDDATE: date,
    Field.HIGHYIELD1YDATE: date,
    Field.LOWYIELD1YDATE: date,
    Field.HIGHYIELDYTDDATE: date,
    Field.LOWYIELDYTDDATE: date,
    Field.INCEPTIONDATE: date,
    Field.CEOADMISSIONDATE: date,
    Field.CHAIRMANADMISSIONDATE: date,
    Field.TRADEDTHROUGHDATE: date,
    Field.CONVERTFROMDATE: date,
    Field.CONVERTTODATE: date,
    Field.COUPONDATE: date,
    Field.ASIANTAILSTART: date,
    Field.ASIANTAILEND: date,
    Field.SERVERDATE: date,
    Field.D1: date,
    
    # -------------------------------------------------------------------------
    # Time Fields
    # -------------------------------------------------------------------------
    Field.TIME: time,
    Field.TRADETIME: time,
    Field.TRADECANCELTIME: time,
    Field.SERVERTIME: time,
    
    # -------------------------------------------------------------------------
    # Float/Number Fields (prices, rates, amounts, ratios)
    # -------------------------------------------------------------------------
    # Prices
    Field.BIDPRICE: float,
    Field.ASKPRICE: float,
    Field.LASTPRICE: float,
    Field.DAYHIGHPRICE: float,
    Field.DAYLOWPRICE: float,
    Field.TRADEPRICE: float,
    Field.OPENPRICE: float,
    Field.CLOSEPRICE: float,
    Field.CLOSEBIDPRICE: float,
    Field.CLOSEASKPRICE: float,
    Field.CLOSEDAYHIGHPRICE: float,
    Field.CLOSEDAYLOWPRICE: float,
    Field.STRIKEPRICE: float,
    Field.CLOSEPRICE1D: float,
    Field.CLOSEPRICE1W: float,
    Field.CLOSEPRICE1M: float,
    Field.CLOSEPRICE3M: float,
    Field.CLOSEPRICE6M: float,
    Field.CLOSEPRICE9M: float,
    Field.CLOSEPRICE1Y: float,
    Field.CLOSEPRICE2Y: float,
    Field.CLOSEPRICE3Y: float,
    Field.CLOSEPRICE5Y: float,
    Field.CLOSEPRICE10Y: float,
    Field.CLOSEPRICEWTD: float,
    Field.CLOSEPRICEMTD: float,
    Field.CLOSEPRICEQTD: float,
    Field.CLOSEPRICEYTD: float,
    Field.CLOSEPRICEPYTD: float,
    Field.CLOSEPRICELD: float,
    Field.CLOSEPRICE2W: float,
    Field.CLOSEBIDPRICE1D: float,
    Field.CLOSEBIDPRICE1W: float,
    Field.ATH: float,
    Field.ATL: float,
    Field.HIGHPRICE1Y: float,
    Field.LOWPRICE1Y: float,
    Field.HIGHPRICEYTD: float,
    Field.LOWPRICEYTD: float,
    Field.REDEMPTIONPRICE: float,
    Field.SUBSCRIPTIONPRICE: float,
    Field.BARRIERPRICE: float,
    Field.CONVERSIONPRICE: float,
    Field.ISSUEPRICE: float,
    
    # Quantities & Turnover
    Field.QUANTITY: float,
    Field.TURNOVER: float,
    Field.TRADEQUANTITY: float,
    Field.BIDQUANTITY: float,
    Field.ASKQUANTITY: float,
    Field.CLOSEQUANTITY: float,
    Field.CLOSETURNOVER: float,
    Field.INTERNALQUANTITY: float,
    Field.INTERNALTURNOVER: float,
    Field.CLOSEINTERNALQUANTITY: float,
    Field.CLOSEINTERNALTURNOVER: float,
    
    # Yields
    Field.BIDYIELD: float,
    Field.ASKYIELD: float,
    Field.LASTYIELD: float,
    Field.OPENYIELD: float,
    Field.DAYHIGHYIELD: float,
    Field.DAYLOWYIELD: float,
    Field.CLOSEBIDYIELD: float,
    Field.CLOSEASKYIELD: float,
    Field.CLOSEYIELD: float,
    Field.CLOSEDAYHIGHYIELD: float,
    Field.CLOSEDAYLOWYIELD: float,
    Field.CLOSEYIELD1D: float,
    Field.CLOSEYIELD1W: float,
    Field.CLOSEYIELD2W: float,
    Field.CLOSEYIELD1M: float,
    Field.CLOSEYIELD3M: float,
    Field.CLOSEYIELD6M: float,
    Field.CLOSEYIELD9M: float,
    Field.CLOSEYIELD1Y: float,
    Field.CLOSEYIELD2Y: float,
    Field.CLOSEYIELD3Y: float,
    Field.CLOSEYIELD5Y: float,
    Field.CLOSEYIELD10Y: float,
    Field.CLOSEYIELDWTD: float,
    Field.CLOSEYIELDMTD: float,
    Field.CLOSEYIELDQTD: float,
    Field.CLOSEYIELDYTD: float,
    Field.CLOSEYIELDPYTD: float,
    Field.CLOSEYIELDLD: float,
    Field.CLOSEBIDYIELD1D: float,
    Field.CLOSEBIDYIELD1W: float,
    Field.ATHYIELD: float,
    Field.ATLYIELD: float,
    Field.HIGHYIELD1Y: float,
    Field.LOWYIELD1Y: float,
    Field.HIGHYIELDYTD: float,
    Field.LOWYIELDYTD: float,
    Field.TRADEYIELD: float,
    
    # Fund/NAV
    Field.NAV: float,
    Field.CLOSENAV: float,
    Field.TIS: float,
    Field.CLOSETIS: float,
    
    # Dividends
    Field.DIVIDEND: float,
    
    # Shares & Adjustments
    Field.ADJUSTMENTFACTOR: float,
    Field.NUMBEROFSHARES: float,
    Field.NUMBEROFSHARESDELTA: float,
    Field.NEWSHARES: float,
    Field.OLDSHARES: float,
    Field.NOMINALVALUE: float,
    
    # Market Metrics
    Field.VWAP: float,
    Field.CLOSEVWAP: float,
    Field.MCAP: float,
    Field.CONTRACTSIZE: float,
    Field.BASERATIO: float,
    Field.OPENINTEREST: float,
    
    # Financial Statement Items
    Field.SALES: float,
    Field.EBIT: float,
    Field.PRETAXPROFIT: float,
    Field.NETPROFIT: float,
    Field.EPS: float,
    Field.DILUTEDEPS: float,
    Field.EBITDA: float,
    Field.EBITA: float,
    Field.NETFININCOME: float,
    Field.GROSSPROFIT: float,
    Field.NETSALES: float,
    Field.ADJUSTEDEBITA: float,
    
    # Balance Sheet Items
    Field.INTANGIBLEASSET: float,
    Field.GOODWILL: float,
    Field.FIXEDASSET: float,
    Field.FINANCIALASSET: float,
    Field.NONCURRENTASSET: float,
    Field.INVENTORY: float,
    Field.OTHERCURRENTASSET: float,
    Field.ACCOUNTSRECEIVABLE: float,
    Field.OTHERRECEIVABLES: float,
    Field.SHORTTERMINV: float,
    Field.CCE: float,
    Field.CURRENTASSETS: float,
    Field.TOTALASSETS: float,
    Field.SHEQUITY: float,
    Field.MINORITYINTEREST: float,
    Field.PROVISIONS: float,
    Field.LTLIABILITIES: float,
    Field.CURLIABILITIES: float,
    Field.TOTSHEQLIABILITIES: float,
    Field.NIBL: float,
    Field.IBL: float,
    Field.ACCOUNTSPAYABLE: float,
    
    # Cash Flow Items
    Field.CASHFLOWBWC: float,
    Field.CASHFLOWAWC: float,
    Field.CASHFLOWIA: float,
    Field.CASHFLOWFA: float,
    Field.CASHFLOWTOTAL: float,
    Field.OPERATINGCASHFLOW: float,
    
    # Ratios & Percentages
    Field.VOTINGPOWERPRC: float,
    Field.CAPITALPRC: float,
    Field.EQUITYRATIO: float,
    
    # Fund-Specific
    Field.FUNDYEARLYMGMTFEE: float,
    Field.FUNDPPMFEE: float,
    Field.FUNDLEVERAGE: float,
    Field.STANDARDDEVIATION3Y: float,
    Field.ANNUALIZEDRETURN1Y: float,
    Field.ANNUALIZEDRETURN2Y: float,
    Field.ANNUALIZEDRETURN3Y: float,
    Field.ANNUALIZEDRETURN4Y: float,
    Field.ANNUALIZEDRETURN5Y: float,
    Field.ANNUALIZEDRETURN10Y: float,
    Field.SHARPERATIO3Y: float,
    Field.MORNINGSTARATING: float,
    Field.SALESFEE: float,
    Field.PURCHASEFEE: float,
    Field.MINSTARTAMOUNT: float,
    Field.MINSUBSCRIPTIONAMOUNT: float,
    Field.PERFORMANCEFEE: float,
    Field.MINADDITIONALAMOUNT: float,
    Field.TOTALFEE: float,
    
    # Options/Derivatives
    Field.DURATION: float,
    Field.CAP: float,
    Field.FINANCIALINCOME: float,
    Field.FINANCIALCOST: float,
    Field.FINANCINGLEVEL: float,
    Field.PARTICIPATIONRATE: float,
    Field.MAXLEVEL: float,
    
    # Statistics
    Field.AVERAGE: float,
    Field.MIN: float,
    Field.MAX: float,
    
    # Income Statement
    Field.INTERESTINCOME: float,
    Field.OTHERFINANCIALINCOME: float,
    Field.INTERESTEXPENSE: float,
    Field.OTHERFINANCIALEXPENSE: float,
    Field.MINORITYINTERESTRES: float,
    
    # Placeholders (numeric)
    Field.N1: float,
    Field.N2: float,
    Field.N3: float,
    Field.N4: float,
    Field.N5: float,
    
    # -------------------------------------------------------------------------
    # Integer Fields (counts, codes, flags, enum values, insref)
    # -------------------------------------------------------------------------
    # Order Book
    Field.ORDERLEVEL: int,
    Field.NUMBIDORDERS: int,
    Field.NUMASKORDERS: int,
    Field.NUMTRADES: int,
    Field.CLOSENUMTRADES: int,
    
    # Request/Status
    Field.REQUESTSTATUS: int,
    Field.REQUESTTYPE: int,
    Field.REQUESTCLASS: int,
    
    # Instrument References (insref type)
    Field.COMPANY: int,
    Field.FUNDCOMPANY: int,
    Field.UNDERLYINGID: int,
    Field.MARKETPLACE: int,
    Field.PRIMARYMARKETPLACE: int,
    Field.TICKTABLE: int,
    
    # Instrument Classification
    Field.INSTRUMENTTYPE: int,
    Field.INSTRUMENTSUBTYPE: int,
    Field.DERIVATIVEINDICATOR: int,
    Field.EXERCISETYPE: int,
    Field.INSTRUMENTCLASS: int,
    
    # Trade & Market State
    Field.TRADECODE: int,
    Field.EXECUTEDSIDE: int,
    Field.SPECIALCONDITION: int,
    Field.TRADESTATE: int,
    
    # Corporate Actions
    Field.CATYPE: int,
    Field.CASUBTYPE: int,
    
    # News
    Field.NEWSCODINGTYPE: int,
    Field.NEWSCODINGSUBJECT: int,
    Field.NEWSISLASTBLOCK: int,
    Field.NEWSBLOCKNUMBER: int,
    Field.NEWSRANK: int,
    
    # Fund Codes
    Field.FUNDPPMCODE: int,
    Field.FIINSTITUTENUMBER: int,
    
    # Counts & Indices
    Field.COUNT: int,
    Field.NUMEMPLOYEES: int,
    Field.TID: int,
    
    # Product Classification
    Field.DIVIDENDTYPE: int,
    Field.DIVIDENDFREQUENCY: int,
    Field.FUNDRISK: int,
    Field.EUSIPA: int,
    Field.PRICETYPE: int,
    Field.SETTLEMENTTYPE: int,
    
    # Order Imbalance
    Field.CROSSTYPE: int,
    Field.IMBALANCE: int,
    Field.IMBALANCEDIRECTION: int,
    
    # Other
    Field.VOTINGPOWER: int,
    Field.CONTRACTVALUE: int,
    Field.DELETERECORD: int,
    Field.LOGOFFREASON: int,
    
    # Placeholders (integer)
    Field.I1: int,
    Field.I2: int,
    Field.I3: int,
    Field.I4: int,
    Field.I5: int,
    
    # -------------------------------------------------------------------------
    # List Fields
    # -------------------------------------------------------------------------
    Field.INSREFLIST: list,
    Field.LIST: list,
    Field.NEWSCODINGCOMPANY: list,
    Field.SECTOR: list,
}

