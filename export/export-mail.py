import email
import mailbox
import os
import shutil
from datetime import datetime
from typing import Set, Dict

from bs4 import BeautifulSoup

from utility.constant import CSS_BIG
from utility.image import is_image_file
from utility.parse import date_to_string, month_to_string, html_to_pdf

# Legacy


SRC_MBOX = "收件箱.mbox"

# year-month to output, empty list for all dates
YEAR_MONTHS = []

# named after month
HTML_DIR = "html/"
ATTACH_DIR = "attach/"  # assume as a subdir of HTML_DIR

OUT_PDF = False
PDF_DIR = "pdf/"

SINGLE_OUT_FILE = False
# name for single out files
HTML_FILE = "out.html"
PDF_FILE = "out.pdf"

REPLIER_EMAILS = [""]  # ["gmail.com"]
FIX_DATES = [""]  # ["1/1"]


def get_attach(date: datetime, message: mailbox.mboxMessage) -> Set[str]:
    file_names = set()
    if message.get_content_maintype() == "multipart":
        for m in message.walk():
            if m.get_content_maintype() != "multipart" and m.get(
                    "Content-Disposition") is not None and m.get_filename() is not None:
                file_name = f"{date_to_string(date)}-{m.get_filename()}"
                with open(f"{HTML_DIR}{ATTACH_DIR}{file_name}", "wb") as f:
                    f.write(m.get_payload(decode=True))
                    file_names.add(file_name)
    return file_names


def get_body(date: datetime,
             message: mailbox.mboxMessage,
             add_attach: bool = False,
             add_share: bool = False) -> str:
    parser = email.parser.BytesFeedParser(policy=email.policy.default)
    parser.feed(message.as_bytes())
    html = parser.close().get_body(
            preferencelist=["html", "plain"]).get_content()
    if not add_share:
        for mark in ["今日天气:", "[今日诗词]", "[云·养花]",
                     '<img src="https://github.com/yx-z/YunDaily/blob/master'
                     '/Yun/res/title/flower.png?raw=true"',
                     '<img src="https://raw.githubusercontent.com/yx-z'
                     '/YunDaily/master/Yun/res/title/flower.png"']:
            if mark in html:
                html = html[:html.index(mark)]
    soup = BeautifulSoup(html, "html.parser")

    for quote in soup.find_all("blockquote"):
        quote.extract()

    if not add_share:
        share_div = soup.find(id="bot_email_share")
        if share_div is not None:
            share_div.extract()

    if add_attach:
        file_names = get_attach(date, message)
        first_see = True
        for file in os.listdir(f"{HTML_DIR}{ATTACH_DIR}"):
            if is_image_file(file) and file in file_names:
                if first_see:
                    div = soup.new_tag("div")
                    div.string = "附件图片:"
                    soup.append(div)
                    first_see = False
                soup.append(soup.new_tag("br"))
                soup.append(soup.new_tag("img", src=f"{ATTACH_DIR}{file}",
                                         style=CSS_BIG,
                                         alt="missing picture and u"))

    for img in soup.find_all("img"):
        if not img.has_attr("style") and img.get("alt") != "发发":
            img["style"] = CSS_BIG
        if img.get("src").startswith("cid"):
            img.extract()
    return str(soup) + "<br>"


def subject_to_date(subject: str, year: int) -> datetime:
    slash_idx = subject.index("/")
    start_idx = slash_idx - 1
    while start_idx >= 0 and subject[start_idx].isdigit():
        start_idx -= 1
    end_idx = slash_idx + 1
    while end_idx < len(subject) and subject[end_idx].isdigit():
        end_idx += 1
    date_str = f"{year}/{subject[start_idx + 1:end_idx]}"
    return datetime.strptime(date_str, "%Y/%m/%d")


def decode_mime_words(s) -> str:
    return "".join(
            word.decode(encoding or "utf8") if isinstance(word, bytes) else word
            for word, encoding in email.header.decode_header(s))


if __name__ == '__main__':
    dates = set()
    initiator = {}
    replier = {}

    for msg in mailbox.mbox(SRC_MBOX):  # type: mailbox.mboxMessage
        subject = decode_mime_words(msg["subject"])
        # match subject and sender/receiver
        if any(keyword in subject for keyword in ["☁️", "☀️"]) and (any(
                addr in msg["from"] or addr in msg["to"] for addr in
                REPLIER_EMAILS) or any(
                keyword in subject for keyword in FIX_DATES)):
            exact_date = datetime.fromtimestamp(
                    email.utils.mktime_tz(
                            email.utils.parsedate_tz(msg["date"])))
            date = subject_to_date(subject, year=exact_date.year)
            if len(YEAR_MONTHS) == 0 or month_to_string(date) in YEAR_MONTHS:
                dates.add(date)
                if any(src in msg["from"] for src in REPLIER_EMAILS) or any(
                        keyword in subject for keyword in FIX_DATES):
                    if date not in replier:
                        replier[date] = []
                    replier[date].append((subject, msg, exact_date))
                elif any(keyword in subject for keyword in ["记日的云", "云的日志"]):
                    if date not in initiator:
                        initiator[date] = []
                    initiator[date].append((subject, msg, exact_date))


    def write_date(f, date: datetime):
        def write_from_src(src_dict: Dict):
            if date in src_dict:
                cur_msgs = src_dict[date]
                cur_msgs.sort(key=lambda t: t[2])
                f.write(f"<h3>{cur_msgs[0][0]}</h3>")
                for _, msg, time in cur_msgs:
                    f.write(f"<div>At {time.strftime('%H:%M:%S')}</div>")
                    f.write(get_body(date, msg, add_share=False,
                                     add_attach=msg == src_dict[date][-1][1]))

        f.write("<div style=\"font-family:'PingFang SC' !important\">")
        write_from_src(initiator)
        write_from_src(replier)
        f.write("</div>")


    # clean dirs
    if os.path.exists(HTML_DIR):
        shutil.rmtree(HTML_DIR)
    os.makedirs(f"{HTML_DIR}{ATTACH_DIR}", exist_ok=True)
    if OUT_PDF:
        if os.path.exists(PDF_DIR):
            shutil.rmtree(PDF_DIR)
        os.makedirs(PDF_DIR)

    date_sorted = sorted(list(dates))
    if SINGLE_OUT_FILE:
        with open(f"{HTML_DIR}{HTML_FILE}", "a") as f:
            for date in date_sorted:
                write_date(f, date)
        if OUT_PDF:
            html_to_pdf(f"{HTML_DIR}{HTML_FILE}", f"{PDF_DIR}{PDF_FILE}")
    else:
        file_names = set()
        for date in date_sorted:
            file_name = month_to_string(date)
            file_names.add(file_name)
            with open(f"{HTML_DIR}{file_name}.html", "a") as f:
                write_date(f, date)
        if OUT_PDF:
            for file_name in file_names:
                html_to_pdf(f"{HTML_DIR}{file_name}.html",
                            f"{PDF_DIR}{file_name}.pdf")
