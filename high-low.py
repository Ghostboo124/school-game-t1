from random import randint

guess = ""
number = randint(0,100)
counter = 1

while guess != number:
    try:
        guess = int(input("Make a guess between 0 and 100! "))
    except ValueError:
        print("Guess must be a number")
        continue

    if 100 <= guess or guess <= 0:
        print("Guess must be between 0 and 100")
        continue

    if guess >= number:
        print("Too high")
    elif guess <= number:
        print("Too low")
    else:
        print("Uhhh something has gone severly wrong")
        exit(1)

    counter += 1

print(f"You won in {counter} tries!")