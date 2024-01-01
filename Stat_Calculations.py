from FE4_Stats import *
from math import floor
from random import randint

def PAR_HP_add(parent):
    return max(parent.HP - 20, 0)

def PAR_Lck_add(parent):
    return parent.Lck

# Non-HP/Lck Stat Additions
def PAR_stat_add(parent_stat, base_stat):
    return max(parent_stat - base_stat, 0)

def CHLD_HP_add(level, growth):
    return floor(level * growth)

def CHLD_stat_add(level, growth):
    return floor((level - 1) * growth)

def CHLD_start_gold(main_parent_gold, scnd_parent_gold):
    return floor((main_parent_gold + scnd_parent_gold) / 10) + 2000

def CHLD_start_HP(main_parent_add, scnd_parent_add, child_add):
    return floor(((main_parent_add.HP * 2) + (scnd_parent_add.HP)) / 10) + child_add.HP + 20

# Note: Random number is involved with calculation, so this only provides an approximation
def CHLD_start_Lck(main_parent_add_Lck, scnd_parent_add_Lck, child_add_Lck):
    return floor(((main_parent_add_Lck * 2) + (scnd_parent_add_Lck) + randint(1, 100)) / 10) + child_add_Lck + 1

# Non-HP/Lck Starting Stats
def CHLD_start_stat(main_parent_stat_add, scnd_parent_stat_add, child_parent_stat_add, child_base_stat):
    return ((floor(((main_parent_stat_add * 2) + scnd_parent_stat_add) / 10) + child_parent_stat_add) % 15) + child_base_stat

# Calculates all parent additions and returns them in stat struct
def calc_PAR_adds(parent, base_class):
    HP = PAR_HP_add(parent)
    Str = PAR_stat_add(parent.Str, base_class.Str)
    Mag = PAR_stat_add(parent.Mag, base_class.Mag)
    Skl = PAR_stat_add(parent.Skl, base_class.Skl)
    Spd = PAR_stat_add(parent.Spd, base_class.Spd)
    Lck = PAR_Lck_add(parent)
    Def = PAR_stat_add(parent.Def, base_class.Def)
    Mdf = PAR_stat_add(parent.Mdf, base_class.Mdf)
    return Stats(parent.Name, "additions", HP, Str, Mag, Skl, Spd, Lck, Def, Mdf)

# Calculates all child additions and returns them in stat struct
def calc_CHLD_adds(child, father):
    level = starting_levels[child]
    growths = child_growths[child][father]
    HP = CHLD_HP_add(starting_levels[child], growths.HP)
    Str = CHLD_stat_add(level, growths.Str)
    Mag = CHLD_stat_add(level, growths.Mag)
    Skl = CHLD_stat_add(level, growths.Skl)
    Spd = CHLD_stat_add(level, growths.Spd)
    Lck = CHLD_stat_add(level, growths.Lck)
    Def = CHLD_stat_add(level, growths.Def)
    Mdf = CHLD_stat_add(level, growths.Str)
    return Stats(child, "additions", HP, Str, Mag, Skl, Spd, Lck, Def, Mdf)

# Puts all the calcs together to get starting stats
# main parent and second parent are Stats objects with current parent stats
# promoted is 0 for base class, 1 for promoted class 
# child is name of child as string
def calc_start_stats(main_parent, main_promoted, scnd_parent, scnd_promoted, child_name, father_name):
    # Calculate additions for child and main/second parents
    child_adds = calc_CHLD_adds(child_name, father_name)
    main_class = unit_classes[main_parent.Name][main_promoted]
    main_parent_adds = calc_PAR_adds(main_parent, class_bases[main_class])
    scnd_class = unit_classes[scnd_parent.Name][scnd_promoted]
    scnd_parent_adds = calc_PAR_adds(scnd_parent, class_bases[scnd_class])

    # Calculate each stat
    child_bases = class_bases[unit_classes[child_name][0]]
    HP = CHLD_start_HP(main_parent_adds, scnd_parent_adds, child_adds)
    Str = CHLD_start_stat(main_parent_adds.Str, scnd_parent_adds.Str, child_adds.Str, child_bases.Str)
    Mag = CHLD_start_stat(main_parent_adds.Mag, scnd_parent_adds.Mag, child_adds.Mag, child_bases.Mag)
    Skl = CHLD_start_stat(main_parent_adds.Skl, scnd_parent_adds.Skl, child_adds.Skl, child_bases.Skl)
    Spd = CHLD_start_stat(main_parent_adds.Spd, scnd_parent_adds.Spd, child_adds.Spd, child_bases.Spd)
    Lck = CHLD_start_Lck(main_parent_adds.Lck, scnd_parent_adds.Lck, child_adds.Lck)
    Def = CHLD_start_stat(main_parent_adds.Def, scnd_parent_adds.Def, child_adds.Def, child_bases.Def)
    Mdf = CHLD_start_stat(main_parent_adds.Mdf, scnd_parent_adds.Mdf, child_adds.Mdf, child_bases.Mdf)
    return Stats(child_name, "child", HP, Str, Mag, Skl, Spd, Lck, Def, Mdf)

def check_valid_stats(stats, max_stats):
    if(
        stats.HP > max_stats.HP     or
        stats.Str > max_stats.Str   or
        stats.Mag > max_stats.Mag   or
        stats.Skl > max_stats.Skl   or
        stats.Spd > max_stats.Spd   or
        stats.Lck > max_stats.Lck   or
        stats.Def > max_stats.Def   or
        stats.Mdf > max_stats.Mdf   ):
            return -1
    return 0

def calc_avg_stats_par(unit, lvl):
    if(lvl >= 20):
        promoted = 1
    else:
        promoted = 0
    base_lvl = starting_levels[unit]
    base_stats = unit_bases[unit]
    stat_caps = max_stats[unit_classes[unit][promoted]]
    growths = parent_growths[unit]

    lvl_diff = lvl - base_lvl
    if(lvl_diff < 1):
        return base_stats   # If unit hasn't leveled at all, return base stats

    # Determine if unit promotes and needs promo bonuses
    if((lvl >= 20) and (unit not in pre_promotes)):
        promo_bonus = promo_bonuses[(unit_classes[unit])]
    else:
        promo_bonus = Stats("", "Promo", 0, 0, 0, 0, 0, 0, 0, 0)

    avg_stats = Stats(
        unit,
        "avg",
        min(base_stats.HP + (lvl_diff*growths.HP) + promo_bonus.HP, stat_caps.HP),
        min(base_stats.Str + (lvl_diff*growths.Str) + promo_bonus.Str, stat_caps.Str),
        min(base_stats.Mag + (lvl_diff*growths.Mag) + promo_bonus.Mag, stat_caps.Mag),
        min(base_stats.Skl + (lvl_diff*growths.Skl) + promo_bonus.Skl, stat_caps.Skl),
        min(base_stats.Spd + (lvl_diff*growths.Spd) + promo_bonus.Spd, stat_caps.Spd),
        min(base_stats.Lck + (lvl_diff*growths.Lck) + promo_bonus.Lck, stat_caps.Lck),
        min(base_stats.Def + (lvl_diff*growths.Def) + promo_bonus.Def, stat_caps.Def),
        min(base_stats.Mdf + (lvl_diff*growths.Mdf) + promo_bonus.Mdf, stat_caps.Mdf),
    )
    return avg_stats