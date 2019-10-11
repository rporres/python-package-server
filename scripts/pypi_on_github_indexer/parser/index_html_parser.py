import html
import html.parser


class IndexHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.index_lines = []
        self.a_data = {}

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                self.a_data[attr[0]] = html.escape(attr[1])

    def handle_endtag(self, tag):
        if self.a_data:
            self.index_lines.append(self.a_data)
            self.a_data = {}

    def handle_data(self, data):
        if self.a_data:
            self.a_data['data'] = data

    def get_index_data(self, doc):
        self.feed(doc)
        return self.index_lines
