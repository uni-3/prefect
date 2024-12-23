select
    date_truncate(d, month) as month,
    page_title,
    regexp_replace(page_location, '/$', '') as page_location,
    row_number() over (order by sum(pv) desc) as rank
from blog_info_marts.pv_in_30days
group by all
order by rank asc
