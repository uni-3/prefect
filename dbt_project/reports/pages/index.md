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
  selectAllByDefault=true
>
</Dropdown>

Selected: {inputs.ja_names.value}

```sql pokes
  select
    id
    ,ja_name
    ,weight
    ,sprites__front_default as poke_front_img
    ,sprites__front_shiny as poke_front_shiny_img
  from pokemon.pokemons
  where ja_name in '${inputs.ja_name.value}'
```

<DataTable data={pokes} search=true/>

![An online image](https://i.imgur.com/xyI27iZ.gif)
