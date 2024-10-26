from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from myapp.models import E_learning,feedback,Course,course_skills,enrolled,coursefeedback,course_chptr,paidfeedback,userinfo,assesment,USerassement
import razorpay
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings  # For handling media uploads
import os
import uuid



# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else: 
        us =request.POST['username']
        e = request.POST['email']
        n =  request.POST['name']
        pas = request.POST['password']

        user=User.objects.filter(username = us)
        mil=User.objects.filter(email = e)
        nam = str(User.objects.filter(first_name = n))
        if user.exists():
            messages.warning(request,"username already taken!")
            return redirect('/register')
        
        if mil.exists():
            messages.warning(request,"Email id already exists!")
            return redirect('/register')
        
        if not nam.isalpha():
            # messages.warning(request,"name cant be number!")
            # return redirect('/register')
        

            u=User.objects.create(email=e,first_name=n,username = us)
            u.set_password(pas)
            u.save()
            messages.info(request,'Account created successfully')
            return redirect('/login')
        else:
            messages.warning(request,"name cant be number!")
            return redirect('/register')
            # u=User.objects.create(email=e,first_name=n,username = us)
            # u.set_password(pas)
            # u.save()
            # messages.info(request,'Account created successfully')
            # return redirect('/login')

def login_page(request):
    if  request.method == "GET":
        return render(request,'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username = username).exists:
            messages.warning(request,'Invalid username!')
            return redirect('/login')
        
        user = authenticate(username = username , password = password)
        
        if user is None:
            messages.warning(request,'Invalid password!')
            return redirect('/login')
        
        else:
            login(request,user)
            messages.error(request,'Login successfully!')
            return redirect('/')
        
def logout_page(request):
    logout(request)
    messages.error(request,'User logout successfully')
    return redirect('/')

def Elearning(request):
    userid=request.user.id
    context={}
    if userid is None:
        messages.warning(request,'please login so as to watch videos')
        return render(request,'login.html',context)
    else:
        context={}
        data= E_learning.objects.all()
        context['Elearn']=data
        return render(request,'E-learning.html',context)
    
def watchonline(request,id):
    context = {}
    data = E_learning.objects.get(id = id)
    context['watch']=data
    return render(request,'watchonline.html',context)

def feedbackRating(request,id):
    user = request.user
    e_learning_instance = E_learning.objects.get(id=id)
    if request.method == "POST":
        review = request.POST.get('review', 'no feedback given') 
        rating = request.POST.get('rating')

        if not rating:

            messages.error(request, 'Please provide a rating...')
            return redirect(f'http://127.0.0.1:8000/watchonline/{e_learning_instance.id}')  # Redirect to an appropriate page

        # Create and save the Feedback object
        data= feedback.objects.create(uid=user,E_learning_id=e_learning_instance,review=review,ratings=rating)
        data.save()

        # Show a success message
        messages.error(request, 'Thank you for your feedback. Explore more content!')
        return redirect('/e-learning')  # Redirect to an appropriate page after saving
    else:
    # Handle non-POST requests
        return redirect('/e-learning')
    

def courses(request, code):
    userid=request.user.id
    context={}
    if userid is None:
        messages.warning(request,'please login for course detail')
        return render(request,'login.html',context)
    else:
        context = {}
        
        # Get course data
        course_data = Course.objects.get(title=code)
        context["course"] = course_data

        # Get course skills data
        course_skill_data = course_skills.objects.filter(course_name=code)
        
        # Prepare the course skills and chapters data
        skills_chapters = []
        for skill in course_skill_data:
            chapters = skill.chapter.split(',')  # Split the chapter string by comma
            skills_chapters.append({
                'skill': skill.skill,  # Include the skill name
                'chapter_list': [chapter.strip() for chapter in chapters]  # List of chapters
            })
        
        context["course_skills"] = skills_chapters

        return render(request, "c++_course.html", context)



def payment(request,code):
    context={}
    user = request.user
    data = Course.objects.get(title = code)
    client = razorpay.Client(auth=("rzp_test_tIqAd7OXqu2xWS", "Nt4xEdPZ2llmou7xC55FfCmq"))
    data = { "amount":data.fees*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context["data"]=payment
    context["course"]=code
    # context={'data':payment}
    # context={"course":code}
    return render(request,'pay.html',context)



def enrolled_user(request, title):
    context = {}
    user = request.user
    title = unquote(title)
    

    # Fetch the course instance or return a 404 error if not found
    course_instance = get_object_or_404(Course, title=title)

    # Create a new enrollment record
    enrolled.objects.create(uid=user, course_name=course_instance, paid=True)

    # Send email confirmation
    msg_body = 'Your order has been placed successfully.'
    user_email = user.email

    send_mail(
        'Course Enrollment Confirmation',  # Subject
        msg_body,  # Message body
        "dharmeshhh011@gmail.com",  # From email
        [user_email],  # To email
        fail_silently=False,
    )

    # Add a message to be displayed on the next page
    messages.error(request, 'Course successfully purchased! The premium section is now unlocked. You can download your invoice from "My Batch".')

    # Render the response with context
    return redirect("/")



def course_menu(request):
    course_data = Course.objects.all()
    context={"data":course_data}
    return render(request,'courseMenu.html',context)


@login_required(login_url='login_page')
def premium(request):
    user = request.user
    enrollments = enrolled.objects.filter(uid=user)

    # Check if there's any enrollment where paid is True
    if enrollments.filter(paid=False).exists():
        return redirect('/courseMenu')   


    # courseDetail = Course.objects.filter(title=enrollments)
    course_details = Course.objects.filter(enrolled__in=enrollments).distinct()
    
    context = {"data":course_details,"customer":user}
    return render(request, 'premium.html',context)

# views.py
def chptrlist(request, title):
    context = {}
    user = request.user
    
    # Get course skills for the specified course
    course_skill_data = course_skills.objects.filter(course_name__title=title)
    context["course_name"]=title
        
    # Prepare the course skills and chapters data
    skills_chapters = []
    for skill in course_skill_data:
        chapters = skill.chapter.split(',')  # Split the chapter string by comma
        skills_chapters.append({
            'skill': skill.skill,  # Include the skill name
            'chapter_list': [chapter.strip() for chapter in chapters]  # List of chapters
        })
        
    context["course_skills"] = skills_chapters
    
    # Retrieve paid feedback entries for the user
    complete_feedback = paidfeedback.objects.filter(uid=user).values_list('chapter_name__chapter_name', flat=True)
    context['completed_chapters'] = list(complete_feedback)  # Convert to list for easy checking
    exam = USerassement.objects.filter(uid=user,course_name = title)
    context['exam'] = exam

    return render(request, "chptrList.html", context)




def watchpremium(request,title):
    context = {}
    data = Course.objects.get(title = title)
    context['watchp']=data
    data2=course_skills.objects.filter(course_name = title)
    context['chptr']=data2
    return render(request,'watchpremiume.html',context)


def coursefeedbackandrating(request,title):
    user = request.user
    e_learning_instance = Course.objects.get(title=title)
    if request.method == "POST":
        review = request.POST.get('review', 'no feedback given') 
        rating = request.POST.get('rating')

        # if not rating:

        #     messages.error(request, 'Please provide a rating...')
        #     return redirect(f'http://127.0.0.1:8000/watchonline/{e_learning_instance.id}')  # Redirect to an appropriate page

        # Create and save the Feedback object
        data= coursefeedback.objects.create(uid=user,course_title=e_learning_instance,review=review,ratings=rating)
        data.save()

        # Show a success message
        messages.success(request, 'Thank you for your feedback. Explore more content!')
        return redirect('/e-learning')  # Redirect to an appropriate page after saving
    else:
    # Handle non-POST requests
        return redirect('/e-premium')
    
def support(request,title):
    messages.error(request,"Our expert will get in touch with you shortly to schedule a one-on-one doubt-solving session. We’re here to help you with any questions you have!")
    data=Course.objects.get(title = title)
    return redirect(f"http://127.0.0.1:8000/watchpremium/{title}")


def sortrange(request,ord):
    col=''
    if ord == 'asc':
     col='fees'
    else:
        col= '-fees'
    clist = Course.objects.all().order_by(col)
    context={'data':clist}
    return render(request,'courseMenu.html',context)

# def searchttitle(request):
#     query = request.GET.get('query', '')
#     courses = Course.objects.filter(title__icontains=query)  # Filter courses by title
#     return render(request, 'courseMenu.html', {'courses': courses})

def search_courses(request):
    query = request.GET.get('query', '')
    courses = Course.objects.filter(title__icontains=query)  # Filter courses by title
    return render(request, 'courseMenu.html', {'courses': courses, 'query': query})



def watchchptr(request, title):
    user=request.user
    context = {}
    data = course_chptr.objects.get(chapter_name=title)
    context['chpter_data'] = data
    context['course_name'] = data.course_name.title

    
    # Fetching skills and chapters
    course_skill_data = course_skills.objects.filter(course_name=data.course_name)
    skills_chapters = []
    
    for skill in course_skill_data:
        chapters = skill.chapter.split(',')  # Split the chapter string by comma
        skills_chapters.append({
            'skill': skill.skill,  # Include the skill name
            'chapter_list': [chapter.strip() for chapter in chapters]  # List of chapters
        })

  
    complete_feedback = paidfeedback.objects.filter(uid=user).values_list('chapter_name__chapter_name', flat=True)
    context['completed_chapters'] = list(complete_feedback) 
    
    context["course_skills"] = skills_chapters
    context["heading"] = [skill.skill for skill in course_skill_data]  # List of skills
    return render(request, 'watchvideo.html', context)



def paidcoursereviews(request, chptr_name):
    user = request.user
    context={}
    # Fetch the chapter instance instead of just the chapter name
    try:
        chpters = course_chptr.objects.get(chapter_name=chptr_name)
    except course_chptr.DoesNotExist:
        messages.error(request, 'Chapter not found!')
        return redirect('chptr_list')  # Redirect to an appropriate page

    if request.method == "POST":
        review = request.POST.get('review', 'no feedback given') 
        rating = request.POST.get('rating')

        if not rating:
            messages.error(request, 'Please provide a rating.')
            return redirect(f'/chptrlist/watchp/{chptr_name}')  # Redirect back to the chapter page

        # Create and save the Feedback object with the correct foreign key reference
        data = paidfeedback.objects.create(
            uid=user,
            chapter_name=chpters,  # Pass the actual chapter object here
            course_name=chpters.course_name,  # Assuming course_name is a foreign key in course_chptr
            review=review,
            ratings=rating,
            complete=True
        )
        data.save()

        # Show a success message and redirect to the course page
        messages.success(request, "Video marked as completed! Keep up the great work!")
        return redirect(f'/chptrlist/watchp/{chpters.chapter_name}')  # Redirect to the course page
    else:
        # Handle non-POST requests by redirecting
        return redirect(f'/chptrlist/{chpters.course_name}')




def giveExam(request, course_name):
    user = request.user

    if request.method == "GET":
        # Get all chapters for the course
        watched_chapters = course_chptr.objects.filter(course_name=course_name).values_list('chapter_name', flat=True)
        # Get watched chapters by the user
        user_watched_chapters = paidfeedback.objects.filter(uid=user, course_name=course_name).values_list('chapter_name', flat=True)

        # Check if all chapters are watched
        if set(watched_chapters) == set(user_watched_chapters):
            Data = assesment.objects.filter(course_name=course_name)  # Filter assessments by course name
            exam_given = USerassement.objects.filter(uid=user, course_name=course_name).exists()  # Check if exam is given

            if exam_given:
                # Fetch the saved assessment result
                user_assessment = USerassement.objects.get(uid=user, course_name=course_name)
                marks = user_assessment.correct_anw
                wrong = user_assessment.wrong_anw
                percentage = user_assessment.score

                # Prepare the results for display
                question_data = assesment.objects.filter(course_name=course_name)
                results = []

                for count, data in enumerate(question_data, start=1):
                    # User's answer is not stored, so we cannot highlight it unless you save it in the database
                    results.append({
                        'question': data.question,
                        'options': [data.option1, data.option2, data.option3, data.option4],
                        'correct_answer': data.answer,
                        'user_answer': None  # You can add logic to store and retrieve user's answer if needed
                    })

                context = {
                    'marks': marks,
                    'wrong': wrong,
                    'results': results,
                    'perc': percentage,
                    'course_name':course_name,
                    'given_exam': True  # Set given_exam to True since the exam is given
                }


    

            else:
                context = {
                    "data": Data,
                    "course_name": course_name,
                    "given_exam": False  # Boolean to check if the exam is already given
                }

            return render(request, "exam.html", context)  # Render the exam page
        else:
            messages.error(request, "Watch all videos first")
            return redirect(f"/chptrlist/{course_name}")  # Redirect back to the chapter list

    else:  # POST request for submitting the exam
        marks = 0
        wrong = 0
        results = []
        question_data = assesment.objects.filter(course_name=course_name)  # Filter questions for the course

        for count, data in enumerate(question_data, start=1):
            user_answer = request.POST.get(f'q{count}_answer')
            if data.answer == user_answer:
                marks += 1
            else:
                wrong += 1

            # Store the data with the user's answer and correct answer
            results.append({
                'question': data.question,
                'options': [data.option1, data.option2, data.option3, data.option4],
                'correct_answer': data.answer,
                'user_answer': user_answer
            })

        # Calculate percentage after processing all questions
        total_questions = len(question_data)
        percentage = (marks * 100 / total_questions) if total_questions > 0 else 0

        # Get the Course instance
        course_instance = get_object_or_404(Course, title=course_name)

        # Create and save the Userassement instance
        user_assessment = USerassement.objects.create(
            course_name=course_instance,  # Set the Course instance
            uid=user,                     # Current user
            correct_anw=marks,           # Correct answers
            wrong_anw=wrong,             # Wrong answers
            submitted_at=timezone.now(), # Current date and time
            score=percentage              # Score
        )

        # Return the result view with marks and results data
        return render(request, 'exam.html', {
            'marks': marks,
            'wrong': wrong,
            'results': results,
            'perc': percentage,
            'given_exam': True ,
     # Set given_exam to True after submission
        })

def pregiveExam(request,course_name):
    u= request.user
    watched_chapters = course_chptr.objects.filter(course_name=course_name).values_list('chapter_name', flat=True)
        # Get watched chapters by the user
    user_watched_chapters = paidfeedback.objects.filter(uid=u, course_name=course_name).values_list('chapter_name', flat=True)
    context={}

    if len(watched_chapters) == len(user_watched_chapters):
        user = request.user
        if USerassement.objects.filter(course_name = course_name,uid = user).exists():
            context['status'] = 1
        else:
            context['status'] = 2
        context['course_name'] = course_name

        return render(request,"preexam.html",context)
    else:
        messages.error(request, "Watch all videos first")
        return redirect(f"/chptrlist/{course_name}") 
        




@login_required
def deskboard(request):
    context = {}
    u = request.user  # Get the current logged-in user

    if request.method == "POST":
        # Get or create the userinfo for this user
        user_info, created = userinfo.objects.get_or_create(user=u)

        # Handle personal details form
        if 'name' in request.POST:
            name = request.POST.get('name', user_info.name)  # Default to existing value if not provided
            date_of_birth = request.POST.get('dob', user_info.date_of_birth)
            gender = request.POST.get('gender', user_info.gender)
            address = request.POST.get('address', user_info.address)

            # Handle user photo upload
            if request.FILES.get('user_photo'):
                # Delete old image if a new one is uploaded
                if user_info.user_photo and os.path.isfile(user_info.user_photo.path):
                    os.remove(user_info.user_photo.path)

                user_photo = request.FILES['user_photo']  # Fetch uploaded image
                user_info.user_photo = user_photo

            # Update the user_info instance
            user_info.name = name
            user_info.date_of_birth = date_of_birth
            user_info.gender = gender
            user_info.address = address
            user_info.save()

        # Handle academic details form
        elif 'degree' in request.POST:
            degree = request.POST.get('degree', user_info.degree)
            institute = request.POST.get('institute', user_info.institute)
            year_of_graduation = request.POST.get('year_of_graduation', user_info.year_of_graduation)

            # Update the user_info instance
            user_info.degree = degree
            user_info.institute = institute
            user_info.year_of_graduation = year_of_graduation
            user_info.save()

        # Fetch updated data for rendering after form submission
        data = userinfo.objects.filter(user=u).first()  # Get the specific user info for this user
        context["info"] = data

        userdata = User.objects.get(id=u.id)  # Fetch the user data
        context["user_details"] = userdata  # Pass updated user info

        return render(request, 'userdetails.html', context)
    
    else:
        # For GET request, just fetch user info and other details
        userdata = User.objects.get(id=u.id)  # Fetch user data by id
        paid_details = enrolled.objects.filter(uid=u)

        # Fetch user info details
        data = userinfo.objects.filter(user=u).first()

        # Pass all required data to the context
        context['paid_details'] = paid_details
        context['user_details'] = userdata
        context["info"] = data

        return render(request, 'userdetails.html', context)



def mybatch(request):
    context = {}
    user = request.user
    
    # Get all enrolled instances for the user
    enrolled_courses = enrolled.objects.filter(uid=user)

    # Extract course names from enrolled courses
    course_names = enrolled_courses.values_list('course_name', flat=True)

    if not course_names:
        context['data'] = []
        context['exam'] = []
        context['code'] = 2  # No enrolled courses found
        return render(request, "mybatch.html", context)

    # Fetch the corresponding Course instances based on the course names
    courses = Course.objects.filter(title__in=course_names)

    # Fetch the corresponding USerassement instances based on the user and course names
    assessments = USerassement.objects.filter(uid=user, course_name__in=course_names)

    # Prepare data for the context
    context['data'] = courses
    context['exam'] = assessments

    # Check if there are any assessments and determine the score
    if assessments.exists():  # Check if there are any assessments
        for assessment in assessments:
            if assessment.score >= 70.0:
                context['code'] = 1  # User is eligible for certificate
                print(assessment.score)  # Print the score for debugging
                break
        else:
            context['code'] = 2  # No assessments with score >= 70
    else:
        context['code'] = 2  # No assessments found

    return render(request, "mybatch.html", context)

def certificate_msg(request):
    user = request.user
    # Get all enrolled instances for the user
    enrolled_courses = enrolled.objects.filter(uid=user)
    
    # Extract course names from enrolled courses
    course_names = enrolled_courses.values_list('course_name', flat=True)
    
    if not course_names:
        data = []
        exam = []
    else:
        # Fetch the corresponding Course instances based on the course names
        data = Course.objects.filter(title__in=course_names)
        exam = USerassement.objects.filter(uid=user, course_name__in=course_names)
    messages.error(request,'Your score is less than 70%. You cannot download the certificate.')
    return render(request, "mybatch.html", context={'data': data, 'exam': exam})


def question(request):
    return render(request,"interviewQuestion.html")


def progresscard(request):
    user = request.user
    data = enrolled.objects.filter(uid=user).select_related('course_name')  # Use select_related for optimization
    course_names = data.values_list('course_name', flat=True)
    context={
        'data':data,
        'title':course_names
    }
    return render(request, 'progresscard.html',context)


def generate_invoice(request, title):
    user = request.user
    invoice_number = uuid.uuid4()
    purchase_date = timezone.now()
    data = enrolled.objects.get(uid=user, course_name=title)
    tax = round(data.course_name.fees * 0.18, 2)  
    amountWithoutTax = round(data.course_name.fees - tax, 2)  
    tax = round(tax / 2, 2) 
    
    context = {
        'invoice_number': invoice_number,
        'purchase_date': purchase_date,
        'data': data,
        'tax': tax,
        'notaxammount': amountWithoutTax
    }

    return render(request, 'invoice.html', context)

def tracking(request, course_name):
    user = request.user
    chptr = course_chptr.objects.filter(course_name=course_name)
    chptr_count = len(chptr)
    chptr_watched = paidfeedback.objects.filter(uid=user, course_name=course_name)
    chptr_watched_count = len(chptr_watched)
    exam_detail = USerassement.objects.filter(uid=user, course_name=course_name).last()

    # Initialize digital_marks as a number
    if chptr_count == chptr_watched_count:
        digital_marks = 5  # Using a numeric value instead of '5%'
    else:
        digital_marks = 0  # No marks for incomplete chapters

    # Ensure exam_detail exists and handle the case where it might be None
    if exam_detail:
        exam_score = exam_detail.score
    else:
        exam_score = 0  # Default to 0 if there's no exam data

    # Calculate total_marks
    total_marks = digital_marks + exam_score
    if total_marks >100.0:
        total_marks =100.0
    if total_marks>=75.0:
        marks_need = 0.0
    else:
        marks_need = total_marks - 75.0 

    context = {
        'course_name': course_name,
        'chptr_count': chptr_count,
        'chptr_watched_count': chptr_watched_count,
        'exam_detail': exam_detail,
        'digital_marks':digital_marks ,  # For display purposes, convert back to string with percentage
        'total_marks': total_marks,
        'marks_need':marks_need
        
    }

    return render(request, 'TrackCourse.html', context)