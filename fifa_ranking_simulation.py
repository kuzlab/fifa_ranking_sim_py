#
'''
Conditions
- all teams have same strength -> Win/Draw/Lose randomly
- 2 continents, one(team0-9) is x1 point, another(team10-19) is x0.86 point
- W-cup is held every 4 years
- frendly matches (shuffled) are held 15 matches per year
- every 4 years continental qualification 10 matches. it spends 1 year
- simulating 30 years
- ranking is revised every one year
'''
#

import numpy
import random

TEAM_NUM = 20 # number of joining teams
SIM_YEARS = 30 # how many years for simulation
MAX_A_MATCH_PER_YEAR = 15 # maximum A-match days per 1 year

NUM_MATCH_FOR_W_CUP_QUAL = 10 # number of matches for world cup qualification
NUM_MATCH_FOR_W_CUP = 10 # number of matches for world cup qualification

STRONG_CONTINENT = 1
WEAK_CONTINENT = 0.86
#WEAK_CONTINENT = 1

count_total_win_draw_lose = numpy.zeros((TEAM_NUM, 3), dtype = int)
# sum all the way of this simulation

points_history_48m = numpy.zeros((TEAM_NUM, 4*MAX_A_MATCH_PER_YEAR), dtype = float)
# 0 = old, 47 = latest

count_total_win_draw_lose[0:TEAM_NUM, 0:3] = 0
points_history_48m[0:TEAM_NUM, 0:4*MAX_A_MATCH_PER_YEAR] = 0


def print_win_draw_lose():
    print "\nPrint win/draw/lose count\n"
    for i in range(TEAM_NUM):
        print u"Team%d \t win: %d \t draw: %d \t lose: %d" % (i, count_total_win_draw_lose[i, 0], count_total_win_draw_lose[i, 1], count_total_win_draw_lose[i, 2])
        

def print_points_history(team_num):
    print u"\nPrint points history for Team %d\n" % (team_num)
    for j in range(4):
        for i in range(MAX_A_MATCH_PER_YEAR):
            print u"[%d] %d" % (j*MAX_A_MATCH_PER_YEAR+i, points_history_48m[team_num, j*MAX_A_MATCH_PER_YEAR + i])
        print "-----------------------"
    print "< end >"


#print_win_draw_lose()

#for i in range(10):
#    print_points_history(i)

def add_point(team_num, point):
    temp = numpy.zeros((4*MAX_A_MATCH_PER_YEAR), dtype = float)
    
    for i in range(4*MAX_A_MATCH_PER_YEAR):
        temp[i] = points_history_48m[team_num, i]
    
    for i in range(4*MAX_A_MATCH_PER_YEAR-1):
        points_history_48m[team_num, i] = temp[i+1]
    
    points_history_48m[team_num, 4*MAX_A_MATCH_PER_YEAR -1 ] = point


ranking = numpy.zeros((TEAM_NUM, 2))

for i in range(TEAM_NUM):
    ranking[i, 0] = i + 1
    ranking[i, 1] = 0
    
def get_current_rank(team_num):
    return ranking[team_num, 0]
    
def print_current_rank():
    print "\nPrint latest ranking\n"
    i = 1
    while i <= TEAM_NUM:
        for j in range(TEAM_NUM):
            if get_current_rank(j) == i:
                print u"#%d \t Team%d (%d)" % (i, j, ranking[j, 1])
                i += 1

    
continental_point = numpy.zeros(TEAM_NUM)

for i in range(TEAM_NUM/2):
    continental_point[i] = STRONG_CONTINENT
    continental_point[i + TEAM_NUM/2] = WEAK_CONTINENT
    
def get_continental_point(team_num):
    return continental_point[team_num]
    

def cal_match_point(team_num, enemy_team_num, win_draw_lose, match_type):
    if win_draw_lose == "WIN":
        win_point = 3
    elif win_draw_lose == "DRAW":
        win_point = 1
    else:
        win_point = 0
    
    continental_point = (get_continental_point(team_num) + get_continental_point(enemy_team_num))/2
    
    if match_type == "W_CUP":
        match_type_point = 4
    elif match_type == "W_CUP_QUAL":
        match_type_point = 2.5
    else:
        match_type_point = 1
        
    ranking_point = TEAM_NUM - get_current_rank(enemy_team_num)
        
    return win_point * continental_point * match_type_point * ranking_point

#print u"%d" % cal_match_point(1, 2, "WIN", "W_CUP")
#print u"%d" % cal_match_point(1, 2, "DRAW", "W_CUP")
#print u"%d" % cal_match_point(1, 2, "LOSE", "W_CUP")
#print u"%d" % cal_match_point(3, 2, "WIN", "W_CUP")
#print u"%d" % cal_match_point(1, 3, "WIN", "W_CUP")
#print u"%d" % cal_match_point(1, 2, "WIN", "W_CUP_QUAL")
#print u"%d" % cal_match_point(1, 2, "WIN", "FRENDLY")

def cal_rank_point(team_num):
    averages = [0, 0, 0, 0]
    for i in range(MAX_A_MATCH_PER_YEAR):
        for j in range(4):
            averages[j] += points_history_48m[team_num, j*MAX_A_MATCH_PER_YEAR + i]
    
    averages[0] =  averages[0] * 0.2 / MAX_A_MATCH_PER_YEAR
    averages[1] =  averages[1] * 0.3 / MAX_A_MATCH_PER_YEAR
    averages[2] =  averages[2] * 0.5 / MAX_A_MATCH_PER_YEAR
    averages[3] =  averages[3] * 1.0 / MAX_A_MATCH_PER_YEAR
    
    return averages[0] + averages[1] + averages[2] + averages[3]

def update_ranking():
    points = numpy.zeros(TEAM_NUM)
    flags = numpy.zeros(TEAM_NUM)    
    for i in range(TEAM_NUM):
        points[i] = cal_rank_point(i)
        flags[i] = 0
    
    for i in range(TEAM_NUM):
        max_value = 0
        temp = 0
        for j in range(TEAM_NUM):
            if flags[TEAM_NUM - j - 1] == 0:
                if points[TEAM_NUM - j - 1] >= max_value:
                    temp = TEAM_NUM - j - 1
                    max_value = points[TEAM_NUM - j - 1]
                    
        flags[temp] = 1
        ranking[temp, 0] = i + 1
        ranking[temp, 1] = max_value

#for i in range(4*MAX_A_MATCH_PER_YEAR):
#    add_point(1, i*100)
#print_points_history(1)    

def do_matches_and_add_points(matches_team_nums, offset, match_type):
    for i in range(matches_team_nums.size/2):
        temp = random.random()
        home_team_num = matches_team_nums[2*i] + offset
        away_team_num = matches_team_nums[2*i+1] + offset
        
        if temp > 0.66:
            win_draw_lose = "WIN"
            count_total_win_draw_lose[home_team_num, 0] += 1
            count_total_win_draw_lose[away_team_num, 2] += 1
        elif temp > 0.33:
            win_draw_lose = "DRAW"
            count_total_win_draw_lose[home_team_num, 1] += 1
            count_total_win_draw_lose[away_team_num, 1] += 1            
        else:
            win_draw_lose = "LOSE"
            count_total_win_draw_lose[home_team_num, 2] += 1
            count_total_win_draw_lose[away_team_num, 0] += 1            
        
        add_point(home_team_num, cal_match_point(home_team_num, away_team_num, win_draw_lose, match_type))
        add_point(away_team_num, cal_match_point(away_team_num, home_team_num, win_draw_lose, match_type))

def make_match_nums(num_of_teams):
    random_value = numpy.zeros(num_of_teams)
    flags = numpy.zeros(num_of_teams)
    # make matches by random value
    # all team have random value
    # make matches with 1st place and 2nd place, 3rd and 4th, 5th and 6th ....
    matches_team_nums = numpy.zeros(num_of_teams)
    
    for i in range(num_of_teams):
        random_value[i] = random.random()
        flags[i] = 0
    for i in range(num_of_teams):
        max_value = 0
        temp = 0
        for j in range(num_of_teams):
            if flags[j] == 0:
                if random_value[i] > max_value:
                    temp = i
                    max_value = random_value[i]
        flags[temp] = 1
        matches_team_nums[i] = temp
    return matches_team_nums

def match_maker_for_world_cup():
    for i in range(NUM_MATCH_FOR_W_CUP_QUAL):
        do_matches_and_add_points(make_match_nums(TEAM_NUM), 0, "W_CUP")
    
    match_maker_for_usual_year(MAX_A_MATCH_PER_YEAR - NUM_MATCH_FOR_W_CUP)

    
def match_maker_for_world_cup_qualification():
    offset = 0
    for i in range(NUM_MATCH_FOR_W_CUP_QUAL):
        do_matches_and_add_points(make_match_nums(TEAM_NUM/2), offset, "W_CUP_QUAL")
    offset = TEAM_NUM/2
    for i in range(NUM_MATCH_FOR_W_CUP_QUAL):
        do_matches_and_add_points(make_match_nums(TEAM_NUM/2), offset, "W_CUP_QUAL")
    
    match_maker_for_usual_year(MAX_A_MATCH_PER_YEAR - NUM_MATCH_FOR_W_CUP_QUAL)


def match_maker_for_usual_year(max_a_match_per_year):
    for i in range(max_a_match_per_year):
        random_value = numpy.zeros(TEAM_NUM)
        flags = numpy.zeros(TEAM_NUM)
        # make matches by random value
        # all team have random value
        # make matches with 1st place and 2nd place, 3rd and 4th, 5th and 6th ....
        matches_team_nums = numpy.zeros(TEAM_NUM)
        
        for j in range(TEAM_NUM):
            random_value[j] = random.random()
            flags[j] = 0
        for k in range(TEAM_NUM):
            max_value = 0
            temp = 0
            for j in range(TEAM_NUM):
                if flags[j] == 0:
                    if random_value[j] > max_value:
                        temp = j
                        max_value = random_value[j]
            flags[temp] = 1
            matches_team_nums[k] = temp
        do_matches_and_add_points(matches_team_nums, 0, "FRIENDLY")
        
#        for j in range(TEAM_NUM):
#            print u"%d, %f" % (j, random_value[j])
#        for j in range(TEAM_NUM/2):
#            print u"Team%d vs Team%d" % (matches_team_nums[2*j], matches_team_nums[2*j+1])
        

######## MAIN LOOP ##############

count_A_to_A = 0
count_B_to_A = 0
count_A_to_B = 0
count_B_to_B = 0

TEST_NUM = 100

for j in range(TEST_NUM):
    print u"Test count = %d/%d" % (j, TEST_NUM)
    for i in range(SIM_YEARS):
#        print u"\n------- Year %d --------\n" % (i + 1)
        if i%4 == 3:
            match_maker_for_world_cup()
        elif i%4 == 2:
            match_maker_for_world_cup_qualification()
        else:
            match_maker_for_usual_year(MAX_A_MATCH_PER_YEAR)
            update_ranking()
#            print_current_rank()
#            print_win_draw_lose()
    for i in range(TEAM_NUM/2):
        if ranking[i, 0] <= TEAM_NUM/2:
            count_A_to_A += 1
        else:
            count_A_to_B += 1
        if ranking[i + TEAM_NUM/2, 0] <= TEAM_NUM/2:
            count_B_to_A += 1
        else:
            count_B_to_B += 1

print_win_draw_lose()
print u"\nSTRONG CONTINENT -> A rank : %d (%d percent)" % (count_A_to_A, count_A_to_A * 100 / (count_A_to_A +count_A_to_B))
print u"STRONG CONTINENT -> B rank : %d (%d percent)" % (count_A_to_B, count_A_to_B * 100 / (count_A_to_A +count_A_to_B))
print u"(WEAK CONTINENT -> A rank : %d)" % count_B_to_A
print u"(WEAK CONTINENT -> B rank : %d)" % count_B_to_B

