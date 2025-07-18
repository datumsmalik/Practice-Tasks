#Find max and min numebers from list without built in function

num = [4,2,9,1,7,5]

# pehle index ko max or min consider kr lia he or puri list se compare kr k
max = num[0]
min = num[0]

for i in num:
    if i > max:
        max = i
    if i < min:
        min = i

print(f"max number ye ho ksta he  {max}")
print(f"min number ye ho ksta he  {min}")

