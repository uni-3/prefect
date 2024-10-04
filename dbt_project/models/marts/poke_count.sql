{{ config(
    tags=["pokemon"]
) }}

with t as (
    select 
      name,
      count(*) as c,
    from {{ source('raw_data', 'pokemon') }}
    group by 1
)
select 
  *
from t

