preferences = {'dogs': 0, 'cats': 0, 'burgers': 0, 'pasta': 0, 'pizza': 0, 'sushi': 0, }
counter = 1

def response(input: int = 3, counter: int = 1):
    if counter == 1:
        if input == 1:
            preferences["dogs"] = 1
            print("Noted")
            return(0)
        elif input == 2:
            preferences["cats"] = 1
            print("Noted")
            return(0)
        elif input == 3:
            print("Thank you for playing!")
            exit(0)
        else:
            print("Please enter a valid number!")
            exit(2)
    elif counter == 2:
        if input == 1:
            preferences["burgers"] = 1
            print("Noted")
            return(0)
        elif input == 2:
            preferences["pasta"] = 1
            print("Noted")
            return(0)
        elif input == 3:
            print("Thank you for playing!")
            exit(0)
        else:
            print("Please enter a valid number!")
            exit(2)
    elif counter == 3:
        if input == 1:
            preferences["pizza"] = 1
            print("Noted")
        elif input == 2:
            preferences["sushi"] = 1
            print("Noted")
        elif input == 3:
            print("Thank you for playing!")
            exit(0)
        else:
            print("Please enter a valid number!")
            exit(2)
    else:
        print("Uhhh... something went really wrong!")
        exit(1)

    

while True:
    if counter == 1:
        print("Enter '1' for the first option, '2' for the second option, or '3' to quit.")
        print("Do you prefer dogs or cats?", end=' ')
    elif counter == 2:
        print("Do you prefer burgers or pasta?", end=' ')
    elif counter == 3:
        print("Do you prefer pizza or sushi?", end=' ')
    elif counter == 4:
        print("Thank you for playing!")
        print(f"Your responses were:")
        for key in preferences:
            if preferences[key] == 0:
                print(f"{key}: No")
            elif preferences[key] == 1:
                print(f"{key}: Yes")
            else:
                print("An Error has occured")
                exit(3)
        break

    try:
        userInput = int(input())
        print()
    except ValueError:
        print()
        print("Please enter a number!")
        continue

    response(userInput, counter)
    counter += 1

exit