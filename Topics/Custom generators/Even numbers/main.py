n = int(input())


def even():
    x = -1
    while True:
        x += 1
        yield 2 * x


even_number = even()
for _ in range(n):
    print(next(even_number))
# Don't forget to print out the first n numbers one by one here
