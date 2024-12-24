select
    page_title,
    page_location,
    sum(pv) as pv,
    sum(impressions) as imp,
    sum(clicks) as clicks,
    sum(clicks) / sum(impressions) as ctr,
    sum(pv)::float / max(sum(pv)) over () as normalized_pv,
    sum(impressions)::float / max(sum(impressions)) over () as normalized_imp,
    sum(clicks)::float / max(sum(clicks)) over () as normalized_clicks
from free.metrics
group by all
