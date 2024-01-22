# ECRYPT-ElGamal
ELGAMAL CIPHER -  ECB and CBC implementation

Key Generation
In this case the first user1 generates the following key:
- Choose a large prime number, 𝑝.
- Select a primitive root module 𝑝, denoted as 𝑔.
- Choose a private key, 𝑥, randomly from interval [1, 𝑝 − 2].
- Compute the corresponding public key 𝑦 = 𝑔^𝑥 ∙ mod 𝑝
We get the public key (𝑝,𝑔, 𝑦) , and the private key is 𝑥.

Encryption
For example user2 would do the encryption:
- Choose a random secret key, , 𝑘, from the interval [1, 𝑝 − 2].
- Compute 𝑎 = 𝑔^𝑥 ∙ mod 𝑝.
- Compute 𝑏 = (𝑦^𝑘 ∙ 𝑀) 𝑚𝑜𝑑 𝑝. Where 𝑀 is the plaintext message.
The ciphertext would be (𝑎, 𝑏).

Decryption
This is what Alice should do to decrypt the message.
- Use the private key 𝑥 to compute the inverse of 𝑎 module 𝑝, denoted as 𝑎^(-1).
- Compute 𝑠 = 𝑎^(-𝑥) ∙ 𝑚𝑜𝑑 𝑝.
- Multiply 𝑠 by 𝑏 module 𝑝 to obtain the plaintext message, 𝑀 = (𝑠 ∙ 𝑏) 𝑚𝑜𝑑 𝑝.
Obtaining 𝑀, the original message.
