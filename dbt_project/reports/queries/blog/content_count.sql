select date_trunc('year', created_at) as year, count(*) as c
from free.content
group by all
