with
    t as (
        select date_trunc(date(created_at), year) as created_at, tag, count(*) as count
        from blog_info_staging.stg_parsed_blog_content
        cross join unnest(tags) as tag
        group by created_at, tag
    )
select *
from t
