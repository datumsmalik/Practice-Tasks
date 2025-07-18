#group by product and sum the quantity mene key value logic bna k kia he 


orders=[
    {"product":"apple","quantity":5},
    {"product":"banana","quantity":2},
    {"product":"apple","quantity":3},
]

key = "product"
value = "quantity"

#order list ko iterate kro agar to product already he grouping vali dictionery me to uski quantity ko add kro 
# or agar prouct nahi he grouping vali dictionery me to to product ko add or us ki quantity ko dic me add kro
grouping = {}
for i in orders:
    if i[key] in grouping:
        grouping[i[key]] += i[value]
    else:
        grouping[i[key]] = i[value]

print(grouping)
