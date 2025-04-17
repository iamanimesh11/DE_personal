import concurrent.futures
import requests

def fetch_quote(url):
    response = requests.get(url,verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch quote from {url}")

urls = [
    "https://lucifer-quotes.vercel.app/api/quotes",
    "https://lucifer-quotes.vercel.app/api/quotes",
    # ... more URLs
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(fetch_quote, urls)

for result in results:
    print(result)

url=    "https://lucifer-quotes.vercel.app/api/quotes"
print(url.split('/')[-1])
