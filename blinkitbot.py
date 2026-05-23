from curl_cffi import requests
import os

# --- TELEGRAM CONFIGURATION ---
# These pull securely from your GitHub Secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def notify_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": CHAT_ID, "text": message})
        if response.status_code != 200:
            print(f"❌ Telegram Error: {response.text}")
        else:
            print("✅ Telegram message sent successfully!")
    except Exception as e:
        print(f"❌ Failed to connect to Telegram: {e}")

# Recursive function to parse Blinkit's deeply nested JSON
def find_key(obj, key):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                return v
            if isinstance(v, (dict, list)):
                result = find_key(v, key)
                if result is not None:
                    return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_key(item, key)
            if result is not None:
                return result
    return None

def check_stock():
    url = 'https://blinkit.com/v1/layout/product/774460'
    
    # Your extracted cookies
    cookies = {
        'city': '',
        'gr_1_deviceId': '037b4ff3-7b98-4f72-a27a-53c4f83083cb',
        '_cfuvid': 'HPrlV2iS0Efzu8ZksdcFUk1SDVN542r5dMvowAWhD70-1779565779.0619762-1.0.1.1-_lHdJA4vlxxudPXnWR1zWzYnyayW8cPmVaeEBHsZAuA',
        'gr_1_accessToken': 'v2%3A%3Ae7a9c07f-4b5f-4778-9c28-9be84f156b1f',
        'gr_1_locality': '957',
        'gr_1_lat': '22.4886498',
        'gr_1_lon': '88.3166019',
        'gr_1_landmark': 'undefined',
        '__cf_bm': 'yH3CiYiFHUhCg_6ZMcUaWJ.f8Hb0VuXWzumRR7aB2Hs-1779566937.2486632-1.0.1.1-oBLLunOdWSQSGucCAsddvSCmmv3G9_NPCwhNyOFkW1ezhg6b6IDyUMXnHG4fiGWhF4wtewpKedbn_BL558GX5ZUdNeKA3T6uPCr0olhCrWjVb_urAKKxJNfIfwX0AOCl',
    }
    # Your extracted headers
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'access_token': 'v2::e7a9c07f-4b5f-4778-9c28-9be84f156b1f',
        'app_client': 'consumer_web',
        'app_version': '1010101010',
        'auth_key': 'c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477',
        # 'content-length': '0',
        'content-type': 'application/json',
        'device_id': '5bb53dfcb6cf0c8f',
        'dnt': '1',
        'is-response-compression-enabled': 'false',
        'lat': '22.4886498',
        'lon': '88.3166019',
        'origin': 'https://blinkit.com',
        'priority': 'u=1, i',
        'referer': 'https://blinkit.com/prn/x/prid/774460',
        'rn_bundle_version': '1009003012',
        'sec-ch-ua': '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'session_uuid': '8cf02533-cc9b-45c0-a342-456d624d9317',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'web_app_version': '1008010016',
        'x-age-consent-granted': 'true',
        # 'cookie': 'city=; gr_1_deviceId=037b4ff3-7b98-4f72-a27a-53c4f83083cb; _cfuvid=HPrlV2iS0Efzu8ZksdcFUk1SDVN542r5dMvowAWhD70-1779565779.0619762-1.0.1.1-_lHdJA4vlxxudPXnWR1zWzYnyayW8cPmVaeEBHsZAuA; gr_1_accessToken=v2%3A%3Ae7a9c07f-4b5f-4778-9c28-9be84f156b1f; gr_1_locality=957; gr_1_lat=22.4886498; gr_1_lon=88.3166019; gr_1_landmark=undefined; __cf_bm=yH3CiYiFHUhCg_6ZMcUaWJ.f8Hb0VuXWzumRR7aB2Hs-1779566937.2486632-1.0.1.1-oBLLunOdWSQSGucCAsddvSCmmv3G9_NPCwhNyOFkW1ezhg6b6IDyUMXnHG4fiGWhF4wtewpKedbn_BL558GX5ZUdNeKA3T6uPCr0olhCrWjVb_urAKKxJNfIfwX0AOCl',
    }

    try:
        # The magic trick: impersonate="chrome" to bypass Cloudflare
        response = requests.post(url, cookies=cookies, headers=headers, impersonate="chrome")
        
        if response.status_code != 200:
            print(f"Failed to fetch data! Status Code: {response.status_code}")
            return False

        data = response.json()
        
        inventory_count = find_key(data, "inventory")
        is_sold_out = find_key(data, "is_sold_out")
        
        print(f"Current Status - Inventory: {inventory_count}, Sold Out: {is_sold_out}")
        
        # Trigger condition: Only sends a message if stock is greater than 0
        if inventory_count is not None and inventory_count > 0:
            notify_telegram(f"🚨 Hot Wheels Mini Cooper is IN STOCK! Quantity: {inventory_count}")
            return True
            
    except Exception as e:
        print(f"Error checking stock: {e}")
        
    return False

# --- MAIN EXECUTION FOR GITHUB ACTIONS ---
if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ ERROR: Missing Telegram Token or Chat ID! Did you set your GitHub Secrets?")
    else:
        print("GitHub Action triggered: Checking Blinkit stock...")
        check_stock()