from django.shortcuts import HttpResponse, render
from django.views.generic import TemplateView, View, FormView
from .forms import ContactForm, RegisterForm, UserLogin
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()


class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['ahmed'] = 'Ahmed & Ronny & Joe'
        context['joe'] = 'Joe is a good boy (sometimes not always!)'
        context['header'] = 'Hi! Welcome to my e-commerce app'
        print (context)
        return context

# class Contact(View):
#     template_name = 'contact.html'
#     def get_context_data(self, **kwargs):
#         context = super(Contact, self).get_context_data(**kwargs)
#         context['content'] = 'Enter your contact'
#         print (context)
#         return context
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})
#
#     def post(self, request, *args, **kwargs):
#         data = request.POST
#         print (data['email'], data.get('full_name'), request.path, "   ", request.META['SERVER_PORT'])
#         return render(request, 'home.html', {'ahmed': data['email']})


class Contact(FormView):
    template_name = 'form.html'
    form_class = ContactForm
    # success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(Contact, self).get_context_data(**kwargs)
        context['content'] = 'Enter your contact'
        context['header'] = 'Welcome to the contact form'
        # print (context)
        return context


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = request.POST
            return render(request, 'home.html', {'ahmed': data['email']})
        else:
            return self.form_invalid(form)





class RegisterView(FormView):
    template_name = 'form.html'
    form_class    = RegisterForm
    # success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['content'] = 'Register new user'
        return context



    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # data = request.POST
            user_name   = form.cleaned_data.get('user_name')
            first_name  = form.cleaned_data.get('first_name')
            last_name   = form.cleaned_data.get('last_name')
            email       = form.cleaned_data.get('email')
            password    = form.cleaned_data.get('password')

            new_user    = User.objects.create_user(username = user_name,
                                               password = password,
                                               email = email,
                                               first_name = first_name,
                                               last_name = last_name)
            return render(request, 'home.html', {'ahmed': 'Thanks {0}'.format(user_name)})
        else:
            return self.form_invalid(form)




class LoginView(FormView):
    template_name = 'form.html'
    form_class = UserLogin
    # success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['content'] = 'Login please'
        # print (context)
        return context


    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            # data = request.POST
            username = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if not user == None:
                login(request, user)
                print(request.POST)
                return render(request, 'home.html', {'ahmed': username})
            else:
                return render(request, 'home.html', {'ahmed': "NO SUCH USER YOU'RE ASSHOLE!"})

        else:
            return self.form_invalid(form)
