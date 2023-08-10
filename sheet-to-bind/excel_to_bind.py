# pip install openpyxl
# pip install pandas


import argparse
import pandas as pd

def convert_excel_to_bind(path):
    df = pd.read_excel(path)
    
    # Transform the dataframe to BIND format
    bind_records = []
    for _, row in df.iterrows():
        bind_record = f"{row['name']} 300 IN {row['type']} {row['data']}"
        bind_records.append(bind_record)
    
    return '\n'.join(bind_records)

def main():
    parser = argparse.ArgumentParser(description="Convert Excel to BIND format")
    parser.add_argument("--path", required=True, help="Path to the Excel file")
    args = parser.parse_args()

    bind_output = convert_excel_to_bind(args.path)
    
    # Extracting the domain name from the first record to use as filename
    domain_name = bind_output.split()[0]
    with open(f"{domain_name}.bind", "w") as file:
        file.write(bind_output)
    print(f"Output saved to {domain_name}.bind")

if __name__ == "__main__":
    main()
