# @version ^0.3.7


interface Controller:
    def amm() -> address: view
    def collateral_token() -> address: view
    def monetary_policy() -> address: view
    def debt(user: address) -> uint256: view
    def total_debt() -> uint256: view
    def health(user: address) -> uint256: view
    def user_prices(user: address) -> uint256[2]: view
    def user_state(user: address) -> uint256[4]: view
    def admin_fees() -> uint256: view
    def n_loans() -> uint256: view

interface AMM:
    def price_oracle_contract() -> address: view

interface MonetaryPolicy:
    def rate() -> uint256: view


struct Market:
    controller: address
    amm: address
    monetary_policy: address
    collateral_token: address
    oracle_contract: address

market: public(HashMap[uint256, Market])
n_markets: public(int128)

controllers: public(address[999])
count: public(int128)

event AddMarket:
    controller: address
    amm: address
    monetary_policy: address
    collateral_token: address
    oracle_contract: address

event TransferOwnership:
    admin: address

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
def get_total_debt(_controller: address, _user: address) -> uint256:
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
def get_n_loans(_controller: address) -> uint256:
    return Controller(_controller).n_loans()


@external
@view
def get_admin_fees(_controller: address) -> uint256:
    return Controller(_controller).admin_fees()

# ------ #
@external
@view
def get_total_admin_fees() -> uint256:
    sum: uint256 = 0

    for i in range(10):
        fee: uint256 = Controller(self.controllers[i]).admin_fees()
        sum += fee

    return sum


# --- MONETARY POLICY --- #

@external
@view
def get_rate(_monetary_policy: address) -> uint256:
    return MonetaryPolicy(_monetary_policy).rate()



# ---------- ADDING MARKETS ---------- #

@external
def add_market_from_controller(_id: int128, _controller: address):
    """
    @notice Add market to the MetaMarket
    @dev only callable by the admin
    """
    assert msg.sender == self.admin
    
    c: address = _controller
    a: address = Controller(_controller).amm()
    mp: address = Controller(_controller).monetary_policy()
    ct: address = Controller(_controller).collateral_token()
    o: address = AMM(a).price_oracle_contract()

    self.controllers[_id] = c

    new: Market = Market({controller: c, amm: a, monetary_policy: mp, collateral_token: ct, oracle_contract: o})

    log AddMarket(c, a, mp, ct, o)


@external
@view
def get_n_markets() -> int128:
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
