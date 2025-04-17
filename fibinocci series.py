n = int(input("Enter the number of Fibonacci series to generate: "))
if n <= 0:
    print("Please enter a positive integer.")
elif n == 1:
    print("Fibonacci series: 0")
else:
    f = [0, 1]
    for i in range(2, n):
        f.append(f[-1] + f[-2])
    print("Fibonacci series:")
    print(" ".join(map(str, f)))
