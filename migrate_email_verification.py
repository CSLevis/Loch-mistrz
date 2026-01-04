"""
Skrypt migracji dla weryfikacji email.
Dodaje kolumny: is_verified i verification_code do tabeli user.
"""
from main import app, db
from sqlalchemy import text

def migrate_email():
    print("... Rozpoczynam migrację dla weryfikacji email...")
    with app.app_context():
        try:
            # Sprawdź czy kolumny już istnieją
            with db.engine.connect() as conn:
                # SQLite PRAGMA
                if 'sqlite' in str(db.engine.url):
                    result = conn.execute(text("PRAGMA table_info(user)")).fetchall()
                    columns = [row[1] for row in result]
                else:
                    # Postgres (na przyszłość)
                    # To uproszczona wersja, dla Postgresa trzeba by query do information_schema
                    # Ale na razie zakładamy local dev na sqlite
                    print("⚠️ Wykryto inną bazę niż SQLite. Próba dodania kolumn w ciemno (może rzucić błąd jeśli istnieją).")
                    columns = []

                if 'is_verified' not in columns:
                    print("+ Dodawanie kolumny is_verified...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT 0"))
                else:
                    print("INFO Kolumna is_verified już istnieje.")

                if 'verification_code' not in columns:
                    print("+ Dodawanie kolumny verification_code...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN verification_code VARCHAR(6)"))
                else:
                    print("INFO Kolumna verification_code już istnieje.")
                
                conn.commit()
                print("OK Migracja zakończona sukcesem!")

        except Exception as e:
            print(f"Error Błąd migracji: {e}")

if __name__ == "__main__":
    migrate_email()
