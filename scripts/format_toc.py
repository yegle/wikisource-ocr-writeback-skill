#!/usr/bin/env python3
"""点线目录／索引的 wikitext 生成器（示例骨架）。

要点: 条目数据存成结构化列表, wikitext 由函数生成。
用户改主意时（页码要不要括号、缩进层级、col3-width）只改函数, 重跑即可。
输出到 out/ocr/<页>.txt, 再交给 push_pages.py 写回。
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "ocr")
DOTS = "|symbol=……|spaces=0|col3-width=4em"


def E(lv, text, page, hang=True):
    """一条点线条目。lv=缩进层级(0 顶格), page 照排面决定要不要括号。"""
    t = ("{{Dotted TOC page listing|entrytext=%s|pagetext=%s%s%s}}"
         % (text, page, DOTS, "|hi=1em" if hang else ""))
    return t if lv == 0 else "{{left|offset=%dem|%s}}" % (lv, t)


def P(lv, text):
    """跨页断开的残行: 只有文字, 没有点线和页码（页码在下一页承接）。"""
    return text if lv == 0 else "{{left|offset=%dem|%s}}" % (lv, text)


def H(t):
    return "\n{{c|{{larger|%s}}}}\n" % t


def cols(left, right):
    """双栏（索引常用）。left/right 是 (文字, 页码) 列表, None 表示空行分组。"""
    out = ["{{multicol}}"]
    out += [E(0, e[0], e[1], hang=False) if e else "" for e in left]
    out += ["{{multicol-break}}"]
    out += [E(0, e[0], e[1], hang=False) if e else "" for e in right]
    out += ["{{multicol-end}}"]
    return out


# —— 每页的内容（下面是示例，换成你这本书的实际条目）——
pages = {
    4: [
        "{{c|{{x-larger|清溪文集}}}}", "", H("目　　录"), H("卷一　記遊"),
        E(0, "早春遊西山記", "(1)"),
        "",                                          # 原书的空行分组
        E(0, "記客歲冬日與友人夜話西山舊事", "(5)"),
        E(1, "附：答友人問故園今昔書", "(7)"),
        E(2, "又：友人来书", "(9)"),
        P(1, "附：舊照三帧説明"),                       # 点线和页码在下一页承接
    ],
    429: (["{{c|{{x-larger|篇名索引}}}}", "{{rule|30em}}", "",
           "{{c|{{larger|一——四畫}}}}", ""]
          + cols([("山中答問", 55), ("小園記", 275), None,
                  ("古渡", 87)],
                 [("早春遊西山記", 109), ("秋日過故園記", 93)])),
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p, lines in sorted(pages.items()):
        with open(os.path.join(OUT, "%d.txt" % p), "w") as fh:
            fh.write("\n".join(lines).strip() + "\n")
        print(p, "已生成")
