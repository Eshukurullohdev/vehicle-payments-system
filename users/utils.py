def normalize_phone(phone):
    # faqat raqamlarni qoldiramiz
    digits = ''.join(filter(str.isdigit, phone))

    # agar 998 bilan boshlanmasa — qo‘shamiz
    if digits.startswith('998'):
        return '+' + digits
    elif digits.startswith('8'):
        return '+99' + digits
    elif digits.startswith('9'):
        return '+998' + digits
    else:
        return '+' + digits