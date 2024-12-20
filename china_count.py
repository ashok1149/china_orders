import os
import pdfplumber
from collections import defaultdict
import re  # Regular expressions for extracting SKU code and quantity

# Step 1: Extract Data from USPS Labels
def extract_label_data(label_path):
    """Extracts SKU codes and quantities from all pages of a USPS label."""
    try:
        sku_data = []
        with pdfplumber.open(label_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                print(f"\n--- Extracted Text from Page {page_number} ---\n{text}")  # Debugging line
                
                # Process each line in the text
                for line in text.splitlines():
                    print(f"Processing Line: {line}")  # Debugging line
                    # Match SKU code and quantity in the format "yudu01;*1;"
                    match = re.search(r'([a-zA-Z0-9-]+);[*](\d+);', line)  # Adjusted regex
                    if match:
                        sku_code = match.group(1).strip()  # Extract SKU code
                        quantity = int(match.group(2).strip())  # Extract quantity
                        print(f"Found SKU code: {sku_code}, Quantity: {quantity}")  # Debugging line
                        sku_data.append({'sku_code': sku_code, 'quantity': quantity})
        return sku_data
    except Exception as e:
        print(f"Error extracting data: {e}")
        return []

# Step 2: Count SKUs and Products
def count_skus_and_products(label_folder):
    """Counts total SKUs and products from USPS labels."""
    sku_counts = defaultdict(int)

    for label_file in os.listdir(label_folder):
        if label_file.endswith('.pdf'):
            label_path = os.path.join(label_folder, label_file)
            print(f"\nProcessing label: {label_file}")
            sku_data = extract_label_data(label_path)

            for item in sku_data:
                print(f"Order Data: {item}")  # Debugging line
                sku_counts[item['sku_code']] += item['quantity']

    # Print summary of all SKUs and quantities
    print("\nSKU Counts Summary (Total Quantity per SKU):")
    if not sku_counts:
        print("No SKU data found. Please check the extraction logic or input data.")
    for sku, count in sku_counts.items():
        print(f"  {sku}: {count}")

# Configuration
LABEL_FOLDER = r"E:\china_count"  # Correct path to folder containing USPS labels

# Run the script
if __name__ == '__main__':
    count_skus_and_products(LABEL_FOLDER)
