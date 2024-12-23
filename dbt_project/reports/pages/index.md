---
title: blog dashboard

queries:
  - content_len: blog/content_len.sql
  - content_count: blog/content_count.sql
  - rank_month: blog/rank_month.sql
  - tag_count: blog/tag_count.sql
  - norm_metrics_month: blog/norm_metrics_month.sql
  - norm_pv_day_of_week: blog/norm_pv_day_of_week.sql
---


### 記事に関するデータ

記事数合計: ** <Value data={content_count} column="c" agg="sum" /> **

<Grid cols=2>
  <Group>
    <LineChart
        data={content_count}
        x=year
        y=c
        labels=true
        markers=true
        title="記事数推移"
    />
  </Group>

  <Histogram
      data={content_len}
      x=len_text
      title="記事の文字数分布"
      fillColor=#b8645e
  />

  <BarChart 
      data={tag_count.where(`count >= 3`)}
      x=created_at
      y=count
      series=tag
      legend=false
      title="count by tag(appears 3 or more times)"
  />
</Grid>


### 指標に関するデータ

<LineChart 
    data={norm_metrics_month}
    x=month
    y=normalized_imp
    yMax=1
    markers=true
    title="最大を1としたときのimpression数の推移"
    labels=true
/>

<LineChart 
    data={norm_metrics_month}
    x=month
    y=normalized_pv
    yMax=1
    markers=true
    title="最大を1としたときのPV数の推移"
    labels=true
/>


<BarChart 
    data={norm_pv_day_of_week}
    x=day_of_week
    y=normalized_pv
    labels=true
    title="最大を1としたときの曜日別PV数"
    sort=false
/>

<LineChart 
    data={rank_month.where(`pv_rank <= 10`)}
    x=month
    y=pv_rank
    yMin=1
    yMax=10
    series=page_title
    step=true
    markers=true
    showAllLabels=true
    title="ページごとのPV数順位の推移"
    echartsOptions={{ yAxis: {inverse: true }}}
/>


<LastRefreshed/>
