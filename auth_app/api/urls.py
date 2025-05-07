from django.urls import path
from .views import auth_test_view, RegistrationView, LoginView, EmailCheckView

urlpatterns = [
    path('', auth_test_view, name='auth-test'),  # delete!
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]

# POST "api/registration" (3/3)
#   - request body - check
#   - success response - check
#   - status codes (3/3) - check


# POST "api/login" (3/3)
#   - request body - check
#   - success response - check
#   - status codes (3/3) - check


# POST "api/email-check" (2/3)
#   - request body - check
#   - success response - check
#   - status codes (1/4) - ...

# clean coding (0/2) ...
