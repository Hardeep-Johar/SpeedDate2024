from django.shortcuts import render
from speed_date.course_admin import *
# Create your views here.

from speed_date.models import Course,Group
def welcome(request):
    context = dict()
    the_user = request.user
    if the_user.username == 'hardeepjohar':
        courses = Course.objects.all()
        context['course_list'] = courses
        return render(request,"admin_page.html",context)
    else:
        group = Group.objects.get(user=the_user)
        course = group.course
        context['group'] = group
        context['course'] = course
        return render(request,"welcome.html",context)

def course_control(request):
    context=dict()
    the_user = request.user
    if not the_user.username == 'hardeepjohar':
        context['user_name'] = the_user.username
        return render(request,'unauthorized.html',context)
    else:
        course_num=request.GET['course_choice']
        course = Course.objects.get(course_number=course_num)
        context['course'] = course
        print(course)
        groups = course.group_set.all()
        context['group_list'] = groups
        return render(request,'course_admin.html',context)

def do_course_admin_actions(request):
    context=dict()
    the_user = request.user
    if not the_user.username == 'hardeepjohar':
        context['user_name'] = the_user.username
        return render(request,'unauthorized.html',context)
    else:
        course_num = request.GET['course']
        course = Course.objects.get(course_number=course_num)
        action = None
        if 'edit' in request.GET:
            return do_edit_group(request,course_num)
        elif 'add' in request.GET:
            return do_add_group(request,course_num)
        elif 'generate' in request.GET:
            #print(course.rotation_freeze)
            if course.rotation_freeze:
                groups = course.group_set.all()
                context['message'] = 'Rotations are Frozen!'
                context['group_list'] = groups
                context['course'] = course
                return render(request,"course_admin.html",context)
            return do_rotation_generate(request,course_num)
        elif 'freeze' in request.GET:
            course.rotation_freeze = True
            course.save()
            groups = course.group_set.all()
            context['message'] = 'Rotation Frozen!'
            context['group_list'] = groups
            context['course'] = course
            return render(request,"course_admin.html",context)
        elif 'print' in request.GET:
            return do_rotation_print(request,course_num)
        elif 'compile' in request.GET:
            return do_compile_dollars(request,course_num)
        elif 'allnotes' in request.GET:
            return do_get_all_notes(request,course_num)
        else:
            return render(request,"unauthorized.html")

def add_course(request):
    context=dict()
    the_user = request.user
    if not the_user.username == 'hardeepjohar':
        context['user_name'] = the_user.username
        return render(request,'unauthorized.html',context)
    else:
        return render(request,'add_new_course.html',context)

def create_course(request):
    context=dict()
    the_user = request.user
    if not the_user.username == 'hardeepjohar':
        context['user_name'] = the_user.username
        return render(request,'unauthorized.html',context)
    try:
        course = Course(course_number=request.GET['cnum'],course_title=request.GET['cname'],course_long_name=request.GET['clname'])
    except:
        return render(request,'add_new_course.html',context)
    course.save()
    context['course'] = course
    return render(request,'course_admin.html',context)


def edit_group(request):
    context = dict()
    the_user=request.user
    if not the_user.username == 'hardeepjohar':
        context['user_name'] = the_user.username
        return render(request,'unauthorized.html',context)
    else:
        course_num = request.GET['course_choice']
        course = Course.objects.get(course_number=course_num)
        group_list = course.group_set.all()
        context['course'] = course
        context['group_list'] = group_list
        return render(request,'course_admin.html',context)

def create_group(request):
    context = dict()
    the_user=request.user
    if not the_user.username == 'hardeepjohar':
        context['user_name'] = the_user.username
        return render(request,'unauthorized.html',context)
    if 'done' in request.GET:
        return welcome(request)
    course_number = request.GET['course']
    course = Course.objects.get(course_number=course_number)
    group_number = request.GET['group_number']
    app_name = request.GET['app_name']
    members = request.GET['members']
    new_username = '_'.join(app_name.split())
    N=8
    import random,string
    new_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
    from django.contrib.auth.models import User
    new_user = User.objects.create_user(new_username, 'lennon@thebeatles.com', new_password)
    new_group = Group(group_number=group_number,group_name=app_name,group_members=members,password=new_password,user=new_user,course=course)
    new_group.save()
    if 'done' in request.GET:
        context['course'] = course
        context['group_list'] = course.group_set.all()
        return render(request,'course_admin.html',context)
    return do_add_group(request,course_number)

def do_get_all_notes(request,course_num):
    context=dict()
    notes_list = list()
    course = Course.objects.get(course_number=course_num)
    for group in course.group_set.all():
        for note in group.notes_set.all():
            if note.notes:
                notes_list.append((group.group_name,note.group_2,note.notes))
    print(notes_list)
    context['notes_list'] = notes_list
    return render(request,"all_admin_notes.html",context)