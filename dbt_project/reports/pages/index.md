---
title: blog dashboard

queries:
  - content_len: blog/content_len.sql
  - content_count: blog/content_count.sql
  - rank_month: blog/rank_month.sql
  - tag_count: blog/tag_count.sql
  - norm_metrics_month: blog/norm_metrics_month.sql
  - norm_pv_day_of_week: blog/norm_pv_day_of_week.sql
  - metrics_bubble_chart: blog/metrics_bubble_chart.sql
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
        yGridlines=false
        title="記事数推移"
    />
  </Group>

  <Histogram
      data={content_len}
      x=len_content
      title="記事の文字数分布"
      fillColor=#b8645e
  />

  <BarChart 
      data={tag_count}
      x=created_at
      y=count
      series=tag
      legend=false
      title="count by tag(appears 3 or more times)"
  />
</Grid>


### 指標に関するデータ

<BubbleChart
    title="記事ごとの指標"
    data={metrics_bubble_chart}
    x=ctr
    y=normalized_pv
    xFmt=num2
    yFmt=num2
    sizeFmt=num2
    yGridlines=false
    yMax=1.0
    yMin=0
    series=page_title
    size=normalized_imp
>
</BubbleChart>

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
    yMax=1
    labels=true
    yGridlines=false
    title="最大を1としたときの曜日別PV数"
    sort=false
/>

<LineChart 
    data={rank_month}
    x=month
    y=pv_rank
    yMin=1
    yMax=10
    yGridlines=false
    series=page_title
    step=true
    markers=true
    showAllLabels=true
    title="ページごとのPV数順位の推移"
    echartsOptions={{ yAxis: {inverse: true }, tooltip: {show: false}}}
>
    <ReferencePoint
      data={rank_month}
      x=month
      y=pv_rank
      label=page_title_offset labelPosition=right
    />
</LineChart>


<LastRefreshed/>
