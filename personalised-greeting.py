"""
A Program to get someones age and name and write a personalised greeting
"""

def main() -> int:
    nameInput =        input("Hello, What is your name: ")
    try:
        ageInput = int(input("What is your age: "))
    except ValueError:
        print("Please type a valid intiger!")
        return 1

    print(f'"{nameInput}" Huh, thats a nice name')
    if ageInput <= 5:
        print("Wow, good job, I didn't know you could run this script")
    elif ageInput <= 18:
        print("Hello, you probably can't wait to be an adult, weeelll you should want to wait, it won't be fun")
    elif 18 < ageInput >= 30:
        print("Have you had a midlife crisis yet?", end=" ")
        input()
    elif 30 < ageInput >= 60:
        print('You have definitly had a midlife crisis!')
    elif ageInput >= 80:
        print("Good job, you are still alive")
    elif ageInput >= 100:
        print("Wow, still kicking, nice")
    elif ageInput > 100:
        print('WOW!!! Good Job!!! Over 100!!!!')
    return 0


if __name__ == "__main__":
    code = main()
    if code >= 1:
        exit(code)