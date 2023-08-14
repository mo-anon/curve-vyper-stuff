# @version 0.3.9

mid_fee: public(uint256)

@external
def __init__(_mid_fee: uint256):
    self.mid_fee = _mid_fee



@view
@external
def get_mid_fee() -> uint256:
    """
    @notice Returns the current mid fee
    @return uint256 mid_fee value.
    """
    return self.mid_fee

