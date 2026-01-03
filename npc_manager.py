"""
Modele dla NPC Manager - Bohaterowie Niezależni
Wspiera 3 systemy: Cthulhu, Warhammer, D&D 5e
"""

def create_npc_models(db):
    """Tworzy modele dla NPC Managera"""

    # ===== CTHULHU NPC =====
    class NPCCthulhu(db.Model):
        __tablename__ = 'npc_cthulhu'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        # Podstawowe informacje
        imie = db.Column(db.String(100), nullable=False)
        profesja = db.Column(db.String(100), nullable=True)

        # Cechy (8 podstawowych)
        sila = db.Column(db.Integer, default=50)              # STR
        kondycja = db.Column(db.Integer, default=50)          # CON
        madrosc = db.Column(db.Integer, default=50)           # POW
        zrecznosc = db.Column(db.Integer, default=50)         # DEX
        wyglad = db.Column(db.Integer, default=50)            # APP
        inteligencja = db.Column(db.Integer, default=50)      # INT
        rozmiar = db.Column(db.Integer, default=50)           # SIZ
        wyksztalcenie = db.Column(db.Integer, default=50)     # EDU

        # Punkty
        punkty_zycia = db.Column(db.Integer, default=10)
        punkty_magii = db.Column(db.Integer, default=10)
        poczytalnosc = db.Column(db.Integer, default=50)
        pancerz = db.Column(db.Integer, default=0)

        # Umiejętności (6 slotów)
        skill_1_name = db.Column(db.String(100), nullable=True)
        skill_1_value = db.Column(db.Integer, default=0)
        skill_2_name = db.Column(db.String(100), nullable=True)
        skill_2_value = db.Column(db.Integer, default=0)
        skill_3_name = db.Column(db.String(100), nullable=True)
        skill_3_value = db.Column(db.Integer, default=0)
        skill_4_name = db.Column(db.String(100), nullable=True)
        skill_4_value = db.Column(db.Integer, default=0)
        skill_5_name = db.Column(db.String(100), nullable=True)
        skill_5_value = db.Column(db.Integer, default=0)
        skill_6_name = db.Column(db.String(100), nullable=True)
        skill_6_value = db.Column(db.Integer, default=0)

        # Notatki
        notatki = db.Column(db.Text, nullable=True)

        # Metadata
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    # ===== WARHAMMER NPC =====
    class NPCWarhammer(db.Model):
        __tablename__ = 'npc_warhammer'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        # Podstawowe informacje
        imie = db.Column(db.String(100), nullable=False)
        profesja = db.Column(db.String(100), nullable=True)

        # Cechy (8 głównych)
        walka_wrecz = db.Column(db.Integer, default=30)           # WW
        umiejetnosci_strzeleckie = db.Column(db.Integer, default=30)  # US
        krzepa = db.Column(db.Integer, default=30)                # K
        odpornosc = db.Column(db.Integer, default=30)             # Odp
        zrecznosc = db.Column(db.Integer, default=30)             # Zr
        inteligencja = db.Column(db.Integer, default=30)          # Int
        sila_woli = db.Column(db.Integer, default=30)             # SW
        oglada = db.Column(db.Integer, default=30)                # Ogd

        # Punkty
        punkty_zycia = db.Column(db.Integer, default=10)
        punkty_szczescia = db.Column(db.Integer, default=0)
        punkty_przeznaczenia = db.Column(db.Integer, default=0)
        pancerz = db.Column(db.Integer, default=0)
        szybkosc = db.Column(db.Integer, default=4)

        # Umiejętności (6 slotów)
        skill_1_name = db.Column(db.String(100), nullable=True)
        skill_1_value = db.Column(db.Integer, default=0)
        skill_2_name = db.Column(db.String(100), nullable=True)
        skill_2_value = db.Column(db.Integer, default=0)
        skill_3_name = db.Column(db.String(100), nullable=True)
        skill_3_value = db.Column(db.Integer, default=0)
        skill_4_name = db.Column(db.String(100), nullable=True)
        skill_4_value = db.Column(db.Integer, default=0)
        skill_5_name = db.Column(db.String(100), nullable=True)
        skill_5_value = db.Column(db.Integer, default=0)
        skill_6_name = db.Column(db.String(100), nullable=True)
        skill_6_value = db.Column(db.Integer, default=0)

        # Notatki
        notatki = db.Column(db.Text, nullable=True)

        # Metadata
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    # ===== D&D 5E NPC =====
    class NPCDnD5e(db.Model):
        __tablename__ = 'npc_dnd5e'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        # Podstawowe informacje
        imie = db.Column(db.String(100), nullable=False)
        profesja = db.Column(db.String(100), nullable=True)

        # Cechy (6 głównych)
        sila = db.Column(db.Integer, default=10)
        sila_mod = db.Column(db.String(10), default='+0')
        zrecznosc = db.Column(db.Integer, default=10)
        zrecznosc_mod = db.Column(db.String(10), default='+0')
        kondycja = db.Column(db.Integer, default=10)
        kondycja_mod = db.Column(db.String(10), default='+0')
        inteligencja = db.Column(db.Integer, default=10)
        inteligencja_mod = db.Column(db.String(10), default='+0')
        madrosc = db.Column(db.Integer, default=10)
        madrosc_mod = db.Column(db.String(10), default='+0')
        charyzma = db.Column(db.Integer, default=10)
        charyzma_mod = db.Column(db.String(10), default='+0')

        # Punkty
        punkty_zycia_max = db.Column(db.Integer, default=10)
        klasa_pancerza = db.Column(db.Integer, default=10)  # KP/AC
        inicjatywa = db.Column(db.String(10), default='+0')
        szybkosc = db.Column(db.Integer, default=30)
        bonus_bieglosci = db.Column(db.String(10), default='+2')

        # Umiejętności (6 slotów)
        skill_1_name = db.Column(db.String(100), nullable=True)
        skill_1_value = db.Column(db.String(10), default='+0')
        skill_2_name = db.Column(db.String(100), nullable=True)
        skill_2_value = db.Column(db.String(10), default='+0')
        skill_3_name = db.Column(db.String(100), nullable=True)
        skill_3_value = db.Column(db.String(10), default='+0')
        skill_4_name = db.Column(db.String(100), nullable=True)
        skill_4_value = db.Column(db.String(10), default='+0')
        skill_5_name = db.Column(db.String(100), nullable=True)
        skill_5_value = db.Column(db.String(10), default='+0')
        skill_6_name = db.Column(db.String(100), nullable=True)
        skill_6_value = db.Column(db.String(10), default='+0')

        # Notatki
        notatki = db.Column(db.Text, nullable=True)

        # Metadata
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    return NPCCthulhu, NPCWarhammer, NPCDnD5e
