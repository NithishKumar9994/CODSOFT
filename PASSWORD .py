import random
import string

# Prompt user for desired password length
try:
    length = int(input("Enter the desired password length: "))
    if length <= 0:
        print("Password length must be greater than 0.")
        exit()
except ValueError:
    print("Please enter a valid number.")
    exit()

# Character sets
characters = string.ascii_letters + string.digits + string.punctuation

# Generate password
password = ''.join(random.choice(characters) for _ in range(length))

# Display password
print(f"Generated Password: {password}")
