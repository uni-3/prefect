select data_date, url, sum(impressions) as impressions, sum(clicks) as clicks
from {{ source("sc", "url_impression") }}
where
    data_date
    between date_add(current_date("Asia/Tokyo"), interval -30 day) and date_add(
        current_date("Asia/Tokyo"), interval -1 day
    )
group by all
