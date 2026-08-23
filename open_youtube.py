import urllib.parse
import webbrowser

def search_youtube(query):
    # Safely format the query string for URL embedding (e.g., handles spaces)
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    print(f"[*] Opening browser and searching YouTube for: '{query}'")
    webbrowser.open(search_url)

if __name__ == "__main__":
    search_youtube("Hip Hop Classics")