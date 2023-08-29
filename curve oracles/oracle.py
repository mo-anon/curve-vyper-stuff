import ape
from ape import chain, networks
import math


# fork eth mainnet
ape.networks.parse_network_choice('ethereum:mainnet-fork').__enter__()


# contract addresses 
price_oracle_contract = ape.Contract('0xc1793A29609ffFF81f10139fa0A7A444c9e106Ad')
TRICRYPTO = ["0x7F86Bf177Dd4F3494b841a37e810A34dD56c829B", "0xf5f5B97624542D72A9E06f04804Bf81baA15e2B4"]
STABLESWAP = ["0x4DEcE678ceceb27446b35C672dC7d61F30bAD69E", "0x390f3595bCa2Df7d23783dFd126427CCeb997BF4"]
STAKEDSWAP = ape.Contract("0x21E27a5E5513D6e65C4f830167390997aA84843a")
WSTETH = ape.Contract("0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0")
stable_agg = ape.Contract("0x18672b1b0c623a30089A280Ed9256379fb0E4E62")


# aggregate needed variables
N_POOLS = price_oracle_contract.N_POOLS()
last_timestamp = price_oracle_contract.last_timestamp()
block_timestamp = chain.provider.get_block("latest").timestamp
TVL_MA_TIME = price_oracle_contract.TVL_MA_TIME()


# empty lists to store tvls in 
last_tvl = []
last_tvl_new = []


#EMA TVLS

# last_tvl stored in last_tvl list. this is used if last_timestamp < block_timestamp
for i in range (0, N_POOLS):
    x = price_oracle_contract.last_tvl(i)
    last_tvl.append(x)


# calculates new last_tvl and stores it in last_tvl_new list.
if last_timestamp < block_timestamp:
    # alpha is a smoothing factory for the tvls
    alpha = float(math.exp(-(block_timestamp - last_timestamp) * 10**18 / TVL_MA_TIME))

    for i in range(0, N_POOLS):
        tri = ape.Contract(TRICRYPTO[i])
        tvl = tri.totalSupply() * tri.virtual_price() / 10**18
        last_tvl_calc = (tvl * (10**18 - alpha) + last_tvl[i] * alpha) / 10**18
        last_tvl_new.append(last_tvl_calc)



# PRICE

weighted_price = 0
weights = 0


for i in range(0, N_POOLS):
    tri = ape.Contract(TRICRYPTO[i])
    stable = ape.Contract(STABLESWAP[i])
    p_crypto_r = tri.price_oracle(1)
    p_stable_r = stable.price_oracle()
    p_stable_agg = stable_agg.price()
    if last_timestamp < block_timestamp:
        weight = last_tvl_new[i]
    else:
        weight = last_tvl[i]
    weights += weight

    weighted_price += p_crypto_r * p_stable_agg / p_stable_r * weight

p_eth = (weighted_price / weights) / 10**18
print(p_eth)


p_staked = STAKEDSWAP.price_oracle()

p_staked = min(p_staked, 10**18) * WSTETH.stEthPerToken() / 10**18

p_final = p_staked * p_eth / 10**18


print("--------")
print("FINAL WSTETH PRICE:")
print(p_final)
print("--------")


# clear last_tvl_new list as its not needed anymore and needs to be empty to not fuck up the calculation when calling again
last_tvl_new.clear()