from django.core.management.base import BaseCommand
from colleges.models import College, CollegeOutcome # Ensure you added this model
import asyncio
from playwright.async_api import async_playwright

class Command(BaseCommand):
    help = 'Audits LinkedIn alumni data to calculate placement risk scores'

    def handle(self, *args, **options):
        colleges = College.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Starting audit for {colleges.count()} colleges...'))
        
        # Run the async scraper
        asyncio.run(self.run_audit_sequence(colleges))

    async def run_audit_sequence(self, colleges):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for college in colleges:
                self.stdout.write(f'Auditing: {college.name}...')
                
                try:
                    # 1. Scrape Data
                    # Note: Using a generic slug logic; ensure your College model has a linkedin_slug
                    url = f"https://www.linkedin.com/school/{college.slug}/people/"
                    await page.goto(url, wait_until="networkidle", timeout=60000)

                    # Extract count (Example selector)
                    count_text = await page.inner_text('.t-20')
                    
                    # 2. Logic: Let's assume some audited values for now 
                    # In a real scrape, you'd parse the specific 'Open to work' keyword frequency
                    open_to_work = 18.4  # Placeholder logic
                    tenure = 11.5       # Placeholder logic
                    
                    # 3. Calculate Risk Score
                    risk = 0
                    if open_to_work > 12: risk += (open_to_work - 12) * 4
                    if tenure < 14: risk += (14 - tenure) * 5
                    risk_score = min(int(risk), 100)

                    # 4. Save/Update Database
                    outcome, created = CollegeOutcome.objects.update_or_create(
                        college=college,
                        defaults={
                            'alumni_audited_count': 5000, # Placeholder
                            'open_to_work_percent': open_to_work,
                            'avg_tenure_months': tenure,
                            'risk_score': risk_score,
                            'top_employers': [
                                {"name": "TCS", "count": 450},
                                {"name": "Infosys", "count": 320},
                                {"name": "Accenture", "count": 150}
                            ]
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully audited {college.name} - Risk: {risk_score}'))
                    
                    # Avoid rate limiting: Sleep between requests
                    await asyncio.sleep(5)

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed {college.name}: {str(e)}'))

            await browser.close()