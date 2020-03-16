from django.http import HttpResponse
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignupForm,admin_form
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from app1.models import CoepHostel
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from coep.utils import render_to_pdf
from math import ceil
from .forms import Preferenceform
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.http import JsonResponse
from django.template import loader


User = get_user_model()
from django.contrib.auth.decorators import login_required

@login_required
def profile(req):
    u=User.objects.get(username=req.user.username)
    return render(req,'profile/pages-profile.html',{'u':u})

@login_required
def preference(req):
    u=User.objects.get(username=req.user.username)
    return render(req,'profile/preferences.html',{'u':u})

@login_required    
def transaction(req):
    u=User.objects.get(username=req.user.username)
    return render(req,'profile/transaction.html',{'u':u})

def Home(request):
    return render(request,'index.html')

@login_required
def ProSet(request):
    u=User.objects.get(username=request.user.username)
    return render(request,'profile/settings.html',{'u':u})

@login_required
def edit(request):
    u=User.objects.get(username=request.user.username)
    return render(request,'profile/edit.html',{'u':u})


def admin_g(request):
    if request.method == 'POST':
        form = admin_form(request.POST)
        if form.is_valid():
            global no_stud_open
            global no_stud_obc
            global no_stud_minority
            global no_stud
            global no_rooms
            global r_date
            global p_date
            global f_date
            global ra_date
            global pay_date
            no_stud = request.POST.get("no_stud")
            r_date = request.POST.get("r_date")
            p_date = request.POST.get("p_date")
            f_date = request.POST.get("f_date")
            ra_date = request.POST.get("ra_date")
            pay_date =request.POST.get("pay_date")
            print(no_stud)
            print(r_date)
            print(p_date)
            print(f_date)
            print(ra_date)
            print(pay_date)
            no_stud1 = float(no_stud)
            no_stud_obc = ceil(no_stud1*0.19)
            no_stud_open = ceil(no_stud1*0.5)
            no_stud_minority = ceil(no_stud1*0.31)
            no_stud = int(no_stud1)
            no_rooms = no_stud
            return render(request, 'home.html', )
    else:
        form = admin_form()
    return render(request, 'profile/edit.html', {'form': form})

no_stud = 20
no_rooms = 20

def signup(request):
    if request.method == 'POST':
        print("Hello c")
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            global password
            password = request.POST.get("password1")
            password2= request.POST.get("password2")

            if password!=password2:
                con = "Password Doesn't Matched"
                return render(request,"signup.html",{'form':form,'con':con})

            # print(username)
            try:
                # print("username =", username)
                go = CoepHostel.objects.get(c_id=username)
                print(go.email)
                global email
                email = go.email
                #form.first_name = go.name
                year = go.year
                category = go.category
                gender = go.gender
                cet = go.cet
                branch = go.branch
                cgpa = go.cgpa
                name = go.name

            except CoepHostel.DoesNotExist:
               
                con = "College Id Does Not Exist"
                return render(request,"signup.html",{'form':form,'con':con})
            else:
                user=User( email=email ,year=year, name=name ,category=category, password=password ,gender=gender ,cet=cet ,cgpa=cgpa,username=username ,status=0 , branch=branch)
                #user.save(commit=False)
                
                user.set_password(password)
                print(user.category)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                err = "Please Confirm your E-Mail"
                return render(request,'registration/login.html',{"msg":err})
    else:
        form = SignupForm()
        print("sory")
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def catgy(yr , gen , br ):
    global c
    c = 0
    go1 = User.objects.all().filter(year=yr , gender=gen)
    go = go1.filter(branch=br).order_by('-cet')
    # gom1 = go[:10]
    # gom =  go.filter(category='MINORITY' ).exclude(id__in=[o.id for o in gom1])[:6]
    # gobc = go.filter(category='OBC' ).exclude(id__in=[o.id for o in gom1])[:4]
    gom1 = go[:no_stud_open]
    gom =  go.filter(category='MINORITY' ).exclude(id__in=[o.id for o in gom1])[:no_stud_minority]
    gobc = go.filter(category='OBC' ).exclude(id__in=[o.id for o in gom1])[:no_stud_obc]
    for i in gom1 :
        c += 1
        i.status = 1
        t = User.objects.get(username=i.username)
        t.status = 1
        t.save()
    for i in gom :
        c += 1
        i.status = 1
        t = User.objects.get(username=i.username)
        t.status = 1
        t.save()
    for i in gobc :
        c += 1
        i.status = 1
        t = User.objects.get(username=i.username)
        t.status = 1
        t.save()
    print(c)
    context = {
       "go" :gom1, "gom" : gom , "gobc" : gobc
    }
    return context


def catgy_w(yr , gen , br ):
    gom1=[]
    go1 = User.objects.all().filter(year=yr , gender=gen)
    go = go1.filter(branch=br ).order_by('-cet')
    for i in go :
        print(i.status)
        if i.status ==0 :
            gom1.append(i)
            print(gom1)
    context = {
       "go" :gom1, "gom" : {} , "gobc" : {}
    }
    return context


def catgy_f(yr , gen , br ):
    global c
    c = 0
    gom2 = []
    go1 = User.objects.all().filter(year=yr , gender=gen)
    go = go1.filter(branch=br).order_by('-cet')
    gom1 = go[:no_stud_open]
    gom =  go.filter(category='MINORITY' ).exclude(id__in=[o.id for o in gom1])[:no_stud_minority]
    gobc = go.filter(category='OBC' ).exclude(id__in=[o.id for o in gom1])[:no_stud_obc]
    for i in gom1 :
        c += 1
        i.status = 1
        t = User.objects.get(username=i.username)
        t.status = 1
        t.save()
    for i in gom :
        c += 1
        i.status = 1
        t = User.objects.get(username=i.username)
        t.status = 1
        t.save()
    for i in gobc :
        c += 1
        i.status = 1
        t = User.objects.get(username=i.username)
        t.status = 1
        t.save()
    for i in go :
        if c < no_stud and i.status==0:
            c += 1
            i.status = 1
            t = User.objects.get(username=i.username)
            t.status = 1
            t.save()
        else:
            break
    for i in go :
        if i.status ==1 :
            gom2.append(i)
            print(gom2)

    print(c)
    context = {
       "go" :gom2, "gom" : {} , "gobc" : {}
    }
    return context
@login_required
def fe_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('FE' ,'MALE' ,'MECH' )
    con2 = catgy('FE' ,'MALE' ,'COMP' )
    con3 = catgy('FE' ,'MALE' ,'IT' )
    con4 = catgy('FE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE BOYS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def fe_pdf_girls(request, *args, **kwargs):

    template = get_template('pdf/invoice.html')
    con1 = catgy('FE' ,'FEMALE' ,'MECH' )
    con2 = catgy('FE' ,'FEMALE' ,'COMP' )
    con3 = catgy('FE' ,'FEMALE' ,'IT' )
    con4 = catgy('FE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def se_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('SE' ,'MALE' ,'MECH' )
    con2 = catgy('SE' ,'MALE' ,'COMP' )
    con3 = catgy('SE' ,'MALE' ,'IT' )
    con4 = catgy('SE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def se_pdf_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('SE' ,'FEMALE' ,'MECH' )
    con2 = catgy('SE' ,'FEMALE' ,'COMP' )
    con3 = catgy('SE' ,'FEMALE' ,'IT' )
    con4 = catgy('SE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def te_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('TE' ,'MALE' ,'MECH' )
    con2 = catgy('TE' ,'MALE' ,'COMP' )
    con3 = catgy('TE' ,'MALE' ,'IT' )
    con4 = catgy('TE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def te_pdf_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('TE' ,'FEMALE' ,'MECH' )
    con2 = catgy('TE' ,'FEMALE' ,'COMP' )
    con3 = catgy('TE' ,'FEMALE' ,'IT' )
    con4 = catgy('TE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def be_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('BE' ,'MALE' ,'MECH' )
    con2 = catgy('BE' ,'MALE' ,'COMP' )
    con3 = catgy('BE' ,'MALE' ,'IT' )
    con4 = catgy('BE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "type" : 'BE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def be_pdf_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('BE' ,'FEMALE' ,'MECH' )
    con2 = catgy('BE' ,'FEMALE' ,'COMP' )
    con3 = catgy('BE' ,'FEMALE' ,'IT' )
    con4 = catgy('BE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'BE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

#waiting

@login_required
def fe_pdf_w_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_w('FE' ,'MALE' ,'MECH' )
    con2 = catgy_w('FE' ,'MALE' ,'COMP' )
    con3 = catgy_w('FE' ,'MALE' ,'IT' )
    con4 = catgy_w('FE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE BOYS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def fe_pdf_w_girls(request, *args, **kwargs):

    template = get_template('pdf/invoice.html')
    con1 = catgy_w('FE' ,'FEMALE' ,'MECH' )
    con2 = catgy_w('FE' ,'FEMALE' ,'COMP' )
    con3 = catgy_w('FE' ,'FEMALE' ,'IT' )
    con4 = catgy_w('FE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def se_pdf_w_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_w('SE' ,'MALE' ,'MECH' )
    con2 = catgy_w('SE' ,'MALE' ,'COMP' )
    con3 = catgy_w('SE' ,'MALE' ,'IT' )
    con4 = catgy_w('SE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def se_pdf_w_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_w('SE' ,'FEMALE' ,'MECH' )
    con2 = catgy_w('SE' ,'FEMALE' ,'COMP' )
    con3 = catgy_w('SE' ,'FEMALE' ,'IT' )
    con4 = catgy_w('SE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def te_pdf_w_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_w('TE' ,'MALE' ,'MECH' )
    con2 = catgy_w('TE' ,'MALE' ,'COMP' )
    con3 = catgy_w('TE' ,'MALE' ,'IT' )
    con4 = catgy_w('TE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def te_pdf_w_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_w('TE' ,'FEMALE' ,'MECH' )
    con2 = catgy_w('TE' ,'FEMALE' ,'COMP' )
    con3 = catgy_w('TE' ,'FEMALE' ,'IT' )
    con4 = catgy_w('TE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def be_pdf_w_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_w('BE' ,'MALE' ,'MECH' )
    con2 = catgy_w('BE' ,'MALE' ,'COMP' )
    con3 = catgy_w('BE' ,'MALE' ,'IT' )
    con4 = catgy_w('BE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "type" : 'BE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def be_pdf_w_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_w('BE' ,'FEMALE' ,'MECH' )
    con2 = catgy_w('BE' ,'FEMALE' ,'COMP' )
    con3 = catgy_w('BE' ,'FEMALE' ,'IT' )
    con4 = catgy_w('BE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'BE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")




#finallist

@login_required
def fe_pdf_f_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('FE' ,'MALE' ,'MECH' )
    con2 = catgy_f('FE' ,'MALE' ,'COMP' )
    con3 = catgy_f('FE' ,'MALE' ,'IT' )
    con4 = catgy_f('FE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE BOYS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def fe_pdf_f_girls(request, *args, **kwargs):

    template = get_template('pdf/invoice.html')
    con1 = catgy_f('FE' ,'FEMALE' ,'MECH' )
    con2 = catgy_f('FE' ,'FEMALE' ,'COMP' )
    con3 = catgy_f('FE' ,'FEMALE' ,'IT' )
    con4 = catgy_f('FE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def se_pdf_f_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('SE' ,'MALE' ,'MECH' )
    con2 = catgy_f('SE' ,'MALE' ,'COMP' )
    con3 = catgy_f('SE' ,'MALE' ,'IT' )
    con4 = catgy_f('SE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def se_pdf_f_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('SE' ,'FEMALE' ,'MECH' )
    con2 = catgy_f('SE' ,'FEMALE' ,'COMP' )
    con3 = catgy_f('SE' ,'FEMALE' ,'IT' )
    con4 = catgy_f('SE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def te_pdf_f_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('TE' ,'MALE' ,'MECH' )
    con2 = catgy_f('TE' ,'MALE' ,'COMP' )
    con3 = catgy_f('TE' ,'MALE' ,'IT' )
    con4 = catgy_f('TE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def te_pdf_f_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('TE' ,'FEMALE' ,'MECH' )
    con2 = catgy_f('TE' ,'FEMALE' ,'COMP' )
    con3 = catgy_f('TE' ,'FEMALE' ,'IT' )
    con4 = catgy_f('TE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def be_pdf_f_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('BE' ,'MALE' ,'MECH' )
    con2 = catgy_f('BE' ,'MALE' ,'COMP' )
    con3 = catgy_f('BE' ,'MALE' ,'IT' )
    con4 = catgy_f('BE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "type" : 'BE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def be_pdf_f_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('BE' ,'FEMALE' ,'MECH' )
    con2 = catgy_f('BE' ,'FEMALE' ,'COMP' )
    con3 = catgy_f('BE' ,'FEMALE' ,'IT' )
    con4 = catgy_f('BE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'BE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

#preferences

class PreferenceClass(CreateView):
    template_name ='profile/preferences.html'
    form_class =Preferenceform
    
    def get(self,request):
        form=Preferenceform()
        i=request.user.username
        u=User.objects.get(username=i)
        p1=User.objects.filter(username=u.pref1)
        p2=User.objects.filter(username=u.pref2)
        p3=User.objects.filter(username=u.pref3)
        if u.pref1 or u.pref2 or u.pref3:
            print("hello")
            return redirect( '/submitpreference/' ,)
        return render(request ,'profile/preferences.html',{'form':form})    
        

    def post(self ,request):
        template = loader.get_template(self.template_name)
        query1 = request.POST.get('n1')
        query2 = request.POST.get('n2')
        print("query2", query2)
        query3 = request.POST.get('n3')
        print( "query3", query3)
        student1 = User.objects.filter(name__istartswith=query1)
        student2 = User.objects.filter(name__istartswith=query2)
        student3 = User.objects.filter(name__istartswith=query3)
        
        
        context = {'list1':student1 ,'list2':student2 ,'list3':student3 ,'query1':query1 ,'query2':query2 ,'query3':query3  }
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template, content_type='text/html')

class SearchAjaxSubmitView(PreferenceClass):
    template = 'profile/preferences.html'
    response_message = 'This is the AJAX response'
# Create your views here.

def prefer(request):
    if request.method=='POST':
        form  = Preferenceform(request.POST)
        pref1 = request.POST.get('n1')
        temp1=(pref1.split('|')[0])

        pref2 = request.POST.get('n2')
        temp2=(pref2.split('|')[0])


        pref3 = request.POST.get('n3')
        temp3=(pref3.split('|')[0])
        if temp1==request.user.username or temp2==request.user.username or temp3==request.user.username:
            err ="You Can't Enter Your Own Name "
            return render(request ,'profile/preferences.html' ,{'form':form ,"err":err})
        if request.user.pref1 or request.user.pref2 or request.user.pref3:
            err ="You Have Already Submitted Your Preference"
            i=request.user.username
            u=User.objects.get(username=i)
            p1=User.objects.get(username=u.pref1)
            p2=User.objects.get(username=u.pref2)
            p3=User.objects.get(username=u.pref3)
                    
            return render(request ,'profile/preferences.html' ,{'form':form ,"err":err ,'u':u ,'p1':p1.name ,'p2':p2.name ,'p3':p3.name })


        if temp1==temp2 or temp2==temp3 or temp2==temp3 :
            err ="Don't Enter Repeated Entries "
            return render(request ,'profile/preferences.html' ,{'form':form ,"err":err})
        p1 =get_object_or_404(User, username=temp1)
        p2 = get_object_or_404(User,username=temp2)
        p3 =get_object_or_404(User,username=temp3)
        if p3 == None or p2 == None or p1 == None:
            err ="Student With Perticular Id Is Not Selected"
            return render(request ,'profile/preferences.html' ,{'form':form ,"err":err})
        print("user" ,request.user.username)
        request.user.pref1 =p1.username
        request.user.pref2 =p2.username
        request.user.pref3 =p3.username
        request.user.save()
        err="Submitted Preference"
        return redirect('/submitpreference/',{'err':err})
    else:
        form = Preferenceform()
        i=request.user.username
        u=User.objects.get(username=i)
        p1=User.objects.get(username=u.pref1)
        p2=User.objects.get(username=u.pref2)
        p3=User.objects.get(username=u.pref3)
        return render(request ,'profile/preferences.html',{'form':form ,'p1':p1.name,'p2':p2.name ,'p3':p3.name ,'u':u })


def schedule(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy_f('BE' ,'FEMALE' ,'MECH' )
    con2 = catgy_f('BE' ,'FEMALE' ,'COMP' )
    con3 = catgy_f('BE' ,'FEMALE' ,'IT' )
    con4 = catgy_f('BE' ,'FEMALE' ,'PLANNING0')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'BE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def cancellation(request):
    
    if request.method=='POST':
        id=request.user.id
        print(id)
        User.objects.get(pk=id).delete()
    return HttpResponse("deleted user")

def allocation(yr , gen , br ):
    global c
    c = 0
    gom2 = []
    go1 = User.objects.all().filter(year=yr , gender=gen)
    go = go1.filter(branch=br).order_by('-cet')
    for i in go :
        if i.status == 1 :
            gom2.append(i)
    context = {
       "go" :gom2
    }
    return context

@login_required
def fe_room_boys(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('FE','MALE','COMP')
    con1 = allocation('FE','MALE','IT')
    con2 = allocation('FE','MALE','MECH')
    con3 = allocation('FE','MALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='FE' , gender='MALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='MALE',year='FE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'FE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
def fe_room_girls(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('FE','FEMALE','COMP')
    con1 = allocation('FE','FEMALE','IT')
    con2 = allocation('FE','FEMALE','MECH')
    con3 = allocation('FE','FEMALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='FE' , gender='FEMALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='FEMALE',year='FE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'FE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def se_room_boys(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('SE','MALE','COMP')
    con1 = allocation('SE','MALE','IT')
    con2 = allocation('SE','MALE','MECH')
    con3 = allocation('SE','MALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='SE' , gender='MALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='MALE',year='SE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'SE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")



def se_room_girls(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('SE','FEMALE','COMP')
    con1 = allocation('SE','FEMALE','IT')
    con2 = allocation('SE','FEMALE','MECH')
    con3 = allocation('SE','FEMALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='SE' , gender='FEMALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='FEMALE',year='SE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'SE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def te_room_boys(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('TE','MALE','COMP')
    con1 = allocation('TE','MALE','IT')
    con2 = allocation('TE','MALE','MECH')
    con3 = allocation('TE','MALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='TE' , gender='MALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='MALE',year='TE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'TE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
@login_required
def te_room_girls(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('TE','FEMALE','COMP')
    con1 = allocation('TE','FEMALE','IT')
    con2 = allocation('TE','FEMALE','MECH')
    con3 = allocation('TE','FEMALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='TE' , gender='FEMALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='FEMALE',year='TE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'TE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
def be_room_boys(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('BE','MALE','COMP')
    con1 = allocation('BE','MALE','IT')
    con2 = allocation('BE','MALE','MECH')
    con3 = allocation('BE','MALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='BE' , gender='MALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='MALE',year='BE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'BE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def be_room_girls(request):
    v = 1
    k = 0
    l = 0
    m = 0
    n = 0
    con = allocation('BE','FEMALE','COMP')
    con1 = allocation('BE','FEMALE','IT')
    con2 = allocation('BE','FEMALE','MECH')
    con3 = allocation('BE','FEMALE','PLANNING')
    d=con['go']
    d1=con1['go']
    d2=con2['go']
    d3=con3['go']
    c = len(d)
    c1 = len(d1)
    c2 = len(d2)
    c3 = len(d3)
    for j in range(no_stud): #no of students
        if k < c and v <= no_rooms:#no of rooms
            if d[j].astatus == 0:
                d[j].astatus = 1
                d[j].roomno = v
                t = User.objects.get(username=d[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d[j].pref1 != 0 :
                    a1 = d[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d[j].pref2 != 0 :
                        a2 = d[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d[j].pref3 != 0 :
                            a3 = d[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            k += 1

        if l < c1 and v <= no_rooms:
            if d1[j].astatus == 0:
                d1[j].astatus = 1
                d1[j].roomno = v
                t = User.objects.get(username=d1[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d1[j].pref1 != 0 :
                    a1 = d1[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d1[j].pref2 != 0 :
                        a2 = d1[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d1[j].pref3 != 0 :
                            a3 = d1[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            l += 1

        if m < c2 and v <= no_rooms:
            if d2[j].astatus == 0:
                d2[j].astatus = 1
                d2[j].roomno = v
                t = User.objects.get(username=d2[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d2[j].pref1 != 0 :
                    a1 = d2[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d2[j].pref2 != 0 :
                        a2 = d2[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d2[j].pref3 != 0 :
                            a3 = d2[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            m += 1

        if n < c3 and v <= no_rooms:
            if d3[j].astatus == 0:
                d3[j].astatus = 1
                d3[j].roomno = v
                t = User.objects.get(username=d3[j].username)
                t.astatus = 1
                t.roomno = v
                t.save()
                if d3[j].pref1 != 0 :
                    a1 = d3[j].pref1
                    print(a1)
                    u1 = User.objects.get(username=a1)
                    if u1.astatus == 0 :
                        u1.astatus = 1
                        u1.roomno = v
                        u1.save()
                    if d3[j].pref2 != 0 :
                        a2 = d3[j].pref2
                        print(a2)
                        u2 = User.objects.get(username=a2)
                        if u2.astatus == 0 :
                            u2.astatus = 1
                            u2.roomno = v
                            u2.save()
                        if d3[j].pref3 != 0 :
                            a3 = d3[j].pref3
                            print(a3)
                            u3 = User.objects.get(username=a3)
                            if u3.astatus == 0 :
                                u3.astatus = 1
                                u3.roomno = v
                                u3.save()
                v += 1
            n += 1

    g1 = User.objects.all().filter(year='BE' , gender='FEMALE')
    for i in range(no_rooms):#no of rooms
        o = 4
        for j in g1 :
            if j.roomno == i+1 and j.astatus==1 :
                o -= 1
        for p in range(o) :
            f = 0
            for j in g1 :
                if f != 1 :
                    if j.roomno == 0 and j.astatus==0 :
                        j.roomno = i+1
                        t = User.objects.get(username=j.username)
                        t.roomno = i+1
                        t.astatus = 1
                        t.save()
                        f += 1
    template = get_template('pdf/room_allotment.html')
    con1 = []
    gom = User.objects.all().filter(astatus=1,gender='FEMALE',year='BE')
    for i in range(20) :
        for j in gom :
            if j.roomno == i+1 :
                con1.append(j)
    context = {
        "con1" : con1  , "types": 'BE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/room_allotment.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("room_allotment")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")