SELECT date_trunc(date(created_at), month) as created_at, tag, COUNT(*) AS count FROM `free-180413`.`blog_info`.`parsed_blog_content` CROSS JOIN UNNEST(tags) AS tag GROUP BY created_at, tag;
