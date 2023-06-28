import math
import secrets


# Task 1
def are_relatively_prime(e: int, z: int) -> bool:
    """
    Returns if two integers are relatively prime.
    This is equivalent to the question if their biggest common divisor is 1.
    Primes are always relatively prime to every other number.
    This expression is commutative.
    :param e: Number
    :param z: Number
    :return: gcd ?= 1
    """
    return math.gcd(e, z) == 1


# Task 2
def generate_keypair(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Calculates the public and private RSA Keys K+ and K- for two primes p and q.
    Both prime numbers should be very big (1024 bits).
    Non deterministic.
    :param p: large prime number
    :param q: large prime number != q
    :return: (K+, K-)(p,q)
    """
    n = p * q
    z = (p - 1) * (q - 1)
    e = n-1

    # god forgive me for this solution
    while (not are_relatively_prime(e, z)) or e <= 3:
        e = secrets.randbelow(n)

    d = 0

    # Again. I am sorry god
    while not (d * e - 1) % z == 0:
        d = d + 1

    return (n, e), (n, d)


# Task 3
def encrypt(key: tuple[int, int], m: int) -> int:
    """
    Encrypts a message m with the given RSA public key-pair
    :param key: public key
    :param m: message
    :return: K+(m)
    """
    return pow(m, key[1], key[0])


def decrypt(key: tuple[int, int], c: int) -> int:
    """
    Decrypts a cipher c with the given RSA private key-pair
    :param key: private key
    :param c: cipher
    :return: K-(m)
    """
    return pow(c, key[1], key[0])


