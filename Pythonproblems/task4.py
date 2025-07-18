#first non reapearing character in string without built in function

string="aabbcddce"         
for i in string:
    if string.count(i) == 1:
        print(i)
        break 
print("no non reapearing character")    
