select
    date_trunc('month', d) as month,
    sum(pv) as total_pv,
    sum(impressions) as total_imp,
    sum(clicks) as total_clicks,
    round(sum(pv)::float / max(sum(pv)) over (), 3) as normalized_pv,
    round(sum(impressions)::float / max(sum(impressions)) over (), 3) as normalized_imp,
    round(sum(clicks)::float / max(sum(clicks)) over (), 3) as normalized_clicks
from free.metrics
group by date_trunc('month', d)
order by month
;
