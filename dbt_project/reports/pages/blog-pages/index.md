---
title: ページごとのメトリクス
---

```sql pages
select 
    url,
    '/blog-pages/' || slug as link,
    sum(impressions) as i
from free.count_search_word
group by all
order by i desc
```

<!-- {#each pages as p}

- [{p.url} のメトリクス]({p.link})

{/each} -->
impressionの多い順

<DataTable data={pages}>
    <Column id=url title="記事ページ" contentType=link />
    <Column id=link title="メトリクスページ" contentType=link linkLabel="go to metrics page"/>
</DataTable>