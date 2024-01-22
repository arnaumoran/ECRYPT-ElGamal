# ECRYP PROJECT WINTER 2023
# ElGamal cipher (software implementation - 2 ciphering modes – ECB and CBC) 
#
# Arnau Moran Riera               K-7430
#---------------------------------------
# ECB Implementation of ElGamal cipher
# --------------------------------------

# Load required libraries
import random
import time

# Modular exponentiation function
def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base ** 2) % modulus
    return result

# Generation of keys
def generate_keys(p, g, x):
    """
    This function generates both public and private keys.
    p: prime number
    g: generator
    x: private key
    """
    y = mod_exp(g, x, p)  # Public key
    return y, x

# Encryption
def encrypt(message, p, g, y):
    """
    This function encrypts the message.
    message: message to encrypt
    p, g, y: public key parameters
    """
    k = random.randint(2, p-2)  # Ephemeral key (randomly generated)
    print("Ephemeral key: ", k)
    a = mod_exp(g, k, p)
    b = (mod_exp(y, k, p) * message) % p
    return a, b

# Decryption
def decrypt(a, b, p, x):
    """
    This function decrypts the encrypted message.
    a, b: encrypted message
    p, x: private key parameters
    """
    a_inv = mod_exp(a, p-1-x, p)
    message = (b * a_inv) % p
    return message



# -----------------------------------------------------------------------------------------------------------------
# ElGamal encryption, as originally defined, is designed for numerical values within a finite field.
# However, we wanted to try to encrypt non-numerical messages too using ElGamal with some modifications. 
# Our approach is to convert the non-numerical message into a numerical format before encryption and then reverse the process during decryption.
# Each character is substituded by its corresponding ASCII value, thus obtaining a completely numerical message to be encrypted.

# Function to check if a given input is numerical
def is_numerical(input_str):
    try:
        int(input_str)
        return True
    except ValueError:
        return False

# Encryption for non-numeric messages
def encrypt_non_numeric(message, p, g, y):
    ciphertext = [(mod_exp(g, k, p), (ord(char) * mod_exp(y, k, p)) % p) for char, k in zip(message, [random.randint(2, p-2) for _ in range(len(message))])]
    return ciphertext

# Decryption for non-numeric messages
def decrypt_non_numeric(ciphertext, p, x):
    decrypted_message = ''.join([chr((b * mod_exp(a, p-1-x, p)) % p) for a, b in ciphertext])
    return decrypted_message
# ---------------------------------------------------------------------------------------------------------------------

# Algorithm Test
p = 14983  # Prime number
g = 5  # Generator
x = 6  # Private key

# Interface
print("-------------------------------------")
print("ECB Implementation of ElGamal cipher")
print("-------------------------------------")
print("PARAMETERS INTERFACE ")
while True:
    p = int(input("Enter prime number (default - 14983): "))
    if (is_numerical(p) and int(p) > 255):
        break
    else:
        print("Error: has to be a number higher than 255")      #ASCII values go all the way to 255. To avoid the issue of message values being higher than p; p>255.
g = int(input("Enter generator (default - 5): "))
x = int(input("Enter private key (default - 6): "))
print("--------------ALGORITHM ---------------")

# Generate the keys
y, x = generate_keys(p, g, x)

# Ask for the message to encrypt
while True:
    message_input = input("Enter the message to encrypt: ")
    if (is_numerical(message_input) and int(message_input) < p) or (not is_numerical(message_input)):
        break
    else:
        print("Error: Numerical messages should be less than p. Please enter a valid message.")

start_time = time.time()

# Encrypt the message
if is_numerical(message_input):
    # If numerical, use the numerical encryption function
    a, b = encrypt(int(message_input), p, g, y)
    print(f"Encrypted message: {a}, {b}")

    # Decrypt the message
    decrypted_message = decrypt(a, b, p, x)
    print(f"Decrypted message: {decrypted_message}")
else:
# If non-numerical, use the non-numerical encryption function
    encrypted_message = encrypt_non_numeric(message_input, p, g, y)
    print(f"Encrypted message: {encrypted_message}")

    decrypted_message = decrypt_non_numeric(encrypted_message, p, x)
    print(f"Decrypted message: {decrypted_message}")

# Record the end time
end_time = time.time()

# Calculate the total execution time
total_time = end_time - start_time

# Print the total execution time
print(f"Total execution time: {total_time} seconds")


