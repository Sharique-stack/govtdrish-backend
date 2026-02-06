from django.contrib import admin
from .models import College, Course, Lead, Scholarship, CollegeOutcome, Alumni  # <--- Imported here

# Existing registrations...
admin.site.register(Course)
admin.site.register(Lead)
admin.site.register(Scholarship)

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'nirf_rank', 'ownership_type')
    search_fields = ('name', 'city')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CourseInline]

# --- NEW: Register the Detective Model ---
@admin.register(CollegeOutcome)
class CollegeOutcomeAdmin(admin.ModelAdmin):
    list_display = ('college', 'risk_score', 'open_to_work_percent', 'last_updated')
    search_fields = ('college__name',)
@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'college', 'hometown_city', 'hometown_state', 'is_verified')
    list_filter = ('hometown_state', 'is_verified')
    search_fields = ('name', 'hometown_city', 'college__name')