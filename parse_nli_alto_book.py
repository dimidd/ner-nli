#!/usr/bin/env python3
# coding=utf-8

import re
from lxml import etree
from pathlib import Path
import sys
import json
import subprocess

import db_api

from collections import namedtuple


Res_Entry = namedtuple('Res_Entry', 'id type alias alias_len cand_str cand')

chars_to_remove = re.compile(r'[-:+/_־—,\'".!.)(~*©§■•|}{£«□¥#♦^<>?✓=;\\[\]]+')


def extract_words_from_alto_xml(filepath):
    """
    extract words from an xml file in alto format
    return list of words, each word is accompanied with metadata
    to locate its source

    """
    with filepath.open() as f:
        tree = etree.parse(f)
    words = []
    for word in tree.xpath("//String[@CONTENT]"):
        words.append({
            "ID": word.get("ID"),
            "CONTENT": word.get("CONTENT"),
            "PARENT": word.getparent().get("ID"),
            "GRANDPARENT": word.getparent().getparent().get("ID"),
            "PAGE_FILE": str(filepath),
            })
    return words


def lookup(candidate, entities):
    """
        return first record in entities that match candidate
    """
    for record in entities:
        if candidate == record['name']:
            return record['id']
    return None


def slice(l, size):
    for i in range(len(l) + 1 - size):
        yield l[i:i + size]


def candidate2text(candidate):
    return " ".join([w for w in candidate])


def remove_special_chars(candidate_as_str):
    temp_str = chars_to_remove.sub(' ', candidate_as_str)
    return re.sub(r' +', ' ', temp_str.strip())


def generate_candidate_variants(candidate):
    just_the_words = [remove_special_chars(w['CONTENT']) for w in candidate]
    if len(just_the_words) == 1:
        if len(just_the_words[0].split()) < 2:
            return
    words_to_discard = [
        '',
        'את',
        'של',
        'על',
        'לא',
        'כי',
        'כל',
        'הוא',
        'עם',
        'גם',
        'זה',
        'אל',
        'ולא',
        'היה',
        'שלא',
        'לו',
        'זו',
        'אם',
        'אין',
        'מה',
        'בכל',
        'מן',
        'אחרי',
        'עד',
        'אלא',
        'רק',
        'אף',
        'אבל',
        'יש',
        'בין',
        'אנו',
        'עוד',
        'ביום',
        "עמ'",
        'נגד',
        'י',
        'אך',
        'הם',
        'היא',
        'או',
        'ראה',
        'כדי',
        ':',
        'להוסיף:',
        'אני',
        'אותו',
        'להם',
        'וראה',
        'אולם',
        'שאין',
        'כן',
        'אמר',
        'לפי',
        'ואל',
        'כמה',
        'באותו',
        'אליו',
        'שם',
        'מתוך',
        'מר',
        'לנו',
        'בו',
        'מי',
        'יותר',
        "גל'",
        'בת',
        'אינו',
        'כאשר',
        'אצל',
        'שום',
        'לכל',
        'כך',
        'ועל',
        "ה'",
        'אז',
        'שנה',
        'שהוא',
        'מפני',
        'היו',
        'כפי',
        'מאת',
        'וכל',
        'הרי',
        'היתה',
        'בפני',
        'מכל',
        'לי',
        'להלן',
        'זאת',
        'בענין',
        'צריך',
        'להיות',
        'הלא',
        'אחת',
        '1',
        '?',
        'פה',
        'זו,',
        'זה,',
        'ואין',
        'בעד',
        'אפילו',
        'עליו',
        'כבר',
        'וכן',
        'ואם',
        'הנ"ל',
        'בקרב',
        'בספר',
        'בהם',
        'אב',
        'עצמו',
        'מטעם',
        'מהם',
        'מ.',
        'לפניו',
        'כאילו',
        'בזה',
        'אסור',
        '*',
        '.',
        'שהיא',
        'יכול',
        'בשנת',
        'פח.',
        'לה',
        'חזר',
        'זה.',
        'אלה',
        '♦',
        '-',
        'יום',
        'רבי',
    ]

    for w in just_the_words:
        if w in words_to_discard:
            return  # skip this candidate

    candidate_as_str = candidate2text(just_the_words)
    candidates = set()
    dash = r'-|־'

    candidates = candidates.union(
        augment_with_prefixless_version(candidate_as_str)
    )
    candidate_as_str = candidate2text(just_the_words[::-1])
    candidates = candidates.union(
        augment_with_prefixless_version(candidate_as_str)
    )
    for w in candidate[0:1]:
        content = w['CONTENT']
        if re.search(dash, content):
            candidates.add(content)
            content_dashless = re.sub(dash, ' ', content)
            candidates.add(content_dashless)
            content = content_dashless
        if content.find(' ') > -1:
            candidates.add(content)
            candidates = candidates.union(augment_with_prefixless_version(content))

    for i in candidates:
        yield i

PREFIXES = ['ה', 'ו', 'ל', 'מ', 'ב', 'כ', 'ש']
PREFIXES2 = [
    'ול', 'ומ', 'וב', 'וכ', 'וש', 'וה',
    'מה',
    'שה', 'של', 'שמ', 'שב', 'שכ', 'שכ'
]
PREFIXES3 = [
    'וכש', 'שכש', 'לכש', 'ולכש',
    'ומה', 'ושה', 'כשה', 'וכשה',
    'לכשה', 'ולכשה', 'ומש', 'ומשה'
]


def augment_with_prefixless_version(word):
    """build set that includes @word and the set of word without prefixes

    we start with trying to remove prefixes of length 1, if none are found
    we try longer prefixes
    """
    res = get_prefixless_set(word, PREFIXES)
    if len(res) == 0:
        res = get_prefixless_set(word, PREFIXES2)
    if len(res) == 0:
        res = get_prefixless_set(word, PREFIXES3)

    res.add(word)
    return res


def get_prefixless_set(word, prefixes):
    """build set of strings where each one is @word without one of the @prefixes
    """
    res = set()
    for p in prefixes:
        if word.startswith(p):
            res.add(word[len(p):])

    return res

SPELLINGS = {'שרות': 'שירות'}


def check_spell(cand):
    for w in cand:
        if w['CONTENT'] in SPELLINGS:
            w['CONTENT'] = SPELLINGS[w['CONTENT']]

    return cand


def traverse_cand_strs(cand_strs, cand, no_other=True):
    res = []
    query_count = 0
    for cs in cand_strs:
        query_count += 1
        t = db_api.lookup(cs, no_other)
        for r in t:
            res.append(
                Res_Entry(
                    int(r['id']),
                    r['type'],
                    r['aliases'][0],
                    len(r['aliases']),
                    cs,
                    cand
                )
            )

    return (res, query_count)


MAX_WORDS_IN_QUERY = 6  # should be 32 for current max alias in NLI entities...


def look_for_entities(words):
    res = []
    query_count = 0
    word_index = 0
    while word_index < len(words):
        for slice_length in range(MAX_WORDS_IN_QUERY, 0, -1):
            candidate = words[word_index:word_index + slice_length]
            # print(candidate)
            cand_strs = generate_candidate_variants(candidate)
            (cur_res, cur_query_count) = traverse_cand_strs(
                cand_strs, candidate)
            query_count += cur_query_count
            cur_res = remove_dupes(cur_res)
            res += cur_res

            if cur_res:
                # found at least one match so skip over all words in it
                word_index += slice_length
                break
        else:  # no matches found that start at current word
            word_index += 1
    print("number of queries: {}".format(query_count))
    return res


def path_to_file_list(dir_path, page=-1):
    '''
    Return a list of alto file(s) in a dir.

    @return : list : alto file paths.

    @dir_path : string : relative or absolute path to a dir containing alto files
    @page : int : the page number, starting from 1, or -1 for all pages
    '''

    folder = Path(path)
    files = list(folder.glob('*.xml'))
    files = sorted(files)

    if page != -1:
        page_ind = page - 1
        if page_ind < 0 or page_ind >= len(files):
            print("Wrong page")
            sys.exit(1)
        return [files[page_ind]]
    return files


def gather_info_from_files(files):
    '''
    Return a list of alto words from the supplied files.

    @return : list : alto words
    @files  : list : alto files
    '''
    res = []
    for f in files:
        words = extract_words_from_alto_xml(f)
        res += words

    return res


def remove_dupes(res):
    new_res = []
    can_set = set()
    max_size = -1
    for r in res:
        alias = (r.type, r.alias)
        if alias in can_set:
            if r.alias_len > max_size:
                new_res[:] = [x for x in new_res if not (x[1], x[2]) == alias]
                can_set.add(alias)
                new_res.append(r)
        else:
            new_res.append(r)
            can_set.add(alias)

    return new_res

if __name__ == "__main__":
    path = "books2/IE26721743/REP26723234/"
    page = -1  # default - whole book
    if len(sys.argv) > 1:
        page = int(sys.argv[1])
    files = path_to_file_list(path, page)
    words = gather_info_from_files(files)

    # TODO probably send source (name of file which contains page?) also
    res = look_for_entities(words)
    res = remove_dupes(res)
    print("number of results: {}".format(len(res)))

    # TODO: handle errors
    sha1_bytes = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    sha1 = sha1_bytes[0:-1].decode('utf-8')

    if page != -1:
        base = files[0].stem + "_" + sha1 + ".json"
        out_file = files[0].with_name(base)
    else:
        out_file = Path(path + "whole_book_" + sha1 + ".json")
    with out_file.open('w') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
