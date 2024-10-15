from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class E_learning(models.Model):
    title = models.CharField(max_length=100)
    video = models.CharField(max_length=500)
    # notes =models.FileField(upload_to='media',max_length=250,default=None,null=True)
    thumnail = models.ImageField(upload_to='media',default=0)


class feedback(models.Model):
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    E_learning_id=models.ForeignKey(E_learning,db_column="E_learning_id", on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1, blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True,default="no feedback given")


class Course(models.Model):
    title = models.CharField(max_length=100,primary_key=True)
    duration = models.IntegerField(default=None)
    certificate = models.ImageField(upload_to='media',default=0)
    thumnail = models.ImageField(upload_to='media',default=0)
    fees = models.IntegerField(default=None)
    video = models.CharField(max_length=500,null=True)
    notes =models.FileField(upload_to='media',max_length=250,default=None,null=True)
    video1 = models.CharField(max_length=500,null=True)


class course_skills(models.Model):
    course_name = models.ForeignKey(Course,db_column="course_name", on_delete=models.CASCADE)
    skill = models.CharField(max_length=100,null=True,default=None)
    chapter = models.CharField(max_length=500,default=None)

class course_chptr(models.Model):
    chapter_name = models.CharField(max_length=250,primary_key=True)
    course_name = models.ForeignKey(Course,db_column="course_name", on_delete=models.CASCADE)
    video= models.FileField(upload_to='media')
    notes_img=models.FileField(upload_to="media",default=None)
    # rating = models.CharField(max_length=1)
    # feedback=models.CharField(max_length=300,default=None)

class enrolled(models.Model):
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course,db_column="course_name", on_delete=models.CASCADE)
    paid=models.BooleanField(default=False)

class coursefeedback(models.Model):
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    course_title=models.ForeignKey(Course,db_column="E_learning_id", on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1, blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True,default="no feedback given")

class paidfeedback(models.Model):
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    course_name=models.ForeignKey(Course,db_column="course__name", on_delete=models.CASCADE)
    chapter_name = models.ForeignKey(course_chptr,db_column="chapter_name",on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1, blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True,default="no feedback given")
    complete = models.BooleanField(default=False)
    

class userinfo(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)  # Consider using choices for better validation
    address = models.TextField(null=True, blank=True)
    user_photo = models.ImageField(upload_to='media', null=True, blank=True)  # Upload to user_photos directory
    degree = models.CharField(max_length=100, null=True, blank=True)
    institute = models.CharField(max_length=100, null=True, blank=True)
    year_of_graduation = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)


class assesment(models.Model):
    course_name=models.ForeignKey(Course,db_column="course__name", on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

class USerassement(models.Model):
    course_name=models.ForeignKey(Course,db_column="course__name", on_delete=models.CASCADE)
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    correct_anw = models.IntegerField()
    wrong_anw = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True) 
    score = models.FloatField()  




