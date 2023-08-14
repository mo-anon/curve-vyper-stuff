import boa

unpack = boa.load("tricrypto-unpack.vy", 1000)
simple = boa.load("tricrypto-simple_storage.vy", 1000)

boa.env.enable_gas_profiling()

alice = boa.env.generate_address()

unpack.mid_fee()
simple.get_mid_fee()

print(unpack.line_profile().summary())
print("---------------------")
print(simple.line_profile().summary())

