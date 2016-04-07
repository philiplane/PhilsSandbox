import fibonacci

thisFib = fibonacci.fib
thisFib2 = fibonacci.fib2


def main():
    print("this is our first test script file")
    print(fibonacci.__name__)
    thisFib(1000)
    print(thisFib2(100))
main()
