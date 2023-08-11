from web3 import Web3
import utils
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/API_KEY'))
print(w3.is_connected())

contractABI = utils.mp_wsteth_abi
contractAddress = '0x1E7d3bf98d3f8D8CE193236c3e0eC4b00e32DaaE'
contract = w3.eth.contract(address=contractAddress, abi=contractABI)


deploy_block = 17382275
_current_block = w3.eth.block_number
current_block = _current_block
n_blocks = 0
total_rate = 0
block = []
rates = []

for i in range(deploy_block, current_block, 7143):
    result = contract.functions.rate().call(block_identifier=i)
    rate_percentage = (1 + result/10**18)**(365*24*60*60) - 1
    block.append(i)
    rates.append(rate_percentage)
    total_rate += result
    n_blocks += 1

    avg_rate = total_rate / n_blocks
    print(avg_rate)

print(rates)
print(block)

cumsum = [sum(rates[:i+1])/(i+1) for i in range(len(rates))]
plt.plot(block, cumsum, label='1d average', color='orange')


plt.plot(block, rates)
plt.title('wstETH interest rate')
plt.xlabel('block')
plt.ylabel('rate')
plt.legend()
plt.grid(True)
plt.show()

"""
print("---------------")
avg_rate = total_rate / n_blocks
print(avg_rate)
print(n_blocks)

avg_annual_rate = (1 + avg_rate/10**18)**(365*24*60*60) - 1
print(avg_annual_rate)
"""