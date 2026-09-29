from math import gcd

BYTES_PER_MB = 1024 * 1024


class BBS:
    """Blum Blum Shub pseudorandom bit generator.

    P and Q must be distinct primes congruent to 3 mod 4 and the seed must be
    coprime to n = P * Q. Each step squares the state modulo n and outputs the
    parity of the new state.
    """

    def __init__(self, P, Q, seed):
        if P % 4 != 3 or Q % 4 != 3:
            raise ValueError("P and Q must be congruent to 3 mod 4")
        self.p = P
        self.q = Q
        self.n = self.p * self.q
        if gcd(seed, self.n) != 1:
            raise ValueError("the seed must be coprime to P * Q")
        self.x = (seed * seed) % self.n

    def next_bit(self):
        self.x = (self.x * self.x) % self.n
        return bin(self.x).count("1") & 1

    def next_byte(self):
        byte = 0
        for _ in range(8):
            byte = (byte << 1) | self.next_bit()
        return byte

    def generate_bytes(self, no_bytes):
        return bytes(self.next_byte() for _ in range(no_bytes))

    def generate_binary_file(self, no_mb, dir_path):
        """Write no_mb megabytes of random data (8 random bits per byte)."""
        filename = dir_path + "/result_" + str(no_mb) + ".bin"
        with open(filename, "wb") as file:
            for _ in range(no_mb):
                file.write(self.generate_bytes(BYTES_PER_MB))
        return filename
