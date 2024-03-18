
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from adminApp import views
from .views import *

urlpatterns = [

    path('', AdminLoginView.as_view(), name="admin-login"),
    path('logout/', AdminLogoutView.as_view(), name='admin-logout'),
    path('home/', HomeView.as_view(), name="admin-home"),
    path('change-password/<slug>', ChangePasswordView.as_view(), name="change-password"),
    path('forgot-password/', ForgotPasswordView.as_view() , name="forgot-password"),
    path('otp-verify/<slug>/', OtpVerifyView.as_view() , name="otp-verify"),
    path('forgot-password-form/<slug>/', ForgotPasswordFormView.as_view(), name="forgot-password-form"),
    path('category/', CategoryListView.as_view(), name="category-list"),
    path('add-category/', AddCategoryView.as_view(), name='add-category'),
    path('edit-category/<slug>', EditCategoryView.as_view(), name="edit-category"),
    path('delete-category/<slug>', DeleteCategoryView.as_view(), name="delete-category"),
    path('tags/', TagsListView.as_view(), name="tags"),
    path('add-tags/', AddTagsView.as_view(), name='add-tags'),
    path('edit-tags/<slug>', EditTagsView.as_view(), name="edit-tags"),
    path('delete-tags/<slug>', DeleteTagsView.as_view(), name="delete-tags"),
    path('product/', ProductListView.as_view(), name="product"),
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('edit-product/<slug>', EditProductView.as_view(), name="edit-product"),
    path('delete-product/<slug>/', DeleteProductView.as_view(), name="delete-product"),


    

    

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    


    





]
