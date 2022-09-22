from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.views import generic
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import User
from .forms import NewUserForm, EditProfileForm

class RegisterView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = NewUserForm
    success_url = reverse_lazy('login')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
            
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

        return redirect(self.get_success_url())



# Forgot Password (TODO)
def forgot_password(request):
    context = {}
    return render(request=request, template_name="registration/forgot-password.html")


# Profile
class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('profile') # Redirect to index after 

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super(ProfileView, self).post(request, *args, **kwargs)
    
    def get_object(self, **kwargs):
        return self.request.user





class RegisterViewAdmin(generic.FormView):
    template_name = 'registration/register.html'
    form_class = NewUserForm
    success_url = reverse_lazy('login')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('/')
            
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

        return redirect(self.get_success_url())