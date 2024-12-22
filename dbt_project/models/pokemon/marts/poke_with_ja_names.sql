{{ config(
    materialized="table",
    tags=["pokemon"]
) }}

with species_ja_names as (
  select distinct
    s.id,
    p.name as ja_name,
  from {{ source('raw_data', 'species') }} as s
  join (select * from {{ source('raw_data', 'species__names') }} where language__name='ja') as p
  on s._dlt_id = p._dlt_parent_id
)
SELECT distinct
  p.* exclude(_dlt_load_id, _dlt_id),
  s.ja_name
from {{ source('raw_data', 'pokemon') }} as p
join species_ja_names as s
on p.id = s.id