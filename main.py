from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from roller import calculate_dice_roll
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from validators import validate_password
from character_cards import Character
from trader_manager import create_trader_models
from dnd5e_extras import create_dnd5e_extras_models
from npc_manager import create_npc_models

import os
import random
import string
from threading import Thread
from flask_mail import Mail, Message

app = Flask(__name__)

# Security: Prefer environment variables for production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '87484AF684B71AA28BE7A481655C2')

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'u7472955057@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'yzqt ztra jskk vapp'.replace(' ', ''))
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        try:
            print(f"DEBUG: Attempting to send email to {msg.recipients}...")
            mail.send(msg)
            print("DEBUG: Email sent successfully!")
        except Exception as e:
            print(f"CRITICAL ERROR sending email: {e}")
            import traceback
            traceback.print_exc()

# Database: Use PostgreSQL on Render, SQLite locally
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)

CharacterWarhammer = Character.create_warhammer_model(db)
CharacterDnD5e = Character.create_dnd5e_model(db)
CharacterCthulhu = Character.create_cthulhu_model(db)
CthulhuSkill = Character.create_cthulhu_skills_model(db)

# Trader Manager
TraderManager, TraderItem = create_trader_models(db)

# Rozpakuj modele z dnd5e_extras
(DnD5eBieglosc, DnD5eMagia, DnD5eSpell, DnD5eEkwipunek,
 WarhammerBron, WarhammerUmiejetnosc, WarhammerEkwipunek, WarhammerArmor,
 CthulhuBron) = create_dnd5e_extras_models(db)

# NPC Manager
NPCCthulhu, NPCWarhammer, NPCDnD5e = create_npc_models(db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    # Automatyczna migracja dla Trader Manager - sprawdź przed create_all()
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)

        if 'trader_item' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('trader_item')]

            # Sprawdź czy struktura tabeli jest poprawna
            needs_migration = False
            if 'item_index' not in columns:
                needs_migration = True
                print("! Brak kolumny item_index")
            if 'cena' in columns and 'cena_jednostkowa' not in columns:
                needs_migration = True
                print("! Stara nazwa kolumny 'cena' zamiast 'cena_jednostkowa'")

            if needs_migration:
                print("... Usuwanie starych tabel trader_manager...")
                db.session.execute(text('DROP TABLE IF EXISTS trader_item'))
                db.session.execute(text('DROP TABLE IF EXISTS trader_manager'))
                db.session.commit()
                print("OK Stare tabele usunięte")
    except Exception as e:
        print(f"Error Błąd podczas sprawdzania migracji: {e}")
        db.session.rollback()

    # Teraz utwórz wszystkie tabele (w tym trader_manager z poprawną strukturą)
    db.create_all()
    print("OK Wszystkie tabele utworzone")


# ===== REJESTRACJA I LOGOWANIE =====

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        is_valid, error_message = validate_password(password, password2)
        if not is_valid:
            flash(error_message)
            return render_template('register.html', username=username, error_field='password')

        if User.query.filter_by(username=username).first():
            flash('Nazwa użytkownika już istnieje!')
            return render_template('register.html', username=username, error_field='username')

        # Create user without email verification
        user = User(username=username, email=f"{username}@placeholder.local", is_verified=True)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Rejestracja udana! Możesz się teraz zalogować.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    email = request.args.get('email')
    
    if request.method == "POST":
        code = request.form.get('code')
        # Jeśli email nie przyszedł w query params, może użytkownik wpisał go ręcznie?
        # W tej prostej wersji zakładamy że mamy email z sesji lub query, 
        # ale tutaj prostujemy: szukamy usera po kodzie (mało bezpieczne globalnie, ale ok lokalnie) 
        # LUB wymagamy podania maila.
        # Ulepszenie: przekaż email w ukrytym polu formularza.
        
        # Szukamy użytkownika z tym kodem (i ewentualnie mailem jeśli jest)
        if email:
            user = User.query.filter_by(email=email, verification_code=code).first()
        else:
            # Fallback: szukaj po kodzie (ryzyko kolizji, ale małe przy 6 cyfrach i małej bazie)
            user = User.query.filter_by(verification_code=code).first()

        if user:
            user.is_verified = True
            user.verification_code = None # Wyczyść kod
            db.session.commit()
            flash('Konto zweryfikowane pomyślnie! Zaloguj się.')
            return redirect(url_for('login'))
        else:
            flash('Nieprawidłowy kod weryfikacyjny!')
            
    return render_template('verify_email.html', email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.is_verified:
                flash('Konto nie jest zweryfikowane. Sprawdź email.')
                return redirect(url_for('verify_email', email=user.email))
                
            login_user(user, remember=True)
            flash(f'Witaj {user.username}!')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Nieprawidłowe dane logowania!')

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany.')
    return redirect(url_for('index'))


# ===== STRONY GŁÓWNE =====

@app.route("/")
def index():
    return render_template("glowna.html")


@app.route("/roller", methods=["GET", "POST"])
def roller():
    return render_template('roller.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    dice_type = data.get('dice_type')
    dice_number = data.get('dice_number')
    calculated_result = calculate_dice_roll(dice_type, dice_number)

    return jsonify({
        'calculated_value': calculated_result,
        'status': 'success'
    })


@app.route("/roller-embedded")
def roller_embedded():
    return render_template('roller_embedded.html')


@app.route("/roller-embedded-cthulhu")
def roller_embedded_cthulhu():
    return render_template('roller_embedded_cthulhu.html')


@app.route("/karty-postaci")
@login_required
def karty_postaci():
    warhammer_cards = CharacterWarhammer.query.filter_by(user_id=current_user.id).all()
    dnd5e_cards = CharacterDnD5e.query.filter_by(user_id=current_user.id).all()
    cthulhu_cards = CharacterCthulhu.query.filter_by(user_id=current_user.id).all()

    return render_template('karty_postaci.html',
                           warhammer_cards=warhammer_cards,
                           dnd5e_cards=dnd5e_cards,
                           cthulhu_cards=cthulhu_cards)


@app.route("/wybierz-system")
@login_required
def wybierz_system():
    return render_template('wybierz_system.html')


# ===== WARHAMMER =====

@app.route("/nowa-karta-warhammer", methods=["GET", "POST"])
@login_required
def nowa_karta_warhammer():
    if request.method == "POST":
        character = CharacterWarhammer(
            # Podstawowe informacje
            imie=request.form.get('imie', ''),
            gracz=request.form.get('gracz', ''),
            profesja=request.form.get('profesja', ''),
            wiek=request.form.get('wiek', ''),
            plec=request.form.get('plec', ''),
            miejsce=request.form.get('miejsce', ''),
            # Dodatkowe pola
            rasa=request.form.get('rasa', ''),
            poprzednie_profesje=request.form.get('poprzednie_profesje', ''),
            oczy=request.form.get('oczy', ''),
            waga=request.form.get('waga', ''),
            wlosy=request.form.get('wlosy', ''),
            wzrost=request.form.get('wzrost', ''),
            znak_gwiezdny=request.form.get('znak_gwiezdny', ''),
            rodzienstwo=request.form.get('rodzienstwo', ''),
            znaki_szczegolne=request.form.get('znaki_szczegolne', ''),
            # Statystyki Warhammer
            ww=int(request.form.get('ww', 0) or 0),
            us=int(request.form.get('us', 0) or 0),
            k=int(request.form.get('k', 0) or 0),
            odp=int(request.form.get('odp', 0) or 0),
            zr=int(request.form.get('zr', 0) or 0),
            intel=int(request.form.get('int', 0) or 0),
            sw=int(request.form.get('sw', 0) or 0),
            ogd=int(request.form.get('ogd', 0) or 0),
            a=int(request.form.get('a', 0) or 0),
            zyw=int(request.form.get('zyw', 0) or 0),
            s=int(request.form.get('s', 0) or 0),
            wt=int(request.form.get('wt', 0) or 0),
            sz=int(request.form.get('sz', 0) or 0),
            mag=int(request.form.get('mag', 0) or 0),
            po=int(request.form.get('po', 0) or 0),
            pp=int(request.form.get('pp', 0) or 0),
            # Doświadczenie
            doswiadczenie_wolne=int(request.form.get('doswiadczenie_wolne', 0) or 0),
            doswiadczenie_wydane=int(request.form.get('doswiadczenie_wydane', 0) or 0),
            # Ruch
            ruch=int(request.form.get('ruch', 0) or 0),
            szarza=int(request.form.get('szarza', 0) or 0),
            bieg=int(request.form.get('bieg', 0) or 0),
            user_id=current_user.id
        )

        db.session.add(character)
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Karta Warhammer została zapisana!', 'redirect': url_for('karty_postaci')})

        flash('✅ Karta Warhammer została zapisana!')
        return redirect(url_for('karty_postaci'))

    return render_template('nowa_karta_warhammer.html')


@app.route("/edytuj-karte-warhammer/<int:character_id>", methods=["GET", "POST"])
@login_required
def edytuj_karte_warhammer(character_id):
    character = CharacterWarhammer.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        # Podstawowe informacje
        character.imie = request.form.get('imie', '')
        character.gracz = request.form.get('gracz', '')
        character.profesja = request.form.get('profesja', '')
        character.wiek = request.form.get('wiek', '')
        character.plec = request.form.get('plec', '')
        character.miejsce = request.form.get('miejsce', '')
        # Dodatkowe pola
        character.rasa = request.form.get('rasa', '')
        character.poprzednie_profesje = request.form.get('poprzednie_profesje', '')
        character.oczy = request.form.get('oczy', '')
        character.waga = request.form.get('waga', '')
        character.wlosy = request.form.get('wlosy', '')
        character.wzrost = request.form.get('wzrost', '')
        character.znak_gwiezdny = request.form.get('znak_gwiezdny', '')
        character.rodzienstwo = request.form.get('rodzienstwo', '')
        character.znaki_szczegolne = request.form.get('znaki_szczegolne', '')
        # Statystyki Warhammer
        character.ww = int(request.form.get('ww', 0) or 0)
        character.us = int(request.form.get('us', 0) or 0)
        character.k = int(request.form.get('k', 0) or 0)
        character.odp = int(request.form.get('odp', 0) or 0)
        character.zr = int(request.form.get('zr', 0) or 0)
        character.intel = int(request.form.get('int', 0) or 0)
        character.sw = int(request.form.get('sw', 0) or 0)
        character.ogd = int(request.form.get('ogd', 0) or 0)
        character.a = int(request.form.get('a', 0) or 0)
        character.zyw = int(request.form.get('zyw', 0) or 0)
        character.s = int(request.form.get('s', 0) or 0)
        character.wt = int(request.form.get('wt', 0) or 0)
        character.sz = int(request.form.get('sz', 0) or 0)
        character.mag = int(request.form.get('mag', 0) or 0)
        character.po = int(request.form.get('po', 0) or 0)
        character.pp = int(request.form.get('pp', 0) or 0)
        # Doświadczenie
        character.doswiadczenie_wolne = int(request.form.get('doswiadczenie_wolne', 0) or 0)
        character.doswiadczenie_wydane = int(request.form.get('doswiadczenie_wydane', 0) or 0)
        # Ruch
        character.ruch = int(request.form.get('ruch', 0) or 0)
        character.szarza = int(request.form.get('szarza', 0) or 0)
        character.bieg = int(request.form.get('bieg', 0) or 0)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Karta Warhammer została zaktualizowana!'})

        flash('✅ Karta Warhammer została zaktualizowana!')
        return redirect(url_for('karty_postaci'))

    return render_template('edytuj_karte_warhammer.html', character=character)


@app.route("/bron-warhammer/<int:character_id>", methods=["GET", "POST"])
@login_required
def bron_warhammer(character_id):
    character = CharacterWarhammer.query.get_or_404(character_id)
    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        # Usuń starą broń i pancerze
        WarhammerBron.query.filter_by(character_id=character_id).delete()
        WarhammerArmor.query.filter_by(character_id=character_id).delete()

        # Broń - 8 wierszy z HTML (1-8)
        for i in range(1, 9):
            nazwa = request.form.get(f'weapon_name_{i}', '').strip()
            if nazwa:
                item = WarhammerBron(
                    character_id=character_id,
                    bron_index=i - 1,
                    nazwa_broni=nazwa,
                    obciazenie=request.form.get(f'weapon_obc_{i}', '').strip(),
                    typ=request.form.get(f'weapon_category_{i}', '').strip(),
                    sila=request.form.get(f'weapon_sila_{i}', '').strip(),
                    szkody=request.form.get(f'weapon_broni_{i}', '').strip(),
                    zasieg=request.form.get(f'weapon_zasieg_{i}', '').strip(),
                    przeladowanie=request.form.get(f'weapon_przeload_{i}', '').strip(),
                    cechy=request.form.get(f'weapon_cechy_{i}', '').strip()
                )
                db.session.add(item)

        # Pancerze - 8 wierszy z HTML (1-8)
        for i in range(1, 9):
            typ_pancerza = request.form.get(f'armor_type_{i}', '').strip()
            if typ_pancerza:
                armor = WarhammerArmor(
                    character_id=character_id,
                    armor_index=i - 1,
                    armor_type=typ_pancerza,
                    armor_location=request.form.get(f'armor_location_{i}', '').strip(),
                    armor_pz=request.form.get(f'armor_pz_{i}', '').strip()
                )
                db.session.add(armor)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Broń i pancerze zostały zapisane!'})

        flash('✅ Broń i pancerze zostały zapisane!')
        return redirect(url_for('bron_warhammer', character_id=character_id))

    bron = WarhammerBron.query.filter_by(character_id=character_id).all()
    armor = WarhammerArmor.query.filter_by(character_id=character_id).all()
    return render_template('bron_warhammer.html', character=character, bron=bron, armor=armor)


@app.route("/umiejetnosci-warhammer/<int:character_id>", methods=["GET", "POST"])
@login_required
def umiejetnosci_warhammer(character_id):
    character = CharacterWarhammer.query.get_or_404(character_id)
    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        WarhammerUmiejetnosc.query.filter_by(character_id=character_id).delete()

        # Umiejętności podstawowe
        basic_skills = [
            'charakteryzacja', 'dowodzenie', 'hazard', 'jedzdzictwo', 'mocnaglowa',
            'opieka', 'plotkowanie', 'plywanie', 'powozenie', 'przekonywanie',
            'przeszukiwanie', 'skradanie', 'spostrzegawczosc', 'sztuka', 'targowanie',
            'ukrywanie', 'wioslarstwo', 'wspinaczka', 'wycena', 'zastraszanie'
        ]

        skill_index = 0
        for skill_name in basic_skills:
            # Sprawdź czy którakolwiek checkbox jest zaznaczona
            buy = request.form.get(f'basic_{skill_name}_buy')
            plus10 = request.form.get(f'basic_{skill_name}_10')
            plus20 = request.form.get(f'basic_{skill_name}_20')
            related = request.form.get(f'basic_{skill_name}_related', '').strip()

            if buy or plus10 or plus20 or related:
                item = WarhammerUmiejetnosc(
                    character_id=character_id,
                    umiejetnosc_index=skill_index,
                    nazwa_umiejetnosci=skill_name,
                    typ='Podstawowa',
                    poziom='Bought' if buy else '',
                    koszt='+10' if plus10 else '+20' if plus20 else '',
                    wymogi=related,
                    opis=''
                )
                db.session.add(item)
            skill_index += 1

        # Umiejętności zaawansowane (20)
        for i in range(20):
            nazwa = request.form.get(f'advanced_name_{i}', '').strip()
            if nazwa:
                item = WarhammerUmiejetnosc(
                    character_id=character_id,
                    umiejetnosc_index=100 + i,  # Zmieniono na 100+ żeby nie kolidować z basic
                    nazwa_umiejetnosci=nazwa,
                    typ='Zaawansowana',
                    poziom='Bought' if request.form.get(f'advanced_{i}_buy') else '',
                    koszt='+10' if request.form.get(f'advanced_{i}_10') else '+20' if request.form.get(
                        f'advanced_{i}_20') else '',
                    wymogi=request.form.get(f'advanced_{i}_related', '').strip(),
                    opis=''
                )
                db.session.add(item)

        # Zdolności (10)
        for i in range(10):
            nazwa = request.form.get(f'ability_name_{i}', '').strip()
            opis = request.form.get(f'ability_desc_{i}', '').strip()
            if nazwa or opis:
                item = WarhammerUmiejetnosc(
                    character_id=character_id,
                    umiejetnosc_index=200 + i,  # Zmieniono na 200+ dla zdolności
                    nazwa_umiejetnosci=nazwa,
                    typ='Zdolnosc',
                    poziom='',
                    koszt='',
                    wymogi='',
                    opis=opis
                )
                db.session.add(item)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Umiejętności zostały zapisane!'})

        flash('✅ Umiejętności zostały zapisane!')
        return redirect(url_for('umiejetnosci_warhammer', character_id=character_id))

    umiejetnosci = WarhammerUmiejetnosc.query.filter_by(character_id=character_id).all()
    return render_template('umiejetnosci_warhammer.html', character=character, umiejetnosci=umiejetnosci)


@app.route("/ekwipunek-warhammer/<int:character_id>", methods=["GET", "POST"])
@login_required
def ekwipunek_warhammer(character_id):
    character = CharacterWarhammer.query.get_or_404(character_id)
    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        WarhammerEkwipunek.query.filter_by(character_id=character_id).delete()

        # Pieniądze
        charakter_obj = CharacterWarhammer.query.get(character_id)
        charakter_obj.zlote_korony = int(request.form.get('zlote_korony', 0) or 0)
        charakter_obj.srebrne_szyllingi = int(request.form.get('srebrne_szyllingi', 0) or 0)
        charakter_obj.miedziany_pensy = int(request.form.get('miedziany_pensy', 0) or 0)

        # Przedmioty - 40 wierszy
        for i in range(40):
            nazwa = request.form.get(f'item_name_{i}', '').strip()
            if nazwa:
                item = WarhammerEkwipunek(
                    character_id=character_id,
                    przedmiot_index=i,
                    nazwa_przedmiotu=nazwa,
                    obciazenie=request.form.get(f'item_ocb_{i}', '').strip(),
                    wartosc=request.form.get(f'item_value_{i}', '').strip(),
                    jednostka='',
                    opis=request.form.get(f'item_desc_{i}', '').strip()
                )
                db.session.add(item)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Ekwipunek został zapisany!'})

        flash('✅ Ekwipunek został zapisany!')
        return redirect(url_for('ekwipunek_warhammer', character_id=character_id))

    ekwipunek = WarhammerEkwipunek.query.filter_by(character_id=character_id).all()
    return render_template('ekwipunek_warhammer.html', character=character, ekwipunek=ekwipunek)


@app.route("/usun-karte-warhammer/<int:character_id>", methods=["POST"])
@login_required
def usun_karte_warhammer(character_id):
    character = CharacterWarhammer.query.get_or_404(character_id)

    if character.user_id == current_user.id:
        db.session.delete(character)
        db.session.commit()
        flash('✅ Karta Warhammer została usunięta!')
    else:
        flash('❌ Nie masz dostępu do tej karty!')

    return redirect(url_for('karty_postaci'))


# ===== D&D 5e =====

@app.route("/nowa-karta-dnd5e", methods=["GET", "POST"])
@login_required
def nowa_karta_dnd5e():
    if request.method == "POST":
        imie = request.form.get('imie', '')
        gracz = request.form.get('gracz', '')
        klasa = request.form.get('klasa', '')
        pochodzenie = request.form.get('pochodzenie', '')
        rasa = request.form.get('rasa', '')
        charakter = request.form.get('charakter', '')
        poziom = int(request.form.get('poziom', 1) or 1)
        doswiadczenie = int(request.form.get('doswiadczenie', 0) or 0)
        wiek = request.form.get('wiek', '')
        wzrost = request.form.get('wzrost', '')
        waga = request.form.get('waga', '')
        oczy = request.form.get('oczy', '')
        skora = request.form.get('skora', '')
        wlosy = request.form.get('wlosy', '')

        # Atrybuty i modyfikatory
        sila = int(request.form.get('sila', 10) or 10)
        sila_mod = int(request.form.get('sila_mod', 0) or 0)
        zrecznosc = int(request.form.get('zrecznosc', 10) or 10)
        zrecznosc_mod = int(request.form.get('zrecznosc_mod', 0) or 0)
        kondycja = int(request.form.get('kondycja', 10) or 10)
        kondycja_mod = int(request.form.get('kondycja_mod', 0) or 0)
        inteligencja = int(request.form.get('inteligencja', 10) or 10)
        inteligencja_mod = int(request.form.get('inteligencja_mod', 0) or 0)
        madrosc = int(request.form.get('madrosc', 10) or 10)
        madrosc_mod = int(request.form.get('madrosc_mod', 0) or 0)
        charyzma = int(request.form.get('charyzma', 10) or 10)
        charyzma_mod = int(request.form.get('charyzma_mod', 0) or 0)

        # Rzuty obronne
        save_sila = 'save_sila' in request.form
        save_sila_val = int(request.form.get('save_sila_val', 0) or 0)
        save_zrecznosc = 'save_zrecznosc' in request.form
        save_zrecznosc_val = int(request.form.get('save_zrecznosc_val', 0) or 0)
        save_kondycja = 'save_kondycja' in request.form
        save_kondycja_val = int(request.form.get('save_kondycja_val', 0) or 0)
        save_inteligencja = 'save_inteligencja' in request.form
        save_inteligencja_val = int(request.form.get('save_inteligencja_val', 0) or 0)
        save_madrosc = 'save_madrosc' in request.form
        save_madrosc_val = int(request.form.get('save_madrosc_val', 0) or 0)
        save_charyzma = 'save_charyzma' in request.form
        save_charyzma_val = int(request.form.get('save_charyzma_val', 0) or 0)

        klasa_pancerza = int(request.form.get('klasa_pancerza', 10) or 10)
        inicjatywa = int(request.form.get('inicjatywa', 0) or 0)
        szybkosc = int(request.form.get('szybkosc', 30) or 30)
        punkty_zycia = int(request.form.get('punkty_zycia', 0) or 0)
        aktualne_pw = int(request.form.get('aktualne_pw', 0) or 0)
        czasowe_pw = int(request.form.get('czasowe_pw', 0) or 0)
        inspiracja = request.form.get('inspiracja', '')
        premia_bieglości = int(request.form.get('premia_bieglości', 2) or 2)
        pasywna_madrosc = int(request.form.get('pasywna_madrosc', 10) or 10)

        kosci_wytrzymalosci = int(request.form.get('kosci_wytrzymalosci', 0) or 0)

        death_success_1 = 'death_success_1' in request.form
        death_success_2 = 'death_success_2' in request.form
        death_success_3 = 'death_success_3' in request.form

        death_failure_1 = 'death_failure_1' in request.form
        death_failure_2 = 'death_failure_2' in request.form
        death_failure_3 = 'death_failure_3' in request.form

        character = CharacterDnD5e(
            imie=imie,
            gracz=gracz,
            klasa=klasa,
            pochodzenie=pochodzenie,
            rasa=rasa,
            charakter=charakter,
            poziom=poziom,
            doswiadczenie=doswiadczenie,
            wiek=wiek,
            wzrost=wzrost,
            waga=waga,
            oczy=oczy,
            skora=skora,
            wlosy=wlosy,
            sila=sila,
            sila_mod=sila_mod,
            zrecznosc=zrecznosc,
            zrecznosc_mod=zrecznosc_mod,
            kondycja=kondycja,
            kondycja_mod=kondycja_mod,
            inteligencja=inteligencja,
            inteligencja_mod=inteligencja_mod,
            madrosc=madrosc,
            madrosc_mod=madrosc_mod,
            charyzma=charyzma,
            charyzma_mod=charyzma_mod,
            save_sila=save_sila,
            save_sila_val=save_sila_val,
            save_zrecznosc=save_zrecznosc,
            save_zrecznosc_val=save_zrecznosc_val,
            save_kondycja=save_kondycja,
            save_kondycja_val=save_kondycja_val,
            save_inteligencja=save_inteligencja,
            save_inteligencja_val=save_inteligencja_val,
            save_madrosc=save_madrosc,
            save_madrosc_val=save_madrosc_val,
            save_charyzma=save_charyzma,
            save_charyzma_val=save_charyzma_val,
            klasa_pancerza=klasa_pancerza,
            inicjatywa=inicjatywa,
            szybkosc=szybkosc,
            punkty_zycia=punkty_zycia,
            aktualne_pw=aktualne_pw,
            czasowe_pw=czasowe_pw,
            inspiracja=inspiracja,
            premia_bieglości=premia_bieglości,
            pasywna_madrosc=pasywna_madrosc,
            kosci_wytrzymalosci=kosci_wytrzymalosci,
            death_success_1=death_success_1,
            death_success_2=death_success_2,
            death_success_3=death_success_3,
            death_failure_1=death_failure_1,
            death_failure_2=death_failure_2,
            death_failure_3=death_failure_3,
            user_id=current_user.id
        )

        db.session.add(character)
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Karta D&D 5e została zapisana!', 'redirect': url_for('karty_postaci')})

        flash('✅ Karta D&D 5e została zapisana!')
        return redirect(url_for('karty_postaci'))

    return render_template('nowa_karta_dnd5e.html')


@app.route("/edytuj-karte-dnd5e/<int:character_id>", methods=["GET", "POST"])
@login_required
def edytuj_karte_dnd5e(character_id):
    character = CharacterDnD5e.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        character.imie = request.form.get('imie', '')
        character.gracz = request.form.get('gracz', '')
        character.klasa = request.form.get('klasa', '')
        character.pochodzenie = request.form.get('pochodzenie', '')
        character.rasa = request.form.get('rasa', '')
        character.charakter = request.form.get('charakter', '')
        character.poziom = int(request.form.get('poziom', 1) or 1)
        character.doswiadczenie = int(request.form.get('doswiadczenie', 0) or 0)
        character.wiek = request.form.get('wiek', '')
        character.wzrost = request.form.get('wzrost', '')
        character.waga = request.form.get('waga', '')
        character.oczy = request.form.get('oczy', '')
        character.skora = request.form.get('skora', '')
        character.wlosy = request.form.get('wlosy', '')

        # Atrybuty i modyfikatory
        character.sila = int(request.form.get('sila', 10) or 10)
        character.sila_mod = int(request.form.get('sila_mod', 0) or 0)
        character.zrecznosc = int(request.form.get('zrecznosc', 10) or 10)
        character.zrecznosc_mod = int(request.form.get('zrecznosc_mod', 0) or 0)
        character.kondycja = int(request.form.get('kondycja', 10) or 10)
        character.kondycja_mod = int(request.form.get('kondycja_mod', 0) or 0)
        character.inteligencja = int(request.form.get('inteligencja', 10) or 10)
        character.inteligencja_mod = int(request.form.get('inteligencja_mod', 0) or 0)
        character.madrosc = int(request.form.get('madrosc', 10) or 10)
        character.madrosc_mod = int(request.form.get('madrosc_mod', 0) or 0)
        character.charyzma = int(request.form.get('charyzma', 10) or 10)
        character.charyzma_mod = int(request.form.get('charyzma_mod', 0) or 0)

        # Rzuty obronne
        character.save_sila = 'save_sila' in request.form
        character.save_sila_val = int(request.form.get('save_sila_val', 0) or 0)
        character.save_zrecznosc = 'save_zrecznosc' in request.form
        character.save_zrecznosc_val = int(request.form.get('save_zrecznosc_val', 0) or 0)
        character.save_kondycja = 'save_kondycja' in request.form
        character.save_kondycja_val = int(request.form.get('save_kondycja_val', 0) or 0)
        character.save_inteligencja = 'save_inteligencja' in request.form
        character.save_inteligencja_val = int(request.form.get('save_inteligencja_val', 0) or 0)
        character.save_madrosc = 'save_madrosc' in request.form
        character.save_madrosc_val = int(request.form.get('save_madrosc_val', 0) or 0)
        character.save_charyzma = 'save_charyzma' in request.form
        character.save_charyzma_val = int(request.form.get('save_charyzma_val', 0) or 0)

        character.klasa_pancerza = int(request.form.get('klasa_pancerza', 10) or 10)
        character.inicjatywa = int(request.form.get('inicjatywa', 0) or 0)
        character.szybkosc = int(request.form.get('szybkosc', 30) or 30)
        character.punkty_zycia = int(request.form.get('punkty_zycia', 0) or 0)
        character.aktualne_pw = int(request.form.get('aktualne_pw', 0) or 0)
        character.czasowe_pw = int(request.form.get('czasowe_pw', 0) or 0)
        character.inspiracja = request.form.get('inspiracja', '')
        character.premia_bieglości = int(request.form.get('premia_bieglości', 2) or 2)
        character.pasywna_madrosc = int(request.form.get('pasywna_madrosc', 10) or 10)

        character.kosci_wytrzymalosci = int(request.form.get('kosci_wytrzymalosci', 0) or 0)

        character.death_success_1 = 'death_success_1' in request.form
        character.death_success_2 = 'death_success_2' in request.form
        character.death_success_3 = 'death_success_3' in request.form

        character.death_failure_1 = 'death_failure_1' in request.form
        character.death_failure_2 = 'death_failure_2' in request.form
        character.death_failure_3 = 'death_failure_3' in request.form

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Karta D&D 5e została zaktualizowana!'})

        flash('✅ Karta D&D 5e została zaktualizowana!')
        return redirect(url_for('karty_postaci'))

    return render_template('edytuj_karte_dnd5e.html', character=character)


@app.route("/bieglosci-dnd5e/<int:character_id>", methods=["GET", "POST"])
@login_required
def bieglosci_dnd5e(character_id):
    character = CharacterDnD5e.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    bieglosci = DnD5eBieglosc.query.filter_by(character_id=character_id).first()
    if not bieglosci:
        bieglosci = DnD5eBieglosc(character_id=character_id)
        db.session.add(bieglosci)
        db.session.commit()

    if request.method == "POST":
        for i in range(20):
            setattr(bieglosci, f'bieglosc_{i + 1}_nazwa', request.form.get(f'bieglosc_nazwa_{i}', ''))
            setattr(bieglosci, f'bieglosc_{i + 1}_opis', request.form.get(f'bieglosc_opis_{i}', ''))

        for i in range(8):
            setattr(bieglosci, f'jezyk_{i + 1}_nazwa', request.form.get(f'jezyk_nazwa_{i}', ''))
            setattr(bieglosci, f'jezyk_{i + 1}_opis', request.form.get(f'jezyk_opis_{i}', ''))

        for i in range(26):
            setattr(bieglosci, f'zdolnosc_{i + 1}_nazwa', request.form.get(f'zdolnosc_nazwa_{i}', ''))
            setattr(bieglosci, f'zdolnosc_{i + 1}_opis', request.form.get(f'zdolnosc_opis_{i}', ''))

        for i in range(10):
            setattr(bieglosci, f'korzysci_{i + 1}_nazwa', request.form.get(f'korzysci_nazwa_{i}', ''))
            setattr(bieglosci, f'korzysci_{i + 1}_opis', request.form.get(f'korzysci_opis_{i}', ''))

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Biegłości zostały zapisane!'})

        flash('✅ Biegłości zostały zapisane!')
        return redirect(url_for('bieglosci_dnd5e', character_id=character_id))

    return render_template('bieglosci_dnd5e.html', character=character, bieglosci=bieglosci)


@app.route("/magia-dnd5e/<int:character_id>", methods=["GET", "POST"])
@login_required
def magia_dnd5e(character_id):
    character = CharacterDnD5e.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    magia = DnD5eMagia.query.filter_by(character_id=character_id).first()
    if not magia:
        magia = DnD5eMagia(character_id=character_id)
        db.session.add(magia)
        db.session.commit()

    if request.method == "POST":
        magia.magic_cecha = request.form.get('magic_cecha', '')
        magia.magic_st = request.form.get('magic_st', '')
        magia.magic_bonus = request.form.get('magic_bonus', '')

        for i in range(10):
            setattr(magia, f'cells_available_{i}', request.form.get(f'cells_available_{i}', ''))
            setattr(magia, f'cells_used_{i}', request.form.get(f'cells_used_{i}', ''))

        DnD5eSpell.query.filter_by(character_id=character_id).delete()

        for level in range(10):
            for index in range(12):
                nazwa = request.form.get(f'spell_{level}_{index}_name', '').strip()
                if nazwa:
                    spell = DnD5eSpell(
                        character_id=character_id,
                        spell_level=level,
                        spell_index=index,
                        nazwa_czaru=nazwa,
                        zasieg=request.form.get(f'spell_{level}_{index}_range', ''),
                        opis=request.form.get(f'spell_{level}_{index}_desc', '')
                    )
                    db.session.add(spell)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Magia została zapisana!'})

        flash('✅ Magia została zapisana!')
        return redirect(url_for('magia_dnd5e', character_id=character_id))

    spells_by_level = {}
    for level in range(10):
        spells_by_level[level] = DnD5eSpell.query.filter_by(
            character_id=character_id,
            spell_level=level
        ).order_by(DnD5eSpell.spell_index).all()

    return render_template('magia_dnd5e.html',
                           character=character,
                           magia=magia,
                           spells_by_level=spells_by_level)


@app.route("/ekwipunek-dnd5e/<int:character_id>", methods=["GET", "POST"])
@login_required
def ekwipunek_dnd5e(character_id):
    character = CharacterDnD5e.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        DnD5eEkwipunek.query.filter_by(character_id=character_id).delete()

        for i in range(30):
            nazwa = request.form.get(f'equipment_name_{i}', '').strip()
            if nazwa:
                item = DnD5eEkwipunek(
                    character_id=character_id,
                    przedmiot_index=i,
                    nazwa_przedmiotu=nazwa,
                    obciazenie=request.form.get(f'equipment_weight_{i}', ''),
                    wartosc=request.form.get(f'equipment_value_{i}', ''),
                    jednostka=request.form.get(f'equipment_unit_{i}', ''),
                    opis=request.form.get(f'equipment_desc_{i}', '')
                )
                db.session.add(item)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Ekwipunek został zapisany!'})

        flash('✅ Ekwipunek został zapisany!')
        return redirect(url_for('ekwipunek_dnd5e', character_id=character_id))

    ekwipunek = DnD5eEkwipunek.query.filter_by(character_id=character_id).all()

    return render_template('ekwipunek_dnd5e.html',
                           character=character,
                           ekwipunek=ekwipunek)


@app.route("/usun-karte-dnd5e/<int:character_id>", methods=["POST"])
@login_required
def usun_karte_dnd5e(character_id):
    character = CharacterDnD5e.query.get_or_404(character_id)

    if character.user_id == current_user.id:
        db.session.delete(character)
        db.session.commit()
        flash('✅ Karta D&D 5e została usunięta!')
    else:
        flash('❌ Nie masz dostępu do tej karty!')

    return redirect(url_for('karty_postaci'))


# ===== CTHULHU =====

@app.route("/nowa-karta-cthulhu", methods=["GET", "POST"])
@login_required
def nowa_karta_cthulhu():
    if request.method == "POST":
        imie = request.form.get('imie', '')
        gracz = request.form.get('gracz', '')
        profesja = request.form.get('profesja', '')
        wiek = request.form.get('wiek', '')
        plec = request.form.get('plec', '')
        miejsce = request.form.get('miejsce', '')
        s = int(request.form.get('s', 0) or 0)
        zr = int(request.form.get('zr', 0) or 0)
        moc = int(request.form.get('moc', 0) or 0)
        pw1 = int(request.form.get('pw1', 0) or 0)
        pw2 = int(request.form.get('pw2', 0) or 0)
        kon = int(request.form.get('kon', 0) or 0)
        wyg = int(request.form.get('wyg', 0) or 0)
        wyk = int(request.form.get('wyk', 0) or 0)
        szczescie = int(request.form.get('szczescie', 0) or 0)
        bc = int(request.form.get('bc', 0) or 0)
        intel = int(request.form.get('intel', 0) or 0)
        ruch = int(request.form.get('ruch', 0) or 0)
        poczytalnosc = int(request.form.get('poczytalnosc', 0) or 0)

        character = CharacterCthulhu(
            imie=imie,
            gracz=gracz,
            profesja=profesja,
            wiek=wiek,
            plec=plec,
            miejsce=miejsce,
            s=s,
            zr=zr,
            moc=moc,
            pw1=pw1,
            pw2=pw2,
            kon=kon,
            wyg=wyg,
            wyk=wyk,
            szczescie=szczescie,
            bc=bc,
            intel=intel,
            ruch=ruch,
            poczytalnosc=poczytalnosc,
            user_id=current_user.id
        )

        db.session.add(character)
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Karta Cthulhu została zapisana!', 'redirect': url_for('karty_postaci')})

        flash('✅ Karta Cthulhu została zapisana!')
        return redirect(url_for('karty_postaci'))

    return render_template('nowa_karta_cthulhu.html')


@app.route("/edytuj-karte-cthulhu/<int:character_id>", methods=["GET", "POST"])
@login_required
def edytuj_karte_cthulhu(character_id):
    character = CharacterCthulhu.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        character.imie = request.form.get('imie', '')
        character.gracz = request.form.get('gracz', '')
        character.profesja = request.form.get('profesja', '')
        character.wiek = request.form.get('wiek', '')
        character.plec = request.form.get('plec', '')
        character.miejsce = request.form.get('miejsce', '')
        character.s = int(request.form.get('s', 0) or 0)
        character.zr = int(request.form.get('zr', 0) or 0)
        character.moc = int(request.form.get('moc', 0) or 0)
        character.pw1 = int(request.form.get('pw1', 0) or 0)
        character.pw2 = int(request.form.get('pw2', 0) or 0)
        character.kon = int(request.form.get('kon', 0) or 0)
        character.wyg = int(request.form.get('wyg', 0) or 0)
        character.wyk = int(request.form.get('wyk', 0) or 0)
        character.szczescie = int(request.form.get('szczescie', 0) or 0)
        character.bc = int(request.form.get('bc', 0) or 0)
        character.intel = int(request.form.get('intel', 0) or 0)
        character.ruch = int(request.form.get('ruch', 0) or 0)
        character.poczytalnosc = int(request.form.get('poczytalnosc', 0) or 0)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Karta Cthulhu została zaktualizowana!'})

        flash('✅ Karta Cthulhu została zaktualizowana!')
        return redirect(url_for('karty_postaci'))

    return render_template('edytuj_karte_cthulhu.html', character=character)


@app.route("/umiejetnosci-cthulhu/<int:character_id>", methods=["GET", "POST"])
@login_required
def umiejetnosci_cthulhu(character_id):
    character = CharacterCthulhu.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    skills = CthulhuSkill.query.filter_by(character_id=character_id).first()
    if not skills:
        skills = CthulhuSkill(character_id=character_id)
        db.session.add(skills)
        db.session.commit()

    if request.method == "POST":
        skills.antropologia = int(request.form.get('antropologia', 1) or 1)
        skills.archeologia = int(request.form.get('archeologia', 1) or 1)
        skills.bron_karabin_custom = request.form.get('bron_karabin_custom', '')
        skills.bron_karabin = int(request.form.get('bron_karabin', 25) or 25)
        skills.bron_krotka = int(request.form.get('bron_krotka', 20) or 20)
        skills.charakteryzacja = int(request.form.get('charakteryzacja', 5) or 5)
        skills.elektryka = int(request.form.get('elektryka', 10) or 10)
        skills.gadanina = int(request.form.get('gadanina', 5) or 5)
        skills.historia = int(request.form.get('historia', 5) or 5)
        skills.jezdziectwo = int(request.form.get('jezdziectwo', 5) or 5)
        skills.jezyk_obcy_1 = request.form.get('jezyk_obcy_1', '')
        skills.jezyk_obcy_1_val = int(request.form.get('jezyk_obcy_1_val', 1) or 1)
        skills.jezyk_obcy_2 = request.form.get('jezyk_obcy_2', '')
        skills.jezyk_obcy_2_val = int(request.form.get('jezyk_obcy_2_val', 1) or 1)
        skills.jezyk_obcy_3 = request.form.get('jezyk_obcy_3', '')
        skills.jezyk_obcy_3_val = int(request.form.get('jezyk_obcy_3_val', 1) or 1)
        skills.jezyk_ojczysty = request.form.get('jezyk_ojczysty', '')
        skills.jezyk_ojczysty_val = int(request.form.get('jezyk_ojczysty_val', 0) or 0)
        skills.biblioteki = int(request.form.get('biblioteki', 20) or 20)
        skills.ksiegowosc = int(request.form.get('ksiegowosc', 5) or 5)
        skills.majetnosc = int(request.form.get('majetnosc', 0) or 0)
        skills.mechanika = int(request.form.get('mechanika', 10) or 10)
        skills.medycyna = int(request.form.get('medycyna', 1) or 1)
        skills.mity_cthulhu = int(request.form.get('mity_cthulhu', 0) or 0)
        skills.nasluchiwanie = int(request.form.get('nasluchiwanie', 20) or 20)
        skills.nauka_1 = request.form.get('nauka_1', '')
        skills.nauka_1_val = int(request.form.get('nauka_1_val', 1) or 1)
        skills.nauka_2 = request.form.get('nauka_2', '')
        skills.nauka_2_val = int(request.form.get('nauka_2_val', 1) or 1)
        skills.nauka_3 = request.form.get('nauka_3', '')
        skills.nauka_3_val = int(request.form.get('nauka_3_val', 1) or 1)
        skills.nawigacja = int(request.form.get('nawigacja', 10) or 10)
        skills.ciezki_sprzet = int(request.form.get('ciezki_sprzet', 1) or 1)
        skills.okultyzm = int(request.form.get('okultyzm', 5) or 5)
        skills.perswazja = int(request.form.get('perswazja', 10) or 10)
        skills.pierwsza_pomoc = int(request.form.get('pierwsza_pomoc', 30) or 30)
        skills.pilotowanie = request.form.get('pilotowanie', '')
        skills.pilotowanie_val = int(request.form.get('pilotowanie_val', 1) or 1)
        skills.plywanie = int(request.form.get('plywanie', 20) or 20)
        skills.prawo = int(request.form.get('prawo', 5) or 5)
        skills.prowadzenie = int(request.form.get('prowadzenie', 20) or 20)
        skills.psychoanaliza = int(request.form.get('psychoanaliza', 1) or 1)
        skills.psychologia = int(request.form.get('psychologia', 10) or 10)
        skills.rzucanie = int(request.form.get('rzucanie', 20) or 20)
        skills.skakanie = int(request.form.get('skakanie', 20) or 20)
        skills.spostrzegawczosc = int(request.form.get('spostrzegawczosc', 25) or 25)
        skills.sztuka_1 = request.form.get('sztuka_1', '')
        skills.sztuka_1_val = int(request.form.get('sztuka_1_val', 5) or 5)
        skills.sztuka_2 = request.form.get('sztuka_2', '')
        skills.sztuka_2_val = int(request.form.get('sztuka_2_val', 5) or 5)
        skills.sztuka_3 = request.form.get('sztuka_3', '')
        skills.sztuka_3_val = int(request.form.get('sztuka_3_val', 5) or 5)
        skills.przetrwanie = request.form.get('przetrwanie', '')
        skills.przetrwanie_val = int(request.form.get('przetrwanie_val', 10) or 10)
        skills.slusarstwo = int(request.form.get('slusarstwo', 1) or 1)
        skills.tropienie = int(request.form.get('tropienie', 10) or 10)
        skills.ukrywanie = int(request.form.get('ukrywanie', 20) or 20)
        skills.unik = int(request.form.get('unik', 0) or 0)
        skills.urok = int(request.form.get('urok', 15) or 15)
        skills.walka_wrecz = int(request.form.get('walka_wrecz', 25) or 25)
        skills.walka_custom_1 = request.form.get('walka_custom_1', '')
        skills.walka_custom_1_val = int(request.form.get('walka_custom_1_val', 0) or 0)
        skills.walka_custom_2 = request.form.get('walka_custom_2', '')
        skills.walka_custom_2_val = int(request.form.get('walka_custom_2_val', 0) or 0)
        skills.natura = int(request.form.get('natura', 10) or 10)
        skills.wspinaczka = int(request.form.get('wspinaczka', 20) or 20)
        skills.wycena = int(request.form.get('wycena', 5) or 5)
        skills.zastraszanie = int(request.form.get('zastraszanie', 15) or 15)
        skills.zreczne_palce = int(request.form.get('zreczne_palce', 10) or 10)
        skills.custom_skill_1 = request.form.get('custom_skill_1', '')
        skills.custom_skill_1_val = int(request.form.get('custom_skill_1_val', 0) or 0)
        skills.custom_skill_2 = request.form.get('custom_skill_2', '')
        skills.custom_skill_2_val = int(request.form.get('custom_skill_2_val', 0) or 0)
        skills.custom_skill_3 = request.form.get('custom_skill_3', '')
        skills.custom_skill_3_val = int(request.form.get('custom_skill_3_val', 0) or 0)
        skills.custom_skill_4 = request.form.get('custom_skill_4', '')
        skills.custom_skill_4_val = int(request.form.get('custom_skill_4_val', 0) or 0)
        skills.custom_skill_5 = request.form.get('custom_skill_5', '')
        skills.custom_skill_5_val = int(request.form.get('custom_skill_5_val', 0) or 0)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Umiejętności zapisane!'})

        flash('✅ Umiejętności zapisane!')
        return redirect(url_for('edytuj_karte_cthulhu', character_id=character_id))

    return render_template('umiejetnosci_cthulhu.html', character=character, skills=skills)


@app.route("/bron-cthulhu/<int:character_id>", methods=["GET", "POST"])
@login_required
def bron_cthulhu(character_id):
    character = CharacterCthulhu.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    if request.method == "POST":
        CthulhuBron.query.filter_by(character_id=character_id).delete()

        # Broń - 10 wierszy (1-10)
        for i in range(1, 11):
            nazwa = request.form.get(f'weapon_name_{i}', '').strip()
            if nazwa:
                item = CthulhuBron(
                    character_id=character_id,
                    bron_index=i - 1,
                    nazwa_broni=nazwa,
                    normal=request.form.get(f'weapon_normal_{i}', '').strip(),
                    hard=request.form.get(f'weapon_hard_{i}', '').strip(),
                    extreme=request.form.get(f'weapon_extreme_{i}', '').strip(),
                    szkody=request.form.get(f'weapon_damage_{i}', '').strip(),
                    zasieg=request.form.get(f'weapon_range_{i}', '').strip(),
                    attacks=request.form.get(f'weapon_attacks_{i}', '').strip(),
                    ammo=request.form.get(f'weapon_ammo_{i}', '').strip(),
                    malfunction=request.form.get(f'weapon_malfunction_{i}', '').strip()
                )
                db.session.add(item)

        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': '✅ Broń została zapisana!'})

        flash('✅ Broń została zapisana!')
        return redirect(url_for('bron_cthulhu', character_id=character_id))

    bron = CthulhuBron.query.filter_by(character_id=character_id).all()
    return render_template('bron_cthulhu.html', character=character, bron=bron)


@app.route("/usun-karte-cthulhu/<int:character_id>", methods=["POST"])
@login_required
def usun_karte_cthulhu(character_id):
    character = CharacterCthulhu.query.get_or_404(character_id)

    if character.user_id == current_user.id:
        db.session.delete(character)
        db.session.commit()
        flash('✅ Karta Cthulhu została usunięta!')
    else:
        flash('❌ Nie masz dostępu do tej karty!')

    return redirect(url_for('karty_postaci'))


@app.route("/drukuj-karte-cthulhu/<int:character_id>")
@login_required
def drukuj_karte_cthulhu(character_id):
    character = CharacterCthulhu.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    skills = CthulhuSkills.query.filter_by(character_id=character_id).first()
    bron = CthulhuBron.query.filter_by(character_id=character_id).all()

    return render_template('drukuj_karta_cthulhu.html',
                         character=character,
                         skills=skills,
                         bron=bron)


@app.route("/drukuj-karte-warhammer/<int:character_id>")
@login_required
def drukuj_karte_warhammer(character_id):
    character = CharacterWarhammer.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    skills = WarhammerUmiejetnosc.query.filter_by(character_id=character_id).all()
    bron = WarhammerBron.query.filter_by(character_id=character_id).all()
    zbroja = WarhammerArmor.query.filter_by(character_id=character_id).all()
    ekwipunek = WarhammerEkwipunek.query.filter_by(character_id=character_id).all()

    return render_template('drukuj_karta_warhammer.html',
                         character=character,
                         skills=skills,
                         bron=bron,
                         zbroja=zbroja,
                         ekwipunek=ekwipunek)


@app.route("/drukuj-karte-dnd5e/<int:character_id>")
@login_required
def drukuj_karte_dnd5e(character_id):
    character = CharacterDnD5e.query.get_or_404(character_id)

    if character.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_postaci'))

    bieglosci = DnD5eBieglosci.query.filter_by(character_id=character_id).first()
    magia = DnD5eMagia.query.filter_by(character_id=character_id).first()
    ekwipunek = DnD5eEkwipunek.query.filter_by(character_id=character_id).all()

    return render_template('drukuj_karta_dnd5e.html',
                         character=character,
                         bieglosci=bieglosci,
                         magia=magia,
                         ekwipunek=ekwipunek)


# ===== TRADER MANAGER =====

@app.route("/karty-traderow")
@login_required
def karty_traderow():
    trader_cards = TraderManager.query.filter_by(user_id=current_user.id).all()
    return render_template('karty_traderow.html', trader_cards=trader_cards)


@app.route("/nowa-karta-trader", methods=["GET", "POST"])
@login_required
def nowa_karta_trader():
    if request.method == "POST":
        nazwa_postaci = request.form.get('nazwa_postaci', '')

        trader = TraderManager(
            nazwa_postaci=nazwa_postaci,
            user_id=current_user.id
        )

        db.session.add(trader)
        db.session.flush()

        for i in range(30):
            nazwa = request.form.get(f'bought_nazwa_{i}', '').strip()
            if nazwa:
                ilosc = request.form.get(f'bought_ilosc_{i}', '0')
                cena = request.form.get(f'bought_cena_{i}', '0')
                wartosc = request.form.get(f'bought_wartosc_{i}', '0')
                suma_ceny = request.form.get(f'bought_suma_ceny_{i}', '0')
                suma_wartosci = request.form.get(f'bought_suma_wartosci_{i}', '0')

                item = TraderItem(
                    trader_id=trader.id,
                    item_type='bought',
                    item_index=i,
                    nazwa_towaru=nazwa,
                    ilosc_jednostek=ilosc,
                    cena_jednostkowa=cena,
                    wartosc_rynkowa=wartosc,
                    suma_ceny=suma_ceny,
                    suma_wartosci=suma_wartosci
                )
                db.session.add(item)

        for i in range(30):
            nazwa = request.form.get(f'sold_nazwa_{i}', '').strip()
            if nazwa:
                ilosc = request.form.get(f'sold_ilosc_{i}', '0')
                cena = request.form.get(f'sold_cena_{i}', '0')
                suma_ceny = request.form.get(f'sold_suma_ceny_{i}', '0')
                suma_wartosci = request.form.get(f'sold_suma_wartosci_{i}', '0')

                item = TraderItem(
                    trader_id=trader.id,
                    item_type='sold',
                    item_index=i,
                    nazwa_towaru=nazwa,
                    ilosc_jednostek=ilosc,
                    cena_jednostkowa=cena,
                    wartosc_rynkowa='0',  # nie używane w sprzedaży
                    suma_ceny=suma_ceny,
                    suma_wartosci=suma_wartosci
                )
                db.session.add(item)

        db.session.commit()
        flash('✅ Karta Trader Manager\'a została utworzona!')
        return redirect(url_for('karty_traderow'))

    return render_template('nowa_karta_trader.html')


@app.route("/edytuj-karte-trader/<int:trader_id>", methods=["GET", "POST"])
@login_required
def edytuj_karte_trader(trader_id):
    trader = TraderManager.query.get_or_404(trader_id)

    if trader.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_traderow'))

    if request.method == "POST":
        trader.nazwa_postaci = request.form.get('nazwa_postaci', '')

        TraderItem.query.filter_by(trader_id=trader_id).delete()

        for i in range(30):
            nazwa = request.form.get(f'bought_nazwa_{i}', '').strip()
            if nazwa:
                ilosc = request.form.get(f'bought_ilosc_{i}', '0')
                cena = request.form.get(f'bought_cena_{i}', '0')
                wartosc = request.form.get(f'bought_wartosc_{i}', '0')
                suma_ceny = request.form.get(f'bought_suma_ceny_{i}', '0')
                suma_wartosci = request.form.get(f'bought_suma_wartosci_{i}', '0')

                item = TraderItem(
                    trader_id=trader_id,
                    item_type='bought',
                    item_index=i,
                    nazwa_towaru=nazwa,
                    ilosc_jednostek=ilosc,
                    cena_jednostkowa=cena,
                    wartosc_rynkowa=wartosc,
                    suma_ceny=suma_ceny,
                    suma_wartosci=suma_wartosci
                )
                db.session.add(item)

        for i in range(30):
            nazwa = request.form.get(f'sold_nazwa_{i}', '').strip()
            if nazwa:
                ilosc = request.form.get(f'sold_ilosc_{i}', '0')
                cena = request.form.get(f'sold_cena_{i}', '0')
                suma_ceny = request.form.get(f'sold_suma_ceny_{i}', '0')
                suma_wartosci = request.form.get(f'sold_suma_wartosci_{i}', '0')

                item = TraderItem(
                    trader_id=trader_id,
                    item_type='sold',
                    item_index=i,
                    nazwa_towaru=nazwa,
                    ilosc_jednostek=ilosc,
                    cena_jednostkowa=cena,
                    wartosc_rynkowa='0',  # nie używane w sprzedaży
                    suma_ceny=suma_ceny,
                    suma_wartosci=suma_wartosci
                )
                db.session.add(item)

        db.session.commit()
        flash('✅ Karta Trader Manager\'a została zaktualizowana!')
        return redirect(url_for('edytuj_karte_trader', trader_id=trader_id))

    bought_items = TraderItem.query.filter_by(trader_id=trader_id, item_type='bought').all()
    sold_items = TraderItem.query.filter_by(trader_id=trader_id, item_type='sold').all()

    return render_template('edytuj_karte_trader.html',
                           trader=trader,
                           bought_items=bought_items,
                           sold_items=sold_items)


@app.route("/usun-karte-trader/<int:trader_id>", methods=["POST"])
@login_required
def usun_karte_trader(trader_id):
    trader = TraderManager.query.get_or_404(trader_id)

    if trader.user_id != current_user.id:
        flash('Nie masz dostępu do tej karty!')
        return redirect(url_for('karty_traderow'))

    db.session.delete(trader)
    db.session.commit()
    flash('✅ Karta Trader Manager\'a została usunięta!')
    return redirect(url_for('karty_traderow'))


# ===== NPC MANAGER =====

@app.route("/npc-manager")
@login_required
def npc_manager():
    """Strona główna NPC Managera - wybór systemu"""
    return render_template('npc_manager.html')


@app.route("/npc-manager/cthulhu", methods=["GET", "POST"])
@login_required
def npc_manager_cthulhu():
    """Manager NPC dla systemu Cthulhu"""
    if request.method == "POST":
        action = request.form.get('action')

        if action == 'create':
            npc = NPCCthulhu(
                user_id=current_user.id,
                imie=request.form.get('imie', 'Nowy NPC')
            )
            db.session.add(npc)
            db.session.commit()
            return jsonify({'success': True, 'npc_id': npc.id})

        elif action == 'update':
            npc_id = request.form.get('npc_id')
            npc = NPCCthulhu.query.get_or_404(npc_id)
            if npc.user_id == current_user.id:
                for key, value in request.form.items():
                    if key not in ['action', 'npc_id'] and hasattr(npc, key):
                        setattr(npc, key, value)
                db.session.commit()
                return jsonify({'success': True})

        elif action == 'delete':
            npc_id = request.form.get('npc_id')
            npc = NPCCthulhu.query.get_or_404(npc_id)
            if npc.user_id == current_user.id:
                db.session.delete(npc)
                db.session.commit()
                return jsonify({'success': True})

    npcs = NPCCthulhu.query.filter_by(user_id=current_user.id).all()
    return render_template('npc_manager_cthulhu.html', npcs=npcs)


@app.route("/npc-manager/warhammer", methods=["GET", "POST"])
@login_required
def npc_manager_warhammer():
    """Manager NPC dla systemu Warhammer"""
    if request.method == "POST":
        action = request.form.get('action')

        if action == 'create':
            npc = NPCWarhammer(
                user_id=current_user.id,
                imie=request.form.get('imie', 'Nowy NPC')
            )
            db.session.add(npc)
            db.session.commit()
            return jsonify({'success': True, 'npc_id': npc.id})

        elif action == 'update':
            npc_id = request.form.get('npc_id')
            npc = NPCWarhammer.query.get_or_404(npc_id)
            if npc.user_id == current_user.id:
                for key, value in request.form.items():
                    if key not in ['action', 'npc_id'] and hasattr(npc, key):
                        setattr(npc, key, value)
                db.session.commit()
                return jsonify({'success': True})

        elif action == 'delete':
            npc_id = request.form.get('npc_id')
            npc = NPCWarhammer.query.get_or_404(npc_id)
            if npc.user_id == current_user.id:
                db.session.delete(npc)
                db.session.commit()
                return jsonify({'success': True})

    npcs = NPCWarhammer.query.filter_by(user_id=current_user.id).all()
    return render_template('npc_manager_warhammer.html', npcs=npcs)


@app.route("/npc-manager/dnd5e", methods=["GET", "POST"])
@login_required
def npc_manager_dnd5e():
    """Manager NPC dla systemu D&D 5e"""
    if request.method == "POST":
        action = request.form.get('action')

        if action == 'create':
            npc = NPCDnD5e(
                user_id=current_user.id,
                imie=request.form.get('imie', 'Nowy NPC')
            )
            db.session.add(npc)
            db.session.commit()
            return jsonify({'success': True, 'npc_id': npc.id})

        elif action == 'update':
            npc_id = request.form.get('npc_id')
            npc = NPCDnD5e.query.get_or_404(npc_id)
            if npc.user_id == current_user.id:
                for key, value in request.form.items():
                    if key not in ['action', 'npc_id'] and hasattr(npc, key):
                        setattr(npc, key, value)
                db.session.commit()
                return jsonify({'success': True})

        elif action == 'delete':
            npc_id = request.form.get('npc_id')
            npc = NPCDnD5e.query.get_or_404(npc_id)
            if npc.user_id == current_user.id:
                db.session.delete(npc)
                db.session.commit()
                return jsonify({'success': True})

    npcs = NPCDnD5e.query.filter_by(user_id=current_user.id).all()
    return render_template('npc_manager_dnd5e.html', npcs=npcs)


# ===== CONTEXT PROCESSOR =====

@app.context_processor
def inject_user():
    return dict(current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5001)