import re


def mask_card_number(card_number: str) -> str:
    digits = re.sub(r"\D", "", card_number)

    if len(digits) < 13 or len(digits) > 19:
        return card_number

    masked_digits = "*" * (len(digits) - 4) + digits[-4:]

    result = []
    digit_idx = 0

    for char in card_number:
        if char.isdigit():
            result.append(masked_digits[digit_idx])
            digit_idx += 1
        else:
            result.append(char)

    return "".join(result)


def mask_card_numbers_guardrail(result):
    text = result.raw

    card_pattern = re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b|\b\d{13,19}\b")

    sanitized = card_pattern.sub(
        lambda m: mask_card_number(m.group()),
        text,
    )

    return True, sanitized
