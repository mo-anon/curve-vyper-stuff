import boa

t = boa.load("simple.vy")

boa.env.enable_gas_profiling()

alice = boa.env.generate_address()

t.add(1, 2)

print(t.line_profile().summary())

