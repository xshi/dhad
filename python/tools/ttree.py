"""
Module for ROOT Tree.

Borrowed from Peter Onyisi. 

"""

import ROOT
from attr.pdg import *
import tools
import string
import math 


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"



class PyTTree(object):
    def __init__(self, rtree, defaultBranchState=0):
        if not rtree:
            raise ValueError('Need non-null tree.')
        self.rtree = rtree
        if rtree.__class__ == ROOT.TChain:
            self.isChain = 1
        else:
            self.isChain = 0
        self.treeNo = 0
        self.rtree.SetBranchStatus('*',defaultBranchState)
        self.readdict = {}
        self.range = None

    def Add(self, name):
        self.rtree.Add(name)

    def Delete(self, option=''):
        self.rtree.Delete(option)
        

    def GetEntries(self):
        if self.isChain:
            return int(self.rtree.GetEntries())
        else:
            return int(self.rtree.GetEntriesFast())

    def GetEntry(self, entry):
        self.rtree.GetEntry(entry)

    def GetLeaf(self, leaf, entry):
        if self.readdict.has_key(leaf):
            return self.readdict[leaf]
        else:
            aleaf = self.rtree.GetLeaf(leaf)
            if not aleaf:
                raise AttributeError, 'Tree does not contain a leaf called ' \
                      + leaf
            self.rtree.SetBranchStatus(aleaf.GetBranch().GetName(), 1)
            self.GetEntry(entry)
            tname = aleaf.GetTypeName()
            leafcount = aleaf.GetLeafCount()
            if not leafcount:
                leafcount = None
            if tname == 'Float_t' or tname == 'Double_t':
                isFloat = 1
            else:
                isFloat = 0
            retval = (aleaf, isFloat, leafcount)
            self.readdict[leaf] = retval
            return retval

    def SetIterationRange(self, range):
        self.range = range

    def __len__(self):
        return self.GetEntries()

    def __getitem__(self, key):
        self.GetEntry(key)
        if self.isChain and self.treeNo != self.rtree.GetTreeNumber():
            self.readdict.clear()
            self.treeNo = self.rtree.GetTreeNumber()
        return PyTTreeEntry(self, key)

    def __iter__(self):
        self.readdict.clear()
        if self.range == None:
            self.range = xrange(len(self))
        for i in self.range:
            yield self[i]
        self.range = None

    def readBranch(self, bname):
        pass

    def Draw(self, entry):
        self.rtree.Draw(entry)

    def SetBranchStatus(self, bname, status):
        self.rtree.SetBranchStatus(bname, status)
        
    def CloneTree(self, nentries=-1, option=''):
        return self.rtree.CloneTree(nentries, option)
        


class PyTTreeEntry(object):
    def __init__(self, pytree, entry):
        self.pytree = pytree
        self.entry = entry

    def __getattr__(self, name):
        (leaf, isFloat, leafcount) = self.pytree.GetLeaf(name, self.entry)
        if leafcount == None:
            if leaf == None:
                print self.entry, (leaf, isFloat, leafcount)
                print self.pytree.rtree.mcdmode
            retval = leaf.GetValue()
            if isFloat == 0:
                retval = int(retval)
            self.__dict__[name] = retval
            return retval
        else:
            count = int(leafcount.GetValue())
            lgv = leaf.GetValue
            retval = [lgv(i) for i in range(count)]
            if not isFloat:
                retval = map(int, retval)
            self.__dict__[name] = retval
            return retval


class DecayTreeNode(object):
    def __init__(self):
        self.parent = None
        self.daughters = []
        self.index = -1
        self.pdgid = 0

    def __str__(self):
        if self.parent:
            return '->Index = ' + `self.index` + \
                   '\nPDG ID = ' + `self.pdgid` + \
                   '\nParent = ' + `self.parent.index` + \
                   '\nDaughters = ' + `[dau.index for dau in self.daughters]`
        else:
            return '->Index = ' + `self.index` + \
                   '\nPDG ID = ' + `self.pdgid` + \
                   '\nDaughters = ' + `[dau.index for dau in self.daughters]`

    def addParent(self, node):
        self.parent = node
        
    def addDaughter(self, node):
        self.daughters.append(node)
            
    def setIndex(self, index):
        self.index = index
            
    def setPdgId(self, id):
        self.pdgid = id

    def isDescendantOf(self, node):
        if self == node:
            return True
        elif self.parent != None:
            if self.parent == node:
                return True
            else:
                return self.parent.isDescendantOf(node)
        else:
            return False
                

    def interestingDescendants(self, terminii=interesting_particles,
                               stopatradrho=True, stopatraddecay=True,
                               stopatallphodecay=True, stopatradeta=True,
                               stopatradomega=True):
        if self.pdgid == pdgid_gammaFSR:
            return []
        if (abs(self.pdgid) == pdgid_rhop and
            len(self.daughters) < 2):
            print [particle_data.findId(x.pdgid).name for x in self.daughters]
            return self.daughters
        if ((abs(self.pdgid) == pdgid_rhop and
             len(self.daughters) > 1 and
             abs(self.daughters[0].pdgid) == pdgid_pip and
             self.daughters[1].pdgid == pdgid_gamma)):
            print 'rho->pi gamma: hahahaha'
            print self
            for node in self.daughters:
                print node
        # we don't care about decays in flight or pi0 daughters
        # Dumb hack : we don't care right now for non-FSR photons, so
        # terminate if X -> Y gamma, else carry on
        # But hey, this kills radiative K* decays ... make an option
        if self.pdgid in terminii:
            return [self]
        elif (stopatallphodecay and
              len(self.daughters) ==
              len(filter(lambda x: x.pdgid == pdgid_gamma,
                         self.daughters))):
            return [self]
        elif stopatraddecay and (len(self.daughters) == 2 and
                                 pdgid_gamma in (self.daughters[0].pdgid,
                                                 self.daughters[1].pdgid)):
##             if self.pdgid == pdgid_etaprime:
##                 print 'HO'
##                 print 'xxxxxxxxxxx'
##                 print self
##                 print self.daughters[0]
##                 print self.daughters[1]
##                 print 'xxxxxxxxxxx'
##            if self.pdgid == 323:
##                print 'here', terminii, stopatraddecay
            return [self]
        elif stopatradrho and ((abs(self.pdgid) == pdgid_rhop and
                                abs(self.daughters[0].pdgid) == pdgid_pip and
                                self.daughters[1].pdgid == pdgid_gamma)):
            print 'rho check'
            return [self]

        elif stopatradeta and (self.pdgid == pdgid_eta and
                               pdgid_gamma in map(lambda x: x.pdgid,
                                                      self.daughters)):
            return [self]
        elif stopatradomega and (self.pdgid == pdgid_omega and
                                 pdgid_gamma in map(lambda x: x.pdgid,
                                                    self.daughters)):
            #print 'here'
            return [self]

        else:
            return tools.flatten([dau.interestingDescendants(terminii=terminii,
                                                             stopatradrho=stopatradrho,
                                                             stopatraddecay=stopatraddecay,
                                                             stopatallphodecay=stopatallphodecay,
                                                             stopatradeta=stopatradeta,
                                                             stopatradomega=stopatradomega)
                                  for dau in self.daughters])

    def mcDmode(self):
        if abs(self.pdgid) not in (pdgid_Dp, pdgid_Dz, pdgid_Dsp):
            return None
        else:
            list = self.interestingDescendants()
            retval = 0
            for node in list:
                if node.pdgid == pdgid_Km:
                    retval += 1
                elif node.pdgid == pdgid_Kp:
                    retval += 10
                elif node.pdgid in (pdgid_KS, pdgid_KL):
                    retval += 100
                elif node.pdgid == pdgid_pim:
                    retval += 1000
                elif node.pdgid == pdgid_pip:
                    retval += 10000
                elif node.pdgid == pdgid_piz:
                    retval += 100000
                elif node.pdgid == pdgid_gamma:
                    retval += 1000000
                elif abs(node.pdgid) in (pdgid_em, pdgid_nue, pdgid_mum,
                                         pdgid_numu):
                    retval += 10000000
                elif node.pdgid in (pdgid_eta, pdgid_etaprime):
                    retval += 100000000
                else:
                    retval += 1000000000
            return retval

class histBox(object):
    def __init__(self, *args):
        if (len(args)) % 3 != 0:
            raise TypeError('histBox() must have multiple of three arguments')
        self.lowedges = [] ; self.highedges = [] ; self.nbins = [] ;
        self.binwidth = []
        self.initcode = args
        for i in range((len(args)) / 3):
            self.nbins.append(int(args[3*i]))
            self.lowedges.append(float(args[3*i+1]))
            self.highedges.append(float(args[3*i+2]))
            self.binwidth.append((float(args[3*i+2])-float(args[3*i+1]))/
                                 float(args[3*i]))
        self.counts = {}
        self.out_of_range = 0;

    def _findbin(self, *args):
        bin = []
        for i in range(len(args)):
            if not (self.lowedges[i] <= args[i] < self.highedges[i]):
                self.out_of_range += 1.0
                return
            else:
                bin.append(int(math.floor((float(args[i])-self.lowedges[i])
                                          /self.binwidth[i])));
        return tuple(bin)
        
    def fill(self, *args):
        if len(args) != len(self.nbins):
            raise TypeError('fill() must be called with correct dimensionality')
        bin = self._findbin(*args)
        if bin not in self.counts:
            self.counts[bin] = 1.0
        else:
            self.counts[bin] += 1.0

    def getBinContent(self, *args):
        iargs = tuple(map(int,args))
        if len(iargs) != len(self.nbins):
            raise TypeError('Wrong dimensionality')
        for i in range(len(iargs)):
            if not 0 <= iargs[i] < self.nbins[i]:
                raise ValueError('Bin out of range')
        if iargs not in self.counts:
            return 0
        else:
            return self.counts[iargs]

    def lookup(self, *args):
        bin = self._findbin(*args)
        if bin == None:
            print args
##            return self.out_of_range
            return 0
        return self.getBinContent(*bin)

    def __str__(self):
        retval = []
        for i in self.counts:
            retval.append(`i`)
            retval.append(': ')
            retval.append(`self.counts[i]`)
            retval.append('\n')
        return string.join(retval)

    def __div__(self, other):
        if not self.initcode == other.initcode:
            raise TypeError('Mismatch in division')
        retval = histBox(*self.initcode)
        for filledbin in [x for x in self.counts if x in other.counts]:
            retval.counts[filledbin] = self.counts[filledbin]/other.counts[filledbin]
        for filledbin in [x for x in other.counts if x not in self.counts]:
            retval.counts[filledbin] = 0.
        return retval
        
                                                                                        



            
                                                            


