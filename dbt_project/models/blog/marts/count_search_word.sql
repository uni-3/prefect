
{{
    config(
        description="当月含む三ヶ月以内の検索ワードを単語別に集計",
    )
}}
select
    regexp_replace(url, '/$', '') as url,
    array_reverse(split(url, '/'))[offset(1)] as slug,
    if(array_length(split(query, ' ')) >= 4, query, query_word) as query_word,
    sum(impressions) as impressions,
    sum(clicks) as clicks,
    ((sum(sum_position) / sum(impressions)) + 1.0) AS avg_position
from {{ source("sc", "url_impression") }},
    unnest(split(query, ' ')) AS query_word
where
    data_date
    between date_add(current_date("Asia/Tokyo"), interval -2 month) and date_add(
        current_date("Asia/Tokyo"), interval -1 day
    )
    and query != '' -- 匿名化されたクエリを除外
    
group by all