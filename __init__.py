import os
import sys
import time
from calibre.customize import FileTypePlugin

class DJVUCovers(FileTypePlugin):

    name                = "Automatic DJVU Covers"
    description         = "Automatically converts the first page of newly added .djvu books to png and adds it as a cover."
    supported_platforms = ["linux"]
    author              = "xor2003"
    version             = (1, 0, 1)
    file_types          = set(['djvu'])
    on_postimport       = True

    def postimport(self, id, fmt, db):
        db = db.new_api
        path = "/tmp/book" + str(int(time.time())) + ".djvu"
        db.copy_format_to(id, fmt, path)
        context = Context()

        cover_path = context.process(path)
        cover = open(cover_path, 'rb').read()
        bidm = {id: cover}
        db.set_cover(bidm)

        os.remove(cover_path)
        os.remove(path)


class Context:

    def process(self, path):
        self.document = path

        return self.generate_cover()

    def generate_cover(self):
        page = self.document
        filename = "/tmp/cover" + str(int(time.time())) + ".png"
        os.system("convert "+page+"[0] "+filename)
        return filename
