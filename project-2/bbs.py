import bitmath
NO_BIT = 1048576

class BBS:
    
    
    def __init__(self, P, Q, seed):
        
        self.p = P
        self.q = Q
        self.x_0 = seed
        
        self.n = self.p * self.q
    
    def get_rand_parity_bit(self):
        
        next_rand_number = (self.x_0 ** 2) % self.n
        
        self.x_0 = next_rand_number
        
        parity_bit = False
        
        while next_rand_number:
            parity_bit = ~parity_bit
            next_rand_number = next_rand_number & (next_rand_number - 1)
        
        parity_bit = 1 if parity_bit == -1 else 0
            
        return parity_bit.to_bytes(1, byteorder="big")
    
    def generate_binary_file(self, no_mb, dir_path):
        
        no_bits = no_mb * NO_BIT
        
        filename = dir_path + "/result_" + str(no_mb) + ".bin"
        
        file = open(filename, "ab")
        
        for _ in range(no_bits):
            file.write(self.get_rand_parity_bit())
     
        file.close()
