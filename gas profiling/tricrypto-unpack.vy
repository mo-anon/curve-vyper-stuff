# @version 0.3.9

packed_fee_params: public(uint256)  # <---- Packs mid_fee, out_fee, fee_gamma.

@external
def __init__(_packed_fee_params: uint256):
    self.packed_fee_params = _packed_fee_params


@internal
@view
def _unpack(_packed: uint256) -> uint256[3]:
    """
    @notice Unpacks a uint256 into 3 integers (values must be <= 10**18)
    @param val The uint256 to unpack
    @return uint256[3] A list of length 3 with unpacked integers
    """
    return [
        (_packed >> 128) & 18446744073709551615,
        (_packed >> 64) & 18446744073709551615,
        _packed & 18446744073709551615,
    ]

@view
@external
def mid_fee() -> uint256:
    """
    @notice Returns the current mid fee
    @return uint256 mid_fee value.
    """
    return self._unpack(self.packed_fee_params)[0]