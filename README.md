# Data-Reading-Cleaning-Statistical-Computation-and-Visualization
This Python script performs data reading, cleaning, statistical computation, and visualization generation using various libraries such as os, pandas, and plotly. 


Imports:
```
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
```
os: Provides functions to interact with the operating system, used here for directory operations.
pandas: Used for data manipulation and analysis. It provides data structures like DataFrame which are crucial for handling tabular data.
plotly.express: Simplifies plotting interactive graphs using Plotly.
plotly.graph_objects: Provides more control over plot customization in Plotly.
plotly.subplots: Allows creating subplots in Plotly figures.
plotly.io: Provides functions for exporting Plotly figures to different file formats.

Directory and Data Handling:
```
# Directory containing the CSV files
csv_directory = '/home/runner/csv'
```
Specifies the directory where CSV files are located.

  
Reading and Consolidating Data:
```
def read_and_consolidate_data(directory):
    csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
    data_frames = []

    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file, encoding='ISO-8859-1')
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue
        data_frames.append(df)

    consolidated_data = pd.concat(data_frames, ignore_index=True)
    return consolidated_data
```

read_and_consolidate_data(directory):
Takes a directory path (directory) as input.
Iterates through all CSV files in the directory.
Attempts to read each CSV file into a Pandas DataFrame (df), handling encoding issues.
Appends each DataFrame to data_frames.
Concatenates all DataFrames in data_frames into consolidated_data and returns it.


Data Cleaning:
```
def clean_data(df):
    print("Columns in DataFrame:", df.columns)

    required_columns = {
        'date': 'ORDERDATE',
        'sales_amount': 'SALES',
        'product_category': 'PRODUCTLINE',
        'customer_id': 'ORDERNUMBER'
    }

    missing_columns = [col for col in required_columns.values() if col not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing columns in DataFrame: {missing_columns}")

    df = df.rename(columns={v: k for k, v in required_columns.items()})

    df['date'] = pd.to_datetime(df['date'])
    df['sales_amount'] = pd.to_numeric(df['sales_amount'])

    df = df.dropna()

    return df
```

clean_data(df):
Takes a DataFrame (df) as input.
Checks for required columns ('ORDERDATE', 'SALES', 'PRODUCTLINE', 'ORDERNUMBER') and renames them to standardized names ('date', 'sales_amount', 'product_category', 'customer_id').
Converts 'date' column to datetime format and 'sales_amount' column to numeric format.
Drops rows with any missing values (NaN).


Computing Aggregate Statistics:
```
def compute_statistics(df):
    total_sales = df['sales_amount'].sum()
    df['month'] = df['date'].dt.to_period('M')
    average_sales_per_month = df.groupby('month')['sales_amount'].mean()
    sales_by_category = df.groupby('product_category')['sales_amount'].sum()
    return total_sales, average_sales_per_month, sales_by_category
```

compute_statistics(df):
Takes cleaned DataFrame (df) as input.
Computes total sales (total_sales) by summing 'sales_amount'.
Adds a 'month' column derived from 'date' and aggregates average monthly sales (average_sales_per_month).
Computes total sales by 'product_category' (sales_by_category).


Generating Visualizations:
```
def generate_visualizations(df, avg_sales_per_month, sales_by_category):
    fig = make_subplots(rows=3, cols=1, subplot_titles=('Sales Over Time', 'Sales by Product Category', 'Regional Sales Comparisons'))

    sales_over_time = df.groupby('date')['sales_amount'].sum()
    fig.add_trace(go.Line(x=sales_over_time.index, y=sales_over_time.values, name='Sales Over Time'), row=1, col=1)

    fig.add_trace(go.Bar(x=sales_by_category.index, y=sales_by_category.values, name='Sales by Product Category'), row=2, col=1)

    if 'COUNTRY' in df.columns:
        sales_by_region = df.groupby('COUNTRY')['sales_amount'].sum()
        fig.add_trace(go.Bar(x=sales_by_region.index, y=sales_by_region.values, name='Sales by Region'), row=3, col=1)
    else:
        print("Column 'COUNTRY' not found in DataFrame. Skipping regional sales comparisons.")

    fig.update_layout(height=800, title_text="Sales Data Analysis")
    return fig
```

generate_visualizations(df, avg_sales_per_month, sales_by_category):
Takes cleaned DataFrame (df), average sales per month (avg_sales_per_month), and sales by category (sales_by_category) as inputs.
Creates a subplot (fig) with three plots:
Line plot ('Sales Over Time') of total sales over time.
Bar plot ('Sales by Product Category') showing sales by product category.
Bar plot ('Sales by Region') showing sales by region if 'COUNTRY' column exists in df.
Updates layout with a specified height and title.


Exporting Data and Visualizations:
```
def export_data_and_visualizations(df, fig):
    df.to_csv('cleaned_sales_data.csv', index=False)

    pio.write_image(fig, 'sales_visualizations.png')
```

export_data_and_visualizations(df, fig):
Takes cleaned DataFrame (df) and generated figure (fig) as inputs.
Writes df to a CSV file ('cleaned_sales_data.csv') without row indices.
Saves fig as an image ('sales_visualizations.png').


Main Execution:
```
if __name__ == '__main__':
    data = read_and_consolidate_data(csv_directory)

    try:
        cleaned_data = clean_data(data)
        total_sales, avg_sales_per_month, sales_by_category = compute_statistics(cleaned_data)

        print(f'Total Sales: {total_sales}')
        print(f'Average Sales per Month: {avg_sales_per_month}')
        print(f'Sales by Product Category: {sales_by_category}')

        fig = generate_visualizations(cleaned_data, avg_sales_per_month, sales_by_category)
        export_data_and_visualizations(cleaned_data, fig)

    except Exception as e:
        print(f"Error occurred: {e}")
```


Main Execution (if __name__ == '__main__':):
Executes the script when it is run directly (not imported as a module).
Reads and consolidates CSV data from csv_directory.
Cleans the data, computes statistics, generates visualizations, and exports cleaned data and visualizations.
Catches and prints any exceptions that occur during execution.

Summary:
This script demonstrates a complete workflow for handling multiple CSV files, cleaning and processing data using Pandas, generating interactive visualizations with Plotly, and exporting results. It's structured to handle errors gracefully and provides detailed output during execution. Each function serves a specific purpose, from data loading to visualization creation, ensuring clarity and maintainability in data analysis tasks.






