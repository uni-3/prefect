select
    -- title抽出 （"title: "の後ろの引用符内のテキストを取得）
    regexp_extract(text, r'title: "([^"]+)"') as title,

    -- created(date)抽出 （"date: "の後ろのISO形式の日時を取得）
    parse_timestamp(
        '%Y-%m-%dT%H:%M:%SZ',
        regexp_extract(
            text, r'date: ([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)'
        )
    ) as created_at,

    -- slug抽出 （"slug: "の後ろのテキストを取得）
    regexp_extract(text, r'slug: ([^\n]+)') as slug,
    -- tagsセクションを抽出して配列化
    array(
        select trim(regexp_extract(line, r'- (.+)'))
        from
            unnest(
                split(
                    -- tags:から始まるブロックを取得
                    regexp_extract(text, r'tags:\n((?:\s*- [^\n]+\n?)+)'), '\n'
                )
            ) as line
        where regexp_contains(line, r'- .+')
    ) as tags,
    length(text) as len_text,
    text
from {{ source("blog_info", "blog_content") }}
