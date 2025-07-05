from utils.parser import parse_log

# Load and parse the sample log file
df = parse_log('logs/sample.log')

# Display the parsed DataFrame
print("\nParsed Log Data:")
print(df)

# Show basic statistics
print("\nTop IP Addresses by Frequency:")
print(df['ip'].value_counts())
