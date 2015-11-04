#!/usr/bin/env bash
[[ -d books_fmt ]] || mkdir books_fmt
for f in books/*.xml; do
    xmllint --format "$f" > books_fmt/"${f#books/}"
done
for f in books_fmt/*TEXT.xml; do
    out_f="${f%.xml}_utf8.xml"
    iconv -f utf-16 -t utf-8 "$f" > "$out_f"
    sed -i '' 's/UTF-16/UTF-8/' "$out_f"
done
