import pandas as pd


df = pd.read_csv("messy_data (1).csv")


#1
df.columns = df.columns.str.strip().str.lower()

#2
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


# 3
df = df[df['name'].notna()]        


df = df[df['name'] != "RandomText"]             

# 4

df = df.drop_duplicates()

# 5

df['name'] = df['name'].str.title()
df['location'] = df['location'].str.title()

# 6

df['age'] = pd.to_numeric(df['age'], errors='coerce')      

df['salary'] = pd.to_numeric(df['salary'], errors='coerce')  


df['salary'].fillna(df['salary'].median(), inplace=True)


df['age'].fillna(df['age'].mean(), inplace=True)


df['notes'].fillna('No notes', inplace=True)


print("Cleaned DataFrame:")
print(df)


df.to_csv("cleaned_data.csv", index=False)
