from django.urls import path

from .views import AboutPageView, HomePageView, PrivacyPolicyView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about", AboutPageView.as_view(), name="about"),
    path("privacy-policy", PrivacyPolicyView.as_view(), name="privacy-policy"),
]
