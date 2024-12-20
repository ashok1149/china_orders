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
            for page in pdf.pages:
                text = page.extract_text()
                print("Extracted Text:", text)  # Debugging line
                # Process each line in the text
                for line in text.splitlines():
                    # Match SKU code (alphanumeric, including letters and numbers)
                    match = re.search(r'([a-zA-Z0-9-]+);[\*\d]+', line)  # Matches SKU code followed by ';*' and quantity
                    if match:
                        sku_code = match.group(1).strip()
                        quantity_match = re.search(r';\*(\d+)', line)  # Match quantity after ';*'
                        if quantity_match:
                            quantity = int(quantity_match.group(1).strip())
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
            print(f"Processing label: {label_file}")
            sku_data = extract_label_data(label_path)

            for item in sku_data:
                print(f"Order Data: {item}")  # Debugging line
                sku_counts[item['sku_code']] += item['quantity']

    # Print summary of all SKUs and quantities
    print("\nSKU Counts Summary (Total Quantity per SKU):")
    for sku, count in sku_counts.items():
        print(f"  {sku}: {count}")

# Configuration
LABEL_FOLDER = r"E:\china_count"  # Path to folder containing USPS labels

# Run the script
if __name__ == '__main__':
    count_skus_and_products(LABEL_FOLDER)
