"""
Skrypt resetowania bazy danych - USUWA wszystkie dane i tworzy czystą bazę
⚠️ UWAGA: Ten skrypt BEZPOWROTNIE USUNIE WSZYSTKIE DANE!
"""

import os
from main import app, db

def reset_database():
    """Usuwa całą bazę danych i tworzy ją od nowa"""

    db_path = os.path.join(app.instance_path, 'rpg.db')

    print("⚠️  UWAGA: Ten skrypt USUNIE WSZYSTKIE DANE z bazy!")
    print(f"📂 Ścieżka do bazy: {db_path}")

    odpowiedz = input("\nCzy na pewno chcesz kontynuować? (wpisz 'TAK' aby potwierdzić): ")

    if odpowiedz != 'TAK':
        print("❌ Anulowano resetowanie bazy danych.")
        return

    with app.app_context():
        try:
            # Usuń plik bazy danych jeśli istnieje
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"🗑️  Usunięto starą bazę danych: {db_path}")

            # Utwórz katalog instance jeśli nie istnieje
            os.makedirs(app.instance_path, exist_ok=True)

            # Utwórz nową bazę danych
            db.create_all()

            print("\n✅ Baza danych została zresetowana pomyślnie!")
            print("\n📋 Utworzono następujące tabele:")
            print("  • user - użytkownicy")
            print("  • characters_cthulhu - postacie Cthulhu")
            print("  • cthulhu_skills - umiejętności Cthulhu")
            print("  • cthulhu_bron - broń Cthulhu")
            print("  • characters_warhammer - postacie Warhammer")
            print("  • warhammer_bron - broń Warhammer")
            print("  • warhammer_armor - pancerze Warhammer (NOWA TABELA)")
            print("  • warhammer_umiejetnosc - umiejętności Warhammer")
            print("  • warhammer_ekwipunek - ekwipunek Warhammer")
            print("  • characters_dnd5e - postacie D&D 5e")
            print("  • dnd5e_bieglosc - biegłości D&D 5e")
            print("  • dnd5e_magia - magia D&D 5e")
            print("  • dnd5e_spell - zaklęcia D&D 5e")
            print("  • dnd5e_ekwipunek - ekwipunek D&D 5e")
            print("  • trader_manager - handlarze")
            print("  • trader_item - przedmioty handlarzy")
            print("\n🎉 Możesz teraz uruchomić aplikację i stworzyć nowe konta i postacie!")

        except Exception as e:
            print(f"❌ Błąd podczas resetowania bazy: {e}")
            raise

if __name__ == "__main__":
    reset_database()
