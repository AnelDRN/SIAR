from owslib.wcs import WebCoverageService
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings

def inspect_wcs_capabilities():
    """
    Connects to the WCS service and lists its available coverages.
    """
    wcs_url = settings.LAND_COVER_WCS_URL
    print(f"Connecting to WCS server at: {wcs_url}")
    
    try:
        wcs = WebCoverageService(wcs_url, version='1.0.0')
        
        print("\n--- Available Coverages ---")
        if not wcs.contents:
            print("No coverages found.")
            return

        for cov_id, coverage in wcs.contents.items():
            print(f"\nID:          {cov_id}")
            print(f"  Title:     {coverage.title}")
            print(f"  Abstract:  {getattr(coverage, 'abstract', 'N/A')}")
            print(f"  CRS List:  {coverage.supportedCRS}")
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    inspect_wcs_capabilities()