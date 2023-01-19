"""为应用程序users定义URL模式"""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns =[
    # 包含默认的身份验证url--/users/login属于默认url，所以与''相匹配
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register')
]
