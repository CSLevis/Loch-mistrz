from datetime import datetime


def create_dnd3e_skills_model(db):
    """Model dla umiejętności D&D 3e"""

    class DnD3eSkills(db.Model):
        __tablename__ = 'dnd3e_skills'

        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd3e.id'), nullable=False)

        # Umiejętności według listy z karty D&D 3e
        # Format: nazwa_klasowe (bool), nazwa_ranga (int), nazwa_mod_cechy (int), nazwa_inne (int), nazwa_razem (int)

        # Alchemia (int)
        alchemia_klasowe = db.Column(db.Boolean, default=False)
        alchemia_ranga = db.Column(db.Integer, default=0)
        alchemia_mod = db.Column(db.Integer, default=0)
        alchemia_inne = db.Column(db.Integer, default=0)
        alchemia_razem = db.Column(db.Integer, default=0)

        # Blefowanie/zwody (cha)
        blefowanie_klasowe = db.Column(db.Boolean, default=False)
        blefowanie_ranga = db.Column(db.Integer, default=0)
        blefowanie_mod = db.Column(db.Integer, default=0)
        blefowanie_inne = db.Column(db.Integer, default=0)
        blefowanie_razem = db.Column(db.Integer, default=0)

        # Ciche poruszanie (zr*)
        ciche_poruszanie_klasowe = db.Column(db.Boolean, default=False)
        ciche_poruszanie_ranga = db.Column(db.Integer, default=0)
        ciche_poruszanie_mod = db.Column(db.Integer, default=0)
        ciche_poruszanie_inne = db.Column(db.Integer, default=0)
        ciche_poruszanie_razem = db.Column(db.Integer, default=0)

        # Czarostwo/Teoria czarów (int)
        czarostwo_klasowe = db.Column(db.Boolean, default=False)
        czarostwo_ranga = db.Column(db.Integer, default=0)
        czarostwo_mod = db.Column(db.Integer, default=0)
        czarostwo_inne = db.Column(db.Integer, default=0)
        czarostwo_razem = db.Column(db.Integer, default=0)

        # Czytanie z warg (int)
        czytanie_warg_klasowe = db.Column(db.Boolean, default=False)
        czytanie_warg_ranga = db.Column(db.Integer, default=0)
        czytanie_warg_mod = db.Column(db.Integer, default=0)
        czytanie_warg_inne = db.Column(db.Integer, default=0)
        czytanie_warg_razem = db.Column(db.Integer, default=0)

        # Dyplomacja (cha)
        dyplomacja_klasowe = db.Column(db.Boolean, default=False)
        dyplomacja_ranga = db.Column(db.Integer, default=0)
        dyplomacja_mod = db.Column(db.Integer, default=0)
        dyplomacja_inne = db.Column(db.Integer, default=0)
        dyplomacja_razem = db.Column(db.Integer, default=0)

        # Fałszerstwo (int)
        falszerstwo_klasowe = db.Column(db.Boolean, default=False)
        falszerstwo_ranga = db.Column(db.Integer, default=0)
        falszerstwo_mod = db.Column(db.Integer, default=0)
        falszerstwo_inne = db.Column(db.Integer, default=0)
        falszerstwo_razem = db.Column(db.Integer, default=0)

        # Jeździectwo (zr)
        jezdziectwo_klasowe = db.Column(db.Boolean, default=False)
        jezdziectwo_ranga = db.Column(db.Integer, default=0)
        jezdziectwo_mod = db.Column(db.Integer, default=0)
        jezdziectwo_inne = db.Column(db.Integer, default=0)
        jezdziectwo_razem = db.Column(db.Integer, default=0)

        # Koncentracja (bc)
        koncentracja_klasowe = db.Column(db.Boolean, default=False)
        koncentracja_ranga = db.Column(db.Integer, default=0)
        koncentracja_mod = db.Column(db.Integer, default=0)
        koncentracja_inne = db.Column(db.Integer, default=0)
        koncentracja_razem = db.Column(db.Integer, default=0)

        # Kradzież kieszonkowa (zr*)
        kradziez_kieszonkowa_klasowe = db.Column(db.Boolean, default=False)
        kradziez_kieszonkowa_ranga = db.Column(db.Integer, default=0)
        kradziez_kieszonkowa_mod = db.Column(db.Integer, default=0)
        kradziez_kieszonkowa_inne = db.Column(db.Integer, default=0)
        kradziez_kieszonkowa_razem = db.Column(db.Integer, default=0)

        # Leczenie (md)
        leczenie_klasowe = db.Column(db.Boolean, default=False)
        leczenie_ranga = db.Column(db.Integer, default=0)
        leczenie_mod = db.Column(db.Integer, default=0)
        leczenie_inne = db.Column(db.Integer, default=0)
        leczenie_razem = db.Column(db.Integer, default=0)

        # Nasłuchiwanie (md)
        nasluchiwanie_klasowe = db.Column(db.Boolean, default=False)
        nasluchiwanie_ranga = db.Column(db.Integer, default=0)
        nasluchiwanie_mod = db.Column(db.Integer, default=0)
        nasluchiwanie_inne = db.Column(db.Integer, default=0)
        nasluchiwanie_razem = db.Column(db.Integer, default=0)

        # Odcyfrowywanie zapisów (int)
        odcyfrowywanie_klasowe = db.Column(db.Boolean, default=False)
        odcyfrowywanie_ranga = db.Column(db.Integer, default=0)
        odcyfrowywanie_mod = db.Column(db.Integer, default=0)
        odcyfrowywanie_inne = db.Column(db.Integer, default=0)
        odcyfrowywanie_razem = db.Column(db.Integer, default=0)

        # Otwieranie zamków (zr*)
        otwieranie_zamkow_klasowe = db.Column(db.Boolean, default=False)
        otwieranie_zamkow_ranga = db.Column(db.Integer, default=0)
        otwieranie_zamkow_mod = db.Column(db.Integer, default=0)
        otwieranie_zamkow_inne = db.Column(db.Integer, default=0)
        otwieranie_zamkow_razem = db.Column(db.Integer, default=0)

        # Pływanie (sił**)
        plywanie_klasowe = db.Column(db.Boolean, default=False)
        plywanie_ranga = db.Column(db.Integer, default=0)
        plywanie_mod = db.Column(db.Integer, default=0)
        plywanie_inne = db.Column(db.Integer, default=0)
        plywanie_razem = db.Column(db.Integer, default=0)

        # Postępowanie ze zwierzętami (cha)
        postepowanie_zwierzeta_klasowe = db.Column(db.Boolean, default=False)
        postepowanie_zwierzeta_ranga = db.Column(db.Integer, default=0)
        postepowanie_zwierzeta_mod = db.Column(db.Integer, default=0)
        postepowanie_zwierzeta_inne = db.Column(db.Integer, default=0)
        postepowanie_zwierzeta_razem = db.Column(db.Integer, default=0)

        # Półsłówka (md)
        polslowka_klasowe = db.Column(db.Boolean, default=False)
        polslowka_ranga = db.Column(db.Integer, default=0)
        polslowka_mod = db.Column(db.Integer, default=0)
        polslowka_inne = db.Column(db.Integer, default=0)
        polslowka_razem = db.Column(db.Integer, default=0)

        # Profesja (md) - 3 sloty
        profesja_1_nazwa = db.Column(db.String(100), default='')
        profesja_1_klasowe = db.Column(db.Boolean, default=False)
        profesja_1_ranga = db.Column(db.Integer, default=0)
        profesja_1_mod = db.Column(db.Integer, default=0)
        profesja_1_inne = db.Column(db.Integer, default=0)
        profesja_1_razem = db.Column(db.Integer, default=0)

        profesja_2_nazwa = db.Column(db.String(100), default='')
        profesja_2_klasowe = db.Column(db.Boolean, default=False)
        profesja_2_ranga = db.Column(db.Integer, default=0)
        profesja_2_mod = db.Column(db.Integer, default=0)
        profesja_2_inne = db.Column(db.Integer, default=0)
        profesja_2_razem = db.Column(db.Integer, default=0)

        profesja_3_nazwa = db.Column(db.String(100), default='')
        profesja_3_klasowe = db.Column(db.Boolean, default=False)
        profesja_3_ranga = db.Column(db.Integer, default=0)
        profesja_3_mod = db.Column(db.Integer, default=0)
        profesja_3_inne = db.Column(db.Integer, default=0)
        profesja_3_razem = db.Column(db.Integer, default=0)

        # Przebieranie (cha)
        przebieranie_klasowe = db.Column(db.Boolean, default=False)
        przebieranie_ranga = db.Column(db.Integer, default=0)
        przebieranie_mod = db.Column(db.Integer, default=0)
        przebieranie_inne = db.Column(db.Integer, default=0)
        przebieranie_razem = db.Column(db.Integer, default=0)

        # Przeszukiwanie (int)
        przeszukiwanie_klasowe = db.Column(db.Boolean, default=False)
        przeszukiwanie_ranga = db.Column(db.Integer, default=0)
        przeszukiwanie_mod = db.Column(db.Integer, default=0)
        przeszukiwanie_inne = db.Column(db.Integer, default=0)
        przeszukiwanie_razem = db.Column(db.Integer, default=0)

        # Równowaga (zr*)
        rownowaga_klasowe = db.Column(db.Boolean, default=False)
        rownowaga_ranga = db.Column(db.Integer, default=0)
        rownowaga_mod = db.Column(db.Integer, default=0)
        rownowaga_inne = db.Column(db.Integer, default=0)
        rownowaga_razem = db.Column(db.Integer, default=0)

        # Rzemiosło (int) - 3 sloty
        rzemioslo_1_nazwa = db.Column(db.String(100), default='')
        rzemioslo_1_klasowe = db.Column(db.Boolean, default=False)
        rzemioslo_1_ranga = db.Column(db.Integer, default=0)
        rzemioslo_1_mod = db.Column(db.Integer, default=0)
        rzemioslo_1_inne = db.Column(db.Integer, default=0)
        rzemioslo_1_razem = db.Column(db.Integer, default=0)

        rzemioslo_2_nazwa = db.Column(db.String(100), default='')
        rzemioslo_2_klasowe = db.Column(db.Boolean, default=False)
        rzemioslo_2_ranga = db.Column(db.Integer, default=0)
        rzemioslo_2_mod = db.Column(db.Integer, default=0)
        rzemioslo_2_inne = db.Column(db.Integer, default=0)
        rzemioslo_2_razem = db.Column(db.Integer, default=0)

        rzemioslo_3_nazwa = db.Column(db.String(100), default='')
        rzemioslo_3_klasowe = db.Column(db.Boolean, default=False)
        rzemioslo_3_ranga = db.Column(db.Integer, default=0)
        rzemioslo_3_mod = db.Column(db.Integer, default=0)
        rzemioslo_3_inne = db.Column(db.Integer, default=0)
        rzemioslo_3_razem = db.Column(db.Integer, default=0)

        # Skakanie (sił*)
        skakanie_klasowe = db.Column(db.Boolean, default=False)
        skakanie_ranga = db.Column(db.Integer, default=0)
        skakanie_mod = db.Column(db.Integer, default=0)
        skakanie_inne = db.Column(db.Integer, default=0)
        skakanie_razem = db.Column(db.Integer, default=0)

        # Stosowanie liny (zr)
        stosowanie_liny_klasowe = db.Column(db.Boolean, default=False)
        stosowanie_liny_ranga = db.Column(db.Integer, default=0)
        stosowanie_liny_mod = db.Column(db.Integer, default=0)
        stosowanie_liny_inne = db.Column(db.Integer, default=0)
        stosowanie_liny_razem = db.Column(db.Integer, default=0)

        # Stosowanie magicznych rzeczy (cha)
        stosowanie_magicznych_klasowe = db.Column(db.Boolean, default=False)
        stosowanie_magicznych_ranga = db.Column(db.Integer, default=0)
        stosowanie_magicznych_mod = db.Column(db.Integer, default=0)
        stosowanie_magicznych_inne = db.Column(db.Integer, default=0)
        stosowanie_magicznych_razem = db.Column(db.Integer, default=0)

        # Szacowanie (int)
        szacowanie_klasowe = db.Column(db.Boolean, default=False)
        szacowanie_ranga = db.Column(db.Integer, default=0)
        szacowanie_mod = db.Column(db.Integer, default=0)
        szacowanie_inne = db.Column(db.Integer, default=0)
        szacowanie_razem = db.Column(db.Integer, default=0)

        # Tajniki dziczy (md)
        tajniki_dziczy_klasowe = db.Column(db.Boolean, default=False)
        tajniki_dziczy_ranga = db.Column(db.Integer, default=0)
        tajniki_dziczy_mod = db.Column(db.Integer, default=0)
        tajniki_dziczy_inne = db.Column(db.Integer, default=0)
        tajniki_dziczy_razem = db.Column(db.Integer, default=0)

        # Ukrywanie się (zr*)
        ukrywanie_klasowe = db.Column(db.Boolean, default=False)
        ukrywanie_ranga = db.Column(db.Integer, default=0)
        ukrywanie_mod = db.Column(db.Integer, default=0)
        ukrywanie_inne = db.Column(db.Integer, default=0)
        ukrywanie_razem = db.Column(db.Integer, default=0)

        # Unieszkodliwianie urządzeń (int)
        unieszkodliwianie_klasowe = db.Column(db.Boolean, default=False)
        unieszkodliwianie_ranga = db.Column(db.Integer, default=0)
        unieszkodliwianie_mod = db.Column(db.Integer, default=0)
        unieszkodliwianie_inne = db.Column(db.Integer, default=0)
        unieszkodliwianie_razem = db.Column(db.Integer, default=0)

        # Upadki/Przewroty (zr*)
        upadki_klasowe = db.Column(db.Boolean, default=False)
        upadki_ranga = db.Column(db.Integer, default=0)
        upadki_mod = db.Column(db.Integer, default=0)
        upadki_inne = db.Column(db.Integer, default=0)
        upadki_razem = db.Column(db.Integer, default=0)

        # Wiedza (int) - 10 slotów
        wiedza_1_nazwa = db.Column(db.String(100), default='')
        wiedza_1_klasowe = db.Column(db.Boolean, default=False)
        wiedza_1_ranga = db.Column(db.Integer, default=0)
        wiedza_1_mod = db.Column(db.Integer, default=0)
        wiedza_1_inne = db.Column(db.Integer, default=0)
        wiedza_1_razem = db.Column(db.Integer, default=0)

        wiedza_2_nazwa = db.Column(db.String(100), default='')
        wiedza_2_klasowe = db.Column(db.Boolean, default=False)
        wiedza_2_ranga = db.Column(db.Integer, default=0)
        wiedza_2_mod = db.Column(db.Integer, default=0)
        wiedza_2_inne = db.Column(db.Integer, default=0)
        wiedza_2_razem = db.Column(db.Integer, default=0)

        wiedza_3_nazwa = db.Column(db.String(100), default='')
        wiedza_3_klasowe = db.Column(db.Boolean, default=False)
        wiedza_3_ranga = db.Column(db.Integer, default=0)
        wiedza_3_mod = db.Column(db.Integer, default=0)
        wiedza_3_inne = db.Column(db.Integer, default=0)
        wiedza_3_razem = db.Column(db.Integer, default=0)

        wiedza_4_nazwa = db.Column(db.String(100), default='')
        wiedza_4_klasowe = db.Column(db.Boolean, default=False)
        wiedza_4_ranga = db.Column(db.Integer, default=0)
        wiedza_4_mod = db.Column(db.Integer, default=0)
        wiedza_4_inne = db.Column(db.Integer, default=0)
        wiedza_4_razem = db.Column(db.Integer, default=0)

        wiedza_5_nazwa = db.Column(db.String(100), default='')
        wiedza_5_klasowe = db.Column(db.Boolean, default=False)
        wiedza_5_ranga = db.Column(db.Integer, default=0)
        wiedza_5_mod = db.Column(db.Integer, default=0)
        wiedza_5_inne = db.Column(db.Integer, default=0)
        wiedza_5_razem = db.Column(db.Integer, default=0)

        wiedza_6_nazwa = db.Column(db.String(100), default='')
        wiedza_6_klasowe = db.Column(db.Boolean, default=False)
        wiedza_6_ranga = db.Column(db.Integer, default=0)
        wiedza_6_mod = db.Column(db.Integer, default=0)
        wiedza_6_inne = db.Column(db.Integer, default=0)
        wiedza_6_razem = db.Column(db.Integer, default=0)

        wiedza_7_nazwa = db.Column(db.String(100), default='')
        wiedza_7_klasowe = db.Column(db.Boolean, default=False)
        wiedza_7_ranga = db.Column(db.Integer, default=0)
        wiedza_7_mod = db.Column(db.Integer, default=0)
        wiedza_7_inne = db.Column(db.Integer, default=0)
        wiedza_7_razem = db.Column(db.Integer, default=0)

        wiedza_8_nazwa = db.Column(db.String(100), default='')
        wiedza_8_klasowe = db.Column(db.Boolean, default=False)
        wiedza_8_ranga = db.Column(db.Integer, default=0)
        wiedza_8_mod = db.Column(db.Integer, default=0)
        wiedza_8_inne = db.Column(db.Integer, default=0)
        wiedza_8_razem = db.Column(db.Integer, default=0)

        wiedza_9_nazwa = db.Column(db.String(100), default='')
        wiedza_9_klasowe = db.Column(db.Boolean, default=False)
        wiedza_9_ranga = db.Column(db.Integer, default=0)
        wiedza_9_mod = db.Column(db.Integer, default=0)
        wiedza_9_inne = db.Column(db.Integer, default=0)
        wiedza_9_razem = db.Column(db.Integer, default=0)

        wiedza_10_nazwa = db.Column(db.String(100), default='')
        wiedza_10_klasowe = db.Column(db.Boolean, default=False)
        wiedza_10_ranga = db.Column(db.Integer, default=0)
        wiedza_10_mod = db.Column(db.Integer, default=0)
        wiedza_10_inne = db.Column(db.Integer, default=0)
        wiedza_10_razem = db.Column(db.Integer, default=0)

        # Wróżenie (int)
        wrozenie_klasowe = db.Column(db.Boolean, default=False)
        wrozenie_ranga = db.Column(db.Integer, default=0)
        wrozenie_mod = db.Column(db.Integer, default=0)
        wrozenie_inne = db.Column(db.Integer, default=0)
        wrozenie_razem = db.Column(db.Integer, default=0)

        # Wspinaczka (sił*)
        wspinaczka_klasowe = db.Column(db.Boolean, default=False)
        wspinaczka_ranga = db.Column(db.Integer, default=0)
        wspinaczka_mod = db.Column(db.Integer, default=0)
        wspinaczka_inne = db.Column(db.Integer, default=0)
        wspinaczka_razem = db.Column(db.Integer, default=0)

        # Wyczucie kierunku (md)
        wyczucie_kierunku_klasowe = db.Column(db.Boolean, default=False)
        wyczucie_kierunku_ranga = db.Column(db.Integer, default=0)
        wyczucie_kierunku_mod = db.Column(db.Integer, default=0)
        wyczucie_kierunku_inne = db.Column(db.Integer, default=0)
        wyczucie_kierunku_razem = db.Column(db.Integer, default=0)

        # Wyczucie pobudek (md)
        wyczucie_pobudek_klasowe = db.Column(db.Boolean, default=False)
        wyczucie_pobudek_ranga = db.Column(db.Integer, default=0)
        wyczucie_pobudek_mod = db.Column(db.Integer, default=0)
        wyczucie_pobudek_inne = db.Column(db.Integer, default=0)
        wyczucie_pobudek_razem = db.Column(db.Integer, default=0)

        # Występy (cha) - 3 sloty
        wystepy_1_nazwa = db.Column(db.String(100), default='')
        wystepy_1_klasowe = db.Column(db.Boolean, default=False)
        wystepy_1_ranga = db.Column(db.Integer, default=0)
        wystepy_1_mod = db.Column(db.Integer, default=0)
        wystepy_1_inne = db.Column(db.Integer, default=0)
        wystepy_1_razem = db.Column(db.Integer, default=0)

        wystepy_2_nazwa = db.Column(db.String(100), default='')
        wystepy_2_klasowe = db.Column(db.Boolean, default=False)
        wystepy_2_ranga = db.Column(db.Integer, default=0)
        wystepy_2_mod = db.Column(db.Integer, default=0)
        wystepy_2_inne = db.Column(db.Integer, default=0)
        wystepy_2_razem = db.Column(db.Integer, default=0)

        wystepy_3_nazwa = db.Column(db.String(100), default='')
        wystepy_3_klasowe = db.Column(db.Boolean, default=False)
        wystepy_3_ranga = db.Column(db.Integer, default=0)
        wystepy_3_mod = db.Column(db.Integer, default=0)
        wystepy_3_inne = db.Column(db.Integer, default=0)
        wystepy_3_razem = db.Column(db.Integer, default=0)

        # Wyzwalanie się/ucieczki (zr*)
        wyzwalanie_klasowe = db.Column(db.Boolean, default=False)
        wyzwalanie_ranga = db.Column(db.Integer, default=0)
        wyzwalanie_mod = db.Column(db.Integer, default=0)
        wyzwalanie_inne = db.Column(db.Integer, default=0)
        wyzwalanie_razem = db.Column(db.Integer, default=0)

        # Zastraszanie (cha)
        zastraszanie_klasowe = db.Column(db.Boolean, default=False)
        zastraszanie_ranga = db.Column(db.Integer, default=0)
        zastraszanie_mod = db.Column(db.Integer, default=0)
        zastraszanie_inne = db.Column(db.Integer, default=0)
        zastraszanie_razem = db.Column(db.Integer, default=0)

        # Zauważenie (md)
        zauwazenie_klasowe = db.Column(db.Boolean, default=False)
        zauwazenie_ranga = db.Column(db.Integer, default=0)
        zauwazenie_mod = db.Column(db.Integer, default=0)
        zauwazenie_inne = db.Column(db.Integer, default=0)
        zauwazenie_razem = db.Column(db.Integer, default=0)

        # Zbieranie informacji (cha)
        zbieranie_info_klasowe = db.Column(db.Boolean, default=False)
        zbieranie_info_ranga = db.Column(db.Integer, default=0)
        zbieranie_info_mod = db.Column(db.Integer, default=0)
        zbieranie_info_inne = db.Column(db.Integer, default=0)
        zbieranie_info_razem = db.Column(db.Integer, default=0)

        # Zwierzęca empatia (cha)
        zwierzeca_empatia_klasowe = db.Column(db.Boolean, default=False)
        zwierzeca_empatia_ranga = db.Column(db.Integer, default=0)
        zwierzeca_empatia_mod = db.Column(db.Integer, default=0)
        zwierzeca_empatia_inne = db.Column(db.Integer, default=0)
        zwierzeca_empatia_razem = db.Column(db.Integer, default=0)

        # Dodatkowe umiejętności (custom) - 5 slotów
        custom_1_nazwa = db.Column(db.String(100), default='')
        custom_1_klasowe = db.Column(db.Boolean, default=False)
        custom_1_ranga = db.Column(db.Integer, default=0)
        custom_1_mod = db.Column(db.Integer, default=0)
        custom_1_inne = db.Column(db.Integer, default=0)
        custom_1_razem = db.Column(db.Integer, default=0)

        custom_2_nazwa = db.Column(db.String(100), default='')
        custom_2_klasowe = db.Column(db.Boolean, default=False)
        custom_2_ranga = db.Column(db.Integer, default=0)
        custom_2_mod = db.Column(db.Integer, default=0)
        custom_2_inne = db.Column(db.Integer, default=0)
        custom_2_razem = db.Column(db.Integer, default=0)

        custom_3_nazwa = db.Column(db.String(100), default='')
        custom_3_klasowe = db.Column(db.Boolean, default=False)
        custom_3_ranga = db.Column(db.Integer, default=0)
        custom_3_mod = db.Column(db.Integer, default=0)
        custom_3_inne = db.Column(db.Integer, default=0)
        custom_3_razem = db.Column(db.Integer, default=0)

        custom_4_nazwa = db.Column(db.String(100), default='')
        custom_4_klasowe = db.Column(db.Boolean, default=False)
        custom_4_ranga = db.Column(db.Integer, default=0)
        custom_4_mod = db.Column(db.Integer, default=0)
        custom_4_inne = db.Column(db.Integer, default=0)
        custom_4_razem = db.Column(db.Integer, default=0)

        custom_5_nazwa = db.Column(db.String(100), default='')
        custom_5_klasowe = db.Column(db.Boolean, default=False)
        custom_5_ranga = db.Column(db.Integer, default=0)
        custom_5_mod = db.Column(db.Integer, default=0)
        custom_5_inne = db.Column(db.Integer, default=0)
        custom_5_razem = db.Column(db.Integer, default=0)

        character = db.relationship('CharacterDnD3e', backref=db.backref('skills', lazy=True, uselist=False))

    return DnD3eSkills


def create_dnd3e_abilities_model(db):
    """Model dla zdolności specjalnych D&D 3e"""

    class DnD3eAbilities(db.Model):
        __tablename__ = 'dnd3e_abilities'

        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd3e.id'), nullable=False)

        # Zdolności rasowe - 10 slotów
        rasowe_1_nazwa = db.Column(db.String(200), default='')
        rasowe_1_opis = db.Column(db.Text, default='')
        rasowe_2_nazwa = db.Column(db.String(200), default='')
        rasowe_2_opis = db.Column(db.Text, default='')
        rasowe_3_nazwa = db.Column(db.String(200), default='')
        rasowe_3_opis = db.Column(db.Text, default='')
        rasowe_4_nazwa = db.Column(db.String(200), default='')
        rasowe_4_opis = db.Column(db.Text, default='')
        rasowe_5_nazwa = db.Column(db.String(200), default='')
        rasowe_5_opis = db.Column(db.Text, default='')
        rasowe_6_nazwa = db.Column(db.String(200), default='')
        rasowe_6_opis = db.Column(db.Text, default='')
        rasowe_7_nazwa = db.Column(db.String(200), default='')
        rasowe_7_opis = db.Column(db.Text, default='')
        rasowe_8_nazwa = db.Column(db.String(200), default='')
        rasowe_8_opis = db.Column(db.Text, default='')
        rasowe_9_nazwa = db.Column(db.String(200), default='')
        rasowe_9_opis = db.Column(db.Text, default='')
        rasowe_10_nazwa = db.Column(db.String(200), default='')
        rasowe_10_opis = db.Column(db.Text, default='')

        # Zdolności klasowe - 20 slotów
        klasowe_1_nazwa = db.Column(db.String(200), default='')
        klasowe_1_opis = db.Column(db.Text, default='')
        klasowe_2_nazwa = db.Column(db.String(200), default='')
        klasowe_2_opis = db.Column(db.Text, default='')
        klasowe_3_nazwa = db.Column(db.String(200), default='')
        klasowe_3_opis = db.Column(db.Text, default='')
        klasowe_4_nazwa = db.Column(db.String(200), default='')
        klasowe_4_opis = db.Column(db.Text, default='')
        klasowe_5_nazwa = db.Column(db.String(200), default='')
        klasowe_5_opis = db.Column(db.Text, default='')
        klasowe_6_nazwa = db.Column(db.String(200), default='')
        klasowe_6_opis = db.Column(db.Text, default='')
        klasowe_7_nazwa = db.Column(db.String(200), default='')
        klasowe_7_opis = db.Column(db.Text, default='')
        klasowe_8_nazwa = db.Column(db.String(200), default='')
        klasowe_8_opis = db.Column(db.Text, default='')
        klasowe_9_nazwa = db.Column(db.String(200), default='')
        klasowe_9_opis = db.Column(db.Text, default='')
        klasowe_10_nazwa = db.Column(db.String(200), default='')
        klasowe_10_opis = db.Column(db.Text, default='')
        klasowe_11_nazwa = db.Column(db.String(200), default='')
        klasowe_11_opis = db.Column(db.Text, default='')
        klasowe_12_nazwa = db.Column(db.String(200), default='')
        klasowe_12_opis = db.Column(db.Text, default='')
        klasowe_13_nazwa = db.Column(db.String(200), default='')
        klasowe_13_opis = db.Column(db.Text, default='')
        klasowe_14_nazwa = db.Column(db.String(200), default='')
        klasowe_14_opis = db.Column(db.Text, default='')
        klasowe_15_nazwa = db.Column(db.String(200), default='')
        klasowe_15_opis = db.Column(db.Text, default='')
        klasowe_16_nazwa = db.Column(db.String(200), default='')
        klasowe_16_opis = db.Column(db.Text, default='')
        klasowe_17_nazwa = db.Column(db.String(200), default='')
        klasowe_17_opis = db.Column(db.Text, default='')
        klasowe_18_nazwa = db.Column(db.String(200), default='')
        klasowe_18_opis = db.Column(db.Text, default='')
        klasowe_19_nazwa = db.Column(db.String(200), default='')
        klasowe_19_opis = db.Column(db.Text, default='')
        klasowe_20_nazwa = db.Column(db.String(200), default='')
        klasowe_20_opis = db.Column(db.Text, default='')

        # Atuty wyuczone (Feats) - 15 slotów
        atuty_1_nazwa = db.Column(db.String(200), default='')
        atuty_1_opis = db.Column(db.Text, default='')
        atuty_2_nazwa = db.Column(db.String(200), default='')
        atuty_2_opis = db.Column(db.Text, default='')
        atuty_3_nazwa = db.Column(db.String(200), default='')
        atuty_3_opis = db.Column(db.Text, default='')
        atuty_4_nazwa = db.Column(db.String(200), default='')
        atuty_4_opis = db.Column(db.Text, default='')
        atuty_5_nazwa = db.Column(db.String(200), default='')
        atuty_5_opis = db.Column(db.Text, default='')
        atuty_6_nazwa = db.Column(db.String(200), default='')
        atuty_6_opis = db.Column(db.Text, default='')
        atuty_7_nazwa = db.Column(db.String(200), default='')
        atuty_7_opis = db.Column(db.Text, default='')
        atuty_8_nazwa = db.Column(db.String(200), default='')
        atuty_8_opis = db.Column(db.Text, default='')
        atuty_9_nazwa = db.Column(db.String(200), default='')
        atuty_9_opis = db.Column(db.Text, default='')
        atuty_10_nazwa = db.Column(db.String(200), default='')
        atuty_10_opis = db.Column(db.Text, default='')
        atuty_11_nazwa = db.Column(db.String(200), default='')
        atuty_11_opis = db.Column(db.Text, default='')
        atuty_12_nazwa = db.Column(db.String(200), default='')
        atuty_12_opis = db.Column(db.Text, default='')
        atuty_13_nazwa = db.Column(db.String(200), default='')
        atuty_13_opis = db.Column(db.Text, default='')
        atuty_14_nazwa = db.Column(db.String(200), default='')
        atuty_14_opis = db.Column(db.Text, default='')
        atuty_15_nazwa = db.Column(db.String(200), default='')
        atuty_15_opis = db.Column(db.Text, default='')

        character = db.relationship('CharacterDnD3e', backref=db.backref('abilities', lazy=True, uselist=False))

    return DnD3eAbilities


def create_dnd3e_equipment_model(db):
    """Model dla ekwipunku D&D 3e"""

    class DnD3eEquipment(db.Model):
        __tablename__ = 'dnd3e_equipment'

        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd3e.id'), nullable=False)
        item_index = db.Column(db.Integer, default=0)  # 0-39 (40 slotów)

        nazwa = db.Column(db.String(200), default='')
        waga = db.Column(db.String(50), default='')
        wartosc = db.Column(db.String(50), default='')
        opis = db.Column(db.Text, default='')

        character = db.relationship('CharacterDnD3e', backref=db.backref('equipment', lazy=True))

    return DnD3eEquipment


def create_dnd3e_magic_model(db):
    """Model dla magii D&D 3e"""

    class DnD3eMagic(db.Model):
        __tablename__ = 'dnd3e_magic'

        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd3e.id'), nullable=False)

        # Parametry czarów
        # Dla każdego poziomu (0p-9p): liczba na dzień, czary premiowe, ST obrony
        poziom_0_na_dzien = db.Column(db.Integer, default=0)
        poziom_0_premiowe = db.Column(db.Integer, default=0)
        poziom_0_st = db.Column(db.Integer, default=10)
        poziom_0_znanych = db.Column(db.Integer, default=0)  # Dla Bardów/Zaklinaczy

        poziom_1_na_dzien = db.Column(db.Integer, default=0)
        poziom_1_premiowe = db.Column(db.Integer, default=0)
        poziom_1_st = db.Column(db.Integer, default=11)
        poziom_1_znanych = db.Column(db.Integer, default=0)

        poziom_2_na_dzien = db.Column(db.Integer, default=0)
        poziom_2_premiowe = db.Column(db.Integer, default=0)
        poziom_2_st = db.Column(db.Integer, default=12)
        poziom_2_znanych = db.Column(db.Integer, default=0)

        poziom_3_na_dzien = db.Column(db.Integer, default=0)
        poziom_3_premiowe = db.Column(db.Integer, default=0)
        poziom_3_st = db.Column(db.Integer, default=13)
        poziom_3_znanych = db.Column(db.Integer, default=0)

        poziom_4_na_dzien = db.Column(db.Integer, default=0)
        poziom_4_premiowe = db.Column(db.Integer, default=0)
        poziom_4_st = db.Column(db.Integer, default=14)
        poziom_4_znanych = db.Column(db.Integer, default=0)

        poziom_5_na_dzien = db.Column(db.Integer, default=0)
        poziom_5_premiowe = db.Column(db.Integer, default=0)
        poziom_5_st = db.Column(db.Integer, default=15)
        poziom_5_znanych = db.Column(db.Integer, default=0)

        poziom_6_na_dzien = db.Column(db.Integer, default=0)
        poziom_6_premiowe = db.Column(db.Integer, default=0)
        poziom_6_st = db.Column(db.Integer, default=16)
        poziom_6_znanych = db.Column(db.Integer, default=0)

        poziom_7_na_dzien = db.Column(db.Integer, default=0)
        poziom_7_premiowe = db.Column(db.Integer, default=0)
        poziom_7_st = db.Column(db.Integer, default=17)
        poziom_7_znanych = db.Column(db.Integer, default=0)

        poziom_8_na_dzien = db.Column(db.Integer, default=0)
        poziom_8_premiowe = db.Column(db.Integer, default=0)
        poziom_8_st = db.Column(db.Integer, default=18)
        poziom_8_znanych = db.Column(db.Integer, default=0)

        poziom_9_na_dzien = db.Column(db.Integer, default=0)
        poziom_9_premiowe = db.Column(db.Integer, default=0)
        poziom_9_st = db.Column(db.Integer, default=19)
        poziom_9_znanych = db.Column(db.Integer, default=0)

        character = db.relationship('CharacterDnD3e', backref=db.backref('magic', lazy=True, uselist=False))

    return DnD3eMagic


def create_dnd3e_spell_model(db):
    """Model dla listy czarów D&D 3e"""

    class DnD3eSpell(db.Model):
        __tablename__ = 'dnd3e_spells'

        id = db.Column(db.Integer, primary_key=True)
        character_id = db.Column(db.Integer, db.ForeignKey('characters_dnd3e.id'), nullable=False)

        spell_type = db.Column(db.String(20), default='wyuczone')  # 'wyuczone' lub 'zapamiętane'
        spell_level = db.Column(db.Integer, default=0)  # 0-9
        spell_index = db.Column(db.Integer, default=0)  # pozycja w obrębie poziomu

        nazwa_czaru = db.Column(db.String(200), default='')

        character = db.relationship('CharacterDnD3e', backref=db.backref('spells', lazy=True))

    return DnD3eSpell
