---
title: blog viewer

queries:
  - content: blog_content.sql
  - pv_rank: blog/pv_rank.sql
  - tag_count: blog/tag_count.sql
---

```sql content_len 
  select
    len_text
  from free.content
```

<Histogram
    data={content_len}
    x=len_text
/>



<LineChart 
    data={pv_rank.limit(10)}
    x=page_title
    y=rank
    markers=true
/>

<BarChart 
    data={tag_count}
    x=created_at
    y=count
    series=tag
    title="count by tag"
/>

<LastRefreshed/>
