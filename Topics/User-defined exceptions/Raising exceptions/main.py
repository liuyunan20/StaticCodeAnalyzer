class NegativeSumError(Exception):
    def __str__(self):
        return "Sum is negative!"


def sum_with_exceptions(a, b):
    if a + b < 0:
        raise NegativeSumError
    else:
        return a + b
