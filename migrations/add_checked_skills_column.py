"""
Migration: Add checked_skills column to cthulhu_skills table
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Sprawdź czy kolumna już istnieje
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='cthulhu_skills'
                AND column_name='checked_skills'
            """))

            if result.fetchone():
                print("✓ Kolumna checked_skills już istnieje")
                return

            # Dodaj kolumnę
            db.session.execute(text("""
                ALTER TABLE cthulhu_skills
                ADD COLUMN checked_skills TEXT DEFAULT '[]'
            """))
            db.session.commit()
            print("✓ Dodano kolumnę checked_skills")

        except Exception as e:
            print(f"✗ Błąd migracji: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate()
