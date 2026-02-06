from django.contrib import admin
from django.urls import path, include
# 👇 IMPORT THIS VIEW
from colleges.views import VoiceCounselorView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/colleges/', include('colleges.urls')),
    # 👇 ADD THIS LINE
    path('api/voice-counselor/', VoiceCounselorView.as_view()), 
]