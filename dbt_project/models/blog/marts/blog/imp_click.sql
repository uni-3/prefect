{{
    config(
        description="3月以内のサイトごとのimp click.",
    )
}}
select
    data_date,
    regexp_replace(url, '/$', '') as url,
    sum(impressions) as impressions,
    sum(clicks) as clicks
from {{ source("sc", "url_impression") }}
where
    data_date
    between date_add(current_date("Asia/Tokyo"), interval -3 month) and date_add(
        current_date("Asia/Tokyo"), interval -1 day
    )
group by all
