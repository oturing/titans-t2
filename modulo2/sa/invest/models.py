
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy import types, UniqueConstraint

Base = declarative_base()

class InvalidChoice(LookupError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = set(choices)
        super(ChoiceType, self).__init__(**kw)

    def validate(self, value):
        if value in self.choices:
            return value
        raise InvalidChoice(value)

    def process_bind_param(self, value, dialect):
        return self.validate(value)

    process_result_value = process_bind_param

# @client(taxPayerID/char,name/char,address/char):taxPayerID

class ClientTable(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    tax_payer_id = Column(String, unique=True)
    name = Column(String)
    address = Column(String)

#   @stock(sTicker/char,sName/char,rating/char,prinBus/char,
#       sHigh/numeric,sLow/numeric,sCurrent/numeric,
#       ret1Yr/numeric,ret5Yr/numeric):sTicker

RATINGS = ['NR', 'A', 'B', 'C']

class StockTable(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True)
    name = Column(String, unique=True)
    rating = Column(ChoiceType(RATINGS))  # vocabulario controlado
    pri_business = Column(String)
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    current = Column(Numeric(10, 2))
    ret1yr = Column(Numeric(10, 2))
    ret5yr = Column(Numeric(10, 2))

# @fundFamily(familyID/char,company/char,cAddress/char):familyID

class FundFamilyTable(Base):
    __tablename__ = 'fund_family'

    id = Column(Integer, primary_key=True)
    company = Column(String, unique=True)
    address = Column(String)

#   @mutualFund(mTicker/char,mName/char,prinObj/char,
#       mHigh/numeric,mLow/numeric,mCurrent/numeric,
#        yield/numeric,familyID/char):mTicker

OBJECTIVES = ['G', 'I', 'S']

class MutualFundTable(Base):
    __tablename__ = 'mutual_fund'

    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True)
    name = Column(String, unique=True)
    pri_objective = Column(ChoiceType(OBJECTIVES))  # vocabulario controlado
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    current = Column(Numeric(10, 2))
    yield_ = Column(Numeric(10, 2))
    family_id = Column(Integer, ForeignKey('fund_family.id'))

# @mutualFundPortfolio(taxPayerID/char,mTicker/char,mNumShares/numeric):
#       taxPayerID,mTicker

class MutualFundPortfolioTable(Base):
    __tablename__ = 'mutual_fund_portfolio'

    client_id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    fund_id = Column(Integer, ForeignKey('mutual_fund.id'), primary_key=True)
    num_shares = Column(Integer)

# @stockPortfolio(taxPayerID/char,sTicker/char,sNumShares/numeric):
#       taxPayerID,sTicker

class StockPortfolioTable(Base):
    __tablename__ = 'stock_portfolio'

    client_id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock.id'), primary_key=True)
    num_shares = Column(Integer)
