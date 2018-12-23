
def create_full_title(record_dictionary):
    full_title_string = ""
    if record_dictionary["Prefix"] != "":
        full_title_string += record_dictionary["Prefix"].strip() + " "
    full_title_string += record_dictionary["Title"].strip()
    if record_dictionary["Subtitle"] not in ["", "N/A"]:
        full_title_string += ": " + record_dictionary["Subtitle"].strip()
    return full_title_string

def remove_tags(text_with_html, italics=False):
    html_to_remove = ['<span style="mso-tab-count:1">',
                      '<span style="mso-bookmark:_Toc526497264">',
                      '<span style="mso-bookmark:_Toc526497273">',
                      '<span style="mso-bookmark:_Toc526497265">',
                      '<span style="mso-ansi-language: EN-US">',
                      '<span style="mso-ansi-language:EN-US>',
                      '<span style="mso-ansi-language:EN-US">',
                      '<span lang=\"EN\">',
                      '</span>',
                      '<o:p></o:p>',
                      '<h3>',
                      '</h3>',
                      '</a>']
    if italics == False:
        html_to_remove += ['<i style="mso-bidi-font-style:normal">',
                           '<i style="mso-bidi-font-style: normal">',
                           '</i>']
    text_cleaned = text_with_html
    for html_piece in html_to_remove:
        text_cleaned = text_cleaned.replace(html_piece, '')
    while "<a " in text_cleaned:
        left_index = text_cleaned.index("<a ")
        left_removed = text_cleaned[left_index:]
        right_index = left_removed.index(">")
        a_tag = left_removed[:right_index + 1]
        text_cleaned = text_cleaned.replace(a_tag, '')
    return text_cleaned

def clean_html_title(html_title):
    html_title_cleaned = remove_tags(html_title)
    if html_title_cleaned[0] in '123456789' and '. ' in html_title_cleaned[:5]:
        html_title_cleaned = ". ".join(html_title_cleaned.split(". ")[1:])
    html_title_cleaned = html_title_cleaned.strip()
    return html_title_cleaned
