from django.urls import path
from .views import auth_test_view, RegistrationView, LoginView

urlpatterns = [
    path('', auth_test_view, name='auth-test'),  # delete!
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]

# POST "api/registration" (3/3)
#   - request body - check
#   - success response - check
#   - status codes (3/3) - check


# POST "api/login" (3/3)
#   - request body - check
#   - success response - check
#   - status codes (3/3) - check

# clean coding (0/2) ...
