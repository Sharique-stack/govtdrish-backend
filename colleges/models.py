from django.db import models

class College(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    ownership_type = models.CharField(max_length=50)
    estd_year = models.IntegerField(default=2000)
    cutoff_rank = models.IntegerField(default=5000, help_text="Closing rank for General category")
    nirf_rank = models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    total_fees = models.IntegerField()
    seats = models.IntegerField()
    eligibility = models.CharField(max_length=255, default="10+2 with 50% marks")
    def __str__(self):
        return self.name

class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    college_name = models.CharField(max_length=255) # We store the college they applied for
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    eligible_category = models.CharField(max_length=50, help_text="e.g. SC, ST, OBC, All")
    max_income = models.IntegerField(help_text="Maximum annual family income in INR")
    state = models.CharField(max_length=100, help_text="Domicile State or 'All'")
    amount = models.CharField(max_length=100, help_text="e.g. ₹30,000/year or Full Fee")

    def __str__(self):
        return self.name

class CollegeOutcome(models.Model):
    college = models.OneToOneField(College, on_delete=models.CASCADE, related_name='outcome')
    alumni_audited_count = models.IntegerField(default=0)
    open_to_work_percent = models.DecimalField(max_digits=5, decimal_places=2)
    avg_tenure_months = models.DecimalField(max_digits=4, decimal_places=1)
    top_employers = models.JSONField(default=list) # List of dicts
    risk_score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

class Alumni(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='alumni')
    name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100, help_text="e.g. B.Tech CS")
    passout_year = models.IntegerField()
    
    # The Hometown Engine Fields (Indexed for speed)
    hometown_city = models.CharField(max_length=100, db_index=True)
    hometown_state = models.CharField(max_length=100, db_index=True)
    
    # Private info for the connection
    whatsapp_number = models.CharField(max_length=15) 
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} from {self.hometown_city}"

    def __str__(self):
        return f"Outcome for {self.college.name}"