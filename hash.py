import bcrypt


def hash_password() -> str:
    """
    Hash a password using bcrypt.

    Parameters:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw('Uno23'.encode(), salt)
    print(hashed.decode())
    return hashed.decode()

hash_password()