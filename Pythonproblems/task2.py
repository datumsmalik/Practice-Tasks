#sort disctionary by value in descending order without built in function
dict = {'alice': 50,'bob': 75,'charlie': 60}

#dict ko list me convert kr lete hain pehle take hamain dic k 2nd member ki access ho jae
list = list(dict.items())



#lamda function use kr k sort kr lete hain
list.sort(key=lambda x: x[1], reverse=True)  # reverse=True means ulta print k sab se bara number pehle de dai ga

# ab list ko dict me convert krt hai    
#dict = dict(list)
dict={index:value for index,value in list}
print(dict)