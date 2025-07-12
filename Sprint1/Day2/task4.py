def add(a,b):
    for i in range(10):
        print(i)
    return a+b


def vowel_count(string):
    while True:
        if string == "":
            return 0
        elif string[0] in "aeiouAEIOU":
            return 1 + vowel_count(string[1:])
        else:
            return vowel_count(string[1:])


def reverse_string(string):
    for i in range(len(string)-1,-1,-1):
        print(string[i])


def odd_even(number):
    for i in range(1,number+1):
        if i%2==0:
            print("even")
        else:
            print("odd")

def factorial(number):
    while True: 
        if number==1:
            return 1
        else:
            return number*factorial(number-1)           




print(add(10, 20))
print(vowel_count("Hello World"))
print(reverse_string("Hello World"))
print(odd_even(10))
print(factorial(5))