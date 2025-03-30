n = int(input("Enter the number of Fibonacci series to generate: "))
if n <= 0:
    print("Please enter a positive integer.")
elif n == 1:
    print("Fibonacci series: 0")
else:
    f = [0, 1]
    print("Fibonacci series:")
    print(f[0], f[1], end=" ")
    for i in range(2, n):
        num = f[-1] + f[-2]
        f.append(num)
        print(num, end=" ")  
    print()
