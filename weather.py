import requests
import re
import time

# Define the URL
url = "https://www.meteohobby.it/dtm_montegrappa/dtm_panettone.php"

# Function to extract float values between two markers
def parse_float_value(data, label_start, label_end):
    pattern = f"{re.escape(label_start)}(.*?){re.escape(label_end)}"
    match = re.search(pattern, data)
    if match:
        return float(match.group(1))
    return 0.0

# Function to extract string values between two markers
def parse_string_value(data, label_start, label_end):
    pattern = f"{re.escape(label_start)}(.*?){re.escape(label_end)}"
    match = re.search(pattern, data)
    if match:
        return match.group(1)
    return ""

# Main function to request and process data
def fetch_weather_data():
    try:
        # Make the HTTP GET request
        response = requests.get(url)
        if response.status_code == 200:
            # Get the HTML content as a string
            html_content = response.text
            
            # Extract values based on the observed HTML structure
            vento = parse_float_value(html_content, "<span class=\"vel\">", "</span>")
            da = parse_string_value(html_content, "da <font size=\"6\">", "</font>")
            max_value = parse_float_value(html_content, "<span class=\"max\">", "</span>")

            # Print extracted values
            print(f"Vento: {vento}")
            print(f"da: {da}")
            print(f"Max: {max_value}")
        else:
            print(f"Error in HTTP request: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Fetch data every 10 seconds (as per your Arduino code's loop delay)
while True:
    fetch_weather_data()
    time.sleep(10)  # Wait for 10 seconds before the next request

