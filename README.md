# 🎯 Multi-Criteria Inventory Classification with Python

## 📖 Overview

Traditional ABC Analysis classifies inventory using a single criterion—typically annual consumption value. While effective, modern supply chains often require decisions based on multiple factors rather than cost alone.

Multi-Criteria Inventory Classification extends the traditional ABC approach by evaluating inventory items using several performance indicators simultaneously, such as revenue, demand frequency, profitability, lead time, criticality, or other business-specific metrics. This provides a more comprehensive and realistic prioritization of inventory, enabling better procurement, stocking, and operational decisions.

In this project, an end-to-end Multi-Criteria Inventory Classification is implemented in Python using Pandas and Matplotlib, from data preparation and criteria weighting to scoring, ranking, visualization, and export.

---

## 🎯 Project Objectives

This project demonstrates how to:

- Prepare and clean inventory data for multi-criteria evaluation.
- Select and analyze multiple decision criteria relevant to inventory performance.
- Normalize the criteria to ensure fair comparison.
- Apply weights to each criterion based on business priorities.
- Compute a composite score for every inventory item.
- Rank inventory items according to their overall importance.
- Classify inventory into priority groups for improved inventory management.
- Visualize the classification using professional charts.
- Export the classified inventory dataset for further reporting and decision-making.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib

## 📊 Loading the Dataset

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

df = pd.read_csv('retail_multicriteria.csv')
df.head()

```

| Country | Description | Quantity | Price | Revenue |
|---------|-------------|---------:|------:|--------:|
| Nigeria | Product_001 | 870 | 95.80 | 83,346.19 |
| USA | Product_001 | 3,782 | 300.44 | 1,136,267.21 |
| Australia | Product_001 | 476 | 54.49 | 25,936.09 |
| Germany | Product_001 | 3,454 | 302.55 | 1,045,014.37 |
| Canada | Product_001 | 140 | 15.19 | 2,126.51 |
| Nigeria | Product_002 | 779 | 362.39 | 282,301.34 |
| USA | Product_002 | 2,443 | 95.00 | 232,093.21 |
| Australia | Product_002 | 1,194 | 155.60 | 185,786.29 |
| Germany | Product_002 | 4,127 | 8.50 | 35,070.51 |
| Canada | Product_002 | 2,914 | 149.16 | 434,647.65 |

## 📊 Aggragating the Data

```python
df.head()

grouped = df.groupby("Description").agg(
    total_sales = ("Quantity", 'sum'),
    total_revenue = ('Revenue', "sum")
).reset_index()

grouped

```
| Description | Total Sales | Total Revenue |
|-------------|------------:|--------------:|
| Product_001 | 8,722 | 2,292,690.37 |
| Product_002 | 11,457 | 1,169,899.00 |
| Product_003 | 8,787 | 1,996,905.15 |
| Product_004 | 12,852 | 3,475,321.75 |
| Product_005 | 9,642 | 1,102,118.78 |
| Product_006 | 13,816 | 4,203,148.67 |
| Product_007 | 14,978 | 3,106,976.71 |
| Product_008 | 12,058 | 3,009,257.07 |
| Product_009 | 15,167 | 3,250,684.68 |
| Product_010 | 11,417 | 3,494,797.57 |

## 📊 Create a reusable ABC Function

```python
def abc_classification(series):
    df_temp = pd.DataFrame(
        {'metrics': series})
    
    df_temp = df_temp.sort_values(
        by = "metrics",
        ascending= False
    )
    df_temp['cummulative_percentage'] = (df_temp['metrics'].cumsum() / df_temp['metrics'].sum())

    def classifier(values):
        if values <= 0.8:
            return 'A'
        elif values <= 0.95:
            return 'B'
        return 'C'
    
    df_temp['ABC'] = df_temp['cummulative_percentage'].apply(classifier)

    return df_temp['ABC']
print("Function abc_classification successfully created")

```
## 📊 ABC Analysis on Sales

``` python

sales_df = grouped.copy()
sales_df = sales_df.sort_values('total_sales', ascending= False)

sales_df['Sales_abc'] = abc_classification(sales_df['total_sales'])

print(sales_df.sample(10))

```

| Description | Total Sales | Total Revenue | Sales ABC |
|-------------|------------:|--------------:|:---------:|
| Product_012 | 8,891 | 2,706,574.84 | B |
| Product_031 | 16,469 | 2,861,821.85 | A |
| Product_042 | 10,873 | 3,651,203.53 | B |
| Product_072 | 13,196 | 4,498,459.13 | A |
| Product_067 | 14,206 | 3,239,306.65 | A |
| Product_014 | 13,359 | 3,445,665.43 | A |
| Product_011 | 4,036 | 667,462.84 | C |
| Product_099 | 10,569 | 1,614,102.37 | B |
| Product_009 | 15,167 | 3,250,684.68 | A |
| Product_034 | 7,022 | 1,466,561.46 | C |


## 📊 ABC on Revenue
```python
revenue_df = grouped.copy()
revenue_df = revenue_df.sort_values('total_revenue', ascending= False)

revenue_df['Revenue_abc'] = abc_classification(sales_df['total_revenue'])

print(revenue_df.sample(10))

```

| Description | Total Sales | Total Revenue | Revenue ABC |
|-------------|------------:|--------------:|:-----------:|
| Product_100 | 14,988 | 5,351,557.82 | A |
| Product_065 | 9,906 | 2,631,467.15 | B |
| Product_062 | 16,107 | 6,551,435.69 | A |
| Product_054 | 8,767 | 2,925,045.49 | A |
| Product_053 | 13,852 | 5,234,102.84 | A |
| Product_036 | 17,479 | 3,535,532.03 | A |
| Product_011 | 4,036 | 667,462.84 | C |
| Product_018 | 10,567 | 3,019,391.10 | A |
| Product_067 | 14,206 | 3,239,306.65 | A |
| Product_086 | 14,670 | 5,156,916.86 | A |

## 📊 Merge Results

```python
# to merge the result for sales 

final_df = grouped.merge(sales_df[['Description', 'Sales_abc']], on = 'Description')

final_df = final_df.merge(revenue_df[['Description', 'Revenue_abc']], on = 'Description')

# to create a product mix along the line

final_df['Product_mix'] = final_df['Sales_abc'] + final_df['Revenue_abc']

print(final_df.sample(10))

```

| Description | Total Sales | Total Revenue | Sales ABC | Revenue ABC | Product Mix |
|-------------|------------:|--------------:|:---------:|:-----------:|:-----------:|
| Product_026 | 13,193 | 3,288,767.34 | A | A | AA |
| Product_007 | 14,978 | 3,106,976.71 | A | A | AA |
| Product_008 | 12,058 | 3,009,257.07 | A | A | AA |
| Product_009 | 15,167 | 3,250,684.68 | A | A | AA |
| Product_055 | 12,563 | 2,384,685.45 | A | B | AB |
| Product_030 | 12,951 | 2,661,369.33 | A | A | AA |
| Product_031 | 16,469 | 2,861,821.85 | A | A | AA |
| Product_049 | 14,278 | 4,116,475.33 | A | A | AA |
| Product_083 | 9,622 | 2,580,048.63 | B | B | BB |
| Product_070 | 11,319 | 1,939,172.88 | A | B | AB |


## 📊 Visualizations: Count of Product Mix

``` python
plt.figure(figsize=(10, 7))

sns.set_theme(style="whitegrid")

ax = sns.countplot(
    data=final_df,
    y='Product_mix',
    order=final_df['Product_mix'].value_counts().index
)

# Add count labels
for p in ax.patches:
    ax.annotate(
        f'{int(p.get_width())}',
        (p.get_width() + 0.3,
         p.get_y() + p.get_height() / 2),
        ha='left',
        va='center',
        fontsize=10
    )

plt.title('Product Mix Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Number of Sales', fontsize=12)
plt.ylabel('Product Mix', fontsize=12)

sns.despine()

plt.tight_layout()
plt.show()

```
![](https://github.com/paragon-tech001/Multi-Criteria-ABC-Analysis/blob/main/Product%20Mix%20Distribution.png)

## 📊 Visualization: Revenue by Product Mix

```python

print(final_df["Product_mix"].value_counts())

```

| Product Mix | Count |
|:-----------:|------:|
| AA | 56 |
| AB | 11 |
| BA | 9 |
| BB | 7 |
| CC | 6 |
| BC | 4 |
| CB | 3 |
| AC | 3 |
| CA | 1 |

```python

plt.figure(figsize=(10, 7))

sns.set_theme(style="whitegrid")

sns.barplot(
    y='Product_mix',
    x='total_revenue',
    data=final_df.sort_values('total_revenue', ascending=False),
    errorbar=None
)

plt.title('Revenue by Product Mix', fontsize=16, fontweight='bold')
plt.xlabel('Total Revenue', fontsize=12)
plt.ylabel('Product Mix', fontsize=12)

sns.despine()

plt.tight_layout()
plt.show()

```
![](https://github.com/paragon-tech001/Multi-Criteria-ABC-Analysis/blob/main/Revenue%20by%20Product%20Mix.png)

## 📊 Store-Level Analysis

```python

by_store = (

    df.groupby(
        ["Country",
         "Description"]
    )

    .agg(
        total_sales=("Quantity","sum"),
        total_revenue=("Revenue","sum")
    )

    .reset_index()

)

# to display all the rows in the dataframe

pd.set_option('display.max_rows', None)


print(by_store.sample(10))

```

| Country | Description | Total Sales | Total Revenue |
|---------|-------------|------------:|--------------:|
| Australia | Product_078 | 2,048 | 815,458.87 |
| USA | Product_099 | 1,318 | 281,531.59 |
| USA | Product_006 | 1,031 | 270,569.11 |
| Nigeria | Product_084 | 2,253 | 646,825.92 |
| Germany | Product_030 | 2,960 | 749,621.67 |
| USA | Product_062 | 4,540 | 2,052,351.37 |
| Canada | Product_089 | 1,342 | 229,378.18 |
| Canada | Product_085 | 1,844 | 556,002.02 |
| Australia | Product_079 | 2,645 | 509,739.51 |
| USA | Product_048 | 1,227 | 55,543.40 |
