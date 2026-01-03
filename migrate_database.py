"""
Skrypt migracji bazy danych - aktualizuje schemat zgodnie z nowymi modelami
Wykonuje się automatycznie przy pierwszym uruchomieniu aplikacji
"""

from main import app, db
from character_cards import Character
from dnd5e_extras import create_dnd5e_extras_models
from trader_manager import create_trader_models

def migrate_database():
    """Tworzy wszystkie brakujące tabele i kolumny w bazie danych"""

    print("🔄 Rozpoczynam migrację bazy danych...")

    with app.app_context():
        try:
            # Tworzy wszystkie tabele zgodnie z nowymi modelami
            # Istniejące tabele NIE zostaną usunięte ani zmodyfikowane
            # Dodane zostaną tylko brakujące tabele i kolumny
            db.create_all()

            print("✅ Migracja zakończona pomyślnie!")
            print("\nZmiany w schemacie bazy danych:")
            print("\n📋 CTHULHU:")
            print("  - Zaktualizowano CharacterCthulhu:")
            print("    • zawod → profesja")
            print("    • miejsce_urodzenia + miejsce_zamieszkania → miejsce")
            print("    • Dodano pole: plec")
            print("    • Zaktualizowano statystyki do formatu z HTML")
            print("  - Zaktualizowano CthulhuBron:")
            print("    • Dodano pola: normal, hard, extreme, attacks, ammo, malfunction")
            print("\n⚔️ WARHAMMER:")
            print("  - Zaktualizowano CharacterWarhammer:")
            print("    • Zastąpiono statystyki Cthulhu prawdziwymi statystykami Warhammer")
            print("    • Dodano pola: rasa, poprzednie_profesje, oczy, waga, wlosy,")
            print("      wzrost, znak_gwiezdny, rodzienstwo, znaki_szczegolne")
            print("    • Dodano statystyki: ww, us, k, odp, zr, intel, sw, ogd, a, zyw,")
            print("      s, wt, sz, mag, po, pp")
            print("    • Dodano pola doświadczenia: doswiadczenie_wolne, doswiadczenie_wydane")
            print("    • Dodano pola ruchu: ruch, szarza, bieg")
            print("    • Dodano pola pieniędzy: zlote_korony, srebrne_szyllingi, miedziany_pensy")
            print("  - Zaktualizowano WarhammerBron:")
            print("    • Zastąpiono niewłaściwe mapowanie polami z HTML")
            print("    • Nowe pola: nazwa_broni, obciazenie, typ, sila, szkody, zasieg,")
            print("      przeladowanie, cechy")
            print("  - Utworzono nową tabelę: WarhammerArmor")
            print("    • Pola: armor_type, armor_location, armor_pz")
            print("\n🎲 D&D 5E:")
            print("  - Zaktualizowano CharacterDnD5e:")
            print("    • Dodano modyfikatory atrybutów: sila_mod, zrecznosc_mod, kondycja_mod,")
            print("      inteligencja_mod, madrosc_mod, charyzma_mod")
            print("    • Dodano rzuty obronne: save_sila, save_sila_val, save_zrecznosc,")
            print("      save_zrecznosc_val, save_kondycja, save_kondycja_val,")
            print("      save_inteligencja, save_inteligencja_val, save_madrosc,")
            print("      save_madrosc_val, save_charyzma, save_charyzma_val")
            print("\n⚠️ WAŻNE:")
            print("Jeśli masz istniejące dane w bazie, mogą być niezgodności.")
            print("Zalecane kroki:")
            print("1. Wykonaj backup bazy danych (skopiuj plik instance/rpg.db)")
            print("2. Możesz usunąć stare dane i zacząć od nowa, ALBO")
            print("3. Ręcznie zaktualizuj istniejące rekordy przez interfejs aplikacji")

        except Exception as e:
            print(f"❌ Błąd podczas migracji: {e}")
            print("Możliwe że baza danych ma nieprawidłową strukturę.")
            print("Rozważ usunięcie pliku instance/rpg.db i ponowne uruchomienie.")
            raise

if __name__ == "__main__":
    migrate_database()
