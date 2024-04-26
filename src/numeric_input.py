def get_numeric_input(prompt):
    """
    Ask user for a digit
    This is to assist when the room is noisy
    
    Args:
        - prompt: string of text
    
    Returns:
        - user_input: integer number
    """
    
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Please enter a valid numerical input.")

if __name__ == "__main__":
    num = get_numeric_input("Enter a number: ")
    print("You entered:", num)
