from django import forms
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from pages.models import Media,Field,WorkerInfo,Job,UserInfo


def isWorker(request):
    if not request.user.is_authenticated():
        return False
    return WorkerInfo.objects.filter(user=request.user).count() > 0

# Create your views here.
def login(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('categorylist')
        else:
            return render(request,'login.html',{'message':'Invalid login'})
    else:
        return render(request, 'login.html')

def home(request):
    template = loader.get_template('home.html')
    context = RequestContext(request, {
        'isworker': isWorker(request),
        'title': "Sahayak",
        'mainmenuindex': 1,
    })

    return HttpResponse(template.render(context))

class SignupForm(forms.Form):
    firstname = forms.CharField(
        required=True,
        max_length = 20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required':'required'
            },
        ),
        error_messages={'required': "You must enter your First Name."}
    )

    lastname = forms.CharField(
        required=True,
        max_length = 20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required':'required'
            },
        ),
        error_messages={'required': "You must enter your Last Name."}
    )

    username = forms.CharField(
        required=True,
        min_length=5,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required':'required'
            },
        ),
        error_messages={'required': "You must enter a Username."}
    )

    password = forms.CharField(
        required=True,
        min_length=5,
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter you password',
                'required':'required',
            },
        ),
        error_messages={'required': "You must enter a Password."}
    )

    email = forms.EmailField(
        label='Your Email',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required':'required'
            },
        ),
    )

    latitude = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required':'required',
                'readonly':''
            },
        ),
    )

    longitude = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required':'required',
                'readonly':''
            },
        ),
    )


def signup(request):
        if(request.method=='POST'):
            form = SignupForm(request.POST)
            if form.is_valid():
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                latitude = request.POST['latitude']
                longitude = request.POST['longitude']

                # check if the username or email is already registered
                user = auth.models.User.objects.create_user(username, email, password)
                user.first_name=firstname
                user.last_name=lastname
                user.save()

                userinfo = UserInfo(user=user,latitude=latitude,longitude=longitude)
                userinfo.save()

                user = auth.authenticate(username=username, password=password)
                return HttpResponse('User created')
        else:
            form=SignupForm()
            return render(request,'signup.html',{'form':form})

def categorylist(request):
    template = loader.get_template('categories.html')

    categories = Field.objects.all()

    context = RequestContext(request, {
        'isworker': isWorker(request),
        'title': "Categories : Sahayak",
        'mainmenuindex': 2,
        'categories': categories,
    })

    return HttpResponse(template.render(context))


def categorypage(request, category_name):

    category = get_object_or_404(Field, slug=category_name)
    workers = WorkerInfo.objects.filter(field=category)

    template = loader.get_template('categorypage.html')
    context = RequestContext(request, {
        'title': "All workers working in category "+category.name,
        'mainmenuindex': 2,
        'category': category,
        'workers': workers,
        'isworker': isWorker(request),
    })

    return HttpResponse(template.render(context))


def workerpage(request, worker_number):
    worker = get_object_or_404(WorkerInfo, pk=worker_number)
    userinfo = UserInfo.objects.get(user=worker.user)
    template = loader.get_template('workerpage.html')

    comments = []
    commentobj = Job.objects.filter(worker=worker, status=Job.COMPLETED)
    for comobj in commentobj:
        if len(comobj.ratingtext) > 2:
            comment = {}
            comment["comment"] = comobj.ratingtext
            comment["by"] = comobj.customer.first_name+" "+comobj.customer.last_name
            comment["rating"] = comobj.rating
            comments.append(comment)

    commentscount = len(comments)

    context = RequestContext(request, {
        'title': "Info about  "+worker.getname(),
        'mainmenuindex': 2,
        'worker': worker,
        'comments': comments,
        'commentscount': commentscount,
        'userinfo': userinfo,
        'isworker': isWorker(request),
    })

    return HttpResponse(template.render(context))

class HireForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(HireForm, self).__init__(*args, **kwargs)

    subject = forms.CharField(
        label='Enter Title of Job',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'eg: Sink needs fixing'
            }
        ),
        error_messages={'required': "You must enter a title for your job."}
    )

    description = forms.CharField(
        label='Description of the job',
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        error_messages={'required': "You must enter a description for your job."}
    )

def hireworker(request, worker_number):
    worker = get_object_or_404(WorkerInfo, pk=worker_number)
    userinfo = UserInfo.objects.get(user=worker.user)
    template = loader.get_template('hireworker.html')

    created = False

    if request.method == 'POST':  # If the form has been submitted...
        form = HireForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            # Save the object
            job = Job(
                customer=request.user,
                worker=worker,
                title=subject,
                description=description,
                status=Job.AWAITING,
            )
            job.save()
            created=True
    else:
        form = HireForm()

    context = RequestContext(request, {
        'title': "Hire  "+worker.getname(),
        'mainmenuindex': 2,
        'worker': worker,
        'userinfo': userinfo,
        'form': form,
        'success': created,
        'isworker': isWorker(request),
    })

    return HttpResponse(template.render(context))


def myjobs(request):
    template = loader.get_template('myjobs.html')

    myjobs = Job.objects.filter(customer = request.user)

    context = RequestContext(request, {
        'title': "My Jobs",
        'mainmenuindex': 3,
        'jobs': myjobs,
        'isworker': isWorker(request),
    })

    return HttpResponse(template.render(context))
