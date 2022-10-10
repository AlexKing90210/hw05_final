from django.core.paginator import Paginator


def paginator_func(request, page, ordering):
    paginator = Paginator(page, ordering)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
