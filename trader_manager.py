"""
Trader Manager Model
Niezależny system zarządzania handlem towarami
"""

from datetime import datetime


def create_trader_models(db):
    """Tworzy modele Trader Manager'a"""

    class TraderManager(db.Model):
        __tablename__ = 'trader_manager'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        nazwa_postaci = db.Column(db.String(255), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

        # Relacja z itemami
        items = db.relationship('TraderItem', backref='trader', lazy=True, cascade='all, delete-orphan')

        def __repr__(self):
            return f'<TraderManager {self.nazwa_postaci}>'

    class TraderItem(db.Model):
        __tablename__ = 'trader_item'
        id = db.Column(db.Integer, primary_key=True)
        trader_id = db.Column(db.Integer, db.ForeignKey('trader_manager.id'), nullable=False)
        item_type = db.Column(db.String(20), nullable=False)  # 'bought' lub 'sold'
        item_index = db.Column(db.Integer, nullable=False, default=0)  # indeks 0-29
        nazwa_towaru = db.Column(db.String(255), nullable=False)
        ilosc_jednostek = db.Column(db.String(50), nullable=False)
        cena_jednostkowa = db.Column(db.String(50), nullable=False)
        wartosc_rynkowa = db.Column(db.String(50), nullable=False)
        suma_ceny = db.Column(db.String(50), nullable=True)
        suma_wartosci = db.Column(db.String(50), nullable=True)

        def __repr__(self):
            return f'<TraderItem {self.nazwa_towaru}>'

    return TraderManager, TraderItem