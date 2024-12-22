SELECT
    page_title,
    REGEXP_REPLACE(page_location, '/$', '') as page_location,
    ROW_NUMBER() OVER (ORDER BY SUM(pv) DESC) AS rank
  FROM
    blog_info_marts.pv_in_30days
  GROUP BY all
ORDER BY
  rank DESC
