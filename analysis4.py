import pandas as pd
import sqlite3


# load and clean data
df = pd.read_csv('table4.csv')
df['id'] = df['Category'].str.extract('(\d+)').astype(int)
df['use'] = df['Use'].str.lower()
df['leased'] = df['Leased?'].map({'Yes': True, 'No': False})
df['rentable_sf'] = df['Rentable SF'].str.replace(',', '').str.extract('(\d+)').astype(int)
df['annual_rent_psf'] = df['Rent PSF per Year'].str.replace('$', '').astype(int)
df = df[['id', 'use', 'leased', 'rentable_sf', 'annual_rent_psf']]


# connect to db and import data
conn = sqlite3.connect('database.db')
df.to_sql('spaces', conn, if_exists='replace', index=False)
cursor = conn.cursor()


# Q1: total annual rental income for the building
total_annual_rental_income_query = """
SELECT SUM(rentable_sf * annual_rent_psf) AS total_annual_rental_income
FROM spaces
WHERE leased = 1
"""
cursor.execute(total_annual_rental_income_query)
total_annual_rental_income = cursor.fetchone()[0]


# Q2: space that generates the most gross rental income
space_with_most_gross_rental_income_query = """
SELECT id, rentable_sf * annual_rent_psf AS gross_rental_income
FROM spaces
ORDER BY gross_rental_income DESC
LIMIT 1
"""
cursor.execute(space_with_most_gross_rental_income_query)
space_with_most_gross_rental_income = cursor.fetchone()


# Q3: vacancy rate of retail space in the building
vacancy_rate_retail_query = """
SELECT (1.0 - CAST(SUM(CASE WHEN leased = 1 THEN rentable_sf ELSE 0 END) AS FLOAT) / SUM(rentable_sf)) * 100 AS vacancy_rate
FROM spaces
WHERE use = 'retail'
"""
cursor.execute(vacancy_rate_retail_query)
vacancy_rate_retail = cursor.fetchone()[0]


# Q4: average rent per square foot of leased retail spaces in the building
average_rent_per_sf_leased_retail_query = """
SELECT SUM(rentable_sf * annual_rent_psf) / SUM(rentable_sf) AS average_rent_per_sf
FROM spaces
WHERE use = 'retail' AND leased = 1
"""
cursor.execute(average_rent_per_sf_leased_retail_query)
average_rent_per_sf_leased_retail = cursor.fetchone()[0]


# write results to output file
with open('output4.txt', 'w') as f:
    f.write(f"Total annual rental income for the building: ${total_annual_rental_income:,.0f}\n")
    f.write(f"Space that generates the most gross rental income: Space {space_with_most_gross_rental_income[0]}\n")
    f.write(f"Vacancy rate of retail space in the building: {vacancy_rate_retail:.2f}%\n")
    f.write(f"Average rent per square foot of leased retail spaces in the building: ${average_rent_per_sf_leased_retail:,.2f}\n")


# close db connection
conn.close()
