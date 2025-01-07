select
  url,
  query,
  sum(impressions)::float / max(sum(impressions)) over () as normalized_imp,
  sum(clicks)::float / max(sum(clicks)) over () as normalized_clicks,
from free.count_search_query
where slug = '${params.page}'
group by all
order by normalized_imp desc