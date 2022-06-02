from IPA import IPA
from Phoneme import Vowel, Consonant

ipa = IPA.get_IPA()



for h in range(7):
    for b in range(3):
        for r in range(2):
            print(Vowel(((h, b, r), (1, 0)), 1, ipa))
