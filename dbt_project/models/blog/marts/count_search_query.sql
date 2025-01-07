{{
    config(
        description="当月含む三ヶ月以内の検索ワード",
    )
}}
select
    regexp_replace(url, '/$', '') as url,
    array_reverse(split(url, '/'))[offset(1)] as slug,
    query,
    sum(impressions) as impressions,
    sum(clicks) as clicks,
    ((sum(sum_position) / sum(impressions)) + 1.0) AS avg_position
from {{ source("sc", "url_impression") }}
where
    data_date
    between date_add(current_date("Asia/Tokyo"), interval -2 month) and date_add(
        current_date("Asia/Tokyo"), interval -1 day
    )
    and query != '' -- 匿名化されたクエリを除外
    
group by all