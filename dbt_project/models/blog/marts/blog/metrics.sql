{{
    config(
        description="サイトごとの日付別pv imp click.",
    )
}}
select p.*, c.* except (data_date, url)
from {{ ref("pv") }} as p
left join {{ ref("imp_click") }} as c on p.d = c.data_date and p.page_location = c.url