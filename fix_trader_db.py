"""
Naprawia bazę danych dla Trader Manager - dodaje brakującą kolumnę item_index
lub odtwarza tabele jeśli to konieczne
"""
from main import app, db

def fix_database():
    with app.app_context():
        try:
            # Spróbuj dodać kolumnę item_index jeśli nie istnieje
            db.session.execute('ALTER TABLE trader_item ADD COLUMN item_index INTEGER DEFAULT 0 NOT NULL')
            db.session.commit()
            print("✅ Dodano kolumnę item_index do trader_item")
        except Exception as e:
            print(f"ℹ️  Kolumna item_index już istnieje lub inny błąd: {e}")
            db.session.rollback()

            # Jeśli to nie pomogło, usuń i odtwórz tabele
            try:
                print("\n🔄 Próbuję odtworzyć tabele trader_manager i trader_item...")

                # Usuń tabele
                db.session.execute('DROP TABLE IF EXISTS trader_item')
                db.session.execute('DROP TABLE IF EXISTS trader_manager')
                db.session.commit()

                # Odtwórz tabele używając modelu
                from trader_manager import create_trader_models
                TraderManager, TraderItem = create_trader_models(db)

                TraderManager.__table__.create(db.engine)
                TraderItem.__table__.create(db.engine)

                print("✅ Tabele trader_manager i trader_item zostały odtworzone z nową strukturą")
            except Exception as e2:
                print(f"❌ Błąd podczas odtwarzania tabel: {e2}")
                db.session.rollback()

if __name__ == '__main__':
    fix_database()
