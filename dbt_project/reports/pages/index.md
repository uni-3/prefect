---
title: blog dashboard

queries:
  - content_len: blog/content_len.sql
  - pv_rank: blog/pv_rank.sql
  - tag_count: blog/tag_count.sql
---

- 記事文字数の分布

<Histogram
    data={content_len}
    x=len_text
/>

- PV数top10

<DataTable 
    data={pv_rank.limit(10)}
/>

- タグごとのカウント

<BarChart 
    data={tag_count}
    x=created_at
    y=count
    series=tag
    title="count by tag"
/>

<LastRefreshed/>
