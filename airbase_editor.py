#!/usr/bin/env python

# An editor for the Jomox Airbase99 analog drum module under ALSA (Linux).
# by Sam Brauer (2012)

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pyseq
import sys

# AIRBASE_DATA is a tuple of dictionaries about each instrument (kick, snare, etc).
# Each instrument dict has the keys:
# "label" - the title/name of the instrument
# "parms" - a tuple of dictionaries about each instrument parameter
# Each parm dict must contain at least the keys "label" and "cc".
# Optional keys are "enum" (a tuple of (CC value, descriptive label) pairs)
# or "bool" (a 2-tuple of the CC values for the (false_value, true_value).
# If neither enum nor bool is specified, the parameter is assumed
# to have the full range of values (0-127).

# FIXME: add a "play" key to each instrument which is a tuple of
# of (mindiNoteNum, label) pairs (example: (36, 'kick'), (42, 'CH'), (44, 'CH long'), (46, 'OH'))
# and use it to render one or more play buttons
AIRBASE_DATA = (
    dict(
        label = 'Kick',
        parms = (
            dict(
                label = 'tune',
                cc = 100,
                default = 119,
            ),
            dict(
                label = 'pitch',
                cc = 101,
                default = 15,
            ),
            dict(
                label = 'decay',
                cc = 102,
                default = 75,
            ),
            dict(
                label = 'harmonics',
                cc = 103,
                default = 0,
            ),
            dict(
                label = 'pulse',
                cc = 104,
                default = 16,
            ),
            dict(
                label = 'noise',
                cc = 105,
                default = 16,
            ),
            dict(
                label = 'attack',
                cc = 106,
                default = 127,
            ),
            dict(
                label = 'EQ',
                cc = 107,
                default = 64,
            ),
            dict(
                label = 'level',
                cc = 117,
                default = 127,
            ),
        ),
    ),
    dict(
        label = 'Snare',
        parms = (
            dict(
                label = 'tune',
                cc = 108,
                default = 71,
            ),
            dict(
                label = 'snappy',
                cc = 109,
                default = 125,
            ),
            dict(
                label = 'decay',
                cc = 110,
                default = 114,
            ),
            dict(
                label = 'detune',
                cc = 111,
                default = 64,
            ),
            dict(
                label = 'noise',
                cc = 112,
                default = 25,
            ),
            dict(
                label = 'level',
                cc = 118,
                default = 127,
            ),
        ),
    ),
    dict(
        label = 'Toms',
        parms = (
            dict(
                label = 'lo tune',
                cc = 12,
                default = 63,
            ),
            dict(
                label = 'lo decay',
                cc = 13,
                default = 63,
            ),
            dict(
                label = 'lo level',
                cc = 14,
                default = 127,
            ),
            dict(
                label = 'hi tune',
                cc = 15,
                default = 63,
            ),
            dict(
                label = 'hi decay',
                cc = 16,
                default = 63,
            ),
            dict(
                label = 'hi level',
                cc = 17,
                default = 127,
            ),
        ),
    ),
    dict(
        label = 'Hi-hat',
        parms = (
            dict(
                label = 'tune',
                cc = 18,
                default = 50,
            ),
            dict(
                label = 'closed attack',
                cc = 19,
                default = 0,
            ),
            dict(
                label = 'closed peaktime',
                cc = 20,
                default = 0,
            ),
            dict(
                label = 'closed decay',
                cc = 21,
                default = 5,
            ),
            dict(
                label = 'open attack',
                cc = 22,
                default = 0,
            ),
            dict(
                label = 'open peaktime',
                cc = 23,
                default = 0,
            ),
            dict(
                label = 'open decay',
                cc = 24,
                default = 25,
            ),
            dict(
                label = 'level',
                cc = 25,
                default = 127,
            ),
            dict(
                label = 'high pass cutoff',
                cc = 59,
                default = 100,
            ),
            dict(
                label = 'low pass cutoff',
                cc = 60,
                default = 75,
            ),
            dict(
                label = 'resonance',
                cc = 61,
                default = 100,
            ),
            dict(
                label = 'source',
                cc = 62,
                enum = (
                    (32, 'normal'),
                    (33, 'filter'),
                    (34, 'noise'),
                ),
                default = 32,
            ),
            dict(
                label = 'sample',
                cc = 62,
                enum = (
                    (0, '909'),
                    (1, '808'),
                    (2, 'CR78'),
                    (3, 'JMX'),
                ),
                default = 0,
            ),
            dict(
                label = 'reverse',
                cc = 62,
                bool = (20, 21),
                default = 20,
            ),
        ),
    ),
    dict(
        label = 'Rim',
        parms = (
            dict(
                label = 'tune',
                cc = 44,
                default = 55,
            ),
            dict(
                label = 'attack',
                cc = 45,
                default = 0,
            ),
            dict(
                label = 'peaktime',
                cc = 46,
                default = 0,
            ),
            dict(
                label = 'decay',
                cc = 47,
                default = 64,
            ),
            dict(
                label = 'level',
                cc = 48,
                default = 127,
            ),
            dict(
                label = 'sample',
                cc = 62,
                enum = (
                    (4, '909 rim'),
                    (5, '808 rim'),
                    (6, 'CR78 cowbell'),
                    (7, 'JMX rimshot'),
                ),
                default = 4,
            ),
            dict(
                label = 'reverse',
                cc = 62,
                bool = (22, 23),
                default = 22,
            ),
        ),
    ),
    dict(
        label = 'Clap',
        parms = (
            dict(
                label = 'tune',
                cc = 26,
                default = 55,
            ),
            dict(
                label = 'attack',
                cc = 27,
                default = 0,
            ),
            dict(
                label = 'peaktime',
                cc = 28,
                default = 0,
            ),
            dict(
                label = 'decay',
                cc = 29,
                default = 64,
            ),
            dict(
                label = 'level',
                cc = 30,
                default = 127,
            ),
            dict(
                label = 'sample',
                cc = 62,
                enum = (
                    (8, '909 clap'),
                    (9, '808 clap'),
                    (10, 'CR78 cymbal'),
                    (11, 'JMX handclap'),
                ),
                default = 8,
            ),
            dict(
                label = 'reverse',
                cc = 62,
                bool = (24, 25),
                default = 24,
            ),
        ),
    ),
    dict(
        label = 'Crash',
        parms = (
            dict(
                label = 'tune',
                cc = 49,
                default = 50,
            ),
            dict(
                label = 'attack',
                cc = 50,
                default = 0,
            ),
            dict(
                label = 'peaktime',
                cc = 51,
                default = 15,
            ),
            dict(
                label = 'decay',
                cc = 52,
                default = 64,
            ),
            dict(
                label = 'level',
                cc = 53,
                default = 127,
            ),
            dict(
                label = 'sample',
                cc = 62,
                enum = (
                    (12, '909 crash'),
                    (13, '808 cymbal'),
                    (14, 'CR78 tambourine'),
                    (15, 'JMX crash'),
                ),
                default = 12,
            ),
            dict(
                label = 'reverse',
                cc = 62,
                bool = (26, 27),
                default = 26,
            ),
        ),
    ),
    dict(
        label = 'Ride',
        parms = (
            dict(
                label = 'tune',
                cc = 54,
                default = 50,
            ),
            dict(
                label = 'attack',
                cc = 55,
                default = 0,
            ),
            dict(
                label = 'peaktime',
                cc = 56,
                default = 5,
            ),
            dict(
                label = 'decay',
                cc = 57,
                default = 64,
            ),
            dict(
                label = 'level',
                cc = 58,
                default = 127,
            ),
            dict(
                label = 'sample',
                cc = 62,
                enum = (
                    (16, '909 ride'),
                    (17, '808 cowbell'),
                    (18, 'CR78 guiro'),
                    (19, 'JMX ride'),
                ),
                default = 16,
            ),
            dict(
                label = 'reverse',
                cc = 62,
                bool = (28, 29),
                default = 28,
            ),
        ),
    ),
    dict(
        label = 'LFOs',
        parms = (
            dict(
                label = 'waveform1',
                cc = 75,
                enum = (
                    (0, 'saw up free'),
                    (1, 'saw down free'),
                    (2, 'tri free'),
                    (3, 'rect free'),
                    (8, 'saw up sync'),
                    (9, 'saw down sync'),
                    (10, 'tri sync'),
                    (11, 'rect sync'),
                ),
                default = 0,
            ),
            dict(
                label = 'destination1',
                cc = 76,
                enum = (
                    (0, 'kick tune'),
                    (1, 'snare tune'),
                    (2, 'lo-tom tune'),
                    (3, 'hi-tom tune'),
                    (4, 'hi-hat tune'),
                    (5, 'HP filter cutoff'),
                    (6, 'clap tune'),
                    (7, 'rim tune'),
                    (8, 'crash tune'),
                    (9, 'ride tune'),
                ),
                default = 0,
            ),
            dict(
                label = 'intensity1',
                cc = 77,
                default = 0,
            ),
            dict(
                label = 'rate1',
                cc = 78,
                default = 0,
            ),
            dict(
                label = 'waveform2',
                cc = 79,
                enum = (
                    (0, 'saw up free'),
                    (1, 'saw down free'),
                    (2, 'tri free'),
                    (3, 'rect free'),
                    (8, 'saw up sync'),
                    (9, 'saw down sync'),
                    (10, 'tri sync'),
                    (11, 'rect sync'),
                ),
                default = 0,
            ),
            dict(
                label = 'destination2',
                cc = 80,
                enum = (
                    (0, 'kick tune'),
                    (1, 'snare tune'),
                    (2, 'lo-tom tune'),
                    (3, 'hi-tom tune'),
                ),
                default = 0,
            ),
            dict(
                label = 'intensity2',
                cc = 81,
                default = 0,
            ),
            dict(
                label = 'rate2',
                cc = 82,
                default = 0,
            ),
        ),
    ),
)

class AirbaseSeq(pyseq.PySeq):

    def init(self, *args):
        self.oport=self.createOutPort()
        self.iport=self.createInPort()
        self.channel = 0
        self.cc_event = pyseq.snd_seq_event()

    def set_app(self, app):
        self.app = app

    def set_channel(self, ch):
        self.channel = ch

    def callback(self, ev):
        #print ev
        if ev.type != pyseq.SND_SEQ_EVENT_CONTROLLER: return 1
        data = ev.getData()
        if data.channel != self.channel: return 1
        cc = data.param
        val = data.value
        #print "CC#%s = %s" % (cc, val)
        gobject.idle_add(self.app.handle_cc, cc, val)
        return 1

    def send_cc(self, num, val):
        self.cc_event.setController(self.channel, num, val)
        #print self.cc_event
        self.cc_event.sendNow(self, self.oport)

class AirbaseEditor:
    def __init__(self):
        self.channel = 0 # FIXME: get from commandline arg or config file?
        self.channel = 9 # FIXME: hardcode to ch 10 for now

        self.filename = None

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window = window
        window.set_title("AirbaseEditor")
        window.set_size_request(400, 572)
        #window.set_resizable(False)
        window.set_position(1)
        window.connect("delete_event", self.delete_event)

        box = gtk.VBox(False, 0)
        window.add(box)

        menubar = gtk.MenuBar()
        box.pack_start(menubar, False, False, 0)

        menu = gtk.Menu()
        
        item = gtk.MenuItem("Open...")
        item.connect("activate", self.load_kit_callback)
        menu.append(item)
        
        item = gtk.MenuItem("Reload")
        item.connect("activate", self.reload_kit_callback)
        item.set_sensitive(False)  # Only sensitive (aka "enabled") if self.filename
        self.reload_btn = item
        menu.append(item)
        
        item = gtk.MenuItem("Save")
        item.connect("activate", self.save_kit_callback)
        item.set_sensitive(False)  # Only sensitive (aka "enabled") if self.filename
        self.save_btn = item
        menu.append(item)
        
        item = gtk.MenuItem("Save as...")
        item.connect("activate", self.save_kit_as_callback)
        menu.append(item)
        
        item = gtk.MenuItem("Init")
        item.connect("activate", self.init_kit_callback)
        menu.append(item)
        
        item = gtk.MenuItem("Send")
        item.connect("activate", self.send_kit_callback)
        menu.append(item)
        
        item = gtk.MenuItem("Exit")
        item.connect("activate", self.delete_event)
        menu.append(item)

        item = gtk.MenuItem("Kit")
        item.set_submenu(menu)
        menubar.append(item)

        # FIXME: add instrument menu with Init and Send, and possibly also Load and Save?

        menu = gtk.Menu()
        
        item = gtk.MenuItem("Init")
        item.connect("activate", self.init_instrument_callback)
        menu.append(item)

        item = gtk.MenuItem("Part")
        item.set_submenu(menu)
        menubar.append(item)

        notebook = gtk.Notebook()
        self.notebook = notebook
        notebook.set_border_width(5)
        box.pack_start(notebook, True, True, 0)

        self.parm_values = {}
        self.widgets = {}
        self.parms_by_cc = {}

        for instrument in AIRBASE_DATA:
            parms = instrument['parms']
            table = gtk.Table(len(parms), 2)
            table.set_border_width(5)
            notebook.append_page(table, tab_label=gtk.Label(instrument['label']))
            for (idx, parm) in enumerate(parms):
                label = gtk.Label("%s: " % parm['label'])
                label.set_alignment(1.0, 0.0)
                table.attach(label, 0, 1, idx, idx+1, gtk.FILL, 0)
                parm_key = "%s.%s" % (instrument['label'], parm['label'])
                parm['key'] = parm_key
                cc = parm['cc']
                parms_for_cc = self.parms_by_cc.get(cc, [])
                if not parms_for_cc: self.parms_by_cc[cc] = parms_for_cc
                parms_for_cc.append(parm)
                widget = None
                if parm.has_key('enum'):
                    widget = gtk.OptionMenu()
                    menu = gtk.Menu()
                    for (val, label) in parm['enum']:
                        menu.add(gtk.MenuItem(label=label))
                    widget.set_menu(menu)
                    widget.parm = parm
                    widget.parm_key = parm_key
                    vals = [x[0] for x in parm['enum']]
                    parm['vals'] = vals
                    widget.connect("changed", self.changed_callback)
                elif parm.has_key('bool'):
                    widget = gtk.CheckButton()
                    widget.parm = parm
                    widget.parm_key = parm_key
                    widget.connect("toggled", self.changed_callback)
                else:
                    adj = gtk.Adjustment(0.0, 0.0, 127.0, 1.0, 16.0, 0.0)
                    widget = gtk.HScale(adj)
                    #widget.set_update_policy(gtk.UPDATE_CONTINUOUS)
                    widget.set_update_policy(gtk.UPDATE_DELAYED)
                    widget.set_digits(0)
                    widget.set_value_pos(gtk.POS_TOP)
                    widget.set_draw_value(True)
                    adj.parm = parm
                    adj.parm_key = parm_key
                    adj.connect("value_changed", self.changed_callback)
                table.attach(widget, 1, 2, idx, idx+1, gtk.EXPAND|gtk.FILL, 0)
                self.widgets[parm_key] = widget

        #from pprint import pprint
        #pprint(self.parms_by_cc)

        self.seq = AirbaseSeq('AirbaseEditor')
        self.seq.set_channel(self.channel)
        self.seq.set_app(self)
        self.thread = pyseq.MidiThread(self.seq)
        self.thread.start()

        self.init_kit(send_ccs=False)

        if len(sys.argv) > 1:
            fn = sys.argv[1]
            self.set_filename(fn)
            self.load_kit()
        else:
            self.send_kit_ccs()

        window.show_all()

    def send_kit_ccs(self):
        for idx in range(len(AIRBASE_DATA)):
            self.send_instrument_ccs(idx)

    def send_kit_callback(self, ev):
        self.send_kit_ccs()

    def send_instrument_ccs(self, idx):
        for parm in AIRBASE_DATA[idx]['parms']:
            cc = parm['cc']
            parm_key = parm['key']
            val = self.parm_values[parm_key]
            self.seq.send_cc(cc, val)

    def init_kit(self, send_ccs=True):
        for idx in range(len(AIRBASE_DATA)):
            self.init_instrument(idx, send_ccs=send_ccs)

    def init_kit_callback(self, ev):
        self.init_kit()

    def init_instrument(self, idx, send_ccs=True):
        for parm in AIRBASE_DATA[idx]['parms']:
            self.handle_cc(parm['cc'], parm['default'])
        if send_ccs:
            self.send_instrument_ccs(idx)

    def init_instrument_callback(self, ev):
        self.init_instrument(self.notebook.get_current_page())

    def changed_callback(self, widget):
        parm = widget.parm
        cc = parm['cc']
        if parm.has_key('enum'):
            val = parm['enum'][widget.get_history()][0]
        elif parm.has_key('bool'):
            val = parm['bool'][int(widget.get_active())]
        else:
            val = int(widget.value)
        self.parm_values[widget.parm_key] = val
        self.seq.send_cc(cc, val)

    def delete_event(self, *args):
        self.thread.stop()
        gtk.main_quit()
        #print "Bye!"
        return False

    def handle_cc(self, cc, val):
        parms = self.parms_by_cc.get(cc)
        if parms:
            for parm in parms:
                if parm.has_key('enum'):
                    vals = parm['vals']
                    if val in vals:
                        idx = vals.index(val)
                        parm_key = parm['key']
                        self.parm_values[parm_key] = val
                        self.widgets[parm_key].set_history(idx)
                        return
                elif parm.has_key('bool'):
                    vals = parm['bool']
                    if val in vals:
                        idx = vals.index(val)
                        parm_key = parm['key']
                        self.parm_values[parm_key] = val
                        self.widgets[parm_key].set_active(bool(idx))
                        return
                else:
                    parm_key = parm['key']
                    self.parm_values[parm_key] = val
                    self.widgets[parm_key].set_value(val)
                    return

    def save_kit_as_callback(self, ev):
        chooser = gtk.FileChooserDialog(title="Save kit as...", action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        response = chooser.run()
        save = False
        if response == gtk.RESPONSE_OK:
            self.set_filename(chooser.get_filename())
            save = True
        chooser.destroy()
        if save: self.save_kit()

    def save_kit_callback(self, ev):
        self.save_kit()

    def save_kit(self):
        try:
            outfile = open(self.filename, 'w')
            for instrument in AIRBASE_DATA:
                self.save_instrument_to_file(outfile, instrument)
            outfile.close()
        except:
            dialog = gtk.MessageDialog(flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="Error saving kit.")
            dialog.run()
            dialog.destroy()

    def save_instrument_to_file(self, outfile, instrument):
        for parm in instrument['parms']:
            cc = parm['cc']
            key = parm['key']
            val = self.parm_values[key]
            outfile.write("%s:%s # %s\n" % (cc, val, key))

    def load_kit(self):
        try:
            infile = open(self.filename, 'r')
            data = infile.read().split('\n')
            infile.close()
            for line in data:
                # Strip comments
                if '#' in line:
                    line = line[:line.index('#')]
                line = line.strip()
                # Ignore blank lines
                if not line: continue
                # Assume the line contains a cc# and value pair separated by a semicolon ("CC:VAL")
                (cc, val) = line.split(':', 1)
                self.handle_cc(int(cc), int(val))
        except:
            dialog = gtk.MessageDialog(flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="Error loading kit.")
            dialog.run()
            dialog.destroy()

    def load_kit_callback(self, ev):
        chooser = gtk.FileChooserDialog(title="Load kit...", action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        response = chooser.run()
        load = False
        if response == gtk.RESPONSE_OK:
            self.set_filename(chooser.get_filename())
            load = True
        chooser.destroy()
        if load: self.load_kit()

    def reload_kit_callback(self, ev):
        self.load_kit()

    def set_filename(self, fn):
        self.filename = fn
        if fn:
            self.window.set_title("AirbaseEditor - %s" % fn)
            self.save_btn.set_sensitive(True)
            self.reload_btn.set_sensitive(True)
        else:
            self.window.set_title("AirbaseEditor")
            self.save_btn.set_sensitive(False)
            self.reload_btn.set_sensitive(False)

def main():
    gobject.threads_init()
    app = AirbaseEditor()
    gtk.main()
    return 0

if __name__ == "__main__":
    main()
