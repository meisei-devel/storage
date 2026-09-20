#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import html
import io
import sys
import MeCab

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def mecab_list(text):
    tagger = MeCab.Tagger()
    tagger.parse("")

    node = tagger.parseToNode(text)
    word_class = []

    while node:
        # BOS/EOSノードは surface が空なので除外
        if node.surface:
            features = node.feature.split(",")

            surface = node.surface
            pos1 = features[0] if len(features) > 0 else ""
            pos2 = features[1] if len(features) > 1 else ""
            pos3 = features[2] if len(features) > 2 else ""

            # UniDicでは原形が6番目固定とは限らないので、
            # まずは安全に候補を取得
            base = ""
            if len(features) > 7:
                base = features[7]
            elif len(features) > 6:
                base = features[6]

            word_class.append(
                (surface, pos1, pos2, pos3, base)
            )

        node = node.next

    return word_class


def main():
    form = cgi.FieldStorage()
    mecab_ta = form.getfirst("mecab_ta", "")

    print("Content-Type: text/html; charset=UTF-8")
    print()

    if not mecab_ta:
        return

    result = mecab_list(mecab_ta)

    for item in result:
        surface, pos1, pos2, pos3, base = item

        print(
            "{}　[{}, {}, {}, {}]<br>".format(
                html.escape(surface),
                html.escape(pos1),
                html.escape(pos2),
                html.escape(pos3),
                html.escape(base),
            )
        )


if __name__ == "__main__":
    main()
