def check_isbn(isbn: str) -> bool:
    c = 0
    for i in range(len(isbn)):
        c += int(isbn[i]) * (1 + ((i+1) % 2 == 0) * 2)
    return c % 10 == 0


print(check_isbn("0781566199093"))
