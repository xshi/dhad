#!/usr/bin/env python

import readline
import cmd
import sys
from hep.pdt import default as particle_data
import decimal
from filetools import UserFile

known_models = ['VSS', 'VSS_BMIX', 'PHSP', 'HELAMP', 'JETSET', 'PHOTOS',
                'ISGW2', 'HQET', 'GOITY_ROBERTS', 'VUB', 'SVS',
                'SVV_HELAMP', 'BTOXSGAMMA', 'BTOSLLBALL', 'BTOXSLL',
                'SSD_CP', 'SVV_CP', 'BTO3PI_CP', 'STS', 'JSCONT', 'SLN',
                'CB3PI-P00', 'CB3PI-MPP', 'VSP_PWAVE', 'TAUSCALARNU',
                'TAUHADNU', 'D_DALITZ', 'VLL', 'TSS', 'VVP', 'VVS_PWAVE',
                'PARTWAVE', 'TVS_PWAVE', 'OMEGA_DALITZ', 'ETA_DALITZ',
                'PI0_DALITZ', 'TAUVECTORNU', 'SVP_HELAMP', 'VVPIPI',
                'VPHOTOV', 'VVPIPI_WEIGHTED', 'VPHOTOVISR'
                ]

import os
if 'C3_DATA' in os.environ:
    defdecfile = '%s/DECAY.DEC' % os.environ['C3_DATA']
else:
    defdecfile = '/home/ponyisi/DECAY.DEC'

class DaughterList(dict):
    def __init__(self):
        dict.__init__(self)
        
    def add(self, daughter):
        self[daughter] = self.get(daughter, 0)

class AllowedDecays(object):
    def __init__(self, particle):
        self.decay_of = particle
        self.decays = []

class Decay(object):
    def __init__(self, bf = 0, daughters = None):
        if daughters == None:
            daughters = DaughterList()
        self.bf = bf
        self.daughters = daughters
        self.model = ''
        self.line = ''

    def daughters_to_string(self):
        strs = []
        for dau in self.daughters:
            strs += [dau]*self.daughters[dau]
        def sortkey(x):
            if x in particle_data:
                return abs(particle_data[x].id)
            else:
                return 100000
        strs.sort(key=sortkey, reverse=True)
        return ' '.join(strs)


class decparser(cmd.Cmd):
    def __init__(self, stdin=None, stdout=None):
        self.prompt = ''
        self.file_parse_status = ''
        self.current_decay_top = None
        self.ignoreUntilSemicolon = False
        self.decaylist = {}
        self.cdecay_delayed = []
        self.aliases = {}
        cmd.Cmd.__init__(self, 'tab', stdin, stdout)


    def default(self, line):
        if line[:1] == '#' or 'Photos' in line:
            pass
        elif self.ignoreUntilSemicolon:
            if ';' in line:
                self.ignoreUntilSemicolon = False
        elif self.file_parse_status == 'Decay':
            self.addline(line)

        elif self.file_parse_status == 'RemoveDecay':
            self.delline(line)
        else:
            cmd.Cmd.default(self, line)


    def emptyline(self):
        return ''

##    def precmd(self, line):
##        print line
##        return line

    def do_EOF(self, line):
        return True

    def do_Define(self, line):
        pass

    def do_Alias(self, line):
        spl = line.split()
        if len(spl) != 2:
            raise Exception('Alias line should have two arguments')
        import copy
        if spl[1] not in self.decaylist:
            self.decaylist[spl[1]] = AllowedDecays(spl[1])
        self.decaylist[spl[0]] = self.decaylist[spl[1]]
        self.aliases[spl[0]] = spl[1]
        pass

    def do_ChargeConj(self, line):
        pass

    def do_JetSetPar(self, line):
        pass

    def do_SetLineshapePW(self, line):
        pass

    def do_ModelAlias(self, line):
        if not ';' in line:
            self.ignoreUntilSemicolon = True

    def do_RemoveDecay(self, line):
        self.file_parse_status = 'RemoveDecay'
        particle = line.split()[0]
        if particle in self.aliases:
            # copy old table
            import copy
            print 'copying'
            self.current_decay_top = AllowedDecays(particle)
            self.current_decay_top.decays = copy.deepcopy(self.decaylist[self.aliases[particle]].decays)
        else:
            # reuse old table
            self.current_decay_top = self.decaylist.get(particle,
                                                        AllowedDecays(particle))

    def do_Decay(self, line):
        if self.file_parse_status == 'Decay':
            raise Exception('Repeated Decay statement: %s' % line)
        else:
            self.file_parse_status = 'Decay'
            try:
                particle = line.split()[0]
##                print particle
            except:
                print line
            if particle in self.aliases:
                # force new table
                self.current_decay_top = AllowedDecays(particle)
            else:
                # reuse old table if present
                self.current_decay_top = self.decaylist.get(particle,
                                                            AllowedDecays(particle))

    def do_CDecay(self, line):
##        print 'CDecay for', line
        if self.file_parse_status == 'Decay':
            raise Exception('Cannot do CDecay in Decay block: %s' % line)
        conj = particle_data[line.split()[0]].charge_conjugate.name
        if conj not in self.decaylist:
            print line
            self.cdecay_delayed.append(line)
            return
            raise Exception('CDecay without conjugate mode: %s' % line)
        self.current_decay_top = AllowedDecays(line.split()[0])
##        print conj
        for cdecay in self.decaylist[conj].decays:
##            print cdecay.daughters
            ndecay = Decay()
            ndecay.bf = cdecay.bf
            for dau in cdecay.daughters:
##                print cdecay.daughters
                ndecay.daughters[particle_data[dau].charge_conjugate.name] = cdecay.daughters[dau]
##            print                 ndecay.daughters

##            print cdecay.daughters, ndecay.daughters
##        print line
            self.current_decay_top.decays.append(ndecay)
        self.decaylist[self.current_decay_top.decay_of] = self.current_decay_top
        self.current_decay_top = None

    def do_End(self, line):
##        return self.do_EOF(line)
        if self.cdecay_delayed != []:
            print 'Ought to be [] 0!:', self.cdecay_delayed, len(self.cdecay_delayed)
        while self.cdecay_delayed:
            self.do_CDecay(self.cdecay_delayed.pop())
        pass

    def delline(self, line):
        if line[-1] != ';':
            raise Exception('Need each line to be terminated by semicolon in RemoveDecay; line: %s' % line)
        spl = line[:-1].split()
        daus = {}
        for part in spl:
##            print part,
            daus[part] = daus.get(part, 0)+1
        decfound = None
##         print self.current_decay_top.decay_of
        for knowndec in self.current_decay_top.decays:
##             print knowndec.daughters
            if knowndec.daughters == daus:
                decfound = knowndec
        if decfound != None:
            thisbf = decfound.bf
            self.current_decay_top.decays.remove(decfound)
            for knowndec in self.current_decay_top.decays:
                knowndec.bf /= (1-thisbf)
        else:
            raise Exception('Attempt to delete undefined decay mode %s of %s' % (line[:-1], self.current_decay_top.decay_of))


    def addline(self, line):
        spl = line.split()
        try:
            bf = float(spl[0])
        except:
            raise Exception('Cannot parse decay line: %s' % line)
        mod_found = False
##         for x in known_models:
##             if x in line:
##                 mod_found = True
##         if not mod_found:
##             print '\n', line
        while not spl[-1][-1:] == ';':
##            print 'fixin', line
            if self.use_rawinput:
                line = ' '.join((line, raw_input()))
            else:
                line = ' '.join((line, self.stdin.readline()))
            spl = line.split()

##        print spl
        killindex = None; i = 0
##        print spl
        while killindex == None and i < len(spl):
            if spl[i][-1] == ';':
                spl[i] = spl[i][:-1]
                #print '>>', spl 
            if spl[i] in known_models:
                killindex = i
                model = ' '.join(spl[i:])
                if ';' in model:
                    model = model.replace(';', '')
            i += 1
        if killindex == None:
            print spl
            raise Exception('No decay model specified: %s' % line)
        #print '>>>  ', spl[killindex:]
        decay = Decay()
        #print 'before:', decay.bf, decay.model
        decay.bf = bf
        decay.model = model
        decay.line = line 
        #print 'after:', decay.bf, decay.model

##        print self.current_decay_top.decay_of, 'to',
        for part in spl[1:killindex]:
##            print part,
            if part in decay.daughters:
                decay.daughters[part] += 1
            else:
                decay.daughters[part] = 1
##        print decay.daughters
        self.current_decay_top.decays.append(decay)
##        print self.current_decay_top.decays
        
    def do_Enddecay(self, line):
        if self.file_parse_status not in ('Decay', 'RemoveDecay'):
            raise Exception('Enddecay with no Decay or RemoveDecay: %s' % line)
        else:
            self.file_parse_status = ''
            self.decaylist[self.current_decay_top.decay_of] = self.current_decay_top
            self.current_decay_top = None
            

    
    def do_hi(self, aft):
        print 'hi', aft


class interactive(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.decaylist = {}
        # These are particles we don't decay
        self.termpart = ['pi0', 'K_S0']

    def do_readfile(self, line):
        if line == '':
            fname = defdecfile
        else:
            fname = line
        infile = file(fname, 'r')
        q = decparser(stdin=infile)
        q.use_rawinput = False
        q.cmdloop()
        self.decaylist = q.decaylist

        infile.close()

    def do_dump(self, line):
##        print line
        if line == '':
            lpart = self.decaylist
        else:
            lpart = line.split()
        for part in lpart:
            if part not in self.decaylist:
                print 'Unknown particle %s' % part
            else:
                print '-------------', part, '-------------'
                for decay in self.decaylist[part].decays:
                    print decay.bf, 
                    print decay.daughters_to_string(),
                    print

    def do_total(self, line):
        if line not in self.decaylist:
            print 'Unknown particle %s' % line
        else:
            print 'Total BF for %s: %f' % (line,
                                           sum([x.bf for x in self.decaylist[line].decays]))

    def do_termpart(self, line):
        if line == '':
            print self.termpart
        elif len(line.split()) == 2:
            cmd = line.split()[0].lower()
            if cmd not in ('add', 'del'):
                print 'Unknown command %s' % cmd
            else:
                part = line.split()[1]
                if cmd == 'add' and part not in self.termpart:
                    self.termpart.append(part)
                elif cmd == 'del':
                    if part not in self.termpart:
                        print '%s not in list of terminating particles' % part
                    else:
                        del self.termpart[self.termpart.index(part)]
        else:
            print 'Syntax: termpart [(add|del) particle]'

    def do_exit(self, line):
        return self.do_EOF(line)

    def do_quit(self, line):
        return self.do_EOF(line)

    def do_final(self, line):
##         predeclist = self.decaylist[line].decays[:]
##         declist = []
##         for dec in predeclist:
##             declist.append([[],dec])
##         decaytable = self.decaylist.copy()
##         for j in self.termpart:
##             del decaytable[j]
##         last = []
##         while last != declist:
##             last = declist[:]
##             recurseOneLevel(declist, decaytable)
        declist = self.getDecList(line)
        declist = compactDecayList(declist)
        declist.sort(key=lambda x: x.bf, reverse=True)
        for dec in declist:
##            print dec
            print dec.bf, dec.daughters_to_string()

    def do_neutrals(self, line):
        def neutral_daughters_ok(dec):
            return (False not in [particle_data[dau].charge == 0 
                                  for dau in dec.daughters])

        declist = self.getDecList(line)
        declist = compactDecayList(declist)
        declist = [dec for dec in declist if neutral_daughters_ok(dec)]
        declist.sort(key=lambda x: x.bf, reverse=True)
        ksdeclist = [dec for dec in declist if dec.daughters.get('K_S0', 0) == 1]
        kldeclist = [dec for dec in declist if dec.daughters.get('K_L0', 0) == 1 and 'K_S0' not in dec.daughters]
        mulklist = [dec for dec in declist if dec.daughters.get('K_S0', 0) > 1]
        pideclist = [dec for dec in declist if ('K_S0' not in dec.daughters
                                                and 'K_L0' not in dec.daughters)]
        print 'Total neutral BF:', sum([dec.bf for dec in declist])
        print 'Total 1 K_S0 + neutral BF:', sum([dec.bf for dec in ksdeclist])
        print 'Total K_L0 + neutral BF:', sum([dec.bf for dec in kldeclist])
        print 'Total multi-K_S0 + neutral BF:', sum([dec.bf for dec in mulklist])
        print 'Total non-kaon neutral BF:', sum([dec.bf for dec in pideclist])

        for dec in declist:
            print dec.bf, dec.daughters_to_string()

    def getDecList(self, line):
        predeclist = self.decaylist[line].decays[:]
        declist = []
        for dec in predeclist:
            declist.append([[(line, dec)],dec])
##            print dec
##            declist.append([[],dec])
##         dlist = DaughterList()
##         dlist.add(line)
##         declist = [[[],Decay(1,dlist)]]
        decaytable = self.decaylist.copy()
        for j in self.termpart:
            if j in decaytable:
                del decaytable[j]
        last = []
        while last != declist:
            last = declist[:]
            recurseOneLevel(declist, decaytable)
        return declist
        

    def do_explain(self, line):
        part = raw_input('Parent particle? ')
        if part not in self.decaylist:
            print '%s not known. Have you read the file yet?' % part
            return
        final = raw_input('Final state? ').split()
        finalhash = {}
        termpartcpy = self.termpart[:]
        for p in final:
            finalhash[p] = finalhash.get(p,0) + 1
            if p in self.decaylist and p not in self.termpart:
                self.termpart.append(p)
        declist = self.getDecList(part)
        self.termpart[:] = termpartcpy
        sublist = []
        for dec in declist:
##            print dec[1].daughters
            if dec[1].daughters == finalhash:
                sublist.append(dec)
        print 'Total', sum([x[1].bf for x in sublist])
        sublist.sort(key=lambda x: x[1].bf, reverse=True)
        for entry in sublist:
            print entry[1].bf,
            if len(entry[0]) == 0:
                print 'Direct '
            else:
                print 'Chain: '
                for e2 in entry[0]:
##                    print e2
                    print '\t', e2[0], '->', e2[1].daughters_to_string()

    def explain(self, part, children):
        #part = raw_input('Parent particle? ')
        if part not in self.decaylist:
            print '%s not known. Have you read the file yet?' % part
            return
        #final = raw_input('Final state? ').split()
        final = children
        finalhash = {}
        termpartcpy = self.termpart[:]
        for p in final:
            finalhash[p] = finalhash.get(p,0) + 1
            if p in self.decaylist and p not in self.termpart:
                self.termpart.append(p)
        declist = self.getDecList(part)
        self.termpart[:] = termpartcpy
        sublist = []
        for dec in declist:
##            print dec[1].daughters
            if dec[1].daughters == finalhash:
                sublist.append(dec)
        print 'Total', sum([x[1].bf for x in sublist])
        sublist.sort(key=lambda x: x[1].bf, reverse=True)
        for entry in sublist:
            print entry[1].bf,
            if len(entry[0]) == 0:
                print 'Direct '
            else:
                print 'Chain: '
                for e2 in entry[0]:
##                    print e2
                    print '\t', e2[0], '->', e2[1].daughters_to_string()


    def details(self, part, children, outfile=None):
        if part not in self.decaylist:
            print '%s not known. Have you read the file yet?' % part
            return
        final = children
        finalhash = {}
        termpartcpy = self.termpart[:]
        for p in final:
            finalhash[p] = finalhash.get(p,0) + 1
            if p in self.decaylist and p not in self.termpart:
                self.termpart.append(p)
        declist = self.getDecList(part)

        self.termpart[:] = termpartcpy
        sublist = []
        for dec in declist:
            if dec[1].daughters == finalhash:
                sublist.append(dec)

        decays = self.get_decays_dict(sublist)
        decays = self.normalize_rates(decays)
        aliases, decays = self.alias_decays(decays)

        f = UserFile()
        f.append('\n#\n')
        f.extend(aliases)
        f.append('#\n')
        f.extend(decays)
        f.output(outfile, verbose=1)
        

    def get_decays_dict(self, sublist):
        decays = {}
        for entry in sublist:
            if len(entry[0]) == 0:
                raise ValueError(entry)

            for e2 in entry[0]:
                parent = e2[0]
                decay = e2[1]
                if decay.bf == 1:
                    continue
                tmp = decay.line
                if parent not in decays:
                    decays[parent] = []
                if tmp not in decays[parent]:
                    decays[parent].append(tmp)
        return decays
    
    def get_decay_daughters(self, decay):
        daughters = []
        decay_items = decay.split()
        for item in decay_items:
            model = item.replace(';', '')
            if model in known_models:
                index = decay_items.index(item)
                daughters = decay_items[1:index]
        if daughters == []:
            raise ValueError(decay)
        return daughters

    def get_decays_rate(self, decays, particle):
        rate = 0 
        for decay in decays[particle]:
            bf = float(decay.split()[0])
            rate += bf
        return rate 

    def get_decays_level(self, decays):
        particles = decays.keys()
        decays_level = {}
        for particle in decays:
            decay_list = decays[particle]
            level = len(decay_list)
            if level not in decays_level:
                decays_level[level] = []
            decays_level[level].append(particle)
        return decays_level

    
    def normalize_rates(self, decays):
        decays_level = self.get_decays_level(decays)
        for level in sorted(decays_level.keys()):
            if level == 1:
                continue
            ps = decays_level[level]
            lower_ps = [] 
            for l in decays_level:
                if l < level:
                    lower_ps.extend(decays_level[l])

            for p in ps:
                p_decay_list = decays[p]
                new_p_decay_list = []
                for decay in p_decay_list:
                    daughters = self.get_decay_daughters(decay)
                    for dau in daughters:
                        if dau in lower_ps:
                            dau_bf = self.get_decays_rate(decays, dau)
                            old_bf = decay.split()[0]
                            new_bf = str(float(old_bf)*dau_bf)
                            decay = decay.replace(old_bf, new_bf)

                    bf = decay.split()[0]
                    if 'e' in bf:
                        new_bf = str(decimal.Decimal(str(bf)))
                        decay = decay.replace(bf, new_bf)
                    new_p_decay_list.append(decay)
                decays[p] = new_p_decay_list

        return decays               

    def alias_decays(self, decays):
        aliases = {}
        aliases_lines = [ ]
        aliased_decays = [ ]
        decays_level = self.get_decays_level(decays)
        top = True
        alias_prefix = 'my'
        alias_suffix = ''
        for level in sorted(decays_level.keys(), reverse=True):
            if top:
                if len(decays_level[level]) > 1:
                    raise ValueError(decays_level)
                top_part = decays_level[level][0]
                part_alias = '%s%s' % (alias_prefix, top_part)
                aliases[top_part] = part_alias
                
                if top_part in ['D0', 'D+']:
                    alias_suffix = 'p'
                elif top_part in ['anti-D0', 'D-']:
                    alias_suffix = 'm'
                else:
                    raise NameError(top_part)
                top = False
                continue
            
            for part in decays_level[level]:
                part_alias = '%s%s%s' % (alias_prefix, part, alias_suffix)
                alias_line = 'Alias %s %s\n' % (part_alias, part)
                aliases[part] = part_alias
                aliases_lines.append(alias_line)

        for level in sorted(decays_level.keys(), reverse=True):
            for part in decays_level[level]:
                aliased_decays.append('Decay %s\n' % aliases[part])
                part_decays = decays[part]
                part_decays.sort(key=lambda x: float(x.split()[0]),
                                 reverse=True)
                for part_decay in part_decays:
                    part_daughters = self.get_decay_daughters(part_decay)
                    for p, pa in aliases.items():
                        if p in part_daughters:
                            part_decay = part_decay.replace(p, pa)
                    aliased_decays.append(part_decay+'\n')

                aliased_decays.append('Enddecay\n#\n')
                
        return aliases_lines, aliased_decays
       

        
    def do_multiplicity_one(self, line):
        linesplit = line.split()
        if len(linesplit) < 1:
            part = raw_input('Parent particle? ')
        else:
            part = linesplit[0]
        if part not in self.decaylist:
            print '%s not known. Have you read the file yet?' % part
            return
        if len(linesplit) < 2:
            final = raw_input('Final particle? ')
        else:
            final = linesplit[1]
        termpartcpy = self.termpart[:]
        if final not in self.termpart:
            self.termpart.append(final)
        declist = self.getDecList(part)
        self.termpart[:] = termpartcpy
        sublist = []
        for dec in declist:
##            print dec[1].daughters
            if final in dec[1].daughters:
                sublist.append(dec)
        sublist.sort(key=lambda x: x[1].bf, reverse=True)
        summult = 0
        for entry in sublist:
            thiscontrib = entry[1].bf*entry[1].daughters[final]
            summult += thiscontrib
            print thiscontrib
            if len(entry[0]) == 0:
                print 'Direct '
            else:
                print 'Chain: '
                for e2 in entry[0]:
##                    print e2
                    print '\t', e2[0], '->', e2[1].daughters_to_string()
        print 'Mean multiplicity:', summult
        

    def do_oneshot(self, line):
        declist = self.decaylist[line].decays[:]
        recurseOneLevel(declist, self.decaylist)
        for dec in declist:
            print dec.bf, dec.daughters

    def do_EOF(self, line):
        print
        return True

def recurseOneLevel(decaylist, decaytable):
    """Do one sweep at replacing particles with daughters."""
    """decaylist should be tuple of [[(particle, decay) ...], finalstate]"""
    rv = []
    for decay in decaylist:
        # Only do one daughter!
        toexpand = None
        for dau in decay[1].daughters:
            if toexpand == None and dau in decaytable:
                toexpand = dau
        if toexpand == None:
            rv.append(decay)
        else:
            for subdec in decaytable[toexpand].decays:
                chain = decay[0][:]
                chain.append((toexpand, subdec))
                dlist = DaughterList()
                dlist.update(decay[1].daughters)
                dlist[toexpand] -= 1
                if dlist[toexpand] == 0:
                    del dlist[toexpand]
                for entry in subdec.daughters:
                    dlist[entry] = dlist.get(entry, 0) + subdec.daughters[entry]
                newdecay = Decay(decay[1].bf*subdec.bf, dlist)
                rv.append([chain, newdecay])
    decaylist[:] = rv

def compactDecayList(decaylist):
    rv = []; used_daughter_list = []
    for decay in decaylist:
        if decay[1].daughters not in used_daughter_list:
            rv.append(Decay(decay[1].bf, decay[1].daughters))
            used_daughter_list.append(decay[1].daughters)
        else:
            for dec2 in rv:
                if dec2.daughters == decay[1].daughters:
                    dec2.bf += decay[1].bf
    return rv
            

if __name__ == '__main__':
##     decparser().cmdloop(
##         """Hi! We are beginning the loop."""
##         )
##    q = decparser(stdin=file('/home/ponyisi/DECAY.DEC', 'r'), stdout=sys.stdout)
##    q.use_rawinput = False
##    q.cmdloop()
##    print q.decaylist
    interactive().cmdloop(
        """Hi! Welcome to the DECAY.DEC parser program.\n"""
        """Blame ponyisi@lepp if any problems arise."""
        )
