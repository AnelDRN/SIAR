from django.core.management.base import BaseCommand
from rest_framework.test import APIClient
from analysis.models import AnalysisRequest, AnalysisResult

class Command(BaseCommand):
    help = 'Runs a full end-to-end test of the API analysis trigger.'

    def handle(self, *args, **options):
        self.stdout.write("--- Setting up API client and test data ---")
        client = APIClient()

        # Define the GeoJSON data for the area of interest
        aoi_data = {
            "type": "Polygon",
            "coordinates": [[
                [-73.9, 3.9],
                [-73.7, 3.9],
                [-73.7, 3.7],
                [-73.9, 3.7],
                [-73.9, 3.9],
            ]]
        }

        # Clear any old results to ensure a clean test
        AnalysisRequest.objects.all().delete()
        AnalysisResult.objects.all().delete()
        self.stdout.write("Cleared old test data from the database.")

        self.stdout.write("\n--- Sending POST request to /api/v1/analysis-requests/ ---")
        
        # Make the POST request to the API
        response = client.post("/api/v1/analysis-requests/", {"area_of_interest": aoi_data}, format='json')

        # Check the response
        if response.status_code == 201: # 201 Created
            self.stdout.write(self.style.SUCCESS(f"API request successful (Status: {response.status_code}). Analysis should be complete."))
            request_id = response.data['id']
        else:
            self.stdout.write(self.style.ERROR(f"API request failed! Status: {response.status_code}"))
            self.stdout.write(str(response.data))
            return

        self.stdout.write("\n--- Verifying Results ---")
        result_count = AnalysisResult.objects.filter(request_id=request_id).count()
        self.stdout.write(f"Found {result_count} AnalysisResult object(s) in the database for request {request_id}.")

        if result_count > 0:
            self.stdout.write(self.style.SUCCESS("SUCCESS: End-to-end API-triggered analysis and save process is working."))
        else:
            self.stdout.write(self.style.ERROR("FAILURE: API call was successful but no results were saved to the database."))


        self.stdout.write("\n--- Test finished ---")
