import requests

def fetch_quote():
    try:
        response = requests.get("https://api.quotable.io/random?tags=inspirational", verify=False)
        if response.status_code == 200:
            return f'"{response.json()["content"].upper()}"'
    except Exception as e:
        print(f"Error fetching quote: {e}")

    return "\"WORK HARD AND STAY POSITIVE.\""

