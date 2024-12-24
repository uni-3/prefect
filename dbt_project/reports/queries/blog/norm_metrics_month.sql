select
    date_trunc('month', d) as month, 
    sum(pv)::float / max(sum(pv)) over () as normalized_pv,
    sum(impressions)::float / max(sum(impressions)) over () as normalized_imp,
    sum(clicks)::float / max(sum(clicks)) over () as normalized_clicks
from free.metrics
group by date_trunc('month', d)
order by month
;
