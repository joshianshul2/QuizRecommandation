from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse


z=0
sid = 21000
# Create your views here.
def home(request):
    if request.method == 'POST':
        print(request.POST)
        questions=QuesModel.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'Quiz/result.html',context)
    else:
        questions=QuesModel.objects.all()
        us=StudentDetails.objects.all()
        context = {
            'questions':questions,
            'us':us,
        }
        return render(request,'Quiz/home.html',context)

def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'Quiz/addQuestion.html',context)
    else: 
        return redirect('home') 

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home') 
    else:
        global sid
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid() :
                sid += 1
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                s = StudentDetails.objects.create(Sid=sid, user_name=username, pas=password)
                s.save()
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'Quiz/register.html',context)

def loginPage(request):
    aj=""
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        global z

        username=request.POST.get('username')
        password=request.POST.get('password')
        aj = username
        if StudentDetails.objects.get(user_name=username) :
            all_results=StudentDetails.objects.get(user_name=username)
            print(all_results.user_name)
            print(all_results.Sid)
            z=all_results.Sid
            print("SIDDDD",z)

        # user=authenticate(request,username=username,password=password)
            if(username==all_results.user_name and password==all_results.pas):
                return render(request,'Quiz/home2.html')

    context = {
        'aj': aj,
    }
    return render(request,'Quiz/login.html',context)


# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     if request.method == "POST":
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#
#         all_results = StudentDetails.objects.filter(col1__in=username)
#         print(all_results)
#         context = {}
#         return render(request, 'Quiz/login.html',context)
#
#     return redirect('/')


def logoutPage(request):
    logout(request)
    return redirect('/')


def home2(request):
    return render(request,'Quiz/home.html')

def test1(request):

    if request.method == 'POST':
            print(request.POST)
            questions = QuesModel.objects.all()
            score = 0
            wrong = 0
            correct = 0
            total = 0
            for q in questions:
                total += 1
                print(request.POST.get(q.question))
                print(q.ans)
                print()
                if q.ans == request.POST.get(q.question):
                    score += 10
                    correct += 1
                else:
                    wrong += 1
            percent = score / (total * 10) * 100
            context = {
                'score': score,
                'time': request.POST.get('timer'),
                'correct': correct,
                'wrong': wrong,
                'percent': percent,
                'total': total,

            }
            # Student.objects.
            # if z in
            print("Testing Z",z)
            print("Hiii",type((total)))
            t=Performance.objects.create(Sid=z,result=str(score))
            t.save()
            if Student.objects.filter(Sid=z):
                print("If ke andr")
                a=Student.objects.get(Sid=z)
                print(a.result1)
                r1=float(a.result1)
                c1 = int(a.count1)
                r1 = str((r1 + score) / (c1 + 1))
                c1=str(c1+1)
                s = Student.objects.filter(Sid=z).update(result1=r1,count1=c1)
            else :
                print("else ke andr")
                s=Student.objects.create(Sid=sid,name=" ",result1=score,result2=0,result3=0,count1=1,count2=0,count3=0)
                s.save()
            return render(request, 'Quiz/result.html', context)
    else:
            questions = QuesModel.objects.all()
            context = {
                'questions': questions
            }
            return render(request, 'Quiz/test1.html', context)

def test2(request):

    if request.method == 'POST':
            print(request.POST)
            questions = QuesModel.objects.all()
            score = 0
            wrong = 0
            correct = 0
            total = 0
            for q in questions:
                total += 1
                print(request.POST.get(q.question))
                print(q.ans)
                print()
                if q.ans == request.POST.get(q.question):
                    score += 10
                    correct += 1
                else:
                    wrong += 1
            percent = score / (total * 10) * 100
            context = {
                'score': score,
                'time': request.POST.get('timer'),
                'correct': correct,
                'wrong': wrong,
                'percent': percent,
                'total': total,

            }
            # Student.objects.
            # if z in
            print("Testing Z",z)
            print("Hiii",type((total)))
            t = Performance.objects.create(Sid=z, result=str(score))
            t.save()
            if Student.objects.filter(Sid=z):
                a=Student.objects.get(Sid=z)
                r1=float(a.result2)
                c1 = int(a.count2)
                r1=str((r1+score)/(c1+1))
                c1=str(c1+1)
                s = Student.objects.filter(Sid=z).update(result2=r1,count2=c1)
            else :
                s=Student.objects.create(Sid=sid,name=" ",result2=score,result1=0,result3=0,count2=1,count1=0,count3=0)
                s.save()
            return render(request, 'Quiz/result.html', context)
    else:
            questions = QuesModel.objects.all()
            context = {
                'questions': questions
            }
            return render(request, 'Quiz/test1.html', context)


def test3(request):

    if request.method == 'POST':
            print(request.POST)
            questions = QuesModel.objects.all()
            score = 0
            wrong = 0
            correct = 0
            total = 0
            for q in questions:
                total += 1
                print(request.POST.get(q.question))
                print(q.ans)
                print()
                if q.ans == request.POST.get(q.question):
                    score += 10
                    correct += 1
                else:
                    wrong += 1
            percent = score / (total * 10) * 100
            context = {
                'score': score,
                'time': request.POST.get('timer'),
                'correct': correct,
                'wrong': wrong,
                'percent': percent,
                'total': total,

            }
            # Student.objects.
            # if z in
            print("Testing Z",z)
            print("Hiii",type((total)))
            t = Performance.objects.create(Sid=z, result=str(score))
            t.save()
            if Student.objects.filter(Sid=z):
                print("If ke andr")
                a=Student.objects.get(Sid=z)
                r1=float(a.result3)
                c1=int(a.count3)
                r1 = str((r1 + score)/(c1+1))
                c1=str(c1+1)
                s = Student.objects.filter(Sid=z).update(result3=r1,count3=c1)
            else :
                print("else ke andr")
                s=Student.objects.create(Sid=sid,name=" ",result3=score,result2=0,result1=0,count1=0,count2=0,count3=1)
                s.save()
            return render(request, 'Quiz/result.html', context)
    else:
            questions = QuesModel.objects.all()
            context = {
                'questions': questions
            }
            return render(request, 'Quiz/test1.html', context)





def performance(request):
    res = Performance.objects.filter(Sid=z)
    context = {
        'res' : res
    }
    return render(request, 'Quiz/performance.html',context)



