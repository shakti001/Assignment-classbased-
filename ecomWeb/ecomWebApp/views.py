from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import DeleteView
from .forms import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login

User = get_user_model()


class SignUpView(CreateView):  
    template_name = 'userpanel/auth/signup.html'
    model = User  
    form_class = UserForm
    
    def get_success_url(self):
        messages.success(self.request , "Please Login !!!")
        return reverse_lazy('login')

class MyLoginView(LoginView):
    template_name = 'userpanel/auth/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                messages.error(self.request, "Invalid email and password !!!!!!!")
                return super().form_invalid(form)   
            else:
                login(self.request, self.user_cache)
                messages.success(self.request, "Welcome Login Success !!!!!!!")
                return super().form_valid(form)    
        else:
            return super().form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong !!!!")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return self.success_url
    
class HomePageView(ListView):
    template_name = 'userpanel/index.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "userpanel/product/shop-detail.html"
    context_object_name = 'product'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_data'] = self.object.product_tag_set.all()
        return context

class AddToCartView(CreateView):
    model = CartProduct
    form_class = CartProductForm
    def post(self, request, *args, **kwargs):
        try:
            form = self.get_form()
            if form.is_valid():
                qty = form.cleaned_data['qty']
                product_id = form.cleaned_data['product_id']
                user_id = form.cleaned_data['user_id']
                product_price = request.POST.get('product_price')
                if qty and product_id and user_id is not None:
                    if CartProduct.objects.filter(product_id=product_id.id, user_id=user_id.id).exists():
                        return JsonResponse({'status': 'error', 'message': 'Product already in cart'})
                    total = int(qty) * int(product_price)
                    self.object = self.model.objects.create(
                        qty=qty,
                        product_id=product_id,
                        user_id=user_id,
                        total_amount=total
                    )
                    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
            else:
                
                return JsonResponse({'status': 'error', 'message': 'PLease Login First'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'})

class CartListView(ListView):
    model = CartProduct
    template_name = 'userpanel/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return CartProduct.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_total = CartProduct.objects.filter(user_id=self.request.user.id).aggregate(Sum('total_amount'))
        context['cartTotal'] = cart_total
        return context

class RemoveCartItemsView(DeleteView):
    model = CartProduct
    success_url = '/cart'

class MyLogoutView(LoginRequiredMixin, LogoutView):
    success_url = '/'
    
    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You have been logged out successfully.")
        return HttpResponseRedirect(self.success_url)
        
class Error404(TemplateView):
    template_name = 'userpanel/404.html'
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404  # Set the status code to 404
        return response


