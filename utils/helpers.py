from django.core.paginator import Paginator
from django.db.models import Q

def search_and_paginate(request, model, filters=None, ordering=None, per_page=10):
    """
    Utility to perform search and pagination on a queryset.
    
    Args:
        request: Django HttpRequest object.
        model: Django model or queryset to query from.
        filters: A dictionary of filter fields and their values.
        ordering: Default ordering for the queryset.
        per_page: Number of items per page.
        
    Returns:
        A tuple of:
        - paginated queryset (Page object).
        - search parameters dictionary (to maintain form state in templates).
    """
    query = Q()
    search_params = {}

    # Apply filters if provided
    if filters:
        for field, value in filters.items():
            search_value = request.GET.get(value, '').strip()
            if search_value:
                query &= Q(**{f"{field}__icontains": search_value})
                search_params[value] = search_value

    # Fetch records
    queryset = model.objects.filter(query).order_by(ordering if ordering else '-id')

    # Paginate records
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    paginated_queryset = paginator.get_page(page_number)

    return paginated_queryset, search_params
