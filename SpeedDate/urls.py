"""SpeedDate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login
from speed_date import views
from speed_date import user_programs

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',login,name='login'),
    url(r'^welcome$',views.welcome,name='welcome'),
    url(r'^add_course$',views.add_course,name="add_course"),
    url(r'^create_course$',views.create_course,name="create_course"),
    url(r'^edit_groups$',views.edit_group,name='edit_groups'),
    url(r'^create_group$',views.create_group,name='create_group'),
    url(r'^course_control$',views.course_control,name='course_control'),
    url(r'^do_course_admin_actions$',views.do_course_admin_actions,name='do_course_admin_actions'),
    url(r'^view_rotation$',user_programs.group_rotation,name='view_rotation'),
    url(r'^view_standing$',user_programs.group_standing,name='view_standing'),
    url(r'^invest$',user_programs.group_invest,name='invest'),
    url(r'^do_invest$',user_programs.check_and_do_investment,name='do_invest'),
    url(r'^notes$',user_programs.record_notes,name='notes'),
    url(r'^write_notes$',user_programs.write_notes,name='write_notes'),
    url(r'^process_note$',user_programs.process_note,name='process_note'),
    url(r'^view_all_notes$',user_programs.see_all_notes,name='view_all_notes'),
]
