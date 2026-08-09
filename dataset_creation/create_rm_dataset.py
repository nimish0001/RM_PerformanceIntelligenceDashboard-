# ==================== Google Colab Setup ====================
# @title Install required packages
!pip install faker pandas numpy

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os
from google.colab import files
import zipfile
from IPython.display import display, HTML
import base64
import warnings
warnings.filterwarnings('ignore')

# Initialize Faker
fake = Faker()

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Constants
NUM_RM = 250
NUM_CUSTOMERS = 2500
NUM_LOANS = 10000
NUM_TRANSACTIONS = 15000
NUM_COMPLAINTS = 2500

# RM Names and Cities - Predefined for variety
rm_names = [fake.name() for _ in range(NUM_RM)]
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 
          'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']

# Helper functions to generate messy data
def generate_messy_date(start_date, end_date):
    """Generate dates with some null values and invalid formats"""
    if random.random() < 0.05:  # 5% chance of null
        return np.nan
    date = fake.date_between(start_date=start_date, end_date=end_date)
    # Sometimes return in different formats
    format_choice = random.random()
    if format_choice < 0.7:
        return date.strftime('%Y-%m-%d')
    elif format_choice < 0.85:
        return date.strftime('%d/%m/%Y')
    else:
        return date.strftime('%m-%d-%Y')

def generate_messy_string(base_string):
    """Generate strings with typos, extra spaces, or special characters"""
    if random.random() < 0.1:
        return base_string.upper()
    elif random.random() < 0.05:
        return base_string.lower()
    elif random.random() < 0.03:
        return f" {base_string} "  # Extra spaces
    elif random.random() < 0.02:
        return base_string.replace('a', '@').replace('e', '3')  # Special chars
    return base_string

def safe_int_convert(value):
    """Safely convert to int, handling NaN and None"""
    if pd.isna(value) or value is None:
        return np.nan
    try:
        return int(value)
    except (ValueError, TypeError):
        return np.nan

def safe_float_convert(value):
    """Safely convert to float, handling NaN and None"""
    if pd.isna(value) or value is None:
        return np.nan
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan

print("🚀 Starting Data Generation...")
print("="*60)

# ==================== 1. RM Master Table ====================
print("Generating RM Master Table...")
rm_data = []
for i in range(NUM_RM):
    # Random experience with some outliers
    exp = np.random.normal(8, 4)
    exp = max(0, min(30, int(exp)))
    if random.random() < 0.03:  # Some unrealistic experiences
        exp = random.choice([35, 40, 45])
    
    age = np.random.normal(35, 8)
    age = max(22, min(60, int(age)))
    
    # Some RMs with missing data
    city = random.choice(cities) if random.random() > 0.05 else np.nan
    name = rm_names[i] if random.random() > 0.08 else np.nan
    
    rm_data.append({
        'RM_ID': f'RM{str(i+1).zfill(4)}',
        'RM_Name': name,
        'City': city,
        'Age': age if random.random() > 0.03 else np.nan,
        'Gender': random.choice(['M', 'F']) if random.random() > 0.02 else np.nan,
        'Joining_Date': generate_messy_date(datetime(2010, 1, 1), datetime(2024, 12, 31)),
        'Experience': exp if random.random() > 0.04 else np.nan
    })

rm_df = pd.DataFrame(rm_data)
print(f"✅ Generated {len(rm_df)} RMs")

# ==================== 2. Customers Table ====================
print("Generating Customers Table...")
customers_data = []
rm_ids = rm_df['RM_ID'].dropna().tolist()

for i in range(NUM_CUSTOMERS):
    # Assign RM (some customers without RM)
    rm_id = random.choice(rm_ids) if random.random() > 0.08 else np.nan
    
    # Generate age with some outliers
    age = np.random.normal(42, 15)
    age = max(18, min(80, int(age)))
    
    # Income with outliers (some negative or extremely high)
    if random.random() < 0.03:
        income = random.choice([-1000, -5000, 9999999, 8888888])  # Negative or extreme
    else:
        income = np.random.exponential(50000) + 20000
        income = max(0, min(2000000, int(income)))
    
    # Segment with typos - FIXED
    segment_options = ['Premium', 'Gold', 'Silver', 'Bronze', 'Platinum']
    segment = random.choice(segment_options) if random.random() > 0.05 else np.nan
    
    # Check if segment is not NaN before applying lower()
    if random.random() < 0.03 and isinstance(segment, str):  # Typos only for strings
        segment = segment.lower()
    
    customers_data.append({
        'Customer_ID': f'CUST{str(i+1).zfill(6)}',
        'RM_ID': rm_id,
        'Age': age,
        'Gender': random.choice(['M', 'F']) if random.random() > 0.02 else np.nan,
        'City': random.choice(cities) if random.random() > 0.05 else np.nan,
        'Income': income,
        'Segment': segment
    })

customers_df = pd.DataFrame(customers_data)
print(f"✅ Generated {len(customers_df)} Customers")

# ==================== 3. Loan Table ====================
print("Generating Loan Table...")
loan_data = []
customer_ids = customers_df['Customer_ID'].dropna().tolist()
rm_ids_list = rm_df['RM_ID'].dropna().tolist()

loan_types = ['Home Loan', 'Personal Loan', 'Car Loan', 'Education Loan', 
              'Business Loan', 'Gold Loan', 'Plot Loan']
loan_statuses = ['Active', 'Closed', 'Defaulted', 'Pending', 'Approved', 'Rejected']

for i in range(NUM_LOANS):
    # Some loans without customer or RM
    cust_id = random.choice(customer_ids) if random.random() > 0.05 else np.nan
    rm_id = random.choice(rm_ids_list) if random.random() > 0.06 else np.nan
    
    # Messy loan amounts
    if random.random() < 0.03:
        amount = random.choice([-50000, 0, 999999999, np.nan])
    else:
        amount = np.random.exponential(200000) + 50000
        amount = max(10000, min(5000000, int(amount)))
    
    # Sometimes loan amount is in string format
    if random.random() < 0.02 and not pd.isna(amount):
        amount = f"{amount} INR"
    
    loan_data.append({
        'Loan_ID': f'LN{str(i+1).zfill(7)}',
        'Customer_ID': cust_id,
        'RM_ID': rm_id,
        'Loan_Type': random.choice(loan_types) if random.random() > 0.04 else np.nan,
        'Loan_Amount': amount,
        'Loan_Status': random.choice(loan_statuses) if random.random() > 0.03 else np.nan
    })

loan_df = pd.DataFrame(loan_data)
print(f"✅ Generated {len(loan_df)} Loans")

# ==================== 4. Sales Table ====================
print("Generating Sales Table...")
sales_data = []
products = ['Mutual Funds', 'Life Insurance', 'Health Insurance', 'Fixed Deposit',
            'Recurring Deposit', 'Credit Card', 'Saving Account', 'Current Account',
            'Term Insurance', 'ULIP', 'Loan Against Property', 'Gold Investment']

for i in range(NUM_TRANSACTIONS):
    rm_id = random.choice(rm_ids_list) if random.random() > 0.07 else np.nan
    
    # Messy product names
    product = random.choice(products)
    if random.random() < 0.04:
        product = product.upper() if random.random() < 0.5 else product.lower()
    elif random.random() < 0.02:
        product = f" {product} "  # Extra spaces
    
    # Random sale dates
    sale_date = generate_messy_date(datetime(2019, 1, 1), datetime(2026, 8, 9))
    
    # Messy amounts
    if random.random() < 0.04:
        amount = random.choice([np.nan, -1000, 0, 88888888])
    else:
        amount = np.random.exponential(50000) + 10000
        amount = max(1000, min(10000000, int(amount)))
    
    sales_data.append({
        'RM_ID': rm_id,
        'Product': product,
        'Sale_Date': sale_date,
        'Amount': amount
    })

sales_df = pd.DataFrame(sales_data)
print(f"✅ Generated {len(sales_df)} Sales Records")

# ==================== 5. Target Table ====================
print("Generating Target Table...")
target_data = []
months = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
month_names = [d.strftime('%Y-%m') for d in months]

for rm_id in rm_ids_list:
    # Each RM has targets for 24 months
    for month in month_names:
        # Some months missing
        if random.random() < 0.10:  # 10% missing data
            continue
        
        # Messy targets and achievements - FIXED
        if random.random() < 0.03:
            target = random.choice([np.nan, -10000, 0])
        else:
            target = np.random.exponential(150000) + 50000
            target = max(10000, min(2000000, int(target)))
        
        # Handle achievement calculation with NaN properly
        if random.random() < 0.04:
            achievement = random.choice([np.nan, -5000])
        else:
            # Only calculate if target is not NaN
            if pd.isna(target):
                achievement = np.nan
            else:
                achievement = target * np.random.uniform(0.3, 1.8)
                achievement = max(0, min(target * 2, int(achievement)))
        
        target_data.append({
            'RM_ID': rm_id,
            'Month': month,
            'Target': target,
            'Achievement': achievement
        })

target_df = pd.DataFrame(target_data)
print(f"✅ Generated {len(target_df)} Target Records")

# ==================== 6. Complaint Table ====================
print("Generating Complaint Table...")
complaint_data = []
complaint_types = ['Service Issue', 'Billing Error', 'Product Issue', 'Delay',
                   'Staff Behavior', 'Loan Disbursement', 'Account Access',
                   'Credit Card Issue', 'Insurance Claim', 'Technical Issue']

for i in range(NUM_COMPLAINTS):
    # Some complaints without customer or RM
    cust_id = random.choice(customer_ids) if random.random() > 0.06 else np.nan
    rm_id = random.choice(rm_ids_list) if random.random() > 0.08 else np.nan
    
    # Resolution time with outliers
    if random.random() < 0.04:
        res_time = random.choice([np.nan, -5, 0, 999])
    else:
        res_time = np.random.exponential(5) + 2  # days
        res_time = max(1, min(60, int(res_time)))
    
    complaint_data.append({
        'Complaint_ID': f'CMP{str(i+1).zfill(6)}',
        'Customer_ID': cust_id,
        'RM_ID': rm_id,
        'Complaint_Type': random.choice(complaint_types) if random.random() > 0.03 else np.nan,
        'Resolution_Time': res_time
    })

complaint_df = pd.DataFrame(complaint_data)
print(f"✅ Generated {len(complaint_df)} Complaints")

# ==================== 7. Customer Feedback Table ====================
print("Generating Customer Feedback Table...")
feedback_data = []

for i in range(len(customer_ids)):
    cust_id = customer_ids[i]
    rm_id = random.choice(rm_ids_list) if random.random() > 0.1 else np.nan
    
    # Some customers have multiple feedbacks
    num_feedbacks = 1 if random.random() < 0.8 else random.randint(2, 5)
    
    for j in range(num_feedbacks):
        # Rating with outliers
        if random.random() < 0.03:
            rating = random.choice([np.nan, 0, 6, -1, 10])
        else:
            rating = np.random.normal(4, 1)
            rating = max(1, min(5, round(rating, 1)))
        
        feedback_data.append({
            'Customer_ID': cust_id,
            'RM_ID': rm_id if random.random() > 0.05 else np.nan,
            'Rating': rating,
            'Feedback_Date': generate_messy_date(datetime(2023, 1, 1), datetime(2026, 8, 9)),
            'City': random.choice(cities) if random.random() > 0.05 else np.nan
        })

feedback_df = pd.DataFrame(feedback_data)
print(f"✅ Generated {len(feedback_df)} Feedback Records")

# ==================== Save to CSV Files in Colab ====================
print("\n💾 Saving data to CSV files...")

# Create a directory for the data
if not os.path.exists('rm_data'):
    os.makedirs('rm_data')

# Save all tables
rm_df.to_csv('rm_data/rm_master.csv', index=False)
customers_df.to_csv('rm_data/customers.csv', index=False)
loan_df.to_csv('rm_data/loans.csv', index=False)
sales_df.to_csv('rm_data/sales.csv', index=False)
target_df.to_csv('rm_data/targets.csv', index=False)
complaint_df.to_csv('rm_data/complaints.csv', index=False)
feedback_df.to_csv('rm_data/customer_feedback.csv', index=False)

print("\n✅ Data generation complete! Files saved in 'rm_data' directory.")

# ==================== Create ZIP file for download ====================
print("\n📦 Creating ZIP file for download...")

def zip_files():
    with zipfile.ZipFile('rm_data.zip', 'w') as zipf:
        for root, dirs, files in os.walk('rm_data'):
            for file in files:
                zipf.write(os.path.join(root, file), 
                          os.path.relpath(os.path.join(root, file), 'rm_data'))
    
    print("✅ ZIP file created successfully!")

zip_files()

# ==================== Display summary ====================
print("\n" + "="*80)
print("📊 DATA GENERATION SUMMARY")
print("="*80)
print(f"✅ RM Records: {len(rm_df):,}")
print(f"✅ Customer Records: {len(customers_df):,}")
print(f"✅ Loan Records: {len(loan_df):,}")
print(f"✅ Sales Records: {len(sales_df):,}")
print(f"✅ Target Records: {len(target_df):,}")
print(f"✅ Complaint Records: {len(complaint_df):,}")
print(f"✅ Customer Feedback Records: {len(feedback_df):,}")
print("="*80)

# ==================== Show sample of messy data ====================
print("\n📋 Sample of Messy Data (first 3 rows each):")
print("="*80)

print("\n1️⃣ RM Master Table:")
display(rm_df.head(3))

print("\n2️⃣ Customers Table:")
display(customers_df.head(3))

print("\n3️⃣ Loans Table:")
display(loan_df.head(3))

print("\n4️⃣ Sales Table:")
display(sales_df.head(3))

print("\n5️⃣ Targets Table:")
display(target_df.head(3))

print("\n6️⃣ Complaints Table:")
display(complaint_df.head(3))

print("\n7️⃣ Customer Feedback Table:")
display(feedback_df.head(3))

# ==================== Data Quality Report ====================
print("\n" + "="*80)
print("🔍 DATA QUALITY REPORT - Missing Values Summary:")
print("="*80)

def missing_report(df, name):
    print(f"\n📌 {name}:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
        print(f"Total Missing: {missing.sum():,}")
    else:
        print("✅ No missing values found")

missing_report(rm_df, "RM Master")
missing_report(customers_df, "Customers")
missing_report(loan_df, "Loans")
missing_report(sales_df, "Sales")
missing_report(target_df, "Targets")
missing_report(complaint_df, "Complaints")
missing_report(feedback_df, "Customer Feedback")

# ==================== Download Files ====================
print("\n" + "="*80)
print("📥 Download Options:")
print("="*80)

# Create download button for ZIP
zip_path = 'rm_data.zip'
if os.path.exists(zip_path):
    with open(zip_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="{zip_path}">📥 Click here to download all data as ZIP file</a>'
    display(HTML(href))
    
    # Also provide individual file download options
    print("\n🔹 Or download individual files:")
    files_list = ['rm_master.csv', 'customers.csv', 'loans.csv', 'sales.csv', 
                  'targets.csv', 'complaints.csv', 'customer_feedback.csv']
    for f in files_list:
        print(f"  files.download('rm_data/{f}')")

print("\n" + "="*80)
print("✅ All Done! You can now perform EDA and data cleaning.")
print("="*80)
