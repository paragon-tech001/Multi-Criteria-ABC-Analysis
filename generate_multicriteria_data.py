print('hello world')
import pandas as pd
import numpy as np

np.random.seed(42)

countries = [
    'Nigeria',
    'USA',
    'Australia',
    'Germany',
    'Canada'
]

n_items = 100

products = [f'Product_{i:03d}' for i in range(1, n_items+1)]

row = []

for product in products:
    for country in countries:
        quantity = np.random.randint(10,5000)
        price = np.random.uniform(5,500) # in dollars or any currency
        revenue = quantity * price

        row.append(
            [
                country,
                product,
                quantity,
                round(price, 2),
                round(revenue, 2)
            ]
        )

df = pd.DataFrame(
    row,
    columns = [
        "Country",
        "Description",
        "Quantity",
        "Price",
        "Revenue"
    ]
)

df.to_csv("retail_multicriteria.csv", index = False)
print("We have successfully created the dataset retail_multicriteria.csv")