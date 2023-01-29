import random

biome = [0]


while len(biome) < 8:
    biomenum = random.randrange(1,8)
    if biomenum not in biome:
        biome.append(biomenum)

print(biome)