from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect
from ecomWebApp.models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User, auth
from ecomWebApp.helpers import *
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.generic import *
from django.contrib.auth.views import *
from django.contrib.auth import authenticate, login
from .form import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.hashers import check_password


# Create your views here.

class AdminLoginView(LoginView):
    template_name = 'admin/auth/login.html'
    form_class = adminLoginForm
    
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
    
            if self.user_cache is None:
                messages.error(self.request, "Invalid email and password !!!!!!!")
                return super().form_invalid(form)   
            elif self.user_cache.is_superuser == True:
                login(self.request, self.user_cache)
                messages.success(self.request, "Welcome Login Success !!!!!!!")
                return super().form_valid(form)
            else:
                messages.error(self.request, "Invalid email and password !!!!!!!")
                return super().form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong !!!!")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('admin-home')

class AdminLogoutView(LoginRequiredMixin, LogoutView):
    login_url = '/admin'
    success_url = '/admin'
    
    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You have been logged out successfully.")
        return HttpResponseRedirect(self.success_url)

class HomeView(LoginRequiredMixin,ListView):
    login_url = '/admin'
    template_name = 'admin/home/index.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(is_superuser = False).count()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.all().count()
        return context

class ForgotPasswordView(PasswordResetView):
    template_name = "admin/auth/forgotpassword.html"
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        otp = generateOTP()
        user = User.objects.get(email=email)
        if user:
            if user.is_superuser == True:
                slug = user.slug
                user.Otp = otp
                user.save()
                success_url = reverse_lazy('otp-verify' , kwargs={'slug': slug})
                messages.success(self.request, "Please Enter Otp Here !!!")
                return HttpResponseRedirect(success_url)
            else:
                messages.error(self.request, "Invalid Email id !!!!")
                return super().form_invalid(form)
        else:
            messages.error(self.request, "Invalid Email id !!!!")
            return super().form_invalid(form)
            
    def form_invalid(self, form):
        messages.error(self.request, "Invalid Email id !!!!")
        return super().form_invalid(form)
    
class OtpVerifyView(FormView):
    template_name = 'admin/auth/otp-verify.html'
    form_class = OtpMatchForm

    def form_valid(self, form):
        otp = form.cleaned_data['otp']
        slug = self.kwargs['slug']
        user = User.objects.get(slug=slug)
        if user:
            if user.Otp == otp:
                user.Otp = ""
                user.save()
                success_url = reverse_lazy('forgot-password-form' , kwargs={'slug': slug})
                messages.success(self.request, "Please enter new password !!!")
                return HttpResponseRedirect(success_url)
            else:
                messages.error(self.request, "Otp does not match")
                return super().form_invalid(form)
        else:
            messages.error(self.request, "Otp does not match")
            return super().form_invalid(form)
        
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong !!!!!")
        return super().form_invalid(form)
    
class ForgotPasswordFormView(FormView):
    template_name = 'admin/auth/forgotpasswordform.html'
    form_class = forgotPasswordForm
    success_url = '/admin'
    
    def form_valid(self, form):
        slug = self.kwargs['slug']
        new_password = form.cleaned_data['new_password']
        cnf_new_password = form.cleaned_data['cnf_new_password']
        user = User.objects.get(slug=slug)
        if user:
            if new_password == cnf_new_password:
                user.password = make_password(new_password)
                user.save()
                messages.success(self.request, "Password has been change pls login !!!!!")
                return HttpResponseRedirect(self.success_url)
            else:
                messages.error(self.request, "Password and Confirm password does not match !!!!!")
                return super().form_invalid(form)
        else:
            messages.error(self.request, "password and confirm password does not match !!!!!")
            return super().form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
 
class CategoryListView(LoginRequiredMixin,ListView):
    template_name = 'admin/category/category.html'
    model = Category
    context_object_name = 'category'
    login_url = '/admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddCategoryView(LoginRequiredMixin,CreateView):
    login_url = '/admin'
    model = Category
    template_name = "admin/category/add_category.html"
    form_class = addCategoryForm
    success_url = '/admin/add-category'

    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent_id__isnull=True)
        return context
    
    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        return JsonResponse({'status': 'success', 'message': 'Category created successfully'})
    
    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'message': 'Something went wrong'})
    
class EditCategoryView(LoginRequiredMixin,UpdateView): 
    login_url = '/admin'
    model = Category
    fields = ["name", "parent"]
    
    template_name = 'admin/category/edit-category.html'
   

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context =  super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent_id__isnull=True)
        context['subCategory'] = Category.objects.get(slug=slug)
        return context
    
    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('edit-category', kwargs={'slug': slug})

class DeleteCategoryView(LoginRequiredMixin,DeleteView):
    login_url = '/admin'
    model = Category
    success_url = "/admin/category"

class TagsListView(LoginRequiredMixin,ListView):
    login_url = '/admin'
    template_name = 'admin/tags/tags.html'
    model = Tags
    context_object_name = 'tags'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddTagsView(LoginRequiredMixin, CreateView):
    login_url = '/admin'
    template_name = 'admin/tags/add_tags.html'
    model = Tags
    form_class = AddTagsForm
    success_url = '/admin/add-tags'
    

    def form_valid(self, form):
        tags = form.save(commit=False)
        tags.save()
        messages.success(self.request, "Tag Created sucessfully !!!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "something went wrong")
        return super().form_invalid(form)

class EditTagsView(LoginRequiredMixin,UpdateView):
    login_url = '/admin'
    model = Tags
    fields = ["name"]
    template_name = 'admin/tags/edit_tags.html'
    
    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context =  super().get_context_data(**kwargs)
        context['tags'] = Tags.objects.get(slug=slug)
        return context
    
    def get_success_url(self):
        slug = self.kwargs['slug']
        messages.success(self.request, "Tags update successfully !!!!")
        return reverse_lazy('edit-tags', kwargs={'slug': slug})

class DeleteTagsView(LoginRequiredMixin,DeleteView):
    login_url = '/admin'
    model = Tags
    success_url = '/admin/tags'

class ProductListView(LoginRequiredMixin,ListView):
    login_url = '/admin'
    template_name = 'admin/product/product.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
   
class AddProductView(LoginRequiredMixin,CreateView):
    login_url = '/admin'
    template_name = "admin/product/add_product.html"
    model = Product
    form_class = AddProductForm
    success_url = '/admin/product'
    
    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        return JsonResponse({'status': 'success', 'message': 'Product Created sucessfully !!!'})
    
    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'message': 'Something went wrong !!!'})
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent_id__isnull=True)
        context['tags'] = Tags.objects.all()
        return context

class EditProductView(LoginRequiredMixin,UpdateView):
    login_url = '/admin'
    model = Product
    fields = ['category', 'name', 'image', 'stock', 'price']
    template_name = 'admin/product/edit-product.html'
    
    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context =  super().get_context_data(**kwargs)
        context['data'] = Product.objects.get(slug=slug)
        context['tags'] = Tags.objects.all()
        context['tag_data'] = self.object.product_tag_set.all()
        context['category'] = Category.objects.filter(parent_id__isnull=True)
        return context
    
    def get_success_url(self):
        slug = self.kwargs['slug']
        messages.success(self.request, "Product update successfully !!!!")
        return reverse_lazy('edit-product', kwargs={'slug': slug})

class DeleteProductView(LoginRequiredMixin,DeleteView):
    login_url = '/admin'
    model = Product
    success_url = '/admin/product'

class ChangePasswordView(PasswordChangeView):
    template_name = 'admin/profile/change-password.html'
     
    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password1']
        new_password2 = form.cleaned_data['new_password2']
        slug = self.kwargs['slug']
        if old_password:
            user_password = User.objects.get(slug = slug)
            if check_password(old_password, user_password.password):
                if new_password == new_password2:
                    user_password.password = make_password(new_password)
                    user_password.save()
                    return super().form_valid(form)
                else:
                    return super().form_invalid(form)
            else:
                return super().form_invalid(form)
        else:
            return super().form_invalid(form)
    
    def form_invalid(self , form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        slug = self.kwargs['slug']
        messages.success(self.request, "password change successfully !!!!")
        return reverse_lazy('change-password', kwargs={'slug': slug})
