from IPA import IPA
from IPA_utils import manner_enc
from Phoneme import Vowel, Consonant

ipa = IPA.get_IPA()



for h in range(7):
    for b in range(3):
        for r in range(2):
            vow = Vowel(((h, b, r), (1, 0)), 1, ipa)
            print(vow.ipa, vow.features, sep='\t')


for part in range(12):
    for manner in manner_enc.values():
        for v in range(2):
            vow = Consonant(((part, manner, v), (0, 0, 0)), 0, ipa)
            print(vow.ipa, vow.features, sep='\t')
