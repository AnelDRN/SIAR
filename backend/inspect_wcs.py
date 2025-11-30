from owslib.wcs import WebCoverageService

# The base URL of the WCS service we want to inspect
WCS_URL = 'http://ows.rasdaman.org/rasdaman/ows'

print(f"--- Inspecting WCS Server at: {WCS_URL} ---")

try:
    # Connect to the server, trying WCS version 1.0.0 first
    wcs = WebCoverageService(WCS_URL, version='2.0.1')
    print("[SUCCESS] Connected using WCS version 2.0.1")

    print("\n--- Available Coverages (Layers) ---")
    if not wcs.contents:
        print("No coverages found.")
    else:
        for name, layer in wcs.contents.items():
            print(f"\nCoverage ID: {name}")
            print(f"  - Title: {layer.title}")
            # Bounding box is often useful to see the extent
            if layer.boundingBoxWGS84:
                print(f"  - BBox (WGS84): {layer.boundingBoxWGS84}")
            # Supported formats tell us how we can download the data
            print(f"  - Supported Formats: {layer.supportedFormats}")

except Exception as e:
    print(f"\n[ERROR] Could not connect or inspect the WCS server.")
    print(f"Details: {e}")

print("\n--- Inspection Complete ---")
