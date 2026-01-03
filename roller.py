import secrets
import os


def calculate_dice_roll(dice_type, dice_number):
    dice_type = int(dice_type)
    dice_number = int(dice_number)
    result = 0

    for _ in range(dice_number):
        # Używa entropy z systemu operacyjnego
        random_bytes = os.urandom(4)
        random_value = int.from_bytes(random_bytes, 'big') % dice_type + 1
        result += random_value

    return result