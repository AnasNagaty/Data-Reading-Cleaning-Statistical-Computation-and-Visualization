import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Directory containing the CSV files
csv_directory = '/home/runner/csv'

# Read and consolidate data from multiple CSV files
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

# Data cleaning
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

# Compute aggregate statistics
def compute_statistics(df):
    total_sales = df['sales_amount'].sum()
    df['month'] = df['date'].dt.to_period('M')
    average_sales_per_month = df.groupby('month')['sales_amount'].mean()
    sales_by_category = df.groupby('product_category')['sales_amount'].sum()
    return total_sales, average_sales_per_month, sales_by_category

# Generate interactive visualizations
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

# Export cleaned data and visualizations
def export_data_and_visualizations(df, fig):
    df.to_csv('cleaned_sales_data.csv', index=False)

    pio.write_image(fig, 'sales_visualizations.png')

# Main execution
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
