{{
    config(
        description="当月含む三ヶ月以内のサイトごとのpv",
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
    between date_add(current_date("Asia/Tokyo"), interval -2 month) and date_add(
        current_date("Asia/Tokyo"), interval -1 day
    )
group by all
