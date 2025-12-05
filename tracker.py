import datetime
import requests
from models import get_session, Item, PriceHistory
from dotenv import load_dotenv
from utils import read_config
import os

load_dotenv()
url = read_config("ENDPOINT_URL")
slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
moonshot_cookie = os.environ.get("MOONSHOT_COOKIE")
if moonshot_cookie:
    moonshot_cookie = moonshot_cookie.strip("'\"")

def send_slack(message):
    if slack_webhook_url:
        try:
            response = requests.post(slack_webhook_url, json={"text": message})
            response.raise_for_status()
        except Exception:
            raise

def check_shop():
    session = get_session()
    try:
        headers = {'Cookie': moonshot_cookie}
        response = requests.get(url, headers=headers, timeout=7)
        response.raise_for_status()

        data = response.json()
        items_list = data.get('items', [])

        for item in items_list:
            item_id = item['id']
            name = item['name']
            current_price = item['price']
            discount = item['discountPercent']
            now = datetime.datetime.now()

            db_item = session.query(Item).filter_by(id=item_id).first()

            if not db_item:
                message = f"✨ *New Item Detected*\nItem: {name}\nCurrent Price: {current_price}{f"\nOn Sale! Discount: {discount}%" if discount and discount > 0 else ''}"
                send_slack(message)
                print(message)
                new_item = Item(id=item_id, name=name, price=current_price, last_updated=now)
                session.add(new_item)
                history = PriceHistory(item_id=item_id, price=current_price, timestamp=now)
                session.add(history)
            else:
                if db_item.price != current_price:
                    old_price = db_item.price
                    db_item.price = current_price
                    db_item.last_updated = now
                    history = PriceHistory(item_id=item_id, price=current_price, timestamp=now)
                    session.add(history)
                    if current_price > old_price:
                        message = (
                            "*Price Change: 📈 UP*\n"
                            f"Item: {name}\n"
                            f"Old Price: {old_price} stardust ({old_price / 256:.2f}h) -> New Price: {current_price} stardust ({current_price / 256:.2f}h)\n"
                            f"Increase Percentage: {abs(((current_price - old_price) / old_price) * 100):.2f}%"
                        )
                        send_slack(message)
                        print(message)
                    else:
                        message = (
                            "*Price Change: 📉 DOWN*\n"
                            f"Item: {name}\n"
                            f"Old Price: {old_price} stardust ({old_price / 256:.2f}h) -> New Price: {current_price} stardust ({current_price / 256:.2f}h)\n"
                            f"Discount Percentage: {abs(discount if discount and discount > 0 else ((current_price - old_price) / old_price) * 100):.2f}%"
                        )
                        send_slack(message)
                        print(message)
            session.commit()
    except Exception:
        raise
    finally:
        session.close()

if __name__ == "__main__":
    check_shop()