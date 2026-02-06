from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollegeViewSet, LeadViewSet, ScholarshipViewSet

router = DefaultRouter()

# --- SPECIFIC ROUTES FIRST ---
# (Check these first so they don't get mistaken for a college slug)
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'scholarships', ScholarshipViewSet, basename='scholarship')

# --- CATCH-ALL ROUTE LAST ---
# (Any other text will be treated as a college slug)
router.register(r'', CollegeViewSet, basename='college')

urlpatterns = [
    path('', include(router.urls)),
]