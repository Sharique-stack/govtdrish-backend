from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import College
from .models import College, Lead, Scholarship, Alumni
from .serializers import (
    CollegeListSerializer, 
    CollegeDetailSerializer, 
    LeadSerializer, 
    ScholarshipSerializer,
    AlumniSerializer
)

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        # 🔍 DEBUG: Print the data we received
        print("📥 Received Data:", request.data)
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # ❌ DEBUG: Print why it failed
            print("❌ Validation Errors:", serializer.errors) 
            return Response(serializer.errors, status=400)
            
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
        
class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = College.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CollegeDetailSerializer
        return CollegeListSerializer

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class ScholarshipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer

class HometownAlumniView(APIView):
    """
    Finds alumni from the same city/state as the user.
    """
    def get(self, request, college_id):
        user_city = request.query_params.get('city', '').strip()
        user_state = request.query_params.get('state', '').strip()

        # Base query: Verified alumni from this college
        queryset = Alumni.objects.filter(college_id=college_id, is_verified=True)
        
        # 1. Exact City Match
        city_matches = queryset.filter(hometown_city__iexact=user_city)
        
        if city_matches.exists():
            count = city_matches.count()
            top_profiles = city_matches[:3]
            match_type = "City"
        else:
            # 2. State Fallback
            state_matches = queryset.filter(hometown_state__iexact=user_state)
            count = state_matches.count()
            top_profiles = state_matches[:3]
            match_type = "State"

        data = {
            "count": count,
            "match_type": match_type,
            "profiles": AlumniSerializer(top_profiles, many=True).data
        }
        return Response(data)

class VoiceCounselorView(APIView):
    def post(self, request):
        query_text = request.data.get('text', '').lower()
        print(f"🎤 Voice Query: {query_text}")

        # 1. Detect Intent: Search
        # Simple keyword matching for MVP (Llama 3 would go here in Production)
        response_text = ""
        results = []

        if 'college' in query_text or 'institute' in query_text or 'best' in query_text:
            # Check for State names in the query
            states = ['Bihar', 'Karnataka', 'Delhi', 'Maharashtra', 'Uttar Pradesh']
            detected_state = next((state for state in states if state.lower() in query_text), None)

            if detected_state:
                # Find colleges in that state
                colleges = College.objects.filter(state__iexact=detected_state)[:3]
                if colleges.exists():
                    response_text = f"Mujhe {detected_state} mein ye {colleges.count()} colleges mile hain. Sabse top par {colleges[0].name} hai."
                    # Serialize data for the "Visual Card"
                    results = [{"name": c.name, "city": c.city, "slug": c.slug, "rank": c.nirf_rank} for c in colleges]
                else:
                    response_text = f"Maaf kijiye, mujhe {detected_state} mein abhi koi college nahi mila."
            else:
                response_text = "Aap kis state mein college dhundh rahe hain? Bihar ya Delhi?"
        
        elif 'fees' in query_text or 'paise' in query_text:
            response_text = "Fees ki jaankari ke liye mujhe college ka naam batayein."
        
        else:
            response_text = "Namaste! Main Govt Drish assistant hoon. Aap mujhse colleges ya scholarships ke baare mein pooch sakte hain."

        return Response({
            "reply": response_text,
            "data": results,
            "action": "show_results" if results else "ask_details"
        })