from django.contrib import admin

# Register your models here.
from speed_date.models import Group,Course,Dollars

class DollarsInline(admin.TabularInline):
    model = Dollars
    extra = 3

class GroupInline(admin.TabularInline): #or StackedInline
#    readonly_fields = ('time_since_last_update',)
    model = Group #The model connected
    inlines = [DollarsInline]
    extra = 3 #enough space for three extra Rates


class CourseAdmin(admin.ModelAdmin):
    fields = ['course_number','course_title','course_long_name']
    inlines=[GroupInline]


admin.site.register(Course,CourseAdmin)
