import requests,time,json

def scrape_followings(user_id):
    base_url = f"https://friends.roblox.com/v1/users/{user_id}/followings"
    cursor = None
    page = 1
    all_ids = []
    
    while True:
        if cursor is None:
            url = f"{base_url}?limit=100&sortOrder=Asc"
        else:
            url = f"{base_url}?limit=100&cursor={cursor}&sortOrder=Asc"
        
        print(f"Page {page}")
        
        try:
            response = requests.get(url)
            
            if response.status_code == 429:
                print("Rate limited (429), waiting 3 seconds...")
                time.sleep(3)
                continue
            
            response.raise_for_status()
            data = response.json()
            
            for user in data.get('data', []):
                all_ids.append(str(user['id']))
            
            cursor = data.get('nextPageCursor')
            if not cursor:
                break
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if response.status_code == 429:
                time.sleep(3)
                continue
            break

    with open('following.txt', 'w') as f:
        for user_id in all_ids:
            f.write(user_id + '\n')
    
    print(f"Scraping complete {len(all_ids)} followings saved to following.txt")

user_id = input("Enter user ID: ")
scrape_followings(user_id)
