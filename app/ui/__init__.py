# pass

APPNAME = 'Solaar'
APPVERSION = '0.5'

from . import (notify, status_icon, main_window, pair_window, action)

from gi.repository import (GObject, Gtk)
GObject.threads_init()


def appicon(receiver_status):
	return (APPNAME + '-fail' if receiver_status < 0 else
			APPNAME + '-init' if receiver_status < 1 else
			APPNAME)


_THEME = Gtk.IconTheme.get_default()

def get_icon(name, fallback):
	return name if name and _THEME.has_icon(name) else fallback

def icon_file(name):
	if name and _THEME.has_icon(name):
		return _THEME.lookup_icon(name, 0, 0).get_filename()
	return None


def find_children(container, *child_names):
	def _iterate_children(widget, names, result, count):
		wname = widget.get_name()
		if wname in names:
			index = names.index(wname)
			names[index] = None
			result[index] = widget
			count -= 1

		if count > 0 and isinstance(widget, Gtk.Container):
			for w in widget:
				count = _iterate_children(w, names, result, count)
				if count == 0:
					break

		return count

	names = list(child_names)
	count = len(names)
	result = [None] * count
	_iterate_children(container, names, result, count)
	return tuple(result) if count > 1 else result[0]


def update(receiver, icon, window):
	GObject.idle_add(action.pair.set_sensitive, receiver.status > 0)
	if window:
		GObject.idle_add(main_window.update, window, receiver)
	if icon:
		GObject.idle_add(status_icon.update, icon, receiver)