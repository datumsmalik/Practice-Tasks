import pandas as pd


df = pd.read_csv("messy_data (1).csv")




df.columns = df.columns.str.strip().str.lower()



df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

df = df[df['name'].notna()]  


df = df[df['name'].str.lower() != "randomtext"]  




df = df.drop_duplicates()


df['name'] = df['name'].str.title()

df['location'] = df['location'].str.title()


df['age'] = pd.to_numeric(df['age'], errors='coerce')         

df['salary'] = pd.to_numeric(df['salary'], errors='coerce')   


df['salary'].fillna(df['salary'].median(), inplace=True)

df['age'].fillna(df['age'].mean(), inplace=True)



df['notes'].fillna('No notes', inplace=True)


df = df.sort_values(by=['age', 'salary'], ascending=[True, False])


df.reset_index(drop=True, inplace=True)


print("Cleaned and Sorted DataFrame:")



print(df)


df.to_csv("cleaned_sorted_data.csv", index=False)
