from speed_date.models import Course,Group,Dollars

def roundRobin(units, sets=None):
    if len(units) % 2:
        units.append(None)
    count    = len(units)
    sets     = sets or (count - 1)
    half     = count // 2
    schedule = []
    for turn in range(sets):
        pairings = []
        for i in range(half):
            pairings.append((units[i], units[count-i-1]))
        units.insert(1, units.pop())
        schedule.append(pairings)
    return schedule

def generate_rotations(app_names):
    if len(app_names)%2 != 0:
        app_names.append('None')
    all_rounds=roundRobin(list(range(len(app_names))))
    new_all_rounds=list()
    for pairings in all_rounds:
        new_pairing=list()
        for pair in pairings:
            if (not None in pair and pair[0]>pair[1]):
                new_pairing.append((pair[1],pair[0]))
            else:
                new_pairing.append(pair)
        new_all_rounds.append(new_pairing)
    named_pairs=list()
    teams=app_names
    for pairings in new_all_rounds:
        round_list=list()
        for pair in pairings:
            if not pair[0] == None:
                team1=teams[pair[0]]
            else:
                team1=None
            if not pair[1] == None:
                team2=teams[pair[1]]
            else:
                team2=None
            round_list.append([team1,team2])
        named_pairs.append(round_list)

        team_dict=dict()
    for team in teams:
        team_dict[team]=list()
    num_rounds = len(named_pairs)
    num_tables = len(named_pairs[0])
    for i in range(num_rounds):
        for j in range(num_tables):
            team1=named_pairs[i][j][0]
            team2=named_pairs[i][j][1]
            print(team1,team2)
            round = 'ROUND ' + str(i+1)
            table = 'TABLE ' + str(j+1)
            if not team2 == 'Prof':
                team_dict[team1].append(round + ': '+table + ':  '+ 'View then Demo: ' + team2)
            else:
                team_dict[team1].append(round + ': '+table + ':  '+ 'Demo to prof then relax: ')
            if not team1=='prof':
                team_dict[team2].append(round + ': '+table + ':  '+ 'Demo then View: ' + team1)
            else:
                team_dict[team2].append(round + ': '+table + ':  '+ 'Demo to prof then relax: ')
    return team_dict

def write_rotations_to_file(team_dict,course_num):
    course = Course.objects.get(course_number=course_num)
    for team in team_dict:
        print(team)
        if team == 'None':
            continue
        if not team == 'Prof':
            group = course.group_set.get(group_name=team)
            guser = group.user.username
            gpassword = group.password
        filename = 'static/COURSE_' + str(course_num) + '_TEAM_' + team
        with open(filename,'w') as f:
            f.write('TEAM NAME: ' + team + '\n')
            if not team == 'Prof':
                f.write('GROUP USERNAME: ' + guser + '\n')
                f.write('GROUP PASSWORD: ' + gpassword + '\n\n\n')
            data = team_dict[team]
            for item in data:
                f.write(item + '\n')
            f.write("\nView then demo: First view the other team's project then demo to them")
            f.write("\nEach demo is for 4 minutes")
"""
def write_rotations_to_file(team_dict,course_num):
    course = Course.objects.get(course_number=course_num)
    for team in team_dict:
        if not team == 'Prof':
            group = course.group_set.get(group_name=team)
            guser = group.user.username
            gpassword = group.password
        filename = 'static/COURSE_' + str(course_num) + '_TEAM_' + team
        with open(filename,'w') as f:
            f.write('TEAM NAME: ' + team + '\n')
            if not team == 'Prof':
                f.write('GROUP USERNAME: ' + guser + '\n')
                f.write('GROUP PASSWORD: ' + gpassword + '\n\n\n')
            data = team_dict[team]
            for item in data:
#                if team == 'Prof':
#                    f.write('ROUND:,'+str(item[0])+',TABLE:,'+str(item[1])+',View project of,' + item[3] + '\n')
#                elif item[3] == 'Prof':
#                    f.write('ROUND:,'+str(item[0])+',TABLE:,'+str(item[1])+',Demo your project to the Professor' + '\n')
#                else:
                    f.write('ROUND:,'+str(item[0])+',TABLE:,'+str(item[1])+',VIEW,'+item[3]+',then demo to,'+item[3]+'\n')

"""
