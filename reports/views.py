from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from django.contrib import messages
from django.http import HttpResponse 
from reportlab.lib.pagesizes import letter
import pandas as pd 
from reportlab.pdfgen import canvas
from igp.models import IGP, IGPItem
from ogp.models import OGP, OGPItem
from django.core.paginator import Paginator
from io import BytesIO  # <-- Add this line



@login_required
@role_required('staff', 'hr', 'admin')
def igp_report_view(request):
    igps = IGP.objects.all()

    # Filters (Get Parameters)
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    messer = request.GET.get('messer')  # Filter by Supplier (Messer)
    item_name = request.GET.get('item_name')  # Filter by Item Name

    # Apply filters based on the form input
    if category:
        igps = igps.filter(category__name__icontains=category)
    if date_from and date_to:
        igps = igps.filter(date__range=[date_from, date_to])
    if messer:
        igps = igps.filter(messer__name__icontains=messer)
    if item_name:
        igps = igps.filter(items__item__name__icontains=item_name).distinct()

    # Pagination
    igps = igps.order_by('-date')  # Order by date
    paginator = Paginator(igps, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'igps': page_obj}
    return render(request, 'igp_report.html', context)


@login_required
@role_required('staff', 'hr', 'admin')
def igp_report_filter_csv(request):
    igps = IGP.objects.all()

    # Filters (Get Parameters)
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    messer = request.GET.get('messer')  # Filter by Supplier (Messer)
    item_name = request.GET.get('item_name')  # Filter by Item Name

    # Apply filters
    if category:
        igps = igps.filter(category__name__icontains=category)
    if date_from and date_to:
        igps = igps.filter(date__range=[date_from, date_to])
    if messer:
        igps = igps.filter(messer__name__icontains=messer)
    if item_name:
        igps = igps.filter(items__item__name__icontains=item_name).distinct()

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="igp_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['IGP Number', 'Supplier', 'Date', 'Item Name', 'Description', 'Quantity', 'Unit'])
    
    for igp in igps:
        writer.writerow([igp.igp_number, igp.messer, igp.date, igp.item_name, igp.description, igp.quantity, igp.unit])

    return response


@login_required
@role_required('staff', 'hr', 'admin')
def igp_report_filter_pdf(request):
    igps = IGP.objects.all()

    # Filters (Get Parameters)
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    messer = request.GET.get('messer')  # Filter by Supplier (Messer)
    item_name = request.GET.get('item_name')  # Filter by Item Name

    # Apply filters
    if category:
        igps = igps.filter(category__name__icontains=category)
    if date_from and date_to:
        igps = igps.filter(date__range=[date_from, date_to])
    if messer:
        igps = igps.filter(messer__name__icontains=messer)
    if item_name:
        igps = igps.filter(items__item__name__icontains=item_name).distinct()

    # Create PDF response
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "IGP Report")
    y_position = 730

    for igp in igps:
        p.drawString(100, y_position, f"IGP Number: {igp.igp_number}")
        p.drawString(300, y_position, f"Supplier: {igp.messer}")
        p.drawString(500, y_position, f"Date: {igp.date}")
        y_position -= 20

        p.drawString(100, y_position, f"Item: {igp.item_name}")
        p.drawString(300, y_position, f"Description: {igp.description}")
        p.drawString(500, y_position, f"Quantity: {igp.quantity} {igp.unit}")
        y_position -= 40

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


@login_required
@role_required('staff','hr','admin')
def export_igp_csv(request):
    data = []
    
    for igp in IGP.objects.all():
        for item in igp.items.all():
            data.append({
                'IGP Number' : igp.igp_number,
                'Supplier':igp.messer.name,
                'Date':igp.date,
                'Item Name': item.item.name,
                'Description': item.item.description,
                'Quantity': item.quantity,
                'Unit': item.unit,
            })
            
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="igp_report.csv"'
    
    df.to_csv(path_or_buf=response,index=False)
    return response


@login_required
@role_required('staff','hr','admin')
def export_igp_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="igp_report.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y_position = height - 50
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, y_position, "IGP Report")
    y_position -= 30

    p.setFont("Helvetica", 10)
    columns = ["IGP Number", "Supplier", "Date", "Item Name", "Description", "Quantity", "Unit"]
    col_x_positions = [30, 100, 200, 300, 400, 500, 550]

    for i, col in enumerate(columns):
        p.drawString(col_x_positions[i], y_position, col)

    y_position -= 20
    p.setFont("Helvetica", 9)

    for igp in IGP.objects.all():
        for item in igp.items.all():
            values = [
                str(igp.igp_number), 
                igp.messer.name, 
                str(igp.date),
                item.item.name, 
                item.item.description, 
                str(item.quantity), 
                str(item.unit)
            ]
            
            for i, value in enumerate(values):
                p.drawString(col_x_positions[i], y_position, value)

            y_position -= 15
            if y_position < 50:  # New page if not enough space
                p.showPage()
                p.setFont("Helvetica", 9)
                y_position = height - 50

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required
@role_required('staff','hr','admin')
def export_ogp_csv(request):
    data = []
    
    for ogp in OGP.objects.all():
        for item in ogp.items.all():
            data.append({
                'OGP Number' : ogp.ogp_number,
                'Vendor':ogp.messer.name,
                'Date':ogp.date,
                'Item Name': item.item.name,
                'Description': item.item.description,
                'Quantity': item.quantity,
                'Unit': item.unit,
            })
            
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ogp_report.csv"'
    
    df.to_csv(path_or_buf=response,index=False)
    return response


@login_required
@role_required('staff','hr','admin')
def export_ogp_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ogp_report.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y_position = height - 50
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, y_position, "OGP Report")
    y_position -= 30

    p.setFont("Helvetica", 10)
    columns = ["OGP Number", "Vendor", "Date", "Item Name", "Description", "Quantity", "Unit"]
    col_x_positions = [30, 100, 200, 300, 400, 500, 550]

    for i, col in enumerate(columns):
        p.drawString(col_x_positions[i], y_position, col)

    y_position -= 20
    p.setFont("Helvetica", 9)

    for ogp in OGP.objects.all():
        for item in ogp.items.all():
            values = [
                str(ogp.ogp_number), 
                ogp.messer.name, 
                str(ogp.date),
                item.item.name, 
                item.item.description, 
                str(item.quantity), 
                str(item.unit)
            ]
            
            for i, value in enumerate(values):
                p.drawString(col_x_positions[i], y_position, value)

            y_position -= 15
            if y_position < 50:  # New page if not enough space
                p.showPage()
                p.setFont("Helvetica", 9)
                y_position = height - 50

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response