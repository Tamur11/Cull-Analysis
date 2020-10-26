import csv

# get user input
cull_user = input("Please input name of cull champion: ").title()
abs_focus = input("Absolute Focus? Boolean input: ").title() == "True"
num_adaptive = int(input("How many adaptive runes did you take: "))
adc = input("Please input enemy adc: ").title()
support = input("Please input enemy support: ").title()

# filter values from csv
with open('champion statistics 10_26_2020.csv') as csv:
    rows = [line.split(',') for line in csv.readlines()]
    
    for line in rows:
        if line[0] == cull_user: cull_user_stats = line
        if line[0] == adc: adc_stats = line
        if line[0] == support: support_stats = line

# parse results
hp_cull_user = float(cull_user_stats[1])
hp_scale_cull_user = float(cull_user_stats[2])
ad_cull_user = float(cull_user_stats[9]) + (num_adaptive*5.4) + 7  # 1 adaptive rune gives 5.4 AD and 7 from Cull
ad_scale_cull_user = float(cull_user_stats[10])

# perform the calculations for enemy botlane
for i in range(0, 2):
    if i == 0:
        hp_target = float(adc_stats[1]) + 80  # we assume they take shield or blade
        hp_scale_target = float(adc_stats[2])
        armor_target = float(adc_stats[13]) + 6  # we assume one armor rune
        armor_scale_target = float(adc_stats[14])
        print("\nVersus " + adc + ":")
    else:
        if float(support_stats[18]) > 300:  # we use champion range to determine support item
            hp_target = float(support_stats[1]) + 10
        else:
            hp_target = float(support_stats[1]) + 30
        hp_scale_target = float(support_stats[2])
        armor_target = float(support_stats[13]) + 6  # we assume one armor rune
        armor_scale_target = float(support_stats[14])
        print("Versus " + support + ":")

    for level in range(0, 18):  # calculate for levels 1-18
        actual_hp_cull_user = hp_cull_user + (level*hp_scale_cull_user)
        actual_hp_target = hp_target + (level*hp_scale_target)
        if abs_focus:
            actual_ad_cull_user = ad_cull_user + (level*ad_scale_cull_user) + (0.847+(0.953*(level+1)))
        else:
            actual_ad_cull_user = ad_cull_user + (level*ad_scale_cull_user)

        percent_max_hp = (actual_hp_target-actual_hp_cull_user)/actual_hp_cull_user

        bonus_damage = ((percent_max_hp-0.1)*(1/9))+1.05
        if bonus_damage >= 1.05 and bonus_damage <= 1.15:
            damage_being_added = (actual_ad_cull_user*(100/(100+armor_target+(armor_scale_target*level)))*bonus_damage)-\
                actual_ad_cull_user*(100/(100+armor_target+(armor_scale_target*level)))
            print("At level " +str(level+1) + " adding " + str(damage_being_added) + " damage.")
            seven_ad_as_damage = 7*(100/(100+armor_target+(armor_scale_target*level)))
            print("Dorans' '7 AD' would be doing " + str(seven_ad_as_damage) + " damage.")
            if damage_being_added > seven_ad_as_damage:
                print("Cull is worth it.")
            print("")
        if bonus_damage > 1.15:
            damage_being_added = actual_ad_cull_user*1.15
