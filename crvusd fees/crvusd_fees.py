import ape

ape.networks.parse_network_choice('ethereum:mainnet-fork').__enter__()


wsteth = '0x100daa78fc509db39ef7d04de0c1abd299f4c6ce'
wbtc = '0x4e59541306910ad6dc1dac0ac9dfb29bd9f15c67'
weth = '0xa920de414ea4ab66b97da1bfe9e6eca7d4219635'
sfrxeth = '0x8472a9a7632b173c8cf3a86d3afec50c35548e76'

controllers = ["0x100daa78fc509db39ef7d04de0c1abd299f4c6ce", "0x4e59541306910ad6dc1dac0ac9dfb29bd9f15c67", "0xa920de414ea4ab66b97da1bfe9e6eca7d4219635", "0x8472a9a7632b173c8cf3a86d3afec50c35548e76"]

adminFees = 0

fee = []

for i in controllers:
    c = ape.Contract(i)
    adminFees += c.admin_fees()
    fee.append(adminFees)

print(adminFees/10**18)

print("----------------")

print(fee)