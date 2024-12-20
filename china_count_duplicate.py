import os
import pdfplumber
from collections import defaultdict
import re  # Regular expressions for extracting SKU code and quantity
import openpyxl
from datetime import datetime

# Step 1: Extract Data from USPS Labels
def extract_label_data(label_path):
    """Extracts unique SKU codes and their total quantities from a USPS label."""
    try:
        sku_data = {}
        with pdfplumber.open(label_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                print("Extracted Text:", text)  # Debugging line
                # Track processed SKUs for this label
                processed_skus = set()
                # Process each line in the text
                for line in text.splitlines():
                    match = re.search(r'([a-zA-Z0-9-]+);[\*\d]+', line)  # Matches SKU code followed by ';*' and quantity
                    if match:
                        sku_code = match.group(1).strip()
                        if sku_code in processed_skus:
                            continue  # Skip if already processed
                        quantity_match = re.search(r';\*(\d+)', line)  # Match quantity after ';*'
                        if quantity_match:
                            quantity = int(quantity_match.group(1).strip())
                            print(f"Found SKU code: {sku_code}, Quantity: {quantity}")  # Debugging line
                            # Add to data, avoid counting duplicates
                            if sku_code not in sku_data:
                                sku_data[sku_code] = 0
                            sku_data[sku_code] += quantity
                            processed_skus.add(sku_code)  # Mark this SKU as processed for the current label
        return sku_data
    except Exception as e:
        print(f"Error extracting data: {e}")
        return {}

# Step 2: Count SKUs and Products
def count_skus_and_products(label_folder):
    """Counts total SKUs and products from USPS labels."""
    sku_counts = defaultdict(int)

    for label_file in os.listdir(label_folder):
        if label_file.endswith('.pdf'):
            label_path = os.path.join(label_folder, label_file)
            print(f"\nProcessing label: {label_file}")
            sku_data = extract_label_data(label_path)

            for sku, quantity in sku_data.items():
                print(f"Adding to counts: SKU: {sku}, Quantity: {quantity}")  # Debugging line
                sku_counts[sku] += quantity

    # Print summary of all SKUs and quantities
    print("\nSKU Counts Summary (Total Quantity per SKU):")
    for sku, count in sku_counts.items():
        print(f"  {sku}: {count}")

    # Save to Excel
    save_to_excel(sku_counts, label_folder)

def save_to_excel(sku_counts, label_folder):
    """Saves the SKU counts summary to an Excel file."""
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(label_folder, f"{today}.xlsx")

    # Create a new workbook and add data
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "SKU Counts"
    sheet.append(["SKU Code", "Total Quantity"])  # Add headers

    for sku, count in sku_counts.items():
        sheet.append([sku, count])  # Add rows for SKU data

    workbook.save(output_file)
    print(f"\nSKU Counts Summary saved to {output_file}")

# Configuration
LABEL_FOLDER = r"E:\china_count"  # Path to folder containing USPS labels

# Run the script
if __name__ == '__main__':
    count_skus_and_products(LABEL_FOLDER)
