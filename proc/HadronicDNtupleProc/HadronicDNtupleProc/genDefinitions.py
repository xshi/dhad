#!/usr/bin/env python

import string;
import sys;

def abort(message):
    print message
    sys.exit(1)

tuplenamed = 0;
inblock = 0;
indexlist = { };
blockname = None;
blockisopt = 0;
firstblockvar = 0;

f = open("TUPLE_DEFINITION", 'r')

for line in f.xreadlines():
    splitline = string.split(line)
    if len(splitline) == 0:
        continue	
    #    print splitline
    if string.upper(splitline[0]) == 'DOC':
        continue
    if string.upper(splitline[0]) == 'NTUPLE':
        if (tuplenamed):
            abort('Error: Tuple name already defined')
        tuplename = string.upper(splitline[1]);
        if (len(splitline) <= 2):
            tupledesc = ''
        else:
            tupledesc = string.join(splitline[2:]);
        print 'Defining ntuple', tuplename, 'with description',
        print tupledesc
        tuplenamed = 1
        ftuple = open("tuple_cxx_structure.h", "w+")
#        fhbook = open("tuple_hbook_definition.h", "w+")
#        froot = open("tuple_root_definition.h", "w+")
        finit = open("tuple_init.h", "w+")
#        fhbook.writelines(('HBNT(ntid, const_cast<char*>("',
#                           tupledesc, '"),\n const_cast<char*>(" "));\n\n'))
#        froot.writelines(('tree = new TTree("', string.lower(tuplename),
#                          '", "', tupledesc, '", 1);\n'))
        finit.writelines(('m_description = "', tupledesc, '";\n',
                          'm_shortName = "', string.lower(tuplename), '";\n',
                          'BlockDescriptor* thisBlock;\n'))
        continue
    elif not tuplenamed:
        abort('Error: Tuple name must be first datum')
        
    if string.upper(splitline[0]) != 'BLOCK' and not inblock:
        abort('Error: Nothing can lie between tuple name and first block definition')
    if string.upper(splitline[0]) == 'BLOCK':
        inblock = 1
        if not (len(splitline) == 2 or len(splitline) == 3 and string.upper(splitline[2]) == 'OPTIONAL'):
            abort('Error: Block definition line must have the form BLOCK blockname [OPTIONAL]')
# if closing an already existing block
        if blockname:
 #           fhbook.write('"));\n')
            finit.write('varList.push_back(*thisBlock);\n')
#            if blockisopt:
#                fhbook.write('}\n')
#                froot.write('}\n')
#            fhbook.write('\n')
        if (firstblockvar):
            abort('Error: Block ' + blockname + ' has no variables defined.')
        blockname = string.upper(splitline[1])

        if (len(splitline) == 3):
            blockisopt = 1
        else:
            blockisopt = 0
        print 'Defining block', blockname,

        if blockisopt:
            print 'which is defined as optional'
        else:
            print
        ftuple.writelines(('// ', blockname, ' block\n'))
# note that first variable to follow should finish hbook definition
# this root implementation ignores the concept of 'block'
        firstblockvar = 1
#        if blockisopt:
 #           fhbook.writelines(('if (m_make', blockname, 'block) {\n'))
 #           froot.writelines(('if (m_make', blockname, 'block) {\n'))
 #       fhbook.writelines(('HBNAME(ntid, const_cast<char*>("', blockname, '"),\n'))
        finit.writelines(('thisBlock = new BlockDescriptor("', blockname ,
                          '");\n'))
        
        continue
    
    if string.upper(splitline[0]) == 'INTEGER':
        if not (len(splitline) == 2 or len(splitline) == 3):
            abort('Error: Integer definition line must be of the form INTEGER varname [indexvar]')
        temp = string.lower(splitline[1])
        temp2 = string.upper(splitline[1])
        if firstblockvar:
#            fhbook.writelines(('tuple->', temp, ', const_cast<char*>("\\\n'))
            firstblockvar = 0
        else:
##            fhbook.write(',\\\n')
            pass
        if len(splitline) == 2:
            print 'Defining integer variable', splitline[1]
            ftuple.writelines(('int ', temp, ' ;\n'))
#            fhbook.writelines((temp2, ':I'))
#            froot.writelines(('tree->Branch("', temp, '", &(tuple->',
#                              temp, '), "', temp, '/I");\n'))
            finit.writelines(('thisBlock->addVar(*(new VarDescriptor("',
                              temp, '", "", "", &', temp, ', INTEGER)));\n'))
            continue
        else:
            if splitline[2] not in indexlist.keys():
                abort('Error: The specified index variable ' + splitline[2] + ' for variable ' + splitline[1] + ' has not been defined as an index.')
            print 'Defining integer variable', splitline[1], 'with index', splitline[2]
            temp = string.lower(splitline[1])
            ftuple.writelines(('int ', temp, '[', str(indexlist[splitline[2]][2]), '] ;\n'))
#            fhbook.writelines((temp2, '(', string.upper(splitline[2]), '):I'))
#            froot.writelines(('tree->Branch("', temp, '", &(tuple->',
#                              temp, '), "', temp, '[',
#                              string.lower(splitline[2]),
#                              ']/I");\n'))
            finit.writelines(('thisBlock->addVar(*(new VarDescriptor("',
                              temp, '", "',string.lower(splitline[2]),
                              '", "", &', temp, ', INTEGER)));\n'))
            continue


    if string.upper(splitline[0]) == 'FLOAT':
        if not (len(splitline) == 2 or len(splitline) == 3):
            abort('Error: Float definition line must be of the form FLOAT varname [indexvar]')
        temp = string.lower(splitline[1])
        temp2 = string.upper(splitline[1])
        if firstblockvar:
#            fhbook.writelines('tuple->', temp, ', const_cast<char*>("\\\n')
            firstblockvar = 0
        else:
##            fhbook.write(',\\\n')
            pass
        if len(splitline) == 2:
            print 'Defining float variable', splitline[1]
            ftuple.writelines(('float ', temp, ' ;\n'))
#            fhbook.writelines((temp2, ':R'))
#            froot.writelines(('tree->Branch("', temp, '", &(tuple->',
#                              temp, '), "', temp, '/F");\n'))
            finit.writelines(('thisBlock->addVar(*(new VarDescriptor("',
                              temp, '", "", "", &', temp, ', FLOAT)));\n'))
            continue
        else:
            if splitline[2] not in indexlist.keys():
                abort('Error: The specified index variable ' + splitline[2] + ' for variable ' + splitline[1] + ' has not been defined as an index.')
            print 'Defining float variable', splitline[1], 'with index', splitline[2]
            temp = string.lower(splitline[1])
            ftuple.writelines(('float ', temp, '[', indexlist[splitline[2]][2], '] ;\n'))
#            fhbook.writelines((temp2, '(', string.upper(splitline[2]), '):R'))
#            froot.writelines(('tree->Branch("', temp, '", &(tuple->',
#                              temp, '), "', temp, '[',
#                              string.lower(splitline[2]),
#                              ']/F");\n'))
            finit.writelines(('thisBlock->addVar(*(new VarDescriptor("',
                              temp, '", "',string.lower(splitline[2]),
                              '", "", &', temp, ', FLOAT)));\n'))
            
    if string.upper(splitline[0]) == 'INDEX':
        if not (len(splitline) == 4):
            abort('Error: Index definition line must be of the form INDEX varname min max')
        if splitline[1] in indexlist.keys():
            abort('Error: Attempt to redefine index variable ' + splitline[1])
        min = int(splitline[2])
        max = int(splitline[3])
        indexlist[splitline[1]] = [min,max,'MAX'+string.upper(splitline[1])]
#        print indexlist
        if not (min < max):
            abort('Error: When giving min and max for index variable ' + splitline[1] + ', max must be larger than min')
        if not (min >= 0 and max > 0):
            abort('Error: When giving min and max for index variable ' + splitline[1] + ', max and min must be nonnegative')
        print 'Defining index variable', splitline[1], 'with range [', min, ',', max, ']'
        temp = string.lower(splitline[1])
        temp2 = string.upper(splitline[1])
        if firstblockvar:
#            fhbook.writelines(('tuple->', temp, ', const_cast<char*>("\\\n'))
            firstblockvar = 0
        else:
##            fhbook.write(',\\\n')
            pass
        ftuple.writelines(('int ', temp, ' ;\n'))
        ftuple.writelines(('#define ', indexlist[splitline[1]][2], ' ', str(max), '\n'))
#        fhbook.writelines((temp2, '[', str(min), ',', str(max), ']:I'))
#        froot.writelines(('tree->Branch("', temp, '", &(tuple->',
#                          temp, '), "', temp, '/I");\n'))
        finit.writelines(('thisBlock->addVar(*(new VarDescriptor("',
                          temp, '", "", "[', str(min), ',', str(max),
                          ']", &', temp, ', INTEGER)));\n'))

if (blockname):
#    fhbook.write('"));\n')
    finit.write('varList.push_back(*thisBlock);\n')

#    if blockisopt:
#        fhbook.write('}\n')
#        froot.write('}\n')
    ftuple.write('int end_marker ;\n')

#if (fhbook):
#    fhbook.close()
if (ftuple):
    ftuple.close()
#if (froot):
#    froot.close()
if finit:
    finit.close()
