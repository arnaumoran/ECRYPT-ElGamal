# ECRYP PROJECT WINTER 2023
# ElGamal cipher (software implementation - 2 ciphering modes – ECB and CBC) 
#
# Arnau Moran Riera               K-7430
#---------------------------------------
# CBC Implementation of ElGamal cipher
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
    y = mod_exp(g, x, p)  # Public key
    return y, x

# Encryption for numerical messages
def encrypt_numeric_cbc(plaintext, p, g, y, iv):
    ciphertext = []
    previous_block = iv

    for block in plaintext:
        k = random.randint(2, p-2)
        a = mod_exp(g, k, p)
        b = (mod_exp(y, k, p) * (block ^ previous_block)) % p
        ciphertext.append((a, b))
        previous_block = b

    return ciphertext

# Decryption for numerical messages
def decrypt_numeric_cbc(ciphertext, p, x, iv):
    decrypted_message = ''
    previous_block = iv

    for a, b in ciphertext:
        a_inv = mod_exp(a, p-1-x, p)
        block = (b * a_inv) % p
        decrypted_message += str(block ^ previous_block)
        previous_block = b

    return decrypted_message


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
def encrypt_non_numeric_cbc(message, p, g, y, iv):
    ciphertext = []
    previous_block = iv

    for char in message:
        k = random.randint(2, p-2)
        a = mod_exp(g, k, p)
        b = (mod_exp(y, k, p) * (ord(char) ^ previous_block)) % p
        ciphertext.append((a, b))
        previous_block = b

    return ciphertext

# Decryption for non-numeric messages
def decrypt_non_numeric_cbc(ciphertext, p, x, iv):
    decrypted_message = ''
    for a, b in ciphertext:
        decrypted_char = (b * mod_exp(a, p-1-x, p)) % p
        decrypted_message += chr(decrypted_char ^ iv)
        iv = b  # Update the IV for the next iteration
    return decrypted_message
# ---------------------------------------------------------------------------------------------------------------------

# Algorithm Test
p = 14983  # Prime number
g = 5  # Generator
x = 6  # Private key

# Interface
print("-------------------------------------")
print("CBC Implementation of ElGamal cipher")
print("-------------------------------------")
print("PARAMETERS INTERFACE ")
while True:
    p = int(input("Enter prime number (default - 14983): "))
    if (is_numerical(p) and int(p) > 255):
        break
    else:
        print("Error: has to be a number higher than 255")   #ASCII values go all the way to 255. To avoid the issue of message values being higher than p; p>255.
g = int(input("Enter generator (default - 5): "))
mx = int(input("Enter private key (default - 6): "))
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

# Use a random initialization vector (IV)
iv = random.randint(2, p-2)

# Encrypt the message
if is_numerical(message_input):
    # If numerical, use the numerical encryption function
    plaintext_numeric = [int(char) for char in str(message_input)]
    ciphertext_numeric = encrypt_numeric_cbc(plaintext_numeric, p, g, y, iv)
    print(f"Encrypted message in CBC mode: {ciphertext_numeric}")

    # Decrypt the message
    decrypted_message_numeric = decrypt_numeric_cbc(ciphertext_numeric, p, x, iv)
    print(f"Decrypted message: {decrypted_message_numeric}")
else:
    # If non-numerical, use the non-numerical encryption function
    ciphertext_non_numeric = encrypt_non_numeric_cbc(message_input, p, g, y, iv)
    print(f"Encrypted message in CBC mode: {ciphertext_non_numeric}")

    decrypted_message_non_numeric = decrypt_non_numeric_cbc(ciphertext_non_numeric, p, x, iv)
    print(f"Decrypted message: {decrypted_message_non_numeric}")

# Record the end time
end_time = time.time()

# Calculate the total execution time
total_time = end_time - start_time

# Print the total execution time
print(f"Total execution time: {total_time} seconds")
    


