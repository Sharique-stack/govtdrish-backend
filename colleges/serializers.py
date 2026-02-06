from rest_framework import serializers
from .models import College, Course, Lead, Scholarship, CollegeOutcome, Alumni

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'seats', 'total_fees', 'eligibility']

class CollegeOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeOutcome
        fields = ['alumni_audited_count', 'open_to_work_percent', 'avg_tenure_months', 'top_employers', 'risk_score']

class AlumniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumni
        fields = ['id', 'name', 'course_name', 'passout_year', 'hometown_city']

class CollegeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name', 'slug', 'city', 'state', 'ownership_type', 'nirf_rank']

class CollegeDetailSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    outcome = CollegeOutcomeSerializer(read_only=True)
    related_colleges = serializers.SerializerMethodField()  # <--- NEW FIELD

    class Meta:
        model = College
        fields = [
            'id', 'name', 'slug', 'city', 'state', 'ownership_type', 
            'nirf_rank', 'cutoff_rank', 'estd_year', 'courses', 'outcome',
            'related_colleges'  # <--- Added here
        ]

    def get_related_colleges(self, obj):
        # Find 3 other colleges in the same state
        related = College.objects.filter(state=obj.state).exclude(id=obj.id)[:3]
        return CollegeListSerializer(related, many=True).data

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'