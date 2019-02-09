# 0 - link imagem,
# 1 - nome do monstro,
# 2 - vida do monstro,
# 3 - item para enfrentar,
# 4 - accuracy do monstro
# 5 - evasion do monstro,
# 6 - força do monstro,
# 7 - gold do loot,
# 8 - quantidade da recompença,
# 9 - se o monstro tem bonus ou não
# 10 - defesa do monstro
# 11 - critico do monstro
# 12 - Level do Monstro
# 13 - desesa critica do monstro
# 14 - Loot de itens para dropar
# 15 - hability Monster
# 16 - azar do loot
# 17 - XP
# 18 - Lucky


monster_1 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487582894638891020/t.g._wonder_magician.jpg',
             'Wonder', 1100, 'Pedra_Runica', 10, 15, 15, 250, 5, False, 30, 5, 1, 5, ['Ficha', 'Energia',
                                                                                      'Energia_Concentrada'],
             0, 20, 100, 5],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487582898233278464/doomstar_magician.jpg',
             'Doomstar', 1200, 'Pedra_Runica', 11, 16, 20, 300, 6, False, 35, 6, 2, 5, ['Ficha', 'Energia',
                                                                                        'Energia_Concentrada'],
             0, 20, 100, 6],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487583160838651904/sorciere_de_fleur.jpg',
             'Sorciere', 1300, 'Pedra_Runica', 12, 17, 25, 350, 7, False, 45, 7, 3, 10, ['Ficha', 'Energia',
                                                                                         'Energia_Concentrada'],
             0, 20, 100, 7],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487583170129297408/downerd_magician.png',
             'Downerd', 1400, 'Pedra_Runica', 13, 18, 30, 400, 8, False, 50, 8, 4, 10, ['Ficha', 'Energia',
                                                                                        'Energia_Concentrada'],
             0, 20, 100, 8],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487583547876704256/endymion_the_'
             'master_magician.jpg', 'Endymion', 1500, 'Pedra_Runica', 14, 19, 35, 450, 9, False, 55, 9, 5, 15,
             ['Ficha', 'Energia', 'Energia_Concentrada'], 0, 20, 100, 9],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487583552469467146/arcanite_magician.png',
             'Arcanite', 1600, 'Pedra_Runica', 15, 20, 40, 500, 10, False, 60, 10, 6, 15,
             ['Ficha', 'Energia', 'Energia_Concentrada'], 0, 20, 100, 10]
            ]

monster_2 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487584141324582933/dragon_horn_hunter.png',
             'Horn', 2100, 'Pedra_Runica', 16, 21, 55, 550, 11, True, 65, 11, 13, 20,
             ['Energia_Concentrada', 'Energia', 'Augur'], 0, 25, 150, 11],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487584123884535819/subterror_guru.png',
             'Guru', 2200, 'Pedra_Runica', 17, 22, 60, 600, 12, False, 70, 12, 14, 20,
             ['Energia_Concentrada', 'Energia', 'Blazing'], 0, 25, 150, 12],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487584434489524226/Chaos_Hunter.png',
             'Chaos', 2300, 'Pedra_Runica', 18, 23, 65, 650, 13, True, 75, 13, 15, 25,
             ['Energia_Concentrada', 'Energia', 'Heavenly'], 0, 25, 150, 13],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487584451543564298/subterror_fiendess.png',
             'Fiendess', 2400, 'Pedra_Runica', 19, 24, 70, 700, 14, False, 80, 14, 16, 25,
             ['Energia_Concentrada', 'Energia', 'Hurricane'], 0, 25, 150, 14],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487584691365478420/subterror_behemoth_'
             'speleogeist.png', 'Behemoth Speleogeist', 2500, 'Pedra_Runica', 20, 25, 75, 17, 15, True, 85, 15, 17, 30,
             ['Energia_Concentrada', 'Energia', 'Surpassing'], 0, 25, 150, 15],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487584670473781269/woodland_archer.png',
             'Woodland', 2600, 'Pedra_Runica', 21, 26, 80, 800, 16, False, 90, 16, 18, 30,
             ['Energia_Concentrada', 'Energia', 'Unearthly'], 0, 25, 150, 16]
            ]

monster_3 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487586695538147349/Vylon_Vanguard.png',
             'Vylon Vanguard', 1600, 'Pedra_Runica', 22, 27, 100, 850, 17, False, 95, 17, 25, 35,
             ['Energia_Concentrada', 'Energia_Concentrada', 'Augur'], 0, 30, 200, 17],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487586702253359104/vylon_ohm.jpg',
             'Vylon Ohm', 1700, 'Pedra_Runica', 23, 28, 105, 900, 18, True, 100, 18, 26, 35,
             ['Energia_Concentrada', 'Energia_Concentrada', 'Blazing'], 0, 30, 200, 18],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487587520322994196/Shaddoll_Zefracore.png',
             'Shaddoll Zefracore', 1800, 'Pedra_Runica', 24, 29, 110, 950, 19, False, 105, 19, 27, 40,
             ['Energia_Concentrada', 'Energia_Concentrada', 'Heavenly'], 0, 30, 200, 19],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487587530456301598/Zefraath.png', 'Zefraath',
             1900, 'Pedra_Runica', 25, 30, 115, 100, 20, True, 110, 20, 28, 40,
             ['Energia_Concentrada', 'Energia_Concentrada', 'Hurricane'], 0, 30, 200, 20],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487587790805139466/shaddoll_zefranaga.jpg',
             'Shaddoll Zefranaga', 2000, 'Pedra_Runica', 26, 31, 120, 1050, 21, False, 115, 21, 29, 45,
             ['Energia_Concentrada', 'Energia_Concentrada', 'Surpassing'], 0, 30, 200, 21],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487587785214001152/Vylon_Omega.png',
             'Vylon Omega', 2100, 'Pedra_Runica', 27, 32, 125, 1100, 22, True, 120, 22, 30, 45,
             ['Energia_Concentrada', 'Energia_Concentrada', 'Unearthly'], 0, 30, 200, 22]
            ]

monster_4 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487588431732670471/infernity_beast.jpg',
             'Infernity Beast', 2600, 'Pedra_Runica', 28, 33, 150, 1150, 23, True, 125, 23, 37, 50,
             ['Augur', 'Blazing', 'Heavenly'], 0, 35, 250, 23],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487588459993759754/piercing_moray.jpg',
             'Piercing Moray', 2700, 'Pedra_Runica', 29, 34, 155, 1200, 24, False, 130, 24, 38, 50,
             ['Hurricane', 'Surpassing', 'Unearthly'], 0, 35, 250, 24],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487588397116948490/Beiige__'
             'Vanguard_of_Dark_World.jpg', 'Beiige Vanguard', 2800, 'Pedra_Runica', 30, 35, 160, 1250, 25, True,
             135, 25, 39, 55, ['Augur', 'Blazing', 'Unearthly'], 0, 35, 250, 25],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487588460904054784/sea_monster_of_theseus_'
             'by_yugi_master-dbi0lgh.png', 'Theseus', 2900, 'Pedra_Runica', 31, 36, 165, 1300, 26, False, 140, 26,
             40, 55, ['Surpassing', 'Heavenly', 'Blazing'], 0, 35, 250, 26],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487588444374040596/ocean_dragon_'
             'lord_daedalus.jpg', 'Daedalus', 3000, 'Pedra_Runica', 32, 37, 170, 1350, 27, True, 145, 27,
             41, 60, ['Blazing', 'Surpassing', 'Heavenly'], 0, 35, 250, 27],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487588419472588810/great_maju_garzett.jpg',
             'Maju Garzett', 3100, 'Pedra_Runica', 33, 38, 175, 1400, 28, False, 150, 28, 42, 60,
             ['Augur', 'Hurricane', 'Unearthly'], 0, 35, 250, 28]
            ]

monster_5 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487597258116956160/Volcanic_Counter.jpg',
             'Volcanic Counter', 3100, 'Pedra_Runica', 34, 39, 200, 1450, 29, False, 155, 29, 49, 65,
             ['Augur', 'Blazing', 'Heavenly'], 0, 40, 300, 29],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487597265482022922/soaring_eagle_above_'
             'the_searing_land.jpg', 'Soaring Eagle', 3200, 'Pedra_Runica', 35, 40, 205, 1500, 30, True,
             160, 30, 50, 65, ['Augur', 'Blazing', 'Heavenly'], 0, 40, 300, 30],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487597433145262081/Ancient_Flamvell_'
             'Deity.png', 'Flamvell Deity', 3300, 'Pedra_Runica', 36, 41, 210, 1550, 31, False, 165, 31, 51, 70,
             ['Augur', 'Blazing', 'Heavenly'], 0, 40, 300, 31],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487597446705446912/lavalval_chain.png',
             'Lavalval Chain', 3400, 'Pedra_Runica', 37, 42, 215, 1600, 32, True, 170, 32, 52, 70,
             ['Augur', 'Blazing', 'Heavenly'], 0, 40, 300, 32],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487597658807205890/volcanic_doomfire.jpg',
             'Doomfire', 3500, 'Pedra_Runica', 38, 43, 220, 1650, 33, False, 175, 33, 53, 75,
             ['Augur', 'Blazing', 'Heavenly'], 0, 40, 300, 33],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487597653954396180/mariamne__'
             'the_true_dracophenix.jpg', 'Mariamne', 3600, 'Pedra_Runica', 39, 44, 225, 1700, 34, True,
             180, 34, 54, 75, ['Augur', 'Blazing', 'Heavenly'], 0, 40, 300, 34]
            ]

monster_6 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487598395180056596/predaplant_pterapenthes.'
             'png', 'Pterapenthes', 4100, 'Pedra_Runica', 40, 45, 250, 1750, 35, True, 185, 35, 61, 80,
             ['Hurricane', 'Surpassing', 'Unearthly'], 0, 45, 350, 35],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487598403782443028/seed_of_flame.jpg',
             'Seed of Flame', 4200, 'Pedra_Runica', 41, 46, 255, 1800, 36, False, 190, 36, 62, 80,
             ['Hurricane', 'Surpassing', 'Unearthly'], 0, 45, 350, 36],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487598600109424640/Gigaplant.jpg',
             'Gigaplant', 4300, 'Pedra_Runica', 42, 47, 260, 1850, 37, True, 195, 37, 63, 85,
             ['Hurricane', 'Surpassing', 'Unearthly'], 0, 45, 350, 37],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487598604396265492/Orea_the_Sylvan_'
             'High_Arbiter.jpg', 'Orea', 4400, 'Pedra_Runica', 43, 48, 265, 1900, 38, False, 200, 38, 64, 85,
             ['Hurricane', 'Surpassing', 'Unearthly'], 0, 45, 350, 38],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487598746717126656/Alsei_the_Sylvan_'
             'High_Protector.jpg', 'Alsei', 4500, 'Pedra_Runica', 44, 49, 270, 1950, 39, True, 205, 39, 65, 90,
             ['Hurricane', 'Surpassing', 'Unearthly'], 0, 45, 350, 39],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487598754497560599/leo__the_keeper_of_'
             'the_sacred_tree.png', 'Leo', 4600, 'Pedra_Runica', 45, 50, 275, 2000, 40, False, 210, 40, 66, 90,
             ['Hurricane', 'Surpassing', 'Unearthly'], 0, 45, 350, 40]
            ]

monster_7 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487599851920687104/gem-knight_sardonyx.png',
             'Sardonyx', 3600, 'Pedra_Runica', 46, 51, 300, 2050, 41, False, 215, 41, 73, 95,
             ['Augur', 'Heavenly', 'Hurricane', 'Unearthly'], 0, 50, 400, 41],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487599835290271754/gem-knight_iolite.png',
             'Iolite', 3700, 'Pedra_Runica', 47, 52, 305, 2100, 42, True, 220, 42, 74, 95,
             ['Augur', 'Heavenly', 'Hurricane', 'Unearthly'], 0, 50, 400, 42],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487599816440938497/diamond_direwolf.jpg',
             'Diamond Direwolf', 3800, 'Pedra_Runica', 48, 53, 310, 2150, 43, False, 225, 43, 75, 100,
             ['Augur', 'Heavenly', 'Hurricane', 'Unearthly'], 0, 50, 400, 43],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487599786208395281/number_52__'
             'diamond_crab_king.png', 'Crab King', 3900, 'Pedra_Runica', 49, 54, 315, 2200, 44, True, 230, 44,
             76, 100, ['Augur', 'Heavenly', 'Hurricane', 'Unearthly'], 0, 50, 400, 44],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487599803224817666/cairngorgon_'
             'antiluminescent_knight.png', 'Cairngorgon', 4000, 'Pedra_Runica', 50, 55, 320, 2250, 45, False,
             235, 45, 77, 105, ['Augur', 'Heavenly', 'Hurricane', 'Unearthly'], 0, 50, 400, 45],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487599769032720385/Gem-Knight_Master_'
             'Diamond.png', 'Master Diamond', 4100, 'Pedra_Runica', 51, 56, 325, 2300, 46, True, 240, 46, 78, 105,
             ['Augur', 'Heavenly', 'Hurricane', 'Unearthly'], 0, 50, 400, 46]
            ]

monster_8 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487600708951212037/defender_of_the_'
             'ice_barrier.jpg', 'Defender', 4600, 'Pedra_Runica', 52, 57, 350, 2350, 47, True, 245, 47, 85, 110,
             ['Augur', 'Blazing', 'Heavenly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 55, 450, 47],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487600727573790720/Dewloren_Tiger_'
             'King_of_the_Ice_Barrier.png', 'Dewloren Tiger King', 4700, 'Pedra_Runica', 53, 58, 355, 2400, 48, False,
             250, 48, 86, 110, ['Augur', 'Blazing', 'Heavenly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 55, 450, 48],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487600671592415233/Samurai_of_the_Ice_'
             'Barrier.png', 'Samurai', 4800, 'Pedra_Runica', 54, 59, 360, 2450, 49, True, 255, 49, 87, 115,
             ['Augur', 'Blazing', 'Heavenly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 55, 450, 49],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487600694275211264/Dai_sojo_of_the_Ice_'
             'Barrier.jpg', 'Dai Sojo', 4900, 'Pedra_Runica', 55, 60, 365, 2500, 50, False, 260, 50, 88, 115,
             ['Augur', 'Blazing', 'Heavenly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 55, 450, 50],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487600682526965761/brionac_dragon_of_the_'
             'ice_barrier.jpg', 'Brionac', 5000, 'Pedra_Runica', 56, 61, 370, 2550, 51, True, 265, 55, 89, 120,
             ['Augur', 'Blazing', 'Heavenly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 55, 450, 51],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487600654731313174/gungnir_dragon_of_the_'
             'ice_barrier.jpg', 'Gungnir', 5100, 'Pedra_Runica', 57, 62, 375, 2600, 52, False, 270, 60, 90, 120,
             ['Augur', 'Blazing', 'Heavenly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 55, 450, 52]
            ]

monster_9 = [
            ['https://cdn.discordapp.com/attachments/421862394491437057/487601618536366080/levionia_the_primordial_'
             'chaos_dragon.png', 'Levionia', 5100, 'Pedra_Runica', 58, 63, 400, 2650, 53, False, 275, 61, 97, 125,
             ['Hurricane', 'Surpassing', 'Unearthly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 60, 500, 53],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487601602459598858/ignister_prominence_the_'
             'blasting_dracoslayer.jpg', 'Ignister Prominence', 5200, 'Pedra_Runica', 59, 64, 405, 2700,
             54, True, 280, 62, 98, 125, ['Hurricane', 'Surpassing', 'Unearthly', 'Obsidian', 'Oricalco_Liquefeito'],
             0, 60, 500, 54],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487601568900972544/vandalgyon_the_dark_'
             'dragon_lord.jpg', 'Vandalgyon', 5300, 'Pedra_Runica', 60, 65, 410, 2750, 55, False, 285, 63, 99, 130,
             ['Hurricane', 'Surpassing', 'Unearthly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 60, 500, 55],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487601562642939906/tyrant_red_dragon_'
             'archfiend.jpg', 'Tyrant Red Dragon', 5400, 'Pedra_Runica', 61, 66, 415, 2800, 56, True, 290, 64,
             100, 130, ['Hurricane', 'Surpassing', 'Unearthly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 60, 500, 56],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487601592108056586/hot_red_dragon_'
             'archfiend_king_calamity.png', 'Hot Red Dragon', 5500, 'Pedra_Runica', 62, 67, 420, 2850, 57, False, 295,
             65, 101, 135, ['Hurricane', 'Surpassing', 'Unearthly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 60, 500, 57],
            ['https://cdn.discordapp.com/attachments/421862394491437057/487601577897754634/hot_red_dragon_'
             'archfiend_bane.jpg', 'Red Dragon Archfiend', 5600, 'Pedra_Runica', 63, 68, 425, 2900, 58, True, 300,
             66, 102, 135, ['Hurricane', 'Surpassing', 'Unearthly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 60, 500, 58]
            ]

monster_10 = [
             ['https://cdn.discordapp.com/attachments/421862394491437057/487709114353451008/number_98__antitopian.png',
              'Antitopian', 5700, 'Pedra_Runica', 64, 69, 450, 2950, 59, True, 305, 5, 109, 140,
              ['Augur', 'Blazing', 'Heavenly', 'Hurricane', 'Surpassing', 'Unearthly', 'Obsidian',
               'Oricalco_Liquefeito'], 0, 65, 550, 59],
             ['https://cdn.discordapp.com/attachments/421862394491437057/487709097072787457/Dark_General_Freed.png',
              'General Freed', 5800, 'Pedra_Runica', 65, 70, 460, 3000, 60, False, 310, 5, 110, 140,
              ['Augur', 'Blazing', 'Heavenly', 'Hurricane', 'Surpassing', 'Unearthly', 'Obsidian',
               'Oricalco_Liquefeito'], 0, 65, 550, 60],
             ['https://cdn.discordapp.com/attachments/421862394491437057/487709080379588608/dark_flare_knight.jpg',
              'Flare Knight', 5900, 'Pedra_Runica', 66, 71, 470, 3050, 61, True, 45, 315, 111, 145,
              ['Augur', 'Blazing', 'Heavenly', 'Hurricane', 'Surpassing', 'Unearthly', 'Obsidian',
               'Oricalco_Liquefeito'], 0, 65, 550, 61],
             ['https://cdn.discordapp.com/attachments/421862394491437057/487709069327466496/dark_crusader.jpg',
              'Dark Crusader', 6000, 'Pedra_Runica', 67, 72, 480, 3100, 62, False, 30, 320, 112, 145,
              ['Augur', 'Blazing', 'Heavenly', 'Hurricane', 'Surpassing', 'Unearthly', 'Obsidian',
               'Oricalco_Liquefeito'], 0, 65, 550, 62],
             ['https://cdn.discordapp.com/attachments/421862394491437057/487709061840896000/crimson_knight_'
              'vampire_bram.png', 'Crimson Knight', 6100, 'Pedra_Runica', 68, 73, 490, 3150, 63, True, 45, 325,
              113, 150, ['Augur', 'Blazing', 'Heavenly', 'Hurricane', 'Surpassing', 'Unearthly', 'Obsidian',
                         'Oricalco_Liquefeito'], 0, 65, 550, 63],
             ['https://cdn.discordapp.com/attachments/421862394491437057/487709044744912898/black_luster_soldier_'
              'envoy_of_the_evening_twilight.png', 'Black Luster Evening Twilight', 6200, 'Pedra_Runica', 69, 74,
              500, 3200, 64, False, 45, 330, 114, 150, ['Augur', 'Blazing', 'Heavenly', 'Hurricane', 'Surpassing',
                                                        'Unearthly', 'Obsidian', 'Oricalco_Liquefeito'], 0, 65, 550, 64]
             ]


ataque_mob_1 = [['Ataque Comum', 'Perfurada', 'Veneno', 'Massivo', 'Avalanche', 'Recuperação'],
                ['Ataque Comum', 'Perfurada', 'Veneno', 'Massivo', 'Avalanche', 'Recuperação'],
                ['Ataque Comum', 'Perfurada', 'Veneno', 'Massivo', 'Avalanche', 'Recuperação'],
                ['Ataque Comum', 'Perfurada', 'Veneno', 'Massivo', 'Avalanche', 'Recuperação'],
                ['Ataque Comum', 'Perfurada', 'Veneno', 'Massivo', 'Avalanche', 'Recuperação'],
                ['Ataque Comum', 'Perfurada', 'Veneno', 'Massivo', 'Avalanche', 'Recuperação']]

ataque_mob_2 = [['Ataque Direto', 'Destruição', 'Poison', 'Dano Estelar', 'Ultimate', 'Recuperação'],
                ['Ataque Direto', 'Destruição', 'Poison', 'Dano Estelar', 'Ultimate', 'Recuperação'],
                ['Ataque Direto', 'Destruição', 'Poison', 'Dano Estelar', 'Ultimate', 'Recuperação'],
                ['Ataque Direto', 'Destruição', 'Poison', 'Dano Estelar', 'Ultimate', 'Recuperação'],
                ['Ataque Direto', 'Destruição', 'Poison', 'Dano Estelar', 'Ultimate', 'Recuperação'],
                ['Ataque Direto', 'Destruição', 'Poison', 'Dano Estelar', 'Ultimate', 'Recuperação']]

ataque_mob_3 = [['Ataque Rasteiro', 'Explosão', 'Escoamento', 'Dano Majestral', 'Super Nova', 'Recuperação'],
                ['Ataque Rasteiro', 'Explosão', 'Escoamento', 'Dano Majestral', 'Super Nova', 'Recuperação'],
                ['Ataque Rasteiro', 'Explosão', 'Escoamento', 'Dano Majestral', 'Super Nova', 'Recuperação'],
                ['Ataque Rasteiro', 'Explosão', 'Escoamento', 'Dano Majestral', 'Super Nova', 'Recuperação'],
                ['Ataque Rasteiro', 'Explosão', 'Escoamento', 'Dano Majestral', 'Super Nova', 'Recuperação'],
                ['Ataque Rasteiro', 'Explosão', 'Escoamento', 'Dano Majestral', 'Super Nova', 'Recuperação']]

ataque_mob_4 = [['Ataque Perfurante', 'Penetrante', 'Envenenamento', 'Dano Massivo', 'Portao Infernal', 'Recuperação'],
                ['Ataque Perfurante', 'Penetrante', 'Envenenamento', 'Dano Massivo', 'Portao Infernal', 'Recuperação'],
                ['Ataque Perfurante', 'Penetrante', 'Envenenamento', 'Dano Massivo', 'Portao Infernal', 'Recuperação'],
                ['Ataque Perfurante', 'Penetrante', 'Envenenamento', 'Dano Massivo', 'Portao Infernal', 'Recuperação'],
                ['Ataque Perfurante', 'Penetrante', 'Envenenamento', 'Dano Massivo', 'Portao Infernal', 'Recuperação'],
                ['Ataque Perfurante', 'Penetrante', 'Envenenamento', 'Dano Massivo', 'Portao Infernal', 'Recuperação']]

ataque_mob_5 = [['Ataque Dizimante', 'Rajada', 'Conropimento', 'Dano Sombrio', 'Grande Massivo', 'Recuperação'],
                ['Ataque Dizimante', 'Rajada', 'Conropimento', 'Dano Sombrio', 'Grande Massivo', 'Recuperação'],
                ['Ataque Dizimante', 'Rajada', 'Conropimento', 'Dano Sombrio', 'Grande Massivo', 'Recuperação'],
                ['Ataque Dizimante', 'Rajada', 'Conropimento', 'Dano Sombrio', 'Grande Massivo', 'Recuperação'],
                ['Ataque Dizimante', 'Rajada', 'Conropimento', 'Dano Sombrio', 'Grande Massivo', 'Recuperação'],
                ['Ataque Dizimante', 'Rajada', 'Conropimento', 'Dano Sombrio', 'Grande Massivo', 'Recuperação']]

ataque_mob_6 = [['Ataque Galaxy', 'Lamina Afiada', 'Sangria', 'Dano de Luz', 'Dizimador', 'Recuperação'],
                ['Ataque Galaxy', 'Lamina Afiada', 'Sangria', 'Dano de Luz', 'Dizimador', 'Recuperação'],
                ['Ataque Galaxy', 'Lamina Afiada', 'Sangria', 'Dano de Luz', 'Dizimador', 'Recuperação'],
                ['Ataque Galaxy', 'Lamina Afiada', 'Sangria', 'Dano de Luz', 'Dizimador', 'Recuperação'],
                ['Ataque Galaxy', 'Lamina Afiada', 'Sangria', 'Dano de Luz', 'Dizimador', 'Recuperação'],
                ['Ataque Galaxy', 'Lamina Afiada', 'Sangria', 'Dano de Luz', 'Dizimador', 'Recuperação']]

ataque_mob_7 = [['Ataque Ancestral', 'Luz Divina', 'Intravenosa', 'Dano Maligno', 'Ataque Final', 'Recuperação'],
                ['Ataque Ancestral', 'Luz Divina', 'Intravenosa', 'Dano Maligno', 'Ataque Final', 'Recuperação'],
                ['Ataque Ancestral', 'Luz Divina', 'Intravenosa', 'Dano Maligno', 'Ataque Final', 'Recuperação'],
                ['Ataque Ancestral', 'Luz Divina', 'Intravenosa', 'Dano Maligno', 'Ataque Final', 'Recuperação'],
                ['Ataque Ancestral', 'Luz Divina', 'Intravenosa', 'Dano Maligno', 'Ataque Final', 'Recuperação'],
                ['Ataque Ancestral', 'Luz Divina', 'Intravenosa', 'Dano Maligno', 'Ataque Final', 'Recuperação']]

ataque_mob_8 = [['Ataque do Submundo', 'Sombras', 'Feitiçaria', 'Dano Pesado', 'Ultimo Recurso', 'Recuperação'],
                ['Ataque do Submundo', 'Sombras', 'Feitiçaria', 'Dano Pesado', 'Ultimo Recurso', 'Recuperação'],
                ['Ataque do Submundo', 'Sombras', 'Feitiçaria', 'Dano Pesado', 'Ultimo Recurso', 'Recuperação'],
                ['Ataque do Submundo', 'Sombras', 'Feitiçaria', 'Dano Pesado', 'Ultimo Recurso', 'Recuperação'],
                ['Ataque do Submundo', 'Sombras', 'Feitiçaria', 'Dano Pesado', 'Ultimo Recurso', 'Recuperação'],
                ['Ataque do Submundo', 'Sombras', 'Feitiçaria', 'Dano Pesado', 'Ultimo Recurso', 'Recuperação']]

ataque_mob_9 = [['Ataque Divino', 'Planada', 'Corte Exposto', 'Dano Pesado', 'Nuclear', 'Recuperação'],
                ['Ataque Divino', 'Planada', 'Corte Exposto', 'Dano Pesado', 'Nuclear', 'Recuperação'],
                ['Ataque Divino', 'Planada', 'Corte Exposto', 'Dano Pesado', 'Nuclear', 'Recuperação'],
                ['Ataque Divino', 'Planada', 'Corte Exposto', 'Dano Pesado', 'Nuclear', 'Recuperação'],
                ['Ataque Divino', 'Planada', 'Corte Exposto', 'Dano Pesado', 'Nuclear', 'Recuperação'],
                ['Ataque Divino', 'Planada', 'Corte Exposto', 'Dano Pesado', 'Nuclear', 'Recuperação']]

ataque_mob_10 = [['Ataque Colossal', 'Mão Divina', 'Enfermo', 'Dano Majestico', 'Criação', 'Recuperação'],
                 ['Ataque Colossal', 'Mão Divina', 'Enfermo', 'Dano Majestico', 'Criação', 'Recuperação'],
                 ['Ataque Colossal', 'Mão Divina', 'Enfermo', 'Dano Majestico', 'Criação', 'Recuperação'],
                 ['Ataque Colossal', 'Mão Divina', 'Enfermo', 'Dano Majestico', 'Criação', 'Recuperação'],
                 ['Ataque Colossal', 'Mão Divina', 'Enfermo', 'Dano Majestico', 'Criação', 'Recuperação'],
                 ['Ataque Colossal', 'Mão Divina', 'Enfermo', 'Dano Majestico', 'Criação', 'Recuperação']]


respostas_1 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de Vossa '
                                                                      'Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...',
               'Parece que essa armadura te deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?',
               'Nada demais...', 'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_2 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!',
               'Aaaaaa! Como esperado da força de Vossa Excelencia!', 'Eu ainda estou de pé...', 'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...',
               'Parece que essa armadura te deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_3 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de '
                                                                      'Vossa Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...', 'Parece que essa armadura te '
                                                                                    'deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_4 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de '
                                                                      'Vossa Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...',
               'Parece que essa armadura te deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_5 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de '
                                                                      'Vossa Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...',
               'Parece que essa armadura te deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_6 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de '
                                                                      'Vossa Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...', 'Parece que essa armadura te '
                                                                                    'deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_7 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de Vossa '
                                                                      'Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...', 'Parece que essa armadura '
                                                                                    'te deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_8 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de Vossa '
                                                                      'Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...', 'Parece que essa armadura te '
                                                                                    'deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_9 = [
              ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
               'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
              ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
              ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de Vossa '
                                                                      'Excelencia!', 'Eu ainda estou de pé...',
               'Eu... acertei?'],
              ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...', 'Parece que essa armadura '
                                                                                    'te deixa mais lento'],
              ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
               'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
              ]

respostas_10 = [
               ['Então você acha mesmo que pode me vencer? Cai dentro fracote. Vou até te deixar começar.',
                'Ja vi galinhas mais fortes que isso!', 'Apenas um arranhão', 'LENTOOOOO!'],
               ['Hum... um capitão é? Isso vai ser interessante...', 'Nem doeu...', 'Ok essa doeu', 'Te acertei!'],
               ['Vossa excelencia veio me enfrentar? Será uma honra!', 'Aaaaaa! Como esperado da força de Vossa '
                                                                       'Excelencia!', 'Eu ainda estou de pé...',
                'Eu... acertei?'],
               ['UM GENERAL?!?! pra que tudo isso...', 'Ei vai com calma.', 'ai...', 'Parece que essa armadura te '
                                                                                     'deixa mais lento'],
               ['Um Tenente? O que um subordinado dos capitães faz aqui? Ta perdido?', 'Nada demais...',
                'Até que pra um tenente você é forte...', 'Desceu até aqui pra apanhar!']
               ]


ataque_jogador = [
                 ['Investida', 'Ataque Direto', 'Stun', 'Poison', 'Energia Concentrada'],
                 ['Investida', 'Ataque Direto', 'Stun', 'Poison', 'Energia Concentrada', 'Recuperação'],
                 ['Investida', 'Ataque Direto', 'Stun', 'Poison', 'Energia Concentrada', 'Ultimate'],
                 ['Investida', 'Ataque Direto', 'Stun', 'Poison', 'Energia Concentrada', 'Recuperação', 'Ultimate']
                 ]


API_USER = 'http://api.typheus.me:1996/user/370680094533877763/{}'


corlista = [0xFF0000, 0x01DF01, 0xDF7401, 0xFFFF00, 0x4B088A, 0x0080FF,
            0xFDFBFB, 0x000000, 0xFE2EF7, 0x58D3F7, 0x6E6E6E]


cor_vida = [0x610B0B, 0xAEB404, 0x0B3B0B]


# LISTAS DE PREMIOS
PREMIOS = ['rp!giveitem Coin_de_Bronze {} {}',
           'rp!giveitem Coin_de_Prata {} {}',
           'rp!giveitem Coin_de_Ouro {} {}',
           'rp!giveitem Coin_de_Diamante {} {}',
           'rp!giveitem Coin_de_Esmeralda {} {}',
           'rp!giveitem Coin_de_Platina {} {}',
           'rp!giveitem Coin_de_Safira {} {}',
           'rp!giveitem Coin_de_Ruby {} {}']


# LISTAS DE PROVINCIAS
PROVINCIAS = [450797705703325697,
              450797734161678346,
              450797761479311380,
              450797785348964363,
              450797804894552086,
              450797826268463124,
              450797864151547914,
              450797881780076545,
              450797900973473814,
              450797921718501377]
