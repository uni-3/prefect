select
    dayname(d) as day_of_week,
    sum(pv)::float / max(sum(pv)) over () as normalized_pv,
    case
        dayname(d)
        when 'Monday'
        then 1
        when 'Tuesday'
        then 2
        when 'Wednesday'
        then 3
        when 'Thursday'
        then 4
        when 'Friday'
        then 5
        when 'Saturday'
        then 6
        when 'Sunday'
        then 7
    end as day_number
from free.metrics
group by dayname(d)
order by day_number
;
