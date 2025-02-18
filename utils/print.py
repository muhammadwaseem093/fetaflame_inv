import weasyprint
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings

def print_report(template_name, context_data=None, filename="report.pdf"):
    """
    Reusable function to generate a PDF from HTML template and context.

    Parameters:
    - template_name: The template to render HTML from.
    - context_data: The context data to be passed to the template.
    - filename: The name of the file that will be presented for download.

    Returns:
    - An HttpResponse with the generated PDF.
    """
    try:
        # Render the HTML content using the template and context
        html_content = render_to_string(template_name, context_data or {})

        # Generate the PDF from the HTML content
        pdf = weasyprint.HTML(string=html_content).write_pdf()

        # Create an HTTP response with the PDF as content
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        return response
    except Exception as e:
        # Log the error (you can adjust this based on your logging settings)
        print(f"Error generating PDF: {e}")
        return HttpResponse("An error occurred while generating the PDF.", status=500)
