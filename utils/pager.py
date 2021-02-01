from django.core.paginator import Paginator

def page_fun(table_data_obj, page, page_split, around_count=2):
    '''
    table_data_obj: 数据库査询的对象
    page：获取某页的数据
    around_count：当前页前后各显示多少页码，默认为2
    page_split：每页显示多少数据
    '''
    paginator = Paginator(table_data_obj, page_split)
    page_obj = paginator.get_page(page)
    current_page = page_obj.number  # 获取当前页
    num_pages = paginator.num_pages  # 总的页数
    left_has_more = False
    right_has_more = False
    if current_page <= around_count + 2:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)
    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)  # 左闭右开区间
    return {
        'left_pages': left_pages,
        'right_pages': right_pages,
        'current_page': current_page,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'num_pages': num_pages,
        'page_obj': page_obj,
    }