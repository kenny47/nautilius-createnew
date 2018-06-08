import os
import gtk
import os.path

from gi.repository import Nautilus, GObject, Gtk

def get_user_input(parent, message, title='', default_text=''):
    # Returns user input as a string or None
    # If user does not input text it returns None, NOT AN EMPTY STRING.
    dialogWindow = Gtk.MessageDialog(parent,
                          Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                          Gtk.MessageType.QUESTION,
                          Gtk.ButtonsType.OK_CANCEL,
                          message)

    dialogWindow.set_title(title)

    dialogBox = dialogWindow.get_content_area()
    userEntry = Gtk.Entry()
    userEntry.set_visibility(True)
    userEntry.set_size_request(250,0)
    userEntry.set_text(default_text)
    dialogBox.pack_end(userEntry, False, False, 0)

    dialogWindow.show_all()
    response = dialogWindow.run()
    text = userEntry.get_text() 
    dialogWindow.destroy()
    if (response == Gtk.ResponseType.OK) and (text != ''):
        return text
    else:
        return None

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass
    def menu_create_text(self, menu, window, file):
        filename = get_user_input(window, "", "Name", "untitled.txt")
        if (filename != None): 
		os.system('touch %s/%s & pid=$!' % (file.get_location().get_path(), filename))
                os.system('gedit %s/%s & pid=$!' % (file.get_location().get_path(), filename))
		os.system('rm %s/%s & pid=$!' % (file.get_location().get_path(), filename))
    def menu_create_odt(self, menu, window, file):
        filename = get_user_input(window, "", "Name", "untitled.odt")
        if (filename != None): 
		os.system('touch %s/%s & pid=$!' % (file.get_location().get_path(), filename))
		os.system('libreoffice --writer -o %s/%s & pid=$!' % (file.get_location().get_path(), filename))
    def menu_create_ods(self, menu, window, file):
        filename = get_user_input(window, "", "Name", "untitled.ods")
        if (filename != None): 
                basename, ext = os.path.splitext(filename)
                ext = ext[1:]
		os.system('touch %s/%s.csv & pid=$!' % (file.get_location().get_path(), basename))
		os.system('libreoffice --convert-to %s %s/%s.csv' % (ext, file.get_location().get_path(), basename))
		os.system('rm %s/%s.csv & pid=$!' % (file.get_location().get_path(), basename))
		os.system('libreoffice --calc -o %s/%s & pid=$!' % (file.get_location().get_path(), filename))
    def menu_create_odp(self, menu, window, file):
	# Unfortunately there is no workaround for presentations..
	os.system('libreoffice --impress & pid=$!')

    def get_background_items(self, window, file):
        submenu = Nautilus.Menu()
        createnew = Nautilus.MenuItem(name='ExampleMenuProvider::Foo', 
                                         label='Create new ...', 
                                         tip='',
                                         icon='')
        createnew.set_submenu(submenu)
        newfile = Nautilus.MenuItem(name='ExampleMenuProvider::Foo', 
                                         label='Text file', 
                                         tip='',
                                         icon='')
        newdoc = Nautilus.MenuItem(name='ExampleMenuProvider::Foo', 
                                         label='LibreOffice document', 
                                         tip='',
                                         icon='')
        newsheet = Nautilus.MenuItem(name='ExampleMenuProvider::Foo', 
                                         label='LibreOffice spreadsheet', 
                                         tip='',
                                         icon='')
        newpreso = Nautilus.MenuItem(name='ExampleMenuProvider::Foo', 
                                         label='LibreOffice presentation', 
                                         tip='',
                                         icon='')
        submenu.append_item(newfile)
        newfile.connect('activate', self.menu_create_text, window, file)
        if os.path.isfile("/usr/bin/libreoffice"):
		submenu.append_item(newdoc)
		submenu.append_item(newsheet)
		submenu.append_item(newpreso)
		newdoc.connect('activate', self.menu_create_odt, window, file)
		newsheet.connect('activate', self.menu_create_ods, window, file)
		newpreso.connect('activate', self.menu_create_odp, window, file)
        return createnew,
