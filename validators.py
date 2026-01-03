import re


def validate_password(password, password2):
    """
    Waliduje hasło według określonych kryteriów.
    Zwraca: (bool, str) - (czy_poprawne, komunikat_błędu)
    """

    # Sprawdź czy hasła są identyczne
    if password != password2:
        return False, "Podano różne wersje hasła"

    # Sprawdź długość
    if len(password) < 8:
        return False, "Hasło musi mieć minimum 8 znaków"

    # Sprawdź małe litery
    if not re.search(r"[a-z]", password):
        return False, "Hasło musi zawierać małe litery"

    # Sprawdź duże litery
    if not re.search(r"[A-Z]", password):
        return False, "Hasło musi zawierać DUŻE litery"

    # Sprawdź cyfry
    if not re.search(r"[0-9]", password):
        return False, "Hasło musi zawierać cyfry"

    # Sprawdź znaki specjalne
    if not re.search(r"[!@#$%^&*()+\-=,.\/<>?:]", password):
        return False, "Hasło musi zawierać znak specjalny (!@#$%^&* itp.)"

    # Wszystko OK
    return True, "Hasło poprawne"