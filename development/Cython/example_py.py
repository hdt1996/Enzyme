import timeit

t_start = timeit.default_timer()
def test(x):
    y = 0
    for i in range(x):
        y+=i
    print(x)
    return y

test(10000000000)
print(timeit.default_timer() - t_start)