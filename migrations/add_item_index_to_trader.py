"""
Dodaje pole item_index do tabeli trader_item
"""
from main import app, db

def upgrade():
    with app.app_context():
        # Dodaj kolumnę item_index z wartością domyślną 0
        db.session.execute('ALTER TABLE trader_item ADD COLUMN item_index INTEGER DEFAULT 0 NOT NULL')
        db.session.commit()
        print("✅ Dodano kolumnę item_index do trader_item")

if __name__ == '__main__':
    upgrade()
