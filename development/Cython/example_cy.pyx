import timeit

t_start = timeit.default_timer()
cpdef int test(long long int x):
    cdef long long int y = 0
    cdef long long int i
    for i in range(x):
        y+=i
    print(x)
    return y

test(10000000000)
print(timeit.default_timer() - t_start)