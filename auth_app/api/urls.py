from django.urls import path
from .views import auth_test_view, RegistrationView

urlpatterns = [
    path('', auth_test_view, name='auth-test'),  # delete!
    path('registration', RegistrationView.as_view(), name='registration'),
]

# POST "api/registration" (3/3)
#   - request body - check
#   - success response - check
#   - status codes (3/3) - check


# POST "api/login" (0/?)
#   - request body - ...
#   - success response - ...
#   - status codes (0/?) - ...

# api/auth/registration or api/registration ... ?!