with
    monthly_data as (
        select
            date_trunc('month', d) as month,
            page_title,
            page_location,
            sum(pv) as total_pv,
            sum(impressions) as total_imp,
            sum(clicks) as total_clicks
        from free.metrics
        group by date_trunc('month', d), page_title, page_location
    ),
    rankings as (
        select
            month,
            page_title,
            concat(left(page_title, 10), '...') as page_title_offset,
            page_location,
            row_number() over (partition by month order by total_pv desc) as pv_rank,
            row_number() over (partition by month order by total_imp desc) as imp_rank,
            row_number() over (
                partition by month order by total_clicks desc
            ) as click_rank,
        from monthly_data
    )
select *
from rankings
where pv_rank <= 10 or imp_rank <= 10 or click_rank <= 10
order by month, pv_rank
;
