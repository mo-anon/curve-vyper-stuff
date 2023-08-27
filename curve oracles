crvUSD markets primarily utilize internal oracles to determine the price of the collateral. There is a possibility to use Chainlink oracle prices as safety limits.

The main function in terms of calculating the oracle price of the collateral is the internal function`_raw_price()` and `_ema_tvl()`.
!!!warning
    Every market has its own individual price oracle contract, which can be fetched by calling `price_oracle_contract` within the controller of the market. The [wstETH oracle](https://etherscan.io/address/0xc1793A29609ffFF81f10139fa0A7A444c9e106Ad#code) will be used for the purpose of this documentation. Please be aware that oracle contracts can vary based on the collateral token.

not much functions to call. what can be changed? lots of immutable variables

!!!tip
    The formulas below use slightly different terminologies than in the code itself to make them easier to read.  
    For abbreviations, see [here](#terminology-used-in-code).


- Stableswap pools: crvUSD/USDC and crvUSD/USDT
- Tricrypto pools: tricryptoUSDC and tricryptoUSDT
- Stableswap aggregator is the contract that aggregates the price of crvUSD

when is price oracle updated? every exchange in AMM which is when internal function `_price_oracle_w()` is called.

!!!note
    The formulas above use slightly different terminologies than in the code itself to make it easier to read.  
    For abreviations see [here](#terminology-used-in-code).

## **EMA of TVL**
`_ema_tvl()` calculates the exponential moving average of the total value locked of `TRICRYPTO[i]`. 
This value is later on used in the internal function `_raw_price()` to further compute the weighted price of the collateral.
`_ema_tvl()` calculates the exponential moving average of the total value locked (TVL) for `TRICRYPTO[i]` and returns `last_tvl[i]`, which represents the Exponential Moving Average (EMA) of the TVL of the Tricrypto pool at index i. This variable is updated every time `price_w()` is called and $last_{timestamp} < block.timestamp$. If the latter condition is not met, it will simply return last_tvl.

This function returns `last_tvl[i]`, which represents the ema tvl of the pool. This variable is updated everytime when calling `price_w()` and $last_{timestamp} < block.timestamp$.
This value is subsequently used in the internal function `_raw_price()` to compute the weighted price of ETH.

The function only re-calculates the ema tvl when $last_{timestamp} < block.timestamp$, otherwise it will just return `last_tvl` again as it is still the same timestamp. 

??? quote "`_ema_tvl() -> uint256[N_POOLS]:`"

@@ -50,7 +41,7 @@ The function only re-calculates the ema tvl when $last_{timestamp} < block.times


### *Calculate Smoothing Factor (α)*
When calculating the smoothing factor $\alpha$, the formula is converted to an int256 because `exp()` requires an int256 as input.
When calculating the smoothing factor, represented as $\alpha$, the formula is converted to an int256 type because the exp() function requires an int256 as its input.


$$\alpha = \exp{-\frac{(block.timestamp - \text{last_timestamp}) * 10^{18}}{\text{TVL_MA_TIME}}}$$
@@ -63,16 +54,14 @@ $\text{last_timestamp} = \text{last timestamp when}$ `price_w()` $\text{was call
$\text{TVL_MA_TIME} =$ `TVL_MA_TIME`  

!!!info
    alpha values can range between 1 and 0:     
    alpha values can range between 1 and 0, depening on the time passed since calling:     
    $\alpha = 1.0$ when $\delta t = 0$    
    $\alpha = 0.0$ when $\delta t = \infty$

-----------------------------

### *Calculate TVLs*

After computing $\alpha$, the function calculates the `tvl` of the Tricrypto pools. It does this by iterating through all the pools stored in `TRICRYPTO` (currently tricryptoUSDC and tricryptoUSDT), fetching the `totalSupply`, and multiplying it by the `virtual_price`.
It essentially computes the `weight`, which is later on user in `_raw_prices()` to obtain the final price.
After computing $\alpha$, the function calculates the TVL for the Tricrypto pools. It accomplishes this by iterating through all the pools stored in `TRICRYPTO` (tricryptoUSDC and tricryptoUSDT), fetching its `totalSupply`, and multiplying it by the `virtual_price`. This process essentially computes the **weight**, which is subsequently used in `_raw_prices()` to determine the final price.

$$tvl_{i} = \frac{TS_i * VP_i}{10^{18}}$$

@@ -84,8 +73,7 @@ $VP_i = \text{virtual price of i-th pool}$ in `TRICRYPTO[N_POOLS]`

-----------------------------


In the last step `tvl` get smoothend out with $\alpha$ and `last_tvl` is obtained.
In the last step, TVL is smoothed out using $\alpha$, and `last_tvl` is obtained.

$$\text{last_tvl}_i = \frac{tvl_i * (10^{18} - \alpha) + \text{last_tvl}_i * \alpha}{10^{18}}$$

@@ -144,8 +132,7 @@ $\text{last_tvl}_i = \text{total value locked of i-th pool}$ in `TRICRYPTO[N_POO


## **Calculate Raw Price**

This function requires `tvl´ (which was calculated in the step above) and `agg_price` ((which essential is `STABLESWAP_AGGREGATOR.price()`) as input to calculate the raw price of the collateral.
`_raw_price()` calculates the raw price of the collateral. The function requires the inputs `tvls` (from `_ema_tvl()`) and `agg_price` (from `STABLESWAP_AGGREGATOR.price()`).

??? quote "`_raw_price(tvls: uint256[N_POOLS], agg_price: uint256) -> uint256:`"

@@ -196,15 +183,15 @@ This function requires `tvl´ (which was calculated in the step above) and `agg_

-----------------------------

The function iterates over `N_POOLS` and obtains the following values:
The function iterates over the range of `N_POOLS` and obtains the following values:

- $\text{p_crypto_r} =$ price oracle of eth in the tricrypto pools w.r.t usdc/usdt  
- $\text{p_stable_r} =$ price oracle of stableswap pool  
- $\text{p_crypto_r} =$ price oracle of crvusd   

$$\text{eth_weighted_price} = \text{eth_weighted_price} + (\frac{\text{p_crypto_r} * \text{p_stable_agg}}{\text{p_stable_r}}) * weight$$

While looping through the pools, the variables `weighted_price` and `weights` are summed up of the individual pool's values, which means they represent the sum across all `N_POOLS`.
While looping through the pools, the variables `weighted_price` and `weights` accumulate the values from each individual pool, representing the total sum across all `N_POOLS`.

The **total weighted price of ETH** is then obtained by dividing `weighted_price` by `weights`.

@@ -221,17 +208,13 @@ Now, the **price of stETH w.r.t ETH** is obtained by calling the `price_oracle()

$\text{p_staked} =$ `STAKEDSWAP.price_oracle()`

limit the stETH price: minimum of steth price and 1 eth, because 1 steth can always be redeemed for 1 eth, so we assume 10^18 is the minimum price. then we multiply whatever value is smaller by WSTETH.stEthPerToken() to calculate how much steth it really is, as we provide wsteth (is worth more than steth because its rebasing).

Next, the price of stETH is limited. It takes the minimum value of either the price of steth in the curve pool or 1. This is done because if stETH price in the pool is > 1, there is an arb opportunity to exchange eth for steth 1:1 and then sell it in the pool, which should drive exchange rate back down to 1.

------------------------
Next, the price of stETH w.r.t ETH is capped. It's determined by taking the lesser value between the price of stETH in the curve pool and 1. This adjustment is necessary because if the stETH price in the pool exceeds 1, it creates an arbitrage opportunity. Traders could convert ETH for stETH at a 1:1 ratio and then sell it in the pool, which should push the exchange rate back down to 1.

This limited value is then multiplied by `WSTETH.stEthPerToken()` which is the ratio of wsteth and steth.
This capped value is then multiplied by `WSTETH.stEthPerToken()`, which represents the ratio between wstETH and stETH.

$$\text{p_staked} = min(\text{p_staked}, 10^{18}) * \frac{WSTETH.stEthPerToken()}{10**{18}}$$

Final step: the limited value of p_staked is then multiplied by the price of eth calculated above and then divided by the number of decimals ($10^{18}$).
In the final step, the obtained value of `p_staked` is multiplied by the weighted price of ETH, as calculated earlier, and then divided by the number of decimals (represented by $10^{18}$.


### `raw_price`
@@ -301,7 +284,7 @@ Final step: the limited value of p_staked is then multiplied by the price of eth
        ```

## **Chainlink Limits**
The oracle contracts have the possibility to make use of chainlink prices which act as saftey limits. When toggled on, these limitations essentially hit when the chainlink price deviates more than 1.5% (`BOUND_SIZE`) from the internal price oracles.
The oracle contracts have the option to utilize Chainlink prices, which serve as safety limits. When enabled, these limits are triggered if the Chainlink price deviates by more than 1.5% (represented by `BOUND_SIZE`) from the internal price oracles.

Chainlink limits can be turned on and off by calling `set_use_chainlink(do_it: bool)`, which can only be done by the admin of the factory contract.

@@ -421,7 +404,7 @@ Chainlink limits can be turned on and off by calling `set_use_chainlink(do_it: b

    ??? quote "Source code"

        ```python hl_lines="3"
        ```python hl_lines="1"
        N_POOLS: public(constant(uint256)) = 2
        ```

@@ -550,7 +533,7 @@ Chainlink limits can be turned on and off by calling `set_use_chainlink(do_it: b
        >>> Oracle.STABLECOIN()
        '0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E'
        ```
        
