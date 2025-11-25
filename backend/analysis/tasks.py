from celery import shared_task
from .core import execute_analysis
from .models import AnalysisRequest


@shared_task(bind=True)
def run_analysis_task(self, request_id):
    """
    Celery task to run the geospatial analysis in the background,
    with status tracking.
    """
    try:
        analysis_request = AnalysisRequest.objects.get(id=request_id)

        # Update status to IN_PROGRESS
        analysis_request.status = AnalysisRequest.StatusChoices.IN_PROGRESS
        analysis_request.save()

        # Execute the core analysis function
        execute_analysis(request_id)

        # Update status to COMPLETED
        analysis_request.status = AnalysisRequest.StatusChoices.COMPLETED
        analysis_request.save()

    except AnalysisRequest.DoesNotExist:
        # The request that was supposed to be processed does not exist.
        # No further action needed.
        pass
    except Exception as e:
        # If any other exception occurs, mark the task as FAILED.
        try:
            analysis_request = AnalysisRequest.objects.get(id=request_id)
            analysis_request.status = AnalysisRequest.StatusChoices.FAILED
            analysis_request.save()
        except AnalysisRequest.DoesNotExist:
            # If the request is deleted mid-process, there's nothing to fail.
            pass
        # Optionally, re-raise the exception if you want Celery to record
        # it as a task failure.
        raise e
