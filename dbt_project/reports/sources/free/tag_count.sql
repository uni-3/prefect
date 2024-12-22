SELECT date_trunc(date(created_at), year) as created_at, tag, COUNT(*) AS count FROM blog_info.parsed_blog_content CROSS JOIN UNNEST(tags) AS tag GROUP BY created_at, tag;
