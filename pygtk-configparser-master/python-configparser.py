#!/usr/bin/env python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) Alex Goretoy <alex@goretoy.com>
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE


import os, sys 
import getopt
import threading
import configparser
   
try:
    import pygtk
    pygtk.require("2.0")
    import gtk, gobject
    gobject.threads_init()
    gtk.gdk.threads_init()
except:
    print(sys.stderr, "You need to install the python gtk bindings")
    sys.exit(1)
  
widget_list = {
    "main_window" : [ "add_section_button", "remove_section_button",
                        "section_comboboxentry", 'add_option_button', 
                        'remove_option_button', 'option_name_entry',
                        'option_value_entry', 'config_hbox',
                        'expand_button', 'collapse_button', 'status1_label',
    ],
    'warning_dialog' : [ "warning_dialog_title_label", 'warning_dialog_message_label',
                            'warning_dialog_cancel_button', 'warning_dialog_ok_button',
    ],
    'save_dialog' : [ 'save_dialog_cancel_button', "save_dialog_ok_button",
    ],
    'open_dialog' : [ 'open_dialog_cancel_button', 'open_dialog_cancel_button',
    ],
}


            
class Config(object):
    
    class __Parser(object):
        name = None
        def a(self, name = None):
            if name:
                self.name = name
                self.add_section(self.name)
        def s(self, key = None, value = None, name = None):
            if name:
                self.name = name
            if self.name and key:
                self.set(self.name, key, value)
        def w(self, file):
            with open(file, 'wb') as c:
                self.write(c)
                
    class Conf(ConfigParser.ConfigParser, __Parser):
        pass
    class Raw(ConfigParser.RawConfigParser, __Parser):
        pass
    class Safe(ConfigParser.SafeConfigParser, __Parser):
        pass
        
class uiTreeView(gtk.TreeView):
    columns = []
    rows = {}
    def __init__(self, treestore = None):
        if treestore:
            self.treestore = treestore 
        else:
            self.treestore = gtk.TreeStore(str)
            
        super(uiTreeView, self).__init__(self.treestore)

    def add_columns(self,columns=[], expander_index = -1, edited_callback = None):
        if columns and isinstance(columns, list):
            self.cells = {}
            for i in range(len(columns)):
                def col0_edited_cb( cell, path, new_text, model, callback ):
                    callback(cell, path, new_text, model )
                    #if model[path][2] is not new_text: 
                        #print "Change '%s' to '%s'" % (model[path][2], new_text)
                        #model[path][2] = new_text
                    #return
    
                self.cells[ columns[i] ] = gtk.CellRendererText()
                
                if i == 0:
                    self.cells[ columns[i] ].set_property('cell-background', 'black')
                    self.cells[ columns[i] ].set_property('foreground', 'white')
                else:
                    self.cells[ columns[i] ].set_property( 'editable', True )
                    if edited_callback:
                        self.cells[ columns[i] ].connect( 'edited', col0_edited_cb, self.treestore, edited_callback )
                setattr(self, 'tvcolumn' + str(i), getattr(gtk, 'TreeViewColumn')(columns[i], self.cells[ columns[i] ]))
                curr_column = getattr(self, 'tvcolumn' + str(i) )
                #curr_column.pack_start(self.cell, True)
                #curr_column.set_attribute(cell, 'text', i)
                curr_column.set_attributes(self.cells[ columns[i] ], text=i, cell_background_set=3)
                self.append_column(curr_column)
                if expander_index >= 0 and i == expander_index:
                    self.set_expander_column(curr_column)
    
    def add_row(self,fields = [], index = None):
        return self.append_row(fields, index)
    
    def add_rows(self, rows = []):
        return self.append_rows(rows)
            
    def append_row(self, fields = [], index = None):
        return self.treestore.append(index, fields)
    
    def append_rows(self, rows = []):
        iters = []
        for row in range(len(rows)):
            index, fields = rows[row]
            iters.append(self.append_row(fields, index))
            
        return iters
        
    def other(self):
        # add data
        iter = self.treestore.append(None, ['123', 'Widget'])
        self.treestore.append(iter, ['123-1', 'Widget Frammer'])
        self.treestore.append(iter, ['123-2', 'Widget Whatsit'])
        self.treestore.append(iter, ['123-3', 'Widget Thingy'])
        iter = self.treestore.append(None, ['456', 'Thingamabob'])
        self.treestore.append(iter, ['456-1', 'Thingamabob Frammer'])
        iter1 = self.treestore.append(iter, ['456-2', 'Thingamabob Bunger'])
        self.treestore.append(iter, ['456-2-1', 'Thingamabob Bunger Spring'])


        

        self.b0.connect_object('clicked', gtk.TreeView.expand_all,
                               self.treeview)
        self.b1.connect_object('clicked', gtk.TreeView.collapse_all,
                              self.treeview)
        # make treeview searchable
        self.treeview.set_search_column(0)

        # Allow sorting on the column
        self.tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        #self.treeview.set_reorderable(True)

        self.treeview.enable_model_drag_source(0, [("STRING", 0, 0),
                                                   ('text/plain', 0, 0)
                                                   ],
                                               gtk.gdk.ACTION_DEFAULT)
        self.treeview.enable_model_drag_dest([("STRING", 0, 0),
                                              ('text/plain', 0, 0),
                                              ('text/uri-list', 0, 0)
                                              ],
                                             gtk.gdk.ACTION_DEFAULT)

        self.treeview.connect("drag_data_get", self.drag_data_get_data)
        self.treeview.connect("drag_data_received",
                              self.drag_data_received_data)


class uiBuilder(gtk.Builder):
    def __init__(self, *args, **kwargs):
        super(uiBuilder, self).__init__()
    def add_file(self, file):
        try:
            if os.environ["OS"].startswith("Windows"):
                self.add_from_file(sys.path[0] + '\\' + file ) #+ "\\builder.ui")
        except KeyError:
            self.add_from_file(sys.path[0] + '/' + file ) #+ "/builder.ui")
    def get_widget(self, name = None):
        if name:
            #is name string
            if isinstance(name, basestring):
                setattr(self, name, self.get_object( name ))
                
    def get_widgets(self, name = None):
        if name:    
            #is name dict
            if isinstance(name, dict):
                names = []
                for i in name.keys():
                    if i:
                        names.append(i)
                for i in name.values():
                    if i:
                        if isinstance(i, list):
                            for j in range(len(i)):
                                names.append(i[j])
                        elif isinstance(i, dict):
                            pass
                        else:
                            #else name is a string
                            names.append(i)
                # Get objects (widgets) from the Builder
                for i in range(len(names)):
                    setattr(self, names[i], self.get_object(names[i]))

    def connect_widgets(self, parent):
        self.connect_signals(self)
        
class uiLogic(uiBuilder):
    def __init__(self,*args, **kwargs):
        super(uiLogic, self).__init__(*args, **kwargs)
        file = kwargs.get('builder_file', 'builder.ui')
        self.add_file(file)
        self.get_widgets(widget_list)
        

        self.config_treeview = uiTreeView( gtk.TreeStore(str, str, str, 'gboolean' ) )
        self.config_treeview.connect('button-press-event', self.on_treeview_button_press_event )
        self.config_treeview.add_columns( ['Sections', 'Options','Values'], 0, self.on_column_edited )
        #self.config_treeview.set_default_sort_func( sort_func = None )
        #self.config_treeview.set_property('fixed-height-mode', True)
        self.config_treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
        self.expand_button.connect_object('clicked', gtk.TreeView.expand_all,
                               self.config_treeview)
        self.collapse_button.connect_object('clicked', gtk.TreeView.collapse_all,
                              self.config_treeview)
        
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scrolled_window.add_with_viewport(self.config_treeview)
        
        self.config_hbox.pack_start(scrolled_window)
        
        self.config_treeview.get_selection().connect('changed', self.set_selected_section )
        self.config_treeview.connect('cursor-changed', self.set_selected_section )
        
        self.section_comboboxentry.child.connect('activate', self.on_add_section_button_cb)        
        self.connect_widgets(self)
        self.main_window.show_all()
        
class functions(object):
    pass

    
class DataKeyTypeError(TypeError):
    pass
    
class uiData(dict):  
    def __setitem__(self, key, value):
        if not isinstance(key, basestring):
            self[key] = value
        else:
            print('key must be of type string')
    
    def __getitem__(self, key):
        return self[key]
class uiHelpers(object):
    def _init(self):
        self.config = Config.Raw()
        self.config_filename = None
        self.selected_section = ( None, None )
        self.config_treeview.get_model().clear()
        self.status1_label.set_text('')
        self.warning_dialog_message_label.set_text('')
        self.section_comboboxentry.child.set_text('')
        self.option_name_entry.set_text('')
        self.option_value_entry.set_text('')
        self.main_window.set_title('%s - %s' % ('Untitled', sys.argv[0]))
        self.status1_label.set_text('New Config') 
        self._toggle_option_buttons()
        
    def _toggle_option_buttons(self):
        if self.config.sections() and self.selected_section[0]:
            self.remove_option_button.set_sensitive(True)
            if self.option_name_entry.get_text():
                self.add_option_button.set_sensitive(True)
        else:
            self.add_option_button.set_sensitive(False)
            self.remove_option_button.set_sensitive(False)
        
    def set_selected_section(self, widget, data = None):
        treeselection = self.config_treeview.get_selection()
        treeselection.set_mode(gtk.SELECTION_SINGLE)
        ( tree_model, tree_iter ) = treeselection.get_selected()
        try:
            self.selected_section= ( tree_model.get_value(tree_iter, 0), tree_iter)   
        except TypeError:
            #catch TypeError after removing row
            self.selected_section = (None, None)   
        finally:
            self._toggle_option_buttons()  
            self.option_name_entry.grab_focus()

        
    def update_config_treeview(self):
        self.config_treeview.get_model().clear()
        
        if self.config_filename:
            self.main_window.set_title('%s - %s' % (self.config_filename.split('/')[-1], sys.argv[0]))
        
        for section in self.config.sections():
            section_iter = self.config_treeview.add_row([section, None, None, True], None)
            for name, value in self.config.items( section ):
                 self.config_treeview.add_row([ section, name, value, False ], section_iter)
        self.config_treeview.expand_all()         
        #for section in self.secopt.keys():
        #    section_iter = self.config_treeview.add_row([section, None, None, False], None)
        #    for n in range(len(self.secopt[ section ]['options'])):
        #        self.config_treeview.add_row([section, self.secopt[ section ]['options'][n], self.secopt[ section ]['values'][n], False ], section_iter)
                
class NotAnIter(TypeError):
    '''raised when iter goes stale after remove
    '''
    pass
class uiSignals(uiHelpers):
    def __init__(self, *args, **kwargs):
        super(uiSignals, self).__init__(*args, **kwargs)
        self._init()
    def on_column_edited(self, cell, path, new_text, model ):
        print(dir(cell))
        if model[path][1] != new_text: 
            print("Changed '%s' to '%s'" % (model[path][1], new_text))
            model[path][1] = new_text
            
        if model[path][2] != new_text: 
            print("Change '%s' to '%s'" % (model[path][2], new_text))
            model[path][2] = new_text
        return
    def gtk_widget_hide(self, w, e):
        w.hide()
        return
    def on_menu_new_item_activate(self, w = None, e = None):
        if self.config.sections():
            self.warning_dialog_message_label.set_text('You have some unsaved work.\nAre you sure you want to create a new config file?')
            if self.warning_dialog.run():
                self._init()
                
    def on_menu_open_item_activate(self, w = None, e = None):
        def run():
            if self.open_dialog.run():
                self._init()
                self.status1_label.set_text('Go!') 
                self.config_filename = self.open_dialog.get_filename()
                try:
                    self.config.read([self.config_filename])
                except ConfigParser.MissingSectionHeaderError:
                    self.config_filename = None
                    self.status1_label.set_text('Error: File Missing Section Header')
                self.update_config_treeview()
                
        if self.config.sections():
            self.warning_dialog_message_label.set_text('You have some unsaved work.\nAre you sure you want to open another config file?')
            if self.warning_dialog.run():
                run()
        else:    
            run()
           
    def _save_menu_helper(self):
        if self.config_filename:
            with open(self.config_filename, 'wb') as c:
                self.config.write(c)
            self.status1_label.set_text('Saved %s' % (self.config_filename.split('/')[-1])) 
            return False            
        return True
            
    def on_menu_save_item_activate(self, w = None, e = None):
        #if self.config.sections():
            if(self._save_menu_helper()):
                self.on_menu_save_as_item_activate()
            
    def on_menu_save_as_item_activate(self, w = None, e = None):
        #if self.config.sections():
            if self.save_dialog.run():
                self.config_filename = self.save_dialog.get_filename()
                self._save_menu_helper()
                        
    def on_remove_secopt_button_cb(self, w, e = None):
        #print dir(self.config_treeview.get_selection()), self.config_treeview.get_selection()
        treeselection = self.config_treeview.get_selection()
        (tree_model, tree_iter) = treeselection.get_selected()
        try:
            section = tree_model.get_value(tree_iter, 0)
            option = tree_model.get_value(tree_iter, 1)
            value = tree_model.get_value(tree_iter, 2)
        except TypeError:
            return
                    
        tree_model.remove(tree_iter)
        
        if not option:
            self.status1_label.set_text('Removed %s' % (section)) 
            self.config.remove_section( section )
        else:
            self.status1_label.set_text('Removed %s from %s' % (option, section)) 
            self.config.remove_option( section, option )
     
        self.selected_section = (None, None)
        self.update_config_treeview()
        
    def on_option_name_entry_changed(self,w=None, e=None):
        self._toggle_option_buttons()
        
    def on_add_option_button_cb(self, w, e = None):
        section = self.selected_section[0]
        name, value = (
                        self.option_name_entry.get_text(), 
                        self.option_value_entry.get_text()
        )
        
        if name and section:
            self.config.set( section, name, value )
            
            self.status1_label.set_text('Added %s to %s' % ( name, section ))
            self.option_name_entry.set_text('')
            self.option_value_entry.set_text('')
            self.update_config_treeview()
                
    def on_add_section_button_cb(self, w, e = None):
        section = self.section_comboboxentry.child.get_text()
        if section:
            try:
                self.config.add_section(section)
                self.status1_label.set_text('Added %s' % (section))
            except ConfigParser.DuplicateSectionError:
                self.status1_label.set_text('Duplicate %s' % (section))
            finally:
#                i = self.config_treeview.add_row([section, None, None, True],None)
#                self.selected_section = ( section, i )
                self.update_config_treeview()
                self.option_name_entry.grab_focus()
                self.section_comboboxentry.child.set_text('')
                
    def on_treeview_button_press_event(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                
                popupMenu = gtk.Menu()
                menuPopup1 = gtk.ImageMenuItem (gtk.STOCK_OPEN)
                popupMenu.add(menuPopup1)
                menuPopup2 = gtk.ImageMenuItem (gtk.STOCK_OK)
                popupMenu.add(menuPopup2)
                popupMenu.show_all()
                popupMenu.popup( None, None, None, event.button, time)
            return True
        
    # close the window and quit
    def delete_event(self, widget, event=None, data=None):
        gtk.main_quit()
        return False
    def on_warning_dialog_cancel_button_clicked(self,w=None,e=None):
        self.warning_dialog.hide()
        
    def on_warning_dialog_ok_button_clicked(self, w=None, e=None):
        self.warning_dialog.hide()
    
    def make_pb(self, tvcolumn, cell, model, iter):
        stock = model.get_value(iter, 1)
        pb = self.treeview.render_icon(stock, gtk.ICON_SIZE_MENU, None)
        cell.set_property('pixbuf', pb)
        return

    def str_obj(self, tvcolumn, cell, model, iter):
        obj = model.get_value(iter, 0)
        cell.set_property('text', str(obj))
        return

    def toggled(self, cell, path):
        iter = self.treestore.get_iter(path)
        value = not self.treestore.get_value(iter, 1)
        self.treestore.set_value(iter, 1, value)
        return
        
    def drag_data_get_data(self, treeview, context, selection, target, etime):
        treeselection = treeview.get_selection()
        model, iter = treeselection.get_selected()
        data = model.get_value(iter, 1)
        print(data)
        selection.set('text/plain', 8, data)

    def drag_data_received_data(self, treeview, context, x, y, selection,
                                info, etime):
        print(selection.target, selection.type, selection.format, selection.data)
        drop_info = treeview.get_dest_row_at_pos(x, y)
        if drop_info:
            model = treeview.get_model()
            path, position = drop_info
            data = selection.data
            print(path, data, model.get_value(model.get_iter(path), 1))
        return 
        
class pyGTKConfigParser(uiSignals, uiLogic):
    def __init__(self, *args, **kwargs):
        super(pyGTKConfigParser, self).__init__(*args, **kwargs)
        
        
class options(dict):
    pass
    
#don't worry about passing options to pygtk-parser, it wont really do anything with them atm
##TODO: handle options
def parse_args(args):
    """ Parse args given to program. Change appropriate variables.
    """

    try:
        opts = getopt.getopt(args, "lf:ll:v:h", ['log_filename=', 'log_level=', 'verbose', 'help'])[0]
    except getopt.GetoptError(e):
        print(ArgError, str(e))

    return_args = {
        'interval': 0,
        'user': None,
        'password': None
    }

    for opt, val in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit(1)
        elif opt in ("-lf", "--log_filename"):
            return_args['log_filename'] = val
        elif opt in ("-ll", "--log_level"):
            return_args['log_level'] = get_log_level(val)
        elif opt in ("-v", "--verbose"):
            return_args['verbose'] = True
        else:
            print(ArgError, "Don't know how to handle argument %s" % opt)

    return return_args
    
class ArgError(Exception):
    """ Invalid command line argument exception """
    pass

def main(*args, **kwargs):
    gobject.threads_init()
    pyGTKConfigParser(*args, **kwargs)
    
    #initialize threading system, must be before gtk.main    
    gtk.gdk.threads_init()
    
    #run main gtk
    gtk.main()
    return

if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ArgError(e):
        print("Argument Error: %s!" % e)
        print_help()
        sys.exit(1)

    main(args)

