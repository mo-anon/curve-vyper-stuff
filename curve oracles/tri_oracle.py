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

N_POOLS = price_oracle_contract.N_POOLS()
block = chain.provider.get_block("latest").number
print(block)
print(type(block))


p_eth_usdc = []
p_eth_usdt = []

"""# get eth price in tricrypto pools at a certain block height
for i in range(0, N_POOLS): 
    contract = ape.Contract(TRICRYPTO[i])
    print(TRICRYPTO[i])
    for i in range(18034917, 18034927):
        x = contract.price_oracle(1, block_id=i) / 1e18
        p_eth_usdc.append(x)
        print(x)
    print("------")"""




# get eth/usdc from tricrypto ("0x7F86Bf177Dd4F3494b841a37e810A34dD56c829B") at a specific block range
for i in range(17963625, 18035055, 7143):
    contract = ape.Contract(TRICRYPTO[0])
    x = contract.price_oracle(1, block_id=i) / 1e18
    p_eth_usdc.append(x)




# get eth/usdt from tricrypto ("0x7F86Bf177Dd4F3494b841a37e810A34dD56c829B") at a specific block range
for i in range(17963625, 18035055, 7143):
    contract = ape.Contract(TRICRYPTO[1])
    x = contract.price_oracle(1, block_id=i) / 1e18
    p_eth_usdt.append(x)


print("---")
print(p_eth_usdc)
print("---")
print(p_eth_usdt)
print("---")
