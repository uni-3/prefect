{{
    config(
        description="3月以内のサイトごとのpv",
    )
}}
with
    pvs as (
        select
            date(date) as d,
            page_title,
            regexp_replace(page_location, '/$', '') as page_location,
            count(1) as pv
        from {{ source("ga", "flat_events") }}
        where
            event_name = 'page_view'
            and _table_suffix
            between format_date(
                '%Y%m%d',
                date_add(current_date("Asia/Tokyo"), interval -3 month)
            ) and format_date(
                '%Y%m%d', date_add(current_date("Asia/Tokyo"), interval -1 day)
            )
        group by d, page_title, page_location
    )
select d, page_title, page_location, sum(pv) as pv
from pvs
group by all
