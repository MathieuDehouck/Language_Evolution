"""
some testing of the IPA and phonemes
"""

from IPA import IPA
from Phoneme import Vowel, Consonant

ipa = IPA.get_IPA()
print(ipa.vfeatures)
#for k, v in ipa.feat2ipa.items():
#    print(v, k)


# when creating phonemes we can give whatever string so maybe we should not ??

fts =  (0, 0, 0), (1, 0)
phon = Vowel(fts)
ch = ipa.get_char(phon)
print(ch, fts)


fts =  (0, 0, 1), (0, 1)
phon = Vowel(fts)
ch = ipa.get_char(phon)
print(ch, fts)



print(ipa.cfeatures)
fts =  (11, (0, 1, 0, 0, 0), 1), (0, 0, 0)
phon = Consonant(fts)
ch = ipa.get_char(phon)
print(ch, fts)


fts =  (11, (0, 1, 0, 0, 0), 0), (0, 1, 0)
phon = Consonant(fts)
ch = ipa.get_char(phon)
print(ch, fts)


fts =  (11, (0, 1, 0, 0, 0), 0), (11, 1, 0)
phon = Consonant(fts)
ch = ipa.get_char(phon)
print(ch, fts)


fts = (11, (1, 1, 0, 1, 0), 1), (0, 0, 0)
phon = Consonant(fts)
ch = ipa.get_char(phon)
print(ch, fts)
