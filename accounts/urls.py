from django.urls import path
from .views import UserProfileView, edit_Profile, user_register, SignupView #SignUpSuccessView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', UserProfileView, name='user-profile'),
    path('profile/edit/', edit_Profile, name='edit_profile'),
    path('signup/', user_register, name='user_register'),
    # path('signup_done/', register_done, name='register_done'),
    path('signup/', SignupView.as_view(), name='signup'),
    # path('signup/succes/', SignUpSuccessView.as_view(), name='signup_succes'),



]
