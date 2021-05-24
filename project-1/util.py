ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def caesar_cipher(plaintext, key, decryption=False): 
    
    result = ""
    
    for i in range(len(plaintext)):
        
        c = plaintext[i].lower()
        
        if c in ALPHABET:
            idx = ALPHABET.index(c)
            index = idx + key if decryption == False else (idx - key) 
            new = ALPHABET[index % 26]
            result += new if plaintext[i].islower() else new.upper()
        else:
            result += plaintext[i]           
    
    return result

def otp_cypher(plaintext, key): 

    key = key[:len(plaintext)]
    
    result = ""
    
    for i in range(len(plaintext)):
        c = ord(plaintext[i])
        k = ord(key[i])
        result += chr(c ^ k)

    return result

def write_file(dir_path, plaintext, caesar_key, otp_key, decryption=False):
    
    if decryption == False:
        result = caesar_cipher(plaintext, caesar_key, decryption)
        result = otp_cypher(result, otp_key)
    else:
        result = otp_cypher(plaintext, otp_key)
        result = caesar_cipher(result, caesar_key, decryption)
    
    
    output_file = open(dir_path + "/output.txt", "w")
    
    output_file.write(result)
    
    output_file.close()    
    
    
    
    
   
    
    