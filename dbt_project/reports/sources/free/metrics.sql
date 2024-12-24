select *, safe_divide(clicks, impressions) as ctr from blog_info_marts.metrics
where page_title != ""