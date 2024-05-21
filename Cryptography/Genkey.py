import string
import random
import sys

class XORCipher:
    def __init__(self, key):
        key = key.replace(' ', '-')
        if len(key) < 32:
            key += '-' * (32 - len(key))
        self.key = key

    def encrypt(self, text):
        encrypted_text = ""  #bytearray()
        for i in range(len(text)):
            #print(chr(text[i]))
            encrypted_text += chr(ord(chr(text[i])) ^ ord(self.key[i % len(self.key)]))
        return encrypted_text

    def decrypt(self, encrypted_text):
        decrypted_text = "" #bytearray
        for i in range(len(encrypted_text)):
            decrypted_text += chr(ord(encrypted_text[i]) ^ ord(self.key[i % len(self.key)]))
        return decrypted_text
    

class Genome:
    score = 10000
    alphabet = string.ascii_letters + string.digits + "-_"
    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            self.key = ''.join(random.choices(self.alphabet, k=32))

    def mutate(self, type=None):
        

        key_length = len(self.key)
        start_index = random.randint(0, key_length - 4)  # Ensure a range of at least length 4
        end_index = start_index + 3
        if type is not None and type == 1:
            rand = ''.join(random.choices(self.alphabet, k=4))
            mutated_key = self.key[:start_index] + rand + self.key[end_index+1:]
        # Scramble the characters between start and end indexes
        elif type is not None and type == 2:
            mutated_key = self.key[:start_index] + "".join(random.sample(self.alphabet, 1)) + self.key[start_index+1:]
        else: 
            chars_to_scramble = list(self.key[start_index:end_index+1])
            random.shuffle(chars_to_scramble)
            scramble = ''.join(chars_to_scramble)
            mutated_key = self.key[:start_index] + scramble + self.key[end_index+1:]

        self.key = mutated_key

    def crossover(self, other_genome):
        key_length = len(self.key)
        # Generate a crossover mask with up to 1/4 of the key length being 1's
        mask_length = random.randint(1, key_length // 4)
        mask_indexes = random.sample(range(key_length), mask_length)
        mask = ['1' if i in mask_indexes else '0' for i in range(key_length)]
        mask = ''.join(mask)
        # Apply crossover using the mask
        child1_key = ''.join([self.key[i] if mask[i] == '0' else other_genome.key[i] for i in range(key_length)])
        child2_key = ''.join([other_genome.key[i] if mask[i] == '0' else self.key[i] for i in range(key_length)])
        return Genome(child1_key), Genome(child2_key)

    def getFitness(self, evaluator):
        #print("Getting Fitness...")
        self.score = evaluator.evaluate(self.key)

class Evaluator:
    expfreq = {
        " " : 0.1662397373587528,
        "'" : 0.001809165560335683,
        "(" : 0.0003238341968911917,
        ")" : 0.0003238341968911917,
        "," : 0.01655925232446724,
        "." : 0.007895552061022744,
        "0" : 0.0005434782608695652,
        "1" : 0.0018388150484343322,
        "2" : 0.0005955733273259743,
        "3" : 0.0003238341968911917,
        "5" : 0.0008673124577607569,
        "6" : 0.0002717391304347826,
        "7" : 0.0014628857850867312,
        "8" : 0.0003238341968911917,
        "9" : 0.0003238341968911917,
        "a" : 0.06872463302045699,
        "b" : 0.011936018394410523,
        "c" : 0.020094276447451414,
        "d" : 0.034317955848006024,
        "e" : 0.09744060606573673,
        "f" : 0.020816176328249246,
        "g" : 0.014405174409104925,
        "h" : 0.047566112415167824,
        "i" : 0.05609650662868808,
        "j" : 0.0005955733273259743,
        "k" : 0.0044522112427791555,
        "l" : 0.030343448574155288,
        "m" : 0.019206901721723707,
        "n" : 0.06493636959187285,
        "o" : 0.060570157814970424,
        "p" : 0.011264856415160701,
        "q" : 0.0005955733273259743,
        "r" : 0.04768998502554188,
        "s" : 0.04360905695904223,
        "t" : 0.06296582119196033,
        "u" : 0.01967606647763011,
        "v" : 0.010309057301557427,
        "w" : 0.017331418043045735,
        "y" : 0.013880668036837523,
        "z" : 0.0005434782608695652,
        "\"" : 0.0020263941969820573,
        "-" : 0.0002717391304347826
}
    
    common_words = ["the", "to", "for", "be", "and", "in", 
                    "that", "of", "it", "have", "as", "do", 
                    "on", "with", "not", "this", "but", "by", 
                    "from", "they", "at", "all", "so", "get"]
    
    def __init__(self, encrypted_text):
        self.enc_text = encrypted_text

    def evaluate(self, key):
        score = 0
        cipher = XORCipher(key)
        plain_text = cipher.decrypt(self.enc_text)
        #print(plain_text)
        for c in self.expfreq.keys():
            score += abs((plain_text.count(c) / len(plain_text)) - self.expfreq[c])

        for w in self.common_words:
            if w in plain_text:
                score -= 0.005

        score += sum(1 for char in plain_text if ord(char) >= 128)*0.001

        if score < 0:
            score = 0
        return score