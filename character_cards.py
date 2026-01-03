from datetime import datetime


class Character:
    """Fabryka modeli kart postaci dla różnych systemów"""

    @staticmethod
    def create_warhammer_model(db):
        """Model dla Warhammer Fantasy"""

        class CharacterWarhammer(db.Model):
            __tablename__ = 'characters_warhammer'

            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

            # Podstawowe informacje
            imie = db.Column(db.String(100), default='')
            gracz = db.Column(db.String(100), default='')
            profesja = db.Column(db.String(100), default='')
            wiek = db.Column(db.String(50), default='')
            plec = db.Column(db.String(50), default='')
            miejsce = db.Column(db.String(100), default='')

            # Dodatkowe pola z formularza HTML
            rasa = db.Column(db.String(100), default='')
            poprzednie_profesje = db.Column(db.String(255), default='')
            oczy = db.Column(db.String(100), default='')
            waga = db.Column(db.String(50), default='')
            wlosy = db.Column(db.String(100), default='')
            wzrost = db.Column(db.String(50), default='')
            znak_gwiezdny = db.Column(db.String(100), default='')
            rodzienstwo = db.Column(db.String(255), default='')
            znaki_szczegolne = db.Column(db.Text, default='')

            # Statystyki Warhammer Fantasy (Cechy)
            ww = db.Column(db.Integer, default=0)  # Walka Wręcz
            us = db.Column(db.Integer, default=0)  # Umiejętności Strzeleckie
            k = db.Column(db.Integer, default=0)   # Krzepa
            odp = db.Column(db.Integer, default=0) # Odporność
            zr = db.Column(db.Integer, default=0)  # Zręczność
            intel = db.Column(db.Integer, default=0) # Inteligencja
            sw = db.Column(db.Integer, default=0)  # Siła Woli
            ogd = db.Column(db.Integer, default=0) # Ogłada
            a = db.Column(db.Integer, default=0)   # Ataki
            zyw = db.Column(db.Integer, default=0) # Żywotność
            s = db.Column(db.Integer, default=0)   # Siła
            wt = db.Column(db.Integer, default=0)  # Wytrzymałość
            sz = db.Column(db.Integer, default=0)  # Szybkość
            mag = db.Column(db.Integer, default=0) # Magia
            po = db.Column(db.Integer, default=0)  # Punkty Obrażeń
            pp = db.Column(db.Integer, default=0)  # Punkty Przeznaczenia

            # Doświadczenie
            doswiadczenie_wolne = db.Column(db.Integer, default=0)
            doswiadczenie_wydane = db.Column(db.Integer, default=0)

            # Ruch
            ruch = db.Column(db.Integer, default=0)
            szarza = db.Column(db.Integer, default=0)
            bieg = db.Column(db.Integer, default=0)

            # Pieniądze (używane w ekwipunku)
            zlote_korony = db.Column(db.Integer, default=0)
            srebrne_szyllingi = db.Column(db.Integer, default=0)
            miedziany_pensy = db.Column(db.Integer, default=0)

            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            user = db.relationship('User', backref=db.backref('warhammer_characters', lazy=True))

        return CharacterWarhammer

    @staticmethod
    def create_dnd5e_model(db):
        """Model dla D&D 5e"""

        class CharacterDnD5e(db.Model):
            __tablename__ = 'characters_dnd5e'

            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

            # Dane postaci
            imie = db.Column(db.String(100), default='')
            gracz = db.Column(db.String(100), default='')
            klasa = db.Column(db.String(100), default='')
            rasa = db.Column(db.String(100), default='')
            poziom = db.Column(db.Integer, default=1)
            pochodzenie = db.Column(db.String(100), default='')
            charakter = db.Column(db.String(100), default='')
            doswiadczenie = db.Column(db.Integer, default=0)
            wiek = db.Column(db.String(50), default='')
            wzrost = db.Column(db.String(50), default='')
            waga = db.Column(db.String(50), default='')
            oczy = db.Column(db.String(100), default='')
            skora = db.Column(db.String(100), default='')
            wlosy = db.Column(db.String(100), default='')

            # Atrybuty
            sila = db.Column(db.Integer, default=10)
            sila_mod = db.Column(db.Integer, default=0)
            zrecznosc = db.Column(db.Integer, default=10)
            zrecznosc_mod = db.Column(db.Integer, default=0)
            kondycja = db.Column(db.Integer, default=10)
            kondycja_mod = db.Column(db.Integer, default=0)
            inteligencja = db.Column(db.Integer, default=10)
            inteligencja_mod = db.Column(db.Integer, default=0)
            madrosc = db.Column(db.Integer, default=10)
            madrosc_mod = db.Column(db.Integer, default=0)
            charyzma = db.Column(db.Integer, default=10)
            charyzma_mod = db.Column(db.Integer, default=0)

            # Rzuty obronne
            save_sila = db.Column(db.Boolean, default=False)
            save_sila_val = db.Column(db.Integer, default=0)
            save_zrecznosc = db.Column(db.Boolean, default=False)
            save_zrecznosc_val = db.Column(db.Integer, default=0)
            save_kondycja = db.Column(db.Boolean, default=False)
            save_kondycja_val = db.Column(db.Integer, default=0)
            save_inteligencja = db.Column(db.Boolean, default=False)
            save_inteligencja_val = db.Column(db.Integer, default=0)
            save_madrosc = db.Column(db.Boolean, default=False)
            save_madrosc_val = db.Column(db.Integer, default=0)
            save_charyzma = db.Column(db.Boolean, default=False)
            save_charyzma_val = db.Column(db.Integer, default=0)

            # Walka i HP
            klasa_pancerza = db.Column(db.Integer, default=10)
            inicjatywa = db.Column(db.Integer, default=0)
            szybkosc = db.Column(db.Integer, default=30)
            punkty_zycia = db.Column(db.Integer, default=0)
            aktualne_pw = db.Column(db.Integer, default=0)
            czasowe_pw = db.Column(db.Integer, default=0)
            inspiracja = db.Column(db.String(50), default='')
            premia_bieglości = db.Column(db.Integer, default=2)

            # Pasywne rzuty
            pasywna_madrosc = db.Column(db.Integer, default=10)

            # Kości Wytrzymałości
            kosci_wytrzymalosci = db.Column(db.Integer, default=0)

            # Rzuty Przeciwko Śmierci - Sukcesy
            death_success_1 = db.Column(db.Boolean, default=False)
            death_success_2 = db.Column(db.Boolean, default=False)
            death_success_3 = db.Column(db.Boolean, default=False)

            # Rzuty Przeciwko Śmierci - Porażki
            death_failure_1 = db.Column(db.Boolean, default=False)
            death_failure_2 = db.Column(db.Boolean, default=False)
            death_failure_3 = db.Column(db.Boolean, default=False)

            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            user = db.relationship('User', backref=db.backref('dnd5e_characters', lazy=True))

        return CharacterDnD5e

    @staticmethod
    def create_cthulhu_model(db):
        """Model dla Call of Cthulhu"""

        class CharacterCthulhu(db.Model):
            __tablename__ = 'characters_cthulhu'

            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

            imie = db.Column(db.String(100), default='')
            gracz = db.Column(db.String(100), default='')
            profesja = db.Column(db.String(100), default='')
            wiek = db.Column(db.String(50), default='')
            plec = db.Column(db.String(50), default='')
            miejsce = db.Column(db.String(100), default='')

            # Statystyki z formularza HTML
            s = db.Column(db.Integer, default=0)
            zr = db.Column(db.Integer, default=0)
            moc = db.Column(db.Integer, default=0)
            pw1 = db.Column(db.Integer, default=0)
            pw2 = db.Column(db.Integer, default=0)
            kon = db.Column(db.Integer, default=0)
            wyg = db.Column(db.Integer, default=0)
            wyk = db.Column(db.Integer, default=0)
            szczescie = db.Column(db.Integer, default=0)
            bc = db.Column(db.Integer, default=0)
            intel = db.Column(db.Integer, default=0)
            ruch = db.Column(db.Integer, default=0)
            poczytalnosc = db.Column(db.Integer, default=0)

            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            user = db.relationship('User', backref=db.backref('cthulhu_characters', lazy=True))

        return CharacterCthulhu

    @staticmethod
    def create_cthulhu_skills_model(db):
        """Model dla umiejętności Cthulhu"""

        class CthulhuSkill(db.Model):
            __tablename__ = 'cthulhu_skills'

            id = db.Column(db.Integer, primary_key=True)
            character_id = db.Column(db.Integer, db.ForeignKey('characters_cthulhu.id'), nullable=False)

            # Kolumna 1
            antropologia = db.Column(db.Integer, default=1)
            archeologia = db.Column(db.Integer, default=1)
            bron_karabin = db.Column(db.Integer, default=25)
            bron_karabin_custom = db.Column(db.String(100), default='')
            bron_krotka = db.Column(db.Integer, default=20)
            charakteryzacja = db.Column(db.Integer, default=5)
            elektryka = db.Column(db.Integer, default=10)
            gadanina = db.Column(db.Integer, default=5)
            historia = db.Column(db.Integer, default=5)
            jezdziectwo = db.Column(db.Integer, default=5)
            jezyk_obcy_1 = db.Column(db.String(50), default='')
            jezyk_obcy_1_val = db.Column(db.Integer, default=1)
            jezyk_obcy_2 = db.Column(db.String(50), default='')
            jezyk_obcy_2_val = db.Column(db.Integer, default=1)
            jezyk_obcy_3 = db.Column(db.String(50), default='')
            jezyk_obcy_3_val = db.Column(db.Integer, default=1)
            jezyk_ojczysty = db.Column(db.String(50), default='')
            jezyk_ojczysty_val = db.Column(db.Integer, default=0)
            biblioteki = db.Column(db.Integer, default=20)

            # Kolumna 2
            ksiegowosc = db.Column(db.Integer, default=5)
            majetnosc = db.Column(db.Integer, default=0)
            mechanika = db.Column(db.Integer, default=10)
            medycyna = db.Column(db.Integer, default=1)
            mity_cthulhu = db.Column(db.Integer, default=0)
            nasluchiwanie = db.Column(db.Integer, default=20)
            nauka_1 = db.Column(db.String(50), default='')
            nauka_1_val = db.Column(db.Integer, default=1)
            nauka_2 = db.Column(db.String(50), default='')
            nauka_2_val = db.Column(db.Integer, default=1)
            nauka_3 = db.Column(db.String(50), default='')
            nauka_3_val = db.Column(db.Integer, default=1)
            nawigacja = db.Column(db.Integer, default=10)
            ciezki_sprzet = db.Column(db.Integer, default=1)
            okultyzm = db.Column(db.Integer, default=5)
            perswazja = db.Column(db.Integer, default=10)
            pierwsza_pomoc = db.Column(db.Integer, default=30)
            pilotowanie = db.Column(db.String(50), default='')
            pilotowanie_val = db.Column(db.Integer, default=1)

            # Kolumna 3
            plywanie = db.Column(db.Integer, default=20)
            prawo = db.Column(db.Integer, default=5)
            prowadzenie = db.Column(db.Integer, default=20)
            psychoanaliza = db.Column(db.Integer, default=1)
            psychologia = db.Column(db.Integer, default=10)
            rzucanie = db.Column(db.Integer, default=20)
            skakanie = db.Column(db.Integer, default=20)
            spostrzegawczosc = db.Column(db.Integer, default=25)
            sztuka_1 = db.Column(db.String(50), default='')
            sztuka_1_val = db.Column(db.Integer, default=5)
            sztuka_2 = db.Column(db.String(50), default='')
            sztuka_2_val = db.Column(db.Integer, default=5)
            sztuka_3 = db.Column(db.String(50), default='')
            sztuka_3_val = db.Column(db.Integer, default=5)
            przetrwanie = db.Column(db.String(50), default='')
            przetrwanie_val = db.Column(db.Integer, default=10)
            slusarstwo = db.Column(db.Integer, default=1)
            tropienie = db.Column(db.Integer, default=10)
            ukrywanie = db.Column(db.Integer, default=20)

            # Kolumna 4
            unik = db.Column(db.Integer, default=0)
            urok = db.Column(db.Integer, default=15)
            walka_wrecz = db.Column(db.Integer, default=25)
            walka_custom_1 = db.Column(db.String(50), default='')
            walka_custom_1_val = db.Column(db.Integer, default=0)
            walka_custom_2 = db.Column(db.String(50), default='')
            walka_custom_2_val = db.Column(db.Integer, default=0)
            natura = db.Column(db.Integer, default=10)
            wspinaczka = db.Column(db.Integer, default=20)
            wycena = db.Column(db.Integer, default=5)
            zastraszanie = db.Column(db.Integer, default=15)
            zreczne_palce = db.Column(db.Integer, default=10)
            custom_skill_1 = db.Column(db.String(50), default='')
            custom_skill_1_val = db.Column(db.Integer, default=0)
            custom_skill_2 = db.Column(db.String(50), default='')
            custom_skill_2_val = db.Column(db.Integer, default=0)
            custom_skill_3 = db.Column(db.String(50), default='')
            custom_skill_3_val = db.Column(db.Integer, default=0)
            custom_skill_4 = db.Column(db.String(50), default='')
            custom_skill_4_val = db.Column(db.Integer, default=0)
            custom_skill_5 = db.Column(db.String(50), default='')
            custom_skill_5_val = db.Column(db.Integer, default=0)

            character = db.relationship('CharacterCthulhu', backref=db.backref('skills', lazy=True))

        return CthulhuSkill