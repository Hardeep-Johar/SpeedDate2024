from django.shortcuts import render

from speed_date.views import *
from speed_date.models import Course,Group,Dollars,RotationLine
INVESTMENT_GOAL = 100000


def group_rotation(request):
    context = dict()
    the_user = request.user
    group = Group.objects.get(user=the_user)
    course = group.course
    rotation_file = 'static/COURSE_' + str(course.course_number) + '_TEAM_' + group.group_name
    rotation_list=list()
    print(rotation_file)
    try:
        with open(rotation_file,'r') as f:
            for line in f:
                words = line.split(':')
                print(words)
                if not words:
                    continue
                if not 'ROUND' in words[0]:
                    continue
                print(words[2])
                if 'Demo to prof' in words[2]:
                    team1 = 'Professor'
                    team2 = 'Professor'
                elif words[2] == '  Demo then View':
                    team1 = group.group_name
                    team2 = words[3]
                else:
                    team1 = words[3]
                    team2 = group.group_name
                rnumber = int(words[0].split()[1])
                tnumber = int(words[1].split()[1])
                print(rnumber,tnumber,team1,team2)
                rotation_element = RotationLine(round=rnumber,table=tnumber,first_team=team1,other_team=team2)
                rotation_list.append(rotation_element)
    except:
        rotation_list=list()
    context['rotation_list'] = rotation_list
    context['team'] = group.group_name
    return render(request,"rotation.html",context)

def group_standing(request,done=False):
    context = dict()
    if done:
        context['message'] = 1
    the_user = request.user
    print(the_user)
    group = Group.objects.get(user=the_user)
    context['team'] = group.group_name

    dollars = Dollars.objects.filter(group_2 = group)
    print(dollars)
    interesting=0
    complete=0
    gizmos=0
    for dollar in dollars:
        interesting += dollar.interesting_dollars
        complete += dollar.completeness_dollars
        gizmos += dollar.gizmos_dollars
    total = interesting + complete + gizmos
    context['interesting'] = interesting
    context['complete'] = complete
    context['gizmos'] = gizmos
    context['total'] = total
    return render(request,'standing.html',context)

def group_invest(request,errors=None):
    print(INVESTMENT_GOAL)
    context = dict()
    if errors:
        context['errors'] = errors
    the_user = request.user
    group = Group.objects.get(user=the_user)
    context['team'] = group.group_name
    dollars = group.dollars_set.all()
    context['dollars'] = dollars
    i_total = 0.0
    c_total = 0.0
    g_total = 0.0
    for dollar in dollars:
        i_total += dollar.interesting_dollars
        c_total += dollar.completeness_dollars
        g_total += dollar.gizmos_dollars
    context['interesting_totals'] = i_total
    context['completeness_totals'] = c_total
    context['gizmos_totals'] =g_total
    context['total'] = INVESTMENT_GOAL
    return render(request,'invest.html',context)

def check_and_do_investment(request):
    context = dict()
    alloc_list = ['I','C','G']
    totals=dict()
    for key in alloc_list:
        totals[key] = 0.0
    the_user = request.user
    this_group = Group.objects.get(user=the_user)
    course = this_group.course
    groups = course.group_set.all()
    for group in groups:
        g_name = group.group_name
        if g_name == this_group.group_name:
            continue
        for alloc_char in alloc_list:
            request_key = g_name + alloc_char
            try:
                value = float(request.GET[request_key])
            except:
                value = 0.0
            print(value)
            totals[alloc_char] += value
            dollar_obj = this_group.dollars_set.get(group_2 = g_name)
            if alloc_char == 'I':
                dollar_obj.interesting_dollars = value
            elif alloc_char == 'C':
                dollar_obj.completeness_dollars = value
            else:
                dollar_obj.gizmos_dollars = value
            dollar_obj.save()
    if 'refresh' in request.GET:
        return group_invest(request)
    elif 'reset' in request.GET:
        dollars = this_group.dollars_set.all()
        for dollar in dollars:
            dollar.interesting_dollars=0.0
            dollar.completeness_dollars=0.0
            dollar.gizmos_dollars = 0.0
            dollar.save()
        return group_invest(request)
    else:
        fails=dict()
        for key in alloc_list:
            if not (INVESTMENT_GOAL -1 < totals[key] < INVESTMENT_GOAL + 1):
                fails[key] = INVESTMENT_GOAL - totals[key]
                return group_invest(request,errors=fails)
        return group_standing(request,done=True)

def record_notes(request):
    context = dict()
    the_user = request.user
    this_group = Group.objects.get(user=the_user)
    notes_list = this_group.notes_set.all()
    for note in notes_list:
        print(note.group_2,note.notes)
    context['notes_list'] = notes_list
    return render(request,"notes_selector.html",context)

def write_notes(request):
    context=dict()
    the_user = request.user
    this_group = Group.objects.get(user=the_user)
    if 'home' in request.GET:
        return welcome(request)
    try:
        note_group = request.GET['selected']
    except:
        return welcome(request)
    note_object = this_group.notes_set.get(group_2=note_group)
    print(note_object.group.group_name,note_group,note_object.notes)
    note = note_object.notes
    team = Group.objects.get(group_name=note_group).group_members
    print(note)
    context['note'] = note
    context['group'] = note_group
    context['team'] = team
    return render(request,'edit_note.html',context)

def process_note(request):
    context=dict()
    if 'exit' in request.GET:
        return record_notes(request)
    note = request.GET['note']
    print(note)
    the_user = request.user
    this_group = Group.objects.get(user=the_user)
    group_2 = request.GET['group2']
    note_object = this_group.notes_set.get(group_2=group_2)
    note_object.notes = note
    print(note_object.group.group_name,note_object.group_2)
    note_object.save()
    return record_notes(request)

def see_all_notes(request):
    context = dict()
    notes_list = list()
    the_user = request.user
    this_group = Group.objects.get(user=the_user)
    notes = this_group.notes_set.all()
    for note in notes:
        if not note.notes:
            continue
        group = note.group_2
        note_text = note.notes
        notes_list.append((group,note_text))
    context['notes_list'] = notes_list
    context['this_group'] = this_group
    return render(request,'all_notes.html',context)