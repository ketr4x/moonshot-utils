import atexit
from flask import Flask, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from models import get_session, Item, PriceHistory
from tracker import check_shop
from utils import read_config

app = Flask(__name__)
cors = CORS(app, origins='*')

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_shop, trigger="interval", minutes=int(read_config("CHECK_INTERVAL")))
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route('/api/items')
def get_items():
    db_session = get_session()
    try:
        items = db_session.query(Item).all()
        data = [
            {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "last_updated": item.last_updated.isoformat() if item.last_updated else None
            }
            for item in items
        ]
        return jsonify(data)
    finally:
        db_session.close()

@app.route('/api/history/<item_id>')
def get_history(item_id):
    db_session = get_session()
    try:
        history = db_session.query(PriceHistory).filter_by(item_id=item_id).order_by(PriceHistory.timestamp).all()
        data = [
            {
                "price": entry.price,
                "timestamp": entry.timestamp.isoformat()
            }
            for entry in history
        ]
        return jsonify(data)
    finally:
        db_session.close()

if __name__ == '__main__':
    app.run(debug=True)