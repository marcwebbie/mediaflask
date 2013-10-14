import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append("/usr/lib/python3.3/site-packages/")

from functools import partial
import json
from tempfile import NamedTemporaryFile
from gi.repository import Gtk, Gdk, GdkPixbuf

import downloader


UI_FILE = "desktop.ui.glade"


class PlaylistDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Playlist for download", parent, 0,
                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                            Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(640, 480)

        label = Gtk.Label("Paste urls(one per line) to be downloaded here.")
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("http://www.youtube.com/watch?v=nG4WQtuOkSA\n"
                                 "http://www.youtube.com/watch?v=cq2UgqhGrDU\n"
                                 "http://www.youtube.com/watch?v=g9KZHT2UXpQ")
        scrolledwindow.add(self.textview)

        box = self.get_content_area()
        box.add(label)
        box.add(scrolledwindow)
        self.show_all()


class MediaFlask:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.button_playlist = self.builder.get_object('button_playlist')
        self.url_entry = self.builder.get_object('url_entry')
        self.button_check = self.builder.get_object('button_check')
        self.button_download = self.builder.get_object('button_download')
        self.statusbar = self.builder.get_object('statusbar')

        # thumbnail
        # media title
        # tag title [editable]
        # tag artist [editable]
        # tag album [editable]
        # download [progress]
        # media url [hidden]
        self.store = Gtk.ListStore(str, str, str, str, str, int, str)
        self.tree = self.builder.get_object('tree')
        self.tree.set_model(self.store)

        # renderers
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        text_renderer = Gtk.CellRendererText()
        renderer_progress = Gtk.CellRendererProgress()
        renderer_editabletext_title = Gtk.CellRendererText()
        renderer_editabletext_title.set_property("editable", True)
        renderer_editabletext_artist = Gtk.CellRendererText()
        renderer_editabletext_artist.set_property("editable", True)
        renderer_editabletext_album = Gtk.CellRendererText()
        renderer_editabletext_album.set_property("editable", True)

        # thumbnail
        column_pixbuf = Gtk.TreeViewColumn("Image", renderer_pixbuf, stock_id=0)
        self.tree.append_column(column_pixbuf)

        # retrieved Title
        column_title = Gtk.TreeViewColumn("Media", text_renderer, text=1)
        self.tree.append_column(column_title)

        # tag title [editable]
        column_tag_title = Gtk.TreeViewColumn(
            "Title [editable]", renderer_editabletext_title, text=2)
        self.tree.append_column(column_tag_title)

        # tag artist [editable]
        column_tag_artist = Gtk.TreeViewColumn(
            "Artist [editable]", renderer_editabletext_artist, text=3)
        self.tree.append_column(column_tag_artist)

        # tag album [editable]
        column_tag_album = Gtk.TreeViewColumn(
            "Album [editable]", renderer_editabletext_album, text=4)
        self.tree.append_column(column_tag_album)

        # download [progress]
        column_progress = Gtk.TreeViewColumn("Progress", renderer_progress, value=5)
        self.tree.append_column(column_progress)

        # Selections
        self.current_iter = None
        select = self.tree.get_selection()
        select.connect("changed", self.on_tree_selection_changed)

        renderer_editabletext_title.connect("edited", self.on_edit_title)
        renderer_editabletext_artist.connect("edited", self.on_edit_artist)
        renderer_editabletext_album.connect("edited", self.on_edit_album)

        # Retrieve and show window
        self.window = self.builder.get_object('window')
        self.window.set_title("MediaFlask")
        self.window.show_all()

    def destroy(self, widget):
        Gtk.main_quit()

    def report_hook(self, morceaux, taille_morceau, taille_totale, item_selected=None):
        pourcent = float(taille_morceau * morceaux / taille_totale) * 100
        # sys.stderr.write('\rpourcent: {}\n'.format(pourcent))
        self.store[item_selected][5] = int(pourcent) if pourcent <= 100.0 else 100

    def on_edit_title(self, widget, path, text):
        self.store[path][2] = text

    def on_edit_artist(self, widget, path, text):
        self.store[path][3] = text

    def on_edit_album(self, widget, path, text):
        self.store[path][4] = text

    def on_playlist_clicked(self, widget):
        dialog = PlaylistDialog(self.window)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            tbuffer = dialog.textbuffer
            start_iter = tbuffer.get_start_iter()
            end_iter = tbuffer.get_end_iter()

            spaced_url_list = tbuffer.get_text(start_iter, end_iter, True).split('\n')
            csv_url_list = ';'.join([line.strip() for line in spaced_url_list])
            print(csv_url_list)
            self.url_entry.set_text(csv_url_list)
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()

    def on_important_clicked(self, widget):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "Je t'aime, ma belle.")
        dialog.format_secondary_text(
            "Tu me manques beacoup!")
        dialog.run()
        dialog.destroy()

    def on_button_clicked(self, widget):
        pass

    def on_check_clicked(self, widget):
        url_list = self.url_entry.get_text().split(';')

        for url in url_list:
            self.statusbar.push(0, 'Fetching info for url: {0}...'.format(url))
            info_json = downloader.info(url)
            info_dict = json.loads(info_json)

            if info_dict.get('thumbnail', False):
                thumbnail_url = info_dict['thumbnail']
                thumbnail_img = Gtk.STOCK_NEW
            else:
                thumbnail_img = Gtk.STOCK_NEW

            self.store.append(
                [thumbnail_img, info_dict['stitle'][:30], '<Tag title>', '<Tag artist>', '<Tag album>', 0, info_dict['url']])
            self.statusbar.push(0, 'Retrieved info for url: {0}...'.format(url))

    def on_download_clicked(self, widget):
        if self.current_iter is None:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.OK, "error: No media was selected")
            dialog.format_secondary_text(
                "Select one of the medias already checked on the list.")
            dialog.run()
            dialog.destroy()
            return
        else:
            dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
                                           Gtk.FileChooserAction.SAVE,
                                          (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                           Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            # self.add_filters(dialog)
            selected_iter = self.current_iter

            # title = self.store[selected_iter][2]
            # artist = self.store[selected_iter][3]

            # dialog.set_filename("{0} - {1}.mp3".format(title, artist))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                save_filename = dialog.get_filename()
                # print("save_filename:", save_filename)

                tags = {
                    'title': self.store[selected_iter][2],
                    'artist': self.store[selected_iter][3],
                    'album': self.store[selected_iter][4],
                }

            # artist = self.store[selected_iter][3]
                raw_url = self.store[selected_iter][6]
                rh = partial(self.report_hook, item_selected=selected_iter)
                downloader.download(
                    raw_url, save_filename, export='mp3', bitrate='192', tags=tags, reporthook=rh)
            dialog.destroy()

    def on_tree_selection_changed(self, selection):
        model, curr_iter = selection.get_selected()
        self.current_iter = curr_iter

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("MP3 file")
        filter_text.add_mime_type("audio/mpeg")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python file")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any file")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


if __name__ == "__main__":
    app = MediaFlask()
    Gtk.main()
