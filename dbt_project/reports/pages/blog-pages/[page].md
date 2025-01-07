---
queries:
  - page_query_metrics: blog/page_query_metrics.sql
  - page_word_metrics: blog/page_word_metrics.sql
---

## {$page.params.page}

<BigLink href={$page_query_metrics[0].url}>記事ページ</BigLink>

### 検索クエリ別

<DataTable
    data={page_query_metrics}
    rows=15
    rowShading=true
    rowLines=false
    search=true
>
	<Column id=query wrap=true />
	<Column id=normalized_imp contentType=bar fmt=num2 />
	<Column id=normalized_clicks contentType=bar barColor=#74E677FF fmt=num2/>
</DataTable>



### 検索クエリ単語別

<DataTable
    data={page_word_metrics}
    rowShading=true
    rowLines=false
    search=true
    link=url
/>

<ScatterPlot 
    data={page_word_metrics}
    x=normalized_imp
    y=normalized_clicks
    series=query_word
    xFmt=num2
    yFmt=num2
    yMin=0
    yMax=1
    xMin=0
    xMax=1
/>
