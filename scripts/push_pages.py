#!/usr/bin/env python3
"""把 out/ 下的文本写回 Wikisource 的 Page: 名字空间。

用法: PYWIKIBOT_DIR=<有 user-config.py 的目录> python3 push_pages.py <起页> <止页>
默认跳过已有正文的页面；要覆盖请加 --overwrite（仅在用户明确要求时）。
"""
import os, sys, time
import pywikibot
from pywikibot.proofreadpage import ProofreadPage

# —— 改这三项 ——
INDEX = "<书名>.pdf"    # 与 Index: 页同名
SITE = ("zh", "wikisource")
SUMMARY = "OCR (Google, via ocr.wmcloud.org)"

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "ocr")
QUALITY = 1          # 1 = 未校對。纯 OCR / 未经人工核对的一律用 1。
DELAY = 3            # 每次编辑之间的间隔（秒）


def main():
    overwrite = "--overwrite" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    site = pywikibot.Site(*SITE)
    site.login()
    print("已登录:", site.user())

    for p in range(int(args[0]), int(args[1]) + 1):
        src = os.path.join(SRC, f"{p}.txt")
        if not os.path.exists(src):
            print(p, "无文本，跳过")
            continue
        page = ProofreadPage(site, f"Page:{INDEX}/{p}")
        if not overwrite and page.exists() and page.text.strip() and page.body.strip():
            print(p, "已有正文，跳过")
            continue
        with open(src) as fh:
            page.body = fh.read().strip()
        page.ql = QUALITY        # 注意: page.quality_level 是只读属性，赋值会报错
        page.save(summary=SUMMARY, minor=False)
        print(p, "已保存")
        time.sleep(DELAY)


if __name__ == "__main__":
    main()
