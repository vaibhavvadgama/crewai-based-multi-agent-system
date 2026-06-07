def mask_password(password: str) -> str:
    """
    Masks a password string according to specific rules:
    1. If length > 5: Show '***' prefix and the last 5 characters.
    2. If length <= 5: Mask ALL characters with stars.

    Args:
        password (str): The raw password string.

    Returns:
        str: The masked representation of the password.
    """
    length = len(password)

    if not isinstance(password, str):
        raise TypeError("Input must be a string.")

    # Condition 2: String is shorter than or equal to 5 characters (Mask everything)
    if length <= 5:
        return "*" * length

    # Condition 1: String is longer than 5 characters (Show prefix + suffix)
    else:
        # The last 5 characters are extracted using negative slicing [-5:]
        suffix = password[-5:]

        # We explicitly overwrite the beginning with 3 stars, followed by the visible suffix.
        return "***" + suffix
