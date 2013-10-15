#!/usr/bin/env python
"""
Providing Tools for file handling.

"""

import os
import sys
import shutil
import filecmp
import urllib

__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2007-2010 Xin Shi"
__license__   = "GNU GPL"


class UserFile(object):
    '''Class to handle file  '''
    def __init__(self, filename=None):
        self.data = []    
        if filename:
            self.input(filename)
            self.file = filename

    def input(self, filename, verbose=0):
        fi = open(filename, 'r')
        for line in fi:
            self.data.append(line)
        fi.close()

    def append(self, content):
        self.data.append(content)
        
    def extend(self, content):
        self.data.extend(content)

    def output_screen(self):
        print ''.join(self.data)
        
    def output(self, filename=None, verbose=0):
        if not filename:
            self.output_screen()
            return 

        if os.access(filename, os.F_OK) :
            tmpfile  = filename+'.tmp'
            
            fo = open(tmpfile ,'w')
            for line in self.data:
                fo.write(line)
            fo.close()
             
            if filecmp.cmp(filename, tmpfile, shallow=False):
                message = 'up-to-date: %s' % filename
            else:
                message = 'updating %s ...' %filename
            os.rename(tmpfile, filename)

        else:
            message = 'writing %s ...' %filename
            
            head, tail = os.path.split(filename)
            if head != '' and not os.access(head, os.F_OK) :
                if verbose > 0:
                    sys.stdout.write('creating dir %s ...\n'  % head)
                os.makedirs(head)

            fo = open(filename ,'w')
            for line in self.data:
                fo.write(line)
            fo.close()

        if verbose > 0 :
            sys.stdout.write(message+'\n')

        return message

    def replace(self, old, new):
        line_num = 0
        for line in self.data:
            line_num = line_num + 1
            if old in line:
                self.data[line_num-1] = line.replace(old, new)

    def backup(self, prefix, verbose=0):
        path, name =  os.path.split(self.file)
        backup_file  = os.path.join(path, prefix + name)

        if 'default' in prefix and os.path.exists(backup_file):
            if verbose > 0: 
                sys.stdout.write('\nDefault file exits! : %s\n' % backup_file)
            return

        self.output(backup_file , verbose)



    def restore(self, prefix, verbose=0):
        path, name  =  os.path.split(self.file)
        backup_file =  os.path.join(path, prefix + name)

        f = UserFile(backup_file)
        self.data = f.data
            
            
    def insert(self, index, newline):
        line_num = 0
        for line in self.data:
            line_num = line_num + 1
            if index in line:
                self.data.insert(line_num-1, newline)
                return 
        
    def find(self, pat):
        for line in self.data:
            if pat in line:
                return True
        return False
        

class TEXFile(UserFile):
    "handle LaTeX file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        if filename:
            self.parse()
        
        self.tables = {}

    def parse(self):
        "parse LaTeX file"

        tmp_tables = {}
        tab_no  = 0
        line_no = 0
        tab_start = 0
        tab_end = 0

        for line in self.data:
            line_no += 1
            if 'begin{table' in line:
                tab_no += 1
                tab_start = line_no
                tmp_tables[tab_no] ={}
                
            if 'end{table' in line:
                tab_end = line_no
                tmp_tables[tab_no]= self.parse_table(tab_start,tab_end-1)
                
        self.tables= tmp_tables
 
    def parse_table(self, tab_start, tab_end):
        "parse table in LaTeX file"
        parsed_table = {}
        parsed_table['label']= None
        parsed_table['start']= tab_start
        parsed_table['end']  = tab_end
        table = self.data[tab_start:tab_end]

        content = ''.join(table)
        label    = content.split('label{')[-1].split('}')[0]
        tabular  = content.split('begin{tabular}'\
                                 )[-1].split('\\end{tabular}')[0]

        tabular_format  = tabular.split('}')[0]+'}'
        tabular_content = tabular.replace(tabular_format, '')

        parsed_table['data']     = table
        parsed_table['content']  = content
        parsed_table['label']    = label
        parsed_table['tabular']  = tabular_content

        return parsed_table

    def tables_update(self, tables):

        for label, tabfile in tables:
            
            for k, v in self.tables.items():
                if label == v['label']:
                    if not os.access(tabfile, os.F_OK):
                        print '  skip:       Table %s: %s' %(k, label)
                        continue
                    
                    self.tabular_update(k, tabfile)


    def tabular_update(self, num, tabfile):
        tab = self.tables[num]
        tab_start = tab['start']
        tab_end   = tab['end']
        old_tabular = tab['tabular']
        label = tab['label']

        new_tabular = TEXFile(tabfile)['content']
        if old_tabular != new_tabular:
            print '  updating Table %s: %s ...' %(num, label)
            tab['content'] = tab['content'].replace(
                tab['tabular'], new_tabular)
            self.data[tab_start:tab_end] = tab['content']
            self.parse()
        else:
            print '  up-to-date: Table %s: %s' %(num, label)
            
    
class BASHFile(UserFile):
    "handle Bash file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        
    def get_value(self, key):
        new_data = []

        for line in self.data:
            if key in line:
                value = line.split('= ')[-1].strip()
                return value

    def replace_value(self, old_value, new_value):
        new_data = []
        for line in self.data:
            if old_value in line:
                new_line = line.replace(old_value, new_value)
                line = new_line
            new_data.append(line)

        self.data = new_data


    def set_value(self, key, value):
        new_data = []

        for line in self.data:
            if key in line and line.index(key) ==0:
                line = line.split('=')[0]+'=\n'
                new_line = line.replace('=', '=%s' %value)
                line = new_line
            new_data.append(line)

        self.data = new_data
        
class CLEOGLOGFile(UserFile):
    "handle CLEOG log file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)

        self.stream_event = 'N/A' 
        self.processed_stops = 'N/A' 
        self.trim()
        self.parse()
        

    def parse(self):
        "parse CLEOG log file"
        self.lumi = {}
        self.lumi['Ebeam'] = {}
        line_no = -1
        found_stream_event = False
        start_lumi_info = False
        for line in self.data:
            line_no += 1

            if 'Stream event' in line:
                self.stream_event = line.split(':')[-1].strip()
                found_stream_event = True
                
            if found_stream_event and 'Processed' in line:
                line = line.strip()
                self.processed_stops  = line.split(' ')[1].strip()

            if 'Luminosity =' in line:
                values = line.strip().split('=')[-1].split('+-')
                lumi_val = values[0].strip()
                lumi_err_stat = values[1].strip()
                lumi_err_syst = values[2].replace('*', '').strip()
                total_lumi =  (lumi_val, lumi_err_stat, lumi_err_syst)
                self.lumi['Luminosity'] = total_lumi

            if 'Ebeam # runs' in line:
                start_lumi_info = True
                lumi_beam_start = line_no + 2

            if start_lumi_info and '*............' in line:
                lumi_beam_end = line_no
                for beam_lumi in self.data[lumi_beam_start:lumi_beam_end]:
                    items = beam_lumi.split()
                    ebeam = items[1]
                    lumi_val = items[3].replace('+-', '')
                    lumi_err_stat = items[4].replace('+-', '')
                    lumi_err_syst = items[5]
                    lumi = (lumi_val, lumi_err_stat, lumi_err_syst)
                    self.lumi['Ebeam'][ebeam] = lumi

                start_lumi_info = False

    def trim(self):
        "Trim the CLEOG log file, leave only latest message."
        sep = 'By default C3_ is defined as /nfs/cleo3'
        position = 0
        line_no = -1
        for line in self.data:
            line_no += 1
            if sep in line:
                position = line_no
        self.data = self.data[position:]

                
class DECFile(UserFile):
    "handle DEC file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        
        self.decays = {}
        self.parent = None
        self.modes = []
        self.parse()
        
    def parse(self):
        "parse DEC file"

        line_no = 0

        for line in self.data:
            line_no += 1
            elems = line.strip().split(' ')
            
            if '-----' in elems[0] and '-----' in elems[2] :
                self.parent = elems[1]
                continue

            mode = elems[1:]
            mode.sort() 
            mode = ' '.join(mode)
            ratio = elems[0]
            if mode :
                self.modes.append(mode)
                self.decays[mode] = ratio
            

class PDLFile(UserFile):
    "handle PDL file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        
        self.particles = {}
        self.pnames = []
        self.parse()
        
    def parse(self):
        "parse PDL file"
        line_no = 0

        for line in self.data:
            line_no += 1
            line = line.strip()
            if line == '' or line.startswith('*') or line.startswith(
                'sets') or line.startswith('end') :
                continue
            
            elems = line.strip().split(' ')
            elems = [li for li in elems if li]

            particle_ = {}
            try:
                name_ = elems[3]
                particle_['mass'] = elems[5]
                particle_['type'] = elems[2]
                particle_['id']   = elems[4]
                particle_['width'] = elems[6]
            except IndexError:
                raise ValueError(line)
            
            self.pnames.append(name_)
            self.particles[name_] = particle_


class RunFile(UserFile):
    "handle runlist file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        self.runs = {}
        self.parse()
        
    def parse(self):
        line_no = 0
        for line in self.data:
            line_no += 1
	    elems = line.strip().split(' ')
            elems = [li for li in elems if li]
	    run = {}
	    run_no = int(elems[0])
	    run['lumi'] = eval(elems[2])
	    self.runs[run_no] = run

    def get_total_lumi(self, unit='/nb'):
	total_lumi = 0
	runs = self.runs.keys()
	runs.sort()
	for run in runs:
	    lumi = self.runs[run]['lumi']
	    total_lumi += lumi

	if unit == '/pb':
	    total_lumi = total_lumi/1000
	    
	return total_lumi
	
	
class SHFile(UserFile):
    "handle SH file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        
    def get_value(self, key):
        new_data = []
        for line in self.data:
            if key in line:
                value = line.split('=')[-1].strip()
                return value

    def get_value_from_parentheses(self, value):
        step1= value.split('(')[1]
        value= step1.split(')')[0]
        return value
        
    def replace_value(self, old_value, new_value):
        new_data = []
        for line in self.data:
            if old_value in line:
                new_line = line.replace(old_value, new_value)
                line = new_line

            new_data.append(line)

        self.data = new_data


    def set_value(self, key, value):
        new_data = []

        old_value = self.get_value(key)
        for line in self.data:
            if key in line:
                new_line = line.replace(old_value, value)
                line = new_line
            new_data.append(line)

        self.data = new_data



class BKGFile(UserFile):
    "handle Background file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        
    def scale(self, factor):
        idx = -1
        for line in self.data:
            idx += 1
            if 'absolute' in line:
                stat = float(self.data[idx+2])
                syst = float(self.data[idx+3])

                new_stat = stat*factor
                new_syst = syst*factor

                sys.stdout.write('changing from %s to %s.\n' %(stat, new_stat))
                sys.stdout.write('changing from %s to %s.\n' %(syst, new_syst))

                self.data[idx+2] = str(new_stat)+'\n'
                self.data[idx+3] = str(new_syst)+'\n'

class HTMLFile(UserFile):
    "handle HTML file"
    def __init__(self, filename=None):
        if filename != None and filename.startswith('http'):
            url = filename
            self.parse(url)
        else:
            raise NameError(filename)

    def parse(self, url):
        from HTMLParser import HTMLParser
        from urllib2 import urlopen
        class Spider(HTMLParser):
            def __init__(self, url):
                HTMLParser.__init__(self)
                self.urls = []
                req = urlopen(url)
                self.feed(req.read())
                req.close()
            def handle_starttag(self, tag, attrs):
                if tag == 'a' and attrs:
                    name = attrs[0][0]
                    value = attrs[0][1]
                    if name == 'href':
                        self.urls.append(value)

        s = Spider(url)
        self.urls = s.urls



class TCLFile(UserFile):
    "handle tcl script file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        self.parse()
        
    def parse(self):
        has_inputdata = False
        self.inputdata = {}
        for line in self.data:
            if not has_inputdata and 'INPUTDATA' in line:
                has_inputdata = True
                inputdataname = line.split('==')[-1].split('\"')[1]
                self.inputdata[inputdataname] = []
                continue
            if has_inputdata: 
                if '}' in line:
                    has_inputdata = False
                    continue
            if has_inputdata: 
                self.inputdata[inputdataname].append(line)
                
class BrfFile(UserFile):
    "handle brf fit result file"
    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        self.parsed = {}
        self.parse()

    def parse(self):
        names = ['sigma(D0D0bar)', 'sigma(D+D-)', 'sigma(DDbar)', 'chg/neu']
        for line in self.data:
            for name in names:
                if name in line and line.index(name)==0:
                    value = line.split('=')[-1].strip()
                    value = value.replace('(stat)', '')
                    value = value.replace('(syst)', '')
                    self.parsed[name] = value

                if 'chisq' in line and line.index(
                    'chisq') == 0 and 'ndof' in line:
                    self.parsed['chisq'] = line.strip()
                    
                if 'Correlation coeff between sigma(D0D0bar) and sigma(D+D-)'\
                       in line:
                    self.parsed['coeff_ddbar'] = line.strip()
        
