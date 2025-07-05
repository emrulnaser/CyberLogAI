import re

def scan_text(text):
    results = {}

    # --- Pattern definitions ---
    email_pattern = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b')
    phone_pattern = re.compile(r'\b(?:\+?\d{1,4})?[ -]?\(?\d{1,4}\)?[ -]?\d{3,5}[ -]?\d{4,6}\b')
    nid_pattern = re.compile(r'\b\d{10,17}\b')
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    address_keywords = ['road', 'street', 'avenue', 'house', 'village', 'district']
    address_pattern = re.compile(r'\b(?:' + '|'.join(address_keywords) + r')\b.*', re.IGNORECASE)

    # --- Scan results ---
    results['emails'] = email_pattern.findall(text)
    results['phones'] = phone_pattern.findall(text)
    results['nid_numbers'] = nid_pattern.findall(text)
    results['ip_addresses'] = ip_pattern.findall(text)

    results['possible_addresses'] = []
    for line in text.split('\n'):
        if address_pattern.search(line):
            results['possible_addresses'].append(line.strip())

    return results
