# @version ^0.3.7


interface Controller:
    def amm() -> address: view
    def collateral_token() -> address: view
    def debt(user: address) -> uint256: view
    def loan_exists(user: address) -> bool: view # aggretage across all markets?
    def total_debt() -> uint256: view
    def health(user: address) -> uint256: view
    def amm_price() -> uint256: view
    def user_prices(user: address) -> uint256[2]: view
    def user_state(user: address) -> uint256[4]: view
    def admin_fees() -> uint256: view
    def n_loans() -> uint256: view
    def monetary_policy() -> address: view

interface AMM:
    def coins(i: uint256) -> address: view
    def price_oracle() -> uint256: view
    def read_user_tick_number(user: address) -> int256[2]: view
    def A() -> uint256: view
    def fee() -> uint256: view
    def admin_fee() -> uint256: view
    def active_band() -> int256: view
    def min_band() -> int256: view
    def max_band() -> int256: view
    def admin_fees_x() -> uint256: view
    def admin_fees_y() -> uint256: view 
    def price_oracle_contract() -> address: view

interface MonetaryPolicy:
    def rate() -> uint256: view


struct Market:
    controller: address
    amm: address
    monetary_policy: address
    collateral_token: address
    oracle_contract: address


event AddMarket:
    controller: address
    amm: address
    monetary_policy: address
    collateral_token: address
    oracle_contract: address

event TransferOwnership:
    admin: address



loans_in_market: public(address[MAX_MARKETS])
controllers: public(address[999])
count: public(uint256)

MAX_MARKETS: constant(uint256) = 20
n_markets: public(uint256)


admin: public(address)

@external
def __init__():
    self.admin = msg.sender
    self.n_markets = 0
    self.count = 0


# ---------- GETTER FUNCTIONS ---------- #



# --- CONTROLLER --- #

@external
@view
def get_amm(_controller: address) -> address:
    return Controller(_controller).amm()


@external
@view
def get_collateral_token(_controller: address) -> address:
    return Controller(_controller).collateral_token()


@external
@view
def get_monetary_policy(_controller: address) -> address:
    return Controller(_controller).monetary_policy()    


@external
@view
def get_debt(_controller: address, _user: address) -> uint256:
    return Controller(_controller).debt(_user)

@external
@view
def get_total_debt(_controller: address) -> uint256:
    return Controller(_controller).total_debt()


@external
@view
def get_health(_controller: address, _user: address) -> uint256:
    return Controller(_controller).health(_user)

@external
@view
def get_user_prices(_controller: address, _user: address) -> uint256[2]:
    return Controller(_controller).user_prices(_user)


@external
@view
def get_user_state(_controller: address, _user: address) -> uint256[4]:
    return Controller(_controller).user_state(_user)

@external
@view
def get_loans(_controller: address) -> uint256:
    return Controller(_controller).n_loans()


@external
@view
def get_admin_fees(_controller: address) -> uint256:
    return Controller(_controller).admin_fees()



# --- AGGREGATE FUNCTIONS --- #

@external
@view
def get_total_admin_fees() -> uint256:
    n: uint256 = self.count
    sum: uint256 = 0

    for i in range(MAX_MARKETS):
        if i == n:
            break
        c: address = self.controllers[i]
        fee: uint256 = Controller(c).admin_fees()
        sum += fee

    return sum


@external
@view
def total_debt_markets() -> uint256:
    n: uint256 = self.count
    sum: uint256 = 0

    for i in range(MAX_MARKETS):
        if i == n:
            break
        c: address = self.controllers[i]
        debt: uint256 = Controller(c).total_debt()
        sum += debt

    return sum


@external
@view
def get_total_loans() -> uint256:
    n: uint256 = self.count
    sum: uint256 = 0

    for i in range(MAX_MARKETS):
        if i == n:
            break
        c: address = self.controllers[i]
        loans: uint256 = Controller(c).n_loans()
        sum += loans

    return sum


# --- AMM --- #

@external
@view
def get_admin_fees_x(_amm: address) -> uint256:
    return AMM(_amm).admin_fees_x()

@external
@view
def get_admin_fees_y(_amm: address) -> uint256:
    return AMM(_amm).admin_fees_y() 


# --- MONETARY POLICY --- #

@external
@view
def get_rate(_monetary_policy: address) -> uint256:
    return MonetaryPolicy(_monetary_policy).rate()



# ---------- ADDING MARKETS ---------- #

@external
def add_market_from_controller(_controller: address):
    """
    @notice Add market to the MetaMarket
    @dev only callable admin
    @param _controller Controller address
    """
    assert msg.sender == self.admin
    
    c: address = _controller
    a: address = Controller(_controller).amm()
    mp: address = Controller(_controller).monetary_policy()
    ct: address = Controller(_controller).collateral_token()
    o: address = AMM(a).price_oracle_contract()

    self.controllers[self.count] = c
    self.count += 1

    new: Market = Market({controller: c, amm: a, monetary_policy: mp, collateral_token: ct, oracle_contract: o})

    log AddMarket(c, a, mp, ct, o)


@external
@view
def get_n_markets() -> uint256:
    return self.n_markets


# ---------- ADMIN OWNERSHIP ---------- #

@external
def transfer_ownership(_admin: address):
    """
    @notice Transfer admin ownership
    @dev only callable by the admin
    @param _admin New Admin 
    """
    assert self.admin == msg.sender
    
    self.admin = _admin

    log TransferOwnership(_admin)
