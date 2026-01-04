"""
Skrypt resetowania bazy danych - USUWA wszystkie dane i tworzy czystą bazę
⚠️ UWAGA: Ten skrypt BEZPOWROTNIE USUNIE WSZYSTKIE DANE!
"""

import os
from main import app, db

def reset_database():
    """Usuwa całą bazę danych i tworzy ją od nowa"""

    db_path = os.path.join(app.instance_path, 'users.db')

    print("! UWAGA: Ten skrypt USUNIE WSZYSTKIE DANE z bazy!")
    print(f"- Sciezka do bazy: {db_path}")

    odpowiedz = input("\nCzy na pewno chcesz kontynuowac? (wpisz 'TAK' aby potwierdzic): ")

    if odpowiedz != 'TAK':
        print("- Anulowano resetowanie bazy danych.")
        return

    with app.app_context():
        try:
            # Usum plik bazy danych jesli istnieje
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"- Usunieto stara baze danych: {db_path}")

            # Utwórz katalog instance jeśli nie istnieje
            os.makedirs(app.instance_path, exist_ok=True)

            # Utwórz nową bazę danych
            db.create_all()

            print("\n+ Baza danych zostala zresetowana pomyslnie!")
            print("\n+ Utworzono nastepujace tabele:")
            print("  - user")
            # Skrocona lista
            print("\n+ Mozesz teraz uruchomic aplikacje!")

        except Exception as e:
            print(f"Error: {e}")
            raise

if __name__ == "__main__":
    reset_database()
