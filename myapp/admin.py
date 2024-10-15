from django.contrib import admin
from myapp.models import E_learning,Course,course_skills,course_chptr,assesment


# Register your models here.
class E_learningAdmin(admin.ModelAdmin):
    list_display=['id','title','video','thumnail']

admin.site.register(E_learning,E_learningAdmin)


class courseAdmin(admin.ModelAdmin):
    list_display=['title','duration','certificate','thumnail','fees',"notes",'video',"video1"]

admin.site.register(Course,courseAdmin)



class course_skillAdmin(admin.ModelAdmin):
    list_display=['course_name','skill','chapter']

admin.site.register(course_skills,course_skillAdmin)


class course_chapterAdmin(admin.ModelAdmin):
    list_display=['course_name','video','chapter_name']

admin.site.register(course_chptr,course_chapterAdmin)

class Assesment_Admin(admin.ModelAdmin):
    list_display=['course_name','question','option1','option2','option3','option4','answer']

admin.site.register(assesment,Assesment_Admin)

