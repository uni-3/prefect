---
title: pokemon viewer
---


```sql poke_names 
  select
    id
    ,ja_name
    ,weight
    ,sprites__front_default as poke_front_img
    ,sprites__front_shiny as poke_front_shiny_img
  from pokemon.pokemons
```


<Dropdown
  data={poke_names}
  name=ja_name
  value=ja_name
  multiple=true
  title="表示するポケモン"
  selectAllByDefault=true
>
</Dropdown>

<!-- Selected: {inputs.ja_name.value} -->

```sql pokes
  select
    id
    ,ja_name as name
    ,weight
    ,sprites__front_default as poke_front_img
    ,sprites__front_shiny as poke_front_shiny_img
  from pokemon.pokemons
  where ja_name in ${inputs.ja_name.value}
  order by id asc
```

<DataTable data={pokes} search=true>
  	<Column id=id />
  	<Column id=poke_front_img title="image" contentType=image width=60px align=center />
  	<Column id=poke_front_shiny_img title="イロチ" contentType=image width=60px align=center />
  	<Column id=name />
  	<Column id=weight />
</DataTable>

