from django import forms
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404

def home(request):
    template = loader.get_template('home.html')
    context = RequestContext(request, {
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


def signup(request):
	if(request.method=='POST'):
		form = SignupForm(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			
			# check if the username or email is already registered
			user = auth.models.User.objects.create_user(username, email, password)
			user.first_name=firstname
			user.last_name=lastname
			user.save()

			user = auth.authenticate(username=username, password=password)
			return HttpResponse('User created')
	else:
		form=SignupForm()
		return render(request,'signup.html',{'form':form})
