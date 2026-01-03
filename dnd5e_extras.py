"""
D&D 5e Extras Model + Warhammer + Cthulhu + Trader Manager
Wszystkie modele dla kart postaci i handlu
"""

from datetime import datetime


def create_dnd5e_extras_models(db):
    """Tworzy WSZYSTKIE modele extras"""

    # ===== D&D 5e =====
    class DnD5eBieglosc(db.Model):
        __tablename__ = 'dnd5e_bieglosc'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd5e.id'), nullable=False)

        # Biegłości (20)
        bieglosc_1_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_1_opis = db.Column(db.Text, nullable=True)
        bieglosc_2_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_2_opis = db.Column(db.Text, nullable=True)
        bieglosc_3_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_3_opis = db.Column(db.Text, nullable=True)
        bieglosc_4_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_4_opis = db.Column(db.Text, nullable=True)
        bieglosc_5_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_5_opis = db.Column(db.Text, nullable=True)
        bieglosc_6_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_6_opis = db.Column(db.Text, nullable=True)
        bieglosc_7_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_7_opis = db.Column(db.Text, nullable=True)
        bieglosc_8_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_8_opis = db.Column(db.Text, nullable=True)
        bieglosc_9_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_9_opis = db.Column(db.Text, nullable=True)
        bieglosc_10_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_10_opis = db.Column(db.Text, nullable=True)
        bieglosc_11_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_11_opis = db.Column(db.Text, nullable=True)
        bieglosc_12_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_12_opis = db.Column(db.Text, nullable=True)
        bieglosc_13_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_13_opis = db.Column(db.Text, nullable=True)
        bieglosc_14_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_14_opis = db.Column(db.Text, nullable=True)
        bieglosc_15_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_15_opis = db.Column(db.Text, nullable=True)
        bieglosc_16_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_16_opis = db.Column(db.Text, nullable=True)
        bieglosc_17_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_17_opis = db.Column(db.Text, nullable=True)
        bieglosc_18_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_18_opis = db.Column(db.Text, nullable=True)
        bieglosc_19_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_19_opis = db.Column(db.Text, nullable=True)
        bieglosc_20_nazwa = db.Column(db.String(255), nullable=True)
        bieglosc_20_opis = db.Column(db.Text, nullable=True)

        # Języki (8)
        jezyk_1_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_1_opis = db.Column(db.Text, nullable=True)
        jezyk_2_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_2_opis = db.Column(db.Text, nullable=True)
        jezyk_3_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_3_opis = db.Column(db.Text, nullable=True)
        jezyk_4_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_4_opis = db.Column(db.Text, nullable=True)
        jezyk_5_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_5_opis = db.Column(db.Text, nullable=True)
        jezyk_6_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_6_opis = db.Column(db.Text, nullable=True)
        jezyk_7_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_7_opis = db.Column(db.Text, nullable=True)
        jezyk_8_nazwa = db.Column(db.String(255), nullable=True)
        jezyk_8_opis = db.Column(db.Text, nullable=True)

        # Zdolności (26)
        zdolnosc_1_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_1_opis = db.Column(db.Text, nullable=True)
        zdolnosc_2_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_2_opis = db.Column(db.Text, nullable=True)
        zdolnosc_3_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_3_opis = db.Column(db.Text, nullable=True)
        zdolnosc_4_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_4_opis = db.Column(db.Text, nullable=True)
        zdolnosc_5_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_5_opis = db.Column(db.Text, nullable=True)
        zdolnosc_6_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_6_opis = db.Column(db.Text, nullable=True)
        zdolnosc_7_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_7_opis = db.Column(db.Text, nullable=True)
        zdolnosc_8_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_8_opis = db.Column(db.Text, nullable=True)
        zdolnosc_9_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_9_opis = db.Column(db.Text, nullable=True)
        zdolnosc_10_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_10_opis = db.Column(db.Text, nullable=True)
        zdolnosc_11_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_11_opis = db.Column(db.Text, nullable=True)
        zdolnosc_12_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_12_opis = db.Column(db.Text, nullable=True)
        zdolnosc_13_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_13_opis = db.Column(db.Text, nullable=True)
        zdolnosc_14_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_14_opis = db.Column(db.Text, nullable=True)
        zdolnosc_15_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_15_opis = db.Column(db.Text, nullable=True)
        zdolnosc_16_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_16_opis = db.Column(db.Text, nullable=True)
        zdolnosc_17_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_17_opis = db.Column(db.Text, nullable=True)
        zdolnosc_18_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_18_opis = db.Column(db.Text, nullable=True)
        zdolnosc_19_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_19_opis = db.Column(db.Text, nullable=True)
        zdolnosc_20_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_20_opis = db.Column(db.Text, nullable=True)
        zdolnosc_21_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_21_opis = db.Column(db.Text, nullable=True)
        zdolnosc_22_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_22_opis = db.Column(db.Text, nullable=True)
        zdolnosc_23_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_23_opis = db.Column(db.Text, nullable=True)
        zdolnosc_24_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_24_opis = db.Column(db.Text, nullable=True)
        zdolnosc_25_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_25_opis = db.Column(db.Text, nullable=True)
        zdolnosc_26_nazwa = db.Column(db.String(255), nullable=True)
        zdolnosc_26_opis = db.Column(db.Text, nullable=True)

        # Korzyści (10)
        korzysci_1_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_1_opis = db.Column(db.Text, nullable=True)
        korzysci_2_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_2_opis = db.Column(db.Text, nullable=True)
        korzysci_3_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_3_opis = db.Column(db.Text, nullable=True)
        korzysci_4_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_4_opis = db.Column(db.Text, nullable=True)
        korzysci_5_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_5_opis = db.Column(db.Text, nullable=True)
        korzysci_6_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_6_opis = db.Column(db.Text, nullable=True)
        korzysci_7_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_7_opis = db.Column(db.Text, nullable=True)
        korzysci_8_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_8_opis = db.Column(db.Text, nullable=True)
        korzysci_9_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_9_opis = db.Column(db.Text, nullable=True)
        korzysci_10_nazwa = db.Column(db.String(255), nullable=True)
        korzysci_10_opis = db.Column(db.Text, nullable=True)


    class DnD5eMagia(db.Model):
        __tablename__ = 'dnd5e_magia'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd5e.id'), nullable=False)

        # Parametry magii
        magic_cecha = db.Column(db.String(255), nullable=True)
        magic_st = db.Column(db.String(50), nullable=True)
        magic_bonus = db.Column(db.String(50), nullable=True)

        # Komórki czarów (0-9)
        cells_available_0 = db.Column(db.String(50), nullable=True)
        cells_used_0 = db.Column(db.String(50), nullable=True)
        cells_available_1 = db.Column(db.String(50), nullable=True)
        cells_used_1 = db.Column(db.String(50), nullable=True)
        cells_available_2 = db.Column(db.String(50), nullable=True)
        cells_used_2 = db.Column(db.String(50), nullable=True)
        cells_available_3 = db.Column(db.String(50), nullable=True)
        cells_used_3 = db.Column(db.String(50), nullable=True)
        cells_available_4 = db.Column(db.String(50), nullable=True)
        cells_used_4 = db.Column(db.String(50), nullable=True)
        cells_available_5 = db.Column(db.String(50), nullable=True)
        cells_used_5 = db.Column(db.String(50), nullable=True)
        cells_available_6 = db.Column(db.String(50), nullable=True)
        cells_used_6 = db.Column(db.String(50), nullable=True)
        cells_available_7 = db.Column(db.String(50), nullable=True)
        cells_used_7 = db.Column(db.String(50), nullable=True)
        cells_available_8 = db.Column(db.String(50), nullable=True)
        cells_used_8 = db.Column(db.String(50), nullable=True)
        cells_available_9 = db.Column(db.String(50), nullable=True)
        cells_used_9 = db.Column(db.String(50), nullable=True)


    class DnD5eSpell(db.Model):
        __tablename__ = 'dnd5e_spell'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd5e.id'), nullable=False)
        spell_level = db.Column(db.Integer, nullable=False)  # 0-9
        spell_index = db.Column(db.Integer, nullable=False)  # 0-11 (12 czarów per poziom)

        nazwa_czaru = db.Column(db.String(255), nullable=True)
        zasieg = db.Column(db.String(255), nullable=True)
        opis = db.Column(db.Text, nullable=True)


    class DnD5eEkwipunek(db.Model):
        __tablename__ = 'dnd5e_ekwipunek'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd5e.id'), nullable=False)
        przedmiot_index = db.Column(db.Integer, nullable=False)  # 0-29

        nazwa_przedmiotu = db.Column(db.String(255), nullable=True)
        obciazenie = db.Column(db.String(100), nullable=True)
        wartosc = db.Column(db.String(100), nullable=True)
        jednostka = db.Column(db.String(100), nullable=True)
        opis = db.Column(db.Text, nullable=True)


    # ===== WARHAMMER =====
    class WarhammerBron(db.Model):
        __tablename__ = 'warhammer_bron'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_warhammer.id'), nullable=False)
        bron_index = db.Column(db.Integer, nullable=False)  # 0-7 (8 broni)

        # Pola z formularza HTML bron_warhammer.html
        nazwa_broni = db.Column(db.String(255), nullable=True)    # weapon_name_X
        obciazenie = db.Column(db.String(100), nullable=True)     # weapon_obc_X
        typ = db.Column(db.String(100), nullable=True)            # weapon_category_X
        sila = db.Column(db.String(100), nullable=True)           # weapon_sila_X
        szkody = db.Column(db.String(100), nullable=True)         # weapon_broni_X
        zasieg = db.Column(db.String(100), nullable=True)         # weapon_zasieg_X
        przeladowanie = db.Column(db.String(100), nullable=True)  # weapon_przeload_X
        cechy = db.Column(db.Text, nullable=True)                 # weapon_cechy_X


    class WarhammerUmiejetnosc(db.Model):
        __tablename__ = 'warhammer_umiejetnosc'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_warhammer.id'), nullable=False)
        umiejetnosc_index = db.Column(db.Integer, nullable=False)  # 0-29

        nazwa_umiejetnosci = db.Column(db.String(255), nullable=True)
        typ = db.Column(db.String(100), nullable=True)
        poziom = db.Column(db.String(50), nullable=True)
        koszt = db.Column(db.String(100), nullable=True)
        wymogi = db.Column(db.String(255), nullable=True)
        opis = db.Column(db.Text, nullable=True)


    class WarhammerEkwipunek(db.Model):
        __tablename__ = 'warhammer_ekwipunek'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_warhammer.id'), nullable=False)
        przedmiot_index = db.Column(db.Integer, nullable=False)  # 0-29

        nazwa_przedmiotu = db.Column(db.String(255), nullable=True)
        obciazenie = db.Column(db.String(100), nullable=True)
        wartosc = db.Column(db.String(100), nullable=True)
        jednostka = db.Column(db.String(100), nullable=True)
        opis = db.Column(db.Text, nullable=True)


    class WarhammerArmor(db.Model):
        __tablename__ = 'warhammer_armor'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_warhammer.id'), nullable=False)
        armor_index = db.Column(db.Integer, nullable=False)  # 0-7 (8 pancerzy)

        # Pola z formularza HTML bron_warhammer.html
        armor_type = db.Column(db.String(255), nullable=True)      # armor_type_X
        armor_location = db.Column(db.String(255), nullable=True)  # armor_location_X
        armor_pz = db.Column(db.String(50), nullable=True)         # armor_pz_X


    # ===== CTHULHU =====
    class CthulhuBron(db.Model):
        __tablename__ = 'cthulhu_bron'
        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_cthulhu.id'), nullable=False)
        bron_index = db.Column(db.Integer, nullable=False)  # 0-9 (10 broni)

        # Pola z formularza HTML bron_cthulhu.html
        nazwa_broni = db.Column(db.String(255), nullable=True)
        normal = db.Column(db.String(50), nullable=True)  # weapon_normal_X
        hard = db.Column(db.String(50), nullable=True)    # weapon_hard_X
        extreme = db.Column(db.String(50), nullable=True) # weapon_extreme_X
        szkody = db.Column(db.String(100), nullable=True) # weapon_damage_X
        zasieg = db.Column(db.String(100), nullable=True) # weapon_range_X
        attacks = db.Column(db.String(50), nullable=True) # weapon_attacks_X
        ammo = db.Column(db.String(50), nullable=True)    # weapon_ammo_X
        malfunction = db.Column(db.String(50), nullable=True) # weapon_malfunction_X

    return (DnD5eBieglosc, DnD5eMagia, DnD5eSpell, DnD5eEkwipunek,
            WarhammerBron, WarhammerUmiejetnosc, WarhammerEkwipunek, WarhammerArmor,
            CthulhuBron)