import json
import requests
import pandas as pd
import sqlite3
import argparse

with open('config.json', 'r') as file:
    config = json.load(file)
    API_KEY = config['API_KEY']

def setup_database():
    conn = sqlite3.connect('ip_data.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ip_data (
        ipAddress TEXT PRIMARY KEY,
        abuseConfidenceScore INTEGER,
        countryCode TEXT
    )
    """)
    conn.commit()
    return conn

def check_in_database(conn, ip_address):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ip_data WHERE ipAddress=?", (ip_address,))
    return cursor.fetchone()

def check_ip(ip_address, conn):
    db_result = check_in_database(conn, ip_address)
    
    if db_result:
        return {
            "ipAddress": db_result[0],
            "abuseConfidenceScore": db_result[1],
            "countryCode": db_result[2]
        }
    
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90'
    }
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()['data']
    
    result = {
        "ipAddress": ip_address,
        "abuseConfidenceScore": data['abuseConfidenceScore'],
        "countryCode": data['countryCode']
    }
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ip_data (ipAddress, abuseConfidenceScore, countryCode) VALUES (?, ?, ?)",
                   (result["ipAddress"], result["abuseConfidenceScore"], result["countryCode"]))
    conn.commit()
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Check IP addresses against AbuseIPDB.")
    parser.add_argument("--path", required=True, help="Path to the file containing IP addresses.")
    parser.add_argument("--nginx", action="store_true", help="Generate an NGINX configuration with deny rules.")
    args = parser.parse_args()

    with open(args.path, 'r') as file:
        ip_addresses = [line.strip() for line in file]

    conn = setup_database()
    results = [check_ip(ip, conn) for ip in ip_addresses if check_ip(ip, conn)["abuseConfidenceScore"] > 60]
    
    if args.nginx:
        with open("nginx_deny.conf", "w") as file:
            for result in results:
                file.write(f"deny {result['ipAddress']};\n")
    else:
        df = pd.DataFrame(results)
        df.to_excel("results.xlsx", index=False)
        
    conn.close()

if __name__ == "__main__":
    main()
