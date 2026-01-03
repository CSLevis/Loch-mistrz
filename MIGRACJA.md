# Instrukcja Migracji Bazy Danych

## Wprowadzenie

Zaktualizowano strukturę bazy danych, aby była zgodna z formularzami HTML. Wszystkie pola, które były tracone podczas zapisywania, zostały dodane do modeli i routów.

---

## Zmiany w Bazie Danych

### 🧟 CTHULHU

#### Model `CharacterCthulhu`:
- **Zmieniono nazwę pola:** `zawod` → `profesja`
- **Zmieniono pola miejsca:** `miejsce_urodzenia`, `miejsce_zamieszkania` → `miejsce` (jedno pole)
- **Dodano pole:** `plec`
- **Zaktualizowano statystyki** do zgodności z formularzem HTML:
  - `s`, `zr`, `moc`, `pw1`, `pw2`, `kon`, `wyg`, `wyk`, `szczescie`, `bc`, `intel`, `ruch`, `poczytalnosc`

#### Model `CthulhuBron`:
- **Dodano 6 nowych pól:**
  - `normal` (weapon_normal_X)
  - `hard` (weapon_hard_X)
  - `extreme` (weapon_extreme_X)
  - `attacks` (weapon_attacks_X)
  - `ammo` (weapon_ammo_X)
  - `malfunction` (weapon_malfunction_X)

---

### ⚔️ WARHAMMER

#### Model `CharacterWarhammer`:
- **Zastąpiono statystyki Cthulhu prawdziwymi statystykami Warhammer Fantasy:**
  - Stare: `s`, `zr`, `moc`, `pw1`, `pw2`, `kon`, `wyg`, `wyk`, `szczescie`, `bc`, `intel`, `ruch`, `poczytalnosc`
  - **NOWE:** `ww`, `us`, `k`, `odp`, `zr`, `intel`, `sw`, `ogd`, `a`, `zyw`, `s`, `wt`, `sz`, `mag`, `po`, `pp`

- **Dodano 9 nowych pól z formularza:**
  - `rasa`
  - `poprzednie_profesje`
  - `oczy`
  - `waga`
  - `wlosy`
  - `wzrost`
  - `znak_gwiezdny`
  - `rodzienstwo`
  - `znaki_szczegolne`

- **Dodano pola doświadczenia:**
  - `doswiadczenie_wolne`
  - `doswiadczenie_wydane`

- **Dodano pola ruchu:**
  - `ruch`
  - `szarza`
  - `bieg`

- **Dodano pola pieniędzy:**
  - `zlote_korony`
  - `srebrne_szyllingi`
  - `miedziany_pensy`

#### Model `WarhammerBron`:
- **Zastąpiono nieprawidłowe mapowanie pól:**
  - Stare mapowanie było mylące (np. `weapon_obc` → `waga`, `weapon_przeload` → `cena`)
  - **NOWE pola zgodne z HTML:**
    - `nazwa_broni` (weapon_name_X)
    - `obciazenie` (weapon_obc_X)
    - `typ` (weapon_category_X)
    - `sila` (weapon_sila_X) - **NOWE POLE**
    - `szkody` (weapon_broni_X)
    - `zasieg` (weapon_zasieg_X)
    - `przeladowanie` (weapon_przeload_X)
    - `cechy` (weapon_cechy_X)

#### **NOWA TABELA:** `WarhammerArmor`
- **Utworzono nową tabelę dla pancerzy (wcześniej całkowicie tracone):**
  - `armor_type` (armor_type_X)
  - `armor_location` (armor_location_X)
  - `armor_pz` (armor_pz_X)
  - 8 slotów na pancerze (armor_index 0-7)

---

### 🎲 D&D 5E

#### Model `CharacterDnD5e`:
- **Dodano modyfikatory atrybutów (6 nowych pól):**
  - `sila_mod`
  - `zrecznosc_mod`
  - `kondycja_mod`
  - `inteligencja_mod`
  - `madrosc_mod`
  - `charyzma_mod`

- **Dodano rzuty obronne (12 nowych pól):**
  - `save_sila`, `save_sila_val`
  - `save_zrecznosc`, `save_zrecznosc_val`
  - `save_kondycja`, `save_kondycja_val`
  - `save_inteligencja`, `save_inteligencja_val`
  - `save_madrosc`, `save_madrosc_val`
  - `save_charyzma`, `save_charyzma_val`

---

## Opcje Migracji

### Opcja 1: Migracja z zachowaniem danych (ZALECANA dla produkcji)

```bash
# 1. Zrób backup obecnej bazy
copy instance\rpg.db instance\rpg.db.backup

# 2. Uruchom skrypt migracji
python migrate_database.py
```

**UWAGA:** Po migracji istniejące dane mogą być niepełne, ponieważ nowe kolumny będą miały wartości domyślne. Będziesz musiał ręcznie zaktualizować istniejące postacie przez interfejs aplikacji.

---

### Opcja 2: Reset bazy danych (ZALECANA dla rozwoju)

```bash
# UWAGA: To USUNIE WSZYSTKIE DANE!
python reset_database.py
```

Po uruchomieniu zostaniesz poproszony o potwierdzenie wpisując `TAK`.

---

## Co zostało naprawione?

### Problemy rozwiązane:

✅ **Cthulhu:**
- Formularz wysyłał `profesja`, ale baza miała `zawod` → **NAPRAWIONO**
- Formularz wysyłał 9 pól broni, ale tylko 3 były zapisywane → **NAPRAWIONO**

✅ **Warhammer:**
- Formularz używał statystyk Warhammer, ale baza miała statystyki Cthulhu → **NAPRAWIONO**
- 9 pól formularza (rasa, oczy, waga, itp.) było traconych → **NAPRAWIONO**
- Pole `weapon_sila` było tracone → **NAPRAWIONO**
- **Pancerze (8 slotów × 3 pola) były całkowicie tracone** → **NAPRAWIONO**
- Pola doświadczenia były tracone → **NAPRAWIONO**
- Pola ruchu (szarża, bieg) były tracone → **NAPRAWIONO**

✅ **D&D 5e:**
- Modyfikatory atrybutów (6 pól) były tracone → **NAPRAWIONO**
- Rzuty obronne (12 pól) były tracone → **NAPRAWIONO**

---

## Weryfikacja po migracji

Po migracji sprawdź:

1. **Utwórz nową postać** dla każdego systemu (Cthulhu, Warhammer, D&D 5e)
2. **Wypełnij wszystkie pola** w formularzach
3. **Zapisz i otwórz ponownie** - sprawdź czy wszystkie pola zostały zachowane
4. **Sprawdź broń/pancerze** - upewnij się że wszystkie pola są zapisywane

---

## Debugowanie

Jeśli napotkasz błędy:

1. **Błąd "no such column":**
   - Wykonaj reset bazy danych: `python reset_database.py`

2. **Dane są tracone:**
   - Sprawdź w [main.py](main.py) czy route poprawnie pobiera dane z formularza
   - Sprawdź w plikach modeli czy kolumna istnieje

3. **Błąd importu:**
   - Upewnij się że wszystkie zależności są zainstalowane: `pip install -r requirements.txt`

---

## Struktura plików

```
RPG-Lochmistrz/
├── main.py                  # Główna aplikacja + routy (ZAKTUALIZOWANE)
├── character_cards.py       # Modele postaci (ZAKTUALIZOWANE)
├── dnd5e_extras.py         # Dodatkowe modele (ZAKTUALIZOWANE)
├── trader_manager.py        # Model handlarza (bez zmian)
├── migrate_database.py     # Skrypt migracji (NOWY)
├── reset_database.py       # Skrypt resetowania (NOWY)
├── MIGRACJA.md             # Ten plik (NOWY)
└── templates/              # Formularze HTML (bez zmian)
```

---

## Podsumowanie zmian w kodzie

### Zaktualizowane pliki:

1. **[character_cards.py](character_cards.py)**
   - `CharacterCthulhu`: zmieniono pola na zgodne z HTML
   - `CharacterWarhammer`: całkowita przebudowa statystyk
   - `CharacterDnD5e`: dodano modyfikatory i saves

2. **[dnd5e_extras.py](dnd5e_extras.py)**
   - `CthulhuBron`: dodano 6 pól
   - `WarhammerBron`: przebudowa mapowania pól
   - `WarhammerArmor`: **NOWA TABELA**

3. **[main.py](main.py)**
   - Wszystkie routy Warhammer: zaktualizowano do nowych statystyk
   - Route `/bron-warhammer`: dodano obsługę pancerzy
   - Routy D&D 5e: dodano obsługę modyfikatorów i saves
   - Route `/bron-cthulhu`: dodano obsługę wszystkich pól

---

## Pytania?

Jeśli masz pytania lub problemy, sprawdź kod w plikach:
- Modele: [character_cards.py](character_cards.py), [dnd5e_extras.py](dnd5e_extras.py)
- Routy: [main.py](main.py)
- Formularze: `templates/*.html`
