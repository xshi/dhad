"""
Script for manipulating the tables in text format 

"""

import os
import sys
import types
import decimal
import copy
import locale
import operator
import filecmp
from math import sqrt, fabs


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GNU GPL"



def print_sep(width=80):
    sys.stdout.write('-'*width+'\n')

class UserTable(object):
    '''Class to handle the table file  '''
    def __init__(self, filename=None, bspliter='|', evalcell=False):
        self.data = []

        if filename:
            self.filename = filename
            if filename.split('.')[-1] == 'org':
                self.input_org(filename)
            else:
                self.input_txt(filename, bspliter=bspliter, evalcell=evalcell)

    def input_head(self, list):
        width = len(list) 
        for i in range(width):
            self.head[i]=list[i]
        self.data[0] = self.head


    def input_list(self, list_, rnd= None):
        for line in list_:
            line=line.strip()
            line = line.split()
            for i in range(len(line)):
                cell = line[i]
                cell = cell.strip()
                
                # try:
                #     cell = eval(cell)
                # except NameError:
                #     pass
                # except  SyntaxError:
                #     pass 

                if rnd:
                    cell = self.cell_trim(cell=cell, rnd=rnd)
                line[i] = cell
                
            self.data.append(line)


    def input_org(self, filename):
        f = open(filename,'r')
        length= 0
        for line in f:
            if '|-' in line and '-+-' in line:
                continue
            line = line.strip().split('|')
            line = [li for li in line if li]
            for i in range(len(line)):
                cell = line[i]
                cell = cell.strip()
                line[i] = cell
            self.data.append(line)
        f.close()


 
    def input_tab(self, tab):
        self.data = tab.data
        self.head = self.data[0]


    def input_tex(self, texfile, keywords = None):
        f = open(texfile,'r')
        length= 0
        for line in f:
            line=line.strip()            
            lineMap={}

            list= line.split('&')
            width = len(list) 
            if list == ['']:   continue   #Get rid of empty lines

            for i in range(width):
                if '\pm' in list[i]:
                    list[i] = list[i].replace('\pm', ' +/- ')
                if '$' in list[i]:
                    list[i] = list[i].replace('$', '')
                if '\\\\' in list[i]:
                    list[i] = list[i].replace('\\\\', '')
                if '\\hline' in list[i]:
                    list[i] = list[i].replace('\\hline', '')
                lineMap[i]=list[i].strip()
            self.data[length] = lineMap
            length += 1
        f.close()



    def input_txt(self, filename=None, hspliter='||', bspliter='|',
                  ignoreline=None, start_line_str=None,
                  end_line_str=None, evalcell=False):
        if type(filename) == types.StringType:
            f = open(filename,'r')
        if type(filename) == types.ListType:
            f = filename

        length = 1  # Require the first line be the head
        linum = 0
        for line in f:
            linum += 1
            if ignoreline != None and linum < ignoreline:
                continue
            if line =='':
                continue
            line=line.strip()
            sep = bspliter
            if self.data == []:
                sep = hspliter
            line = line.split(sep)
            for i in range(len(line)):
                cell = line[i]
                cell = cell.strip()
                if evalcell:
                    try:
                        cell = eval(cell)
                    except NameError:
                        pass
                    except  SyntaxError:
                        pass 

                line[i] = cell

            self.data.append(line)
        if type(filename) == types.StringType:
            f.close()


            



## -------------------------
##  Handle Cell
## -------------------------

    def cell_abs(self, a):
        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']
        if a_attr == 'str':
            return a

        a_val = eval(a_parsed['value'])
        a = str(fabs(a_val))
        return a


    def cell_add(self, a, b):

        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str':
            return a
        if b_attr == 'str':
            return b

        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        c_val = str(a_val + b_val)

        c     = c_val

        if a_attr == 'val_err' and b_attr == 'val_err' :

            a_err = eval(a_parsed['error'])
            b_err = eval(b_parsed['error'])

            add1  = a_err**2
            add2  = b_err**2
            c_err = sqrt(add1+add2)
            c     = c_val +' +/- ' + str(c_err)

        if a_attr == 'val_sig' and b_attr == 'val_sig' :

            a_sig = eval(a_parsed['sigma'])
            b_sig = eval(b_parsed['sigma'])

            c_sig = a_sig + b_sig

            if c_val > 0: c_val = '+'+ str(c_val)
            if c_sig > 0: c_sig = '+'+ str(c_sig)

            c = str(c_val)+'('+str(c_sig)+'sigma)'

        return c 

    def cell_add_quadrature(self, a, b):
        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str':
            return a
        if b_attr == 'str':
            return b

        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        c  = str(sqrt(a_val**2 + b_val**2))

        return c 



    def cell_average(self, a, b, rnd=None, err_type=None):

        if  not self.cell_parse(a) or not self.cell_parse(b):
            return a

        c = self.cell_add(a,b)

        c_parsed = self.cell_parse(c)
        c_attr =  c_parsed['attr']
        if c_attr == 'str':
            return c

        ref_err=None
        if c_attr == 'val_err' :
            ref_err = eval(c_parsed['error'])/2

        c = self.cell_divide(c, '2', err_type='Apnd', ref_err=ref_err)
        c = self.cell_trim(c, rnd)

        return c 


    def cell_diff(self, a, b, rnd, factor, err_type=None, opt=''):
        c  = self.cell_subtract(a, b, err_type)
        c_parsed = self.cell_parse(c)
        c_attr =  c_parsed['attr']
        if c_attr == 'str':
            return c

        if  c_parsed['value'] == '0':
            c = '0'
        else:
            #c = self.cell_divide(c, b, err_type) Use cell_diff_pct !
            c = self.cell_trim(c, rnd, factor, opt=opt)
        return c

    def cell_diff_err(self, a, b, rnd, factor, err_type=None, opt=''):
        c  = self.cell_subtract(a, b, err_type= 'Syst')
        c  = self.cell_trim(c, rnd, factor, opt=opt)
        c_parsed = self.cell_parse(c)
        c_attr =  c_parsed['attr']
        if c_attr == 'str': return c
        c_err = c_parsed['error']
        return c_err


    def cell_diff_chisq(self, a, b, rnd, factor, err_type=None, opt=''):
        a_parsed = self.cell_parse(a)
        b_parsed = self.cell_parse(b)
        if a_parsed['attr'] == 'str':
            c = a
        
        elif a_parsed['attr'] == 'val_err' and b_parsed['attr'] == 'val_err':
            a_val = float(a_parsed['value'])
            b_val = float(b_parsed['value'])
            a_err = float(a_parsed['error'])
            b_err = float(b_parsed['error'])
            chisq = ((a_val - b_val)**2)/(a_err**2 + b_err**2)
            c = chisq 
            
        else:
            raise ValueError(a)
        
        c  = self.cell_trim(c, rnd, factor, opt=opt)

        return c


    def cell_diff_pct(self, a, b, rnd, factor=100, err_type=None, opt=''):
        c  = self.cell_subtract(a, b)
        c_parsed = self.cell_parse(c)
        c_attr =  c_parsed['attr']
        if c_attr == 'str':
            return c

        if  c_parsed['value'] == '0':
            c = '0'
        else:
            c = self.cell_divide(c, b, err_type)
            c = self.cell_trim(c, rnd, factor=factor, opt=opt)
        return c


    def cell_diff_sigma(self, a, b, rnd, factor, err_type='Sgma'):
        c  = self.cell_subtract(a, b, err_type='Indp')
        c  = self.cell_divide(c, b, err_type=err_type)
        c  = self.cell_trim(c, opt = '+/-cellsigma', rnd=rnd, factor=factor)
        return c


    def cell_diff_sigma_pct(self, a, b, rnd, factor=100, err_type='Sgma',
                            opt=None):
        c  = self.cell_subtract(a, b, err_type='Indp')
        c  = self.cell_divide(c, b, err_type=err_type)
        c  = self.cell_trim(c, err_type='Sgma', rnd=rnd,
                            factor=factor, opt=opt)
        return c


    def cell_divide(self, a, b, err_type=None, ref_err=None):

        '''
                         a_val 
                c_val = -------
                         b_val

        err_type :


            Apnd: Append error from input c_err


            Efcy: Efficiency 

                *      --------
                  a_err_new   = \/ np(1-p)  

                            ---    ------
                        = \/ np  \/ 1 - p

                        ~         ----------
                        = a_err \/ 1 - c_val

                   * Note:  The a_err_new has taken account the errors
                            other than the Binomial uncertainty.

                   
                           a_err_new
                  c_err = -----------
                             b_val

                                   ----------
                           a_err \/ 1 - c_val
                        =  -------------------    
                                 b_val

                  fac1  = a_err
                  fac2  = sqrt(1 - c_val)
                  fac3  = 1./b_val
                  c_err = fac1*fac2*fac3

                  

           Bino: Binomial Distribution
               
                             --------
                  sigma =  \/ np(1-p)  

                            -------------------------
                  a_err = \/ b_val*c_val (1 - c_val) 


                           a_val
                  c_val = -------
                           b_val


                           a_err
                  c_err = -------
                           b_val

                              --------------------- 
                            \/ b_val*c_val(1-c_val) 
                        =  --------------------------
                                    b_val

                        
                              ----------------------
                             /   c_val (1 - c_val)
                        =   /  ---------------------
                          \/           b_val



                  fac1 = c_val
                  fac2 = 1- c_val
                  fac3 = 1./b_val
                  c_err = sqrt( fabs(fac1*fac2*fac3) )

            Corr: Correlated two numbers, both have errors


                           a_val
                  c_val = -------
                           b_val


                           a_err
                  c_err = -------
                           b_val
              


            Indp: Deal with both errors as independently
     
                 1) if a != 0, b !=0 :
                 
                          |       ------------------ |
                          |      /  sa^2       sb^2  |
                   sc   = | c * /  ------  +  ------ |
                          |   \/     a^2        b^2  |
                  

                  fac1  =  c_val
                  add1  =  a_err**2/a_val**2
                  add2  =  b_err**2/b_val**2
                  fac2  =  sqrt(add1+add2)
                  c_err =  fabs(fac1*fac2)

                 2) if a = 0, b !=0 :
                            
                           |        ------------------ |
                           | a     /  sa^2       sb^2  |
                   sc   =  |--- * /  ------  +  ------ |
                           | b  \/     a^2        b^2  |


                            
                           |    --------------------------|
                           |   /  sa^2       sb^2 * a^2   |
                        =  |  /  ------  +  --------------|
                           |\/     b^2           b^4      |

                           | sa  |
                        =  |---- | 
                           |  b  |

                  3) if b =0: infinite.
                  

           None: No error handle, just value.


           Sgma:

                 Consider two numbers:
                 
                 N1 +/- S1 and N2 +/- S2

                 The "sigma" is calculated as:
                 
                           N1 - N2
                 sigma = ----------
                             S2

                 Inside this "divde" fuction, it follows:
                 
                 a_val = N1 - N2

                 b_val = N2
                 b_err = S2
                 
                           a_val
                 c_val = ---------
                           b_val

                           a_val
                 c_err = ---------   (c_err is the "sigma")  
                           b_err
              
           Sgma2:

                 Consider two numbers:
                 
                 N1 +/- S1 and N2 +/- S2

                 The "sigma" is calculated as:
                 
                              N1 - N2
                 sigma = ------------------
                          sqrt(S1^2 + S2^2)


                 Inside this "divde" fuction, it follows:
                 
                 a_val = N1 - N2
                 a_err = sqrt(S1^2 + S2^2)

                 b_val = N2
                 b_err = S2
                 
                           a_val
                 c_val = ---------
                           b_val

                           a_val
                 c_err = ---------   (c_err is the "sigma")  
                           a_err
              


        '''

        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str' or b_attr == 'str':
            return '--'

        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])
        try:
            c_val = float(a_val)/float(b_val)
        except ZeroDivisionError:
            c_val = 'INF'
        c_err = None

        if err_type == 'Apnd': 
            c_err   = ref_err

        elif err_type == 'Bino':
            fac1 = c_val
            fac2 = 1- c_val
            fac3 = 1./b_val
            if fac2 < 0:
                sys.stdout.write('Warning : Not real Binomial Distribution.\n')
                fac2  = fabs(1-c_val)
            c_err = sqrt( fabs(fac1*fac2*fac3))


        elif err_type == 'Corr':
            if a_attr != 'val_err' :
                raise TypeError(err_type)
            
            a_err = a_parsed['error']
            c_err = fabs(float(a_err)/b_val)

            
        elif err_type == 'Efcy':
            if a_attr != 'val_err' :
                raise TypeError(err_type)

            a_err = a_parsed['error']
            fac1  = float(a_err)
            sub1  =  1 - c_val

            if sub1 < 0:
                sub1  = fabs(1-c_val)
            fac2  = sqrt(sub1)
            fac3  = 1./float(b_val)
            c_err = fac1*fac2*fac3

        elif err_type == 'Indp': 
            if a_attr != 'val_err' or b_attr != 'val_err':
                raise TypeError(err_type)
                
            a_err = eval(a_parsed['error'])
            b_err = eval(b_parsed['error'])

            if b_val ==0:
                raise ValueError('b can not be zero!')
            if a == 0:
                c_err =  a_err/b_val
            else:
                fac1  = float(c_val)
                add1  = float(a_err**2)/a_val**2
                add2  = float(b_err**2)/b_val**2
                fac2  = sqrt(add1+add2)
                c_err = fabs(fac1*fac2)
                
        elif err_type == 'Sgma':
            if b_attr == 'val_err':
                b_err  = eval(b_parsed['error'])
            elif b_attr == 'val_err2':
                b_err1 = eval(b_parsed['error'])
                b_err2 = eval(b_parsed['error2'])
                b_err = sqrt(b_err1**2 + b_err2**2)
            elif a_attr == 'val_err':
                b_err  = eval(a_parsed['error'])
            else:
                raise ValueError(b_attr)
            c_err  = a_val/float(b_err)

        elif err_type == 'Sgma2':
            a_err  = eval(a_parsed['error'])
            c_err  = a_val/float(a_err)

        c = str(c_val)
        
        if c_err != None:
            c += ' +/- '+ str(c_err)

        return c


    def cell_get(self, row, col, opt=None):
        if isinstance(col, str):
            heads = self.data[0]
            for item in heads:
                label  = item.strip()
                if col == label:
                    col = heads.index(item)
                    break
            
        if isinstance(row, str):
            rownames = self.column_get(0)
            for item in rownames:
                rowname = item.strip()
                if row == rowname:
                    row = rownames.index(item)
                    break
        try:
            cell = self.data[row][col]
        except TypeError:
            sys.stdout.write('Please check tabfile: \n %s \n' %self.filename)
            sys.stdout.write('row:%s, col:%s\n' %(row, col))
            raise ValueError(cell)
        
        if opt!=None:
            return self.cell_parse(cell)[opt]

        return cell

    def cell_get_by_square_sum(self, column=None):
        if not isinstance(column, str): 
            raise TypeError(column)
        n = -1
        for cell in self.column_get(column):
            n += 1
            if n == 0:
                continue
            if n == 1:
                sum_cell = self.cell_square(cell)
            else:
                tmp_cell = self.cell_square(cell)
                sum_cell = self.cell_add(tmp_cell, sum_cell)

        return sum_cell
  

    def cell_join(self, a, b, s=' +/- '):
        c = '%s%s%s' %(a, s, b)
        return c
    
    def cell_max(self, a, b):
        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str' or b_attr == 'str':
            return a
        
        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        if a_val > b_val:
            return a
        else :
            return b

    def cell_max_abs(self, a, b):
        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str' or b_attr == 'str':
            return a
        
        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        if abs(a_val) > abs(b_val):
            return a
        else :
            return b

    def cell_min_abs(self, a, b, threshold=None, MIN=0):
        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str' or b_attr == 'str':
            return a
        
        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        c = abs(a_val) 
        if c > abs(b_val):
            c = abs(b_val)

        if threshold !=None and c < threshold:
            c = MIN

        return c


    def cell_parse(self, a):
        '''
        return a Dict as the parse result

        attr : str:

               digit:
                    int
                    float
                    
               val_err:  value +/- error

                        value: 
                        error:
                        value+error:
                        value-error:

               val_err2:  value +/- error +/- error2

               val_err3:  value +/- error +/- error2 +/- error3
                        
        '''
        aDict ={}
        aDict['attr']='str'

        a = str(a) 
        if '+-' in a:
            a= a.replace('+-', '+/-')
        if ',' in a:
            a= a.replace(',', '')
        if '~' in a:
            a= a.replace('~', '')

        if '+/-' in a:
            aList = a.split('+/-')
            value = aList[0].strip()
            error = aList[1].strip()

            if '(' in value:
                value = value.replace('(', '')
            try:
                eval(value)
            except NameError:
                return aDict
            except SyntaxError:
                print value, a, aDict
                raise 
                
            aDict['attr']='val_err'
                    
            aDict['value'] = value
            aDict['error'] = error

            try:
                aDict['value+error'] = str(decimal.Decimal(value) +
                                           decimal.Decimal(error))
                aDict['value-error'] = str(decimal.Decimal(value) -
                                           decimal.Decimal(error))
            except decimal.InvalidOperation:
                aDict['attr']='str'
                return aDict

            if len(aList) > 2:
                aDict['attr']='val_err2'
                error2 = aList[2].strip()

                if ')' in error2:
                    error2  = error2.split(')')[0]

                if '(' in error2:
                    error2  = error2.split('(')[0]

                aDict['error2'] = error2

                if len(aList) > 3:
                    aDict['attr']='val_err3'
                    error3 = aList[3].strip()
                    aDict['error3'] = error3
                

        elif '100 - ' in a:
            aDict['attr']='str'
                    
        elif 'sigma' in a:
            if '(' in a:
                aList = a.split('(')
                value = aList[0].strip()
                sigma = aList[1].strip().replace('sigma)', '')

                aDict['attr']='val_sig'
                aDict['value'] = value
                aDict['sigma'] = sigma
            else:
                sigma = a.replace('sigma', '')
                aDict['attr'] = 'sig'
                aDict['sigma'] = sigma

        else:
            try:
                eval(a)
                aDict['attr']= 'digit'
                if type(eval(a)) == types.IntType:
                    aDict['attr']='int'
                if type(eval(a)) == types.FloatType:
                    aDict['attr']='float'
                aDict['value'] = a

            except NameError : pass
            except SyntaxError: pass
            
        return aDict
        

    def cell_set(self, row, col, cell):
        if isinstance(col, str):
            col = self.column_get_number(col)
        if isinstance(row, str):
            row = self.column_get(0).index(row) 
        self.data[row][col] = cell 
        return cell
    

    def cell_square(self, a):
        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        if a_attr == 'str':
            return a

        if a_attr == 'val_err':
            raise NameError(a_attr)

        if a_attr == 'val_sig':
            a_val = eval(a_parsed['value'])
            c_val = a_val**2 

            a_sig = eval(a_parsed['sigma'])
            c_sig = a_sig**2

            if c_val > 0: c_val = '+'+ str(c_val)
            if c_sig > 0: c_sig = '+'+ str(c_sig)

            c = str(c_val)+'('+str(c_sig)+'sigma)'

        elif a_attr == 'sig':
            a_sig = eval(a_parsed['sigma'])
            c_sig = a_sig**2
            c = str(c_sig)
            
        return c 

        
    def cell_subtract(self, a, b, err_type=None):
        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str' or b_attr == 'str':
            return '--'
            
        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        c  = str(a_val - b_val)
        c_err = None

        if a_attr == 'val_err' and b_attr == 'val_err':

            a_err = eval(a_parsed['error'])
            b_err = eval(b_parsed['error'])

            if err_type == 'Corr':
                c_err = a_err - b_err

            elif err_type == 'Syst':
                c_err = sqrt(abs(a_err**2 - b_err**2))

            else:
                add1  = a_err**2
                add2  = b_err**2
                c_err = sqrt(add1+add2)
            
            
        if a_attr == 'val_err' and b_attr != 'val_err':
            a_err = eval(a_parsed['error'])
            c_err = a_err

        if a_attr != 'val_err' and b_attr == 'val_err':
            b_err = eval(b_parsed['error'])
            c_err = b_err
            
            
        if c_err != None:
            
            c  += ' +/- ' + str(c_err)

        return c 

            
    def cell_subtract_quadrature(self, a, b, err_type=None):

        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str':
            return a
        if b_attr == 'str':
            return b

        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        c  = str(sqrt(abs(a_val**2 - b_val**2)))

        return c 

    def cell_times(self, a, b):

        a_parsed = self.cell_parse(a)
        a_attr   = a_parsed['attr']

        b_parsed = self.cell_parse(b)
        b_attr   = b_parsed['attr']

        if a_attr == 'str' or b_attr == 'str':
            return '--'
            
        a_val = eval(a_parsed['value'])
        b_val = eval(b_parsed['value'])

        c  = str(a_val*b_val)
        if a_attr == 'val_err':
            a_err = eval(a_parsed['error'])
            c_err = str(a_err*b_val)
            c = '%s +/- %s' %(c, c_err)

        return c 


    def cell_trim(self, cell=None,  rnd=None, factor=None,
                  err_type=None, rounding='ROUND_HALF_UP',
                  col = None,
                  row = None,
                  opt = None,
                  format = None):
        
        if format:
            locale.setlocale(locale.LC_ALL, '')

        if row != None and col != None:
            cell = self.cell_get(row, col)

        parsed_cell =  self.cell_parse(cell)
        cell_attr = parsed_cell['attr']

        if cell_attr =='float' or cell_attr == 'int':
            if factor != None:
                cell = float(cell)*factor
            if rnd != None:
                cell = decimal.Decimal(str(cell)).quantize(
                    decimal.Decimal(rnd), rounding=rounding)
                
        elif cell_attr == 'val_err':
            value = parsed_cell['value']
            error = parsed_cell['error']
            if factor != None:
                value = str(eval(value)*factor)
                if err_type != 'Sgma':
                    error = str(eval(error)*factor)

            if rnd != None:
                value = decimal.Decimal(value).quantize(
                    decimal.Decimal(rnd), rounding=rounding)
                
                error = decimal.Decimal(error).quantize(
                    decimal.Decimal(rnd), rounding=rounding)

            if format:
                value = locale.format(format, float(value), True)
                
            cell = str(value)+' +/- '+str(error)

            if err_type == 'None':
                cell = str(value)
                
            elif err_type == 'Only':
                cell = str(error)
                
            elif err_type == 'Sgma':
                sigma = str(error)
                sigma = decimal.Decimal(sigma).quantize(
                    decimal.Decimal(rnd), rounding=rounding)

                if value > 0: value = '+'+ str(value)
                if sigma > 0: sigma = '+'+ str(sigma)
                
                cell = str(value)+'('+str(sigma)+'sigma)'

            elif err_type == 'Efcy':
                if float(value) >= 100:
                    cell = '100 - %s' % error
                
            if err_type and '<' in err_type:
                th  = err_type.replace('<', '')
                if float(value) < float(th):
                    cell = err_type
                    
        elif cell_attr =='val_err2':
            value = parsed_cell['value']
            error = parsed_cell['error']
            error2 = parsed_cell['error2']
            if factor != None:
                value = str(eval(value)*factor)
                error = str(eval(error)*factor)
                error2 = str(eval(error2)*factor)
                if not isinstance(error2, str):
                    error2 = str(eval(error2)*factor)
            if rnd != None:
                value = decimal.Decimal(value).quantize(decimal.Decimal(rnd),
                                                        rounding=rounding)
                error = decimal.Decimal(error).quantize(decimal.Decimal(rnd),
                                                        rounding=rounding)
                error2 = decimal.Decimal(error2).quantize(decimal.Decimal(rnd),
                                                          rounding=rounding)
            
            cell = str(value)+' +/- '+str(error)+' +/- '+str(error2)

        elif cell_attr =='val_err3':
            value = parsed_cell['value']
            error = parsed_cell['error']
            error2 = parsed_cell['error2']
            error3 = parsed_cell['error3']

            if err_type == 'Combined':
                 error = str(sqrt(eval(error)**2 +
                                  eval(error2)**2 +
                                  eval(error3)**2))
            if factor != None:
                value = str(eval(value)*factor)
                error = str(eval(error)*factor)
                error2 = str(eval(error2)*factor)
                error3 = str(eval(error3)*factor)
                if not isinstance(error2, str):
                    error2 = str(eval(error2)*factor)
            if rnd != None:
                value = decimal.Decimal(value).quantize(decimal.Decimal(rnd),
                                                        rounding=rounding)
                error = decimal.Decimal(error).quantize(decimal.Decimal(rnd),
                                                        rounding=rounding)
                error2 = decimal.Decimal(error2).quantize(decimal.Decimal(rnd),
                                                          rounding=rounding)
                error3 = decimal.Decimal(error3).quantize(decimal.Decimal(rnd),
                                                          rounding=rounding)
            
            cell = '%s +/- %s +/- %s +/- %s' % (value, error, error2, error3)
            if err_type == 'Combined':
                cell = '%s +/- %s' % (value, error)

        if cell != '--' and opt:
            if '+/-' in opt :
                opt = opt.replace('+/-', '')
                if cell_attr == 'val_err':
    
                    cell_val = str(value)
                    cell_err = str(error)
                    
                    if value > 0:
                        #cell_val = cell_val.replace('-', '') #protect -0.0 case
                        cell_val = '+' + cell_val

                    if value == 0:
                        cell_val = cell_val.replace('-', '')
                        cell_val = cell_val.replace('+', '')
                        
                    if error > 0:
                        cell_err = '+' + cell_err 

                    if error == 0:
                        cell_err = cell_val.replace('-', '')
                        cell_err = cell_val.replace('+', '')

                        
                    if 'sigma' in opt:
                        cell = cell_err
                    else:
                        cell = cell_val + cell_err
                else:
                    if not isinstance(cell, str):
                        cell = str(cell)
                    value = eval(cell)
                    if value >= 0:
                        cell = cell.replace('-', '') #protect -0.0 case
                        cell = '+' + cell
                    
            if opt == 'chisq':
                cell = cell.split('(')[1].split('sigma')[0].replace('+', '')
            elif opt == 'sigma':
                cell = cell.split('(')[1].split('sigma')[0]
            elif opt == '%(':
                cell = cell.replace('(', '%(')
            elif 'cell' in opt:
                cell = opt.replace('cell', str(cell))

        if row != None and col != None:
            self.cell_set(row, col, cell)
        return cell
    

    def cell_trim_for_org(self, cell):
        cell = str(cell)
        if '+/-' in cell:
            val = cell.split('+/-')[0]
            if '-' in val:
                new_val = val.replace('-', '- ')
                cell = cell.replace(val, new_val)
        return cell
    

##----------------------------------------
##  Handle Column 
##----------------------------------------

    def column_abs(self, title):
        aList = []
        col_a = self.column_get(title)
        for cell in col_a:
            cell = self.cell_abs(cell)
            aList.append(cell)

        self.column_replace(title, aList)     

             

    def column_analyze(self, title, ranges):
        result = []
        for rge in ranges:
            col = self.column_get(title, rge)
            frequencies = len(col)-1
            result.append(str(frequencies))
        return result 
        

    def column_append(self, col, title=None,
                      rnd=None, factor=None, opt=None):

        if title != None:
            col.insert(0, title)

        if self.data == []:
            for item in col:
                self.data.append([])

        for line, newitem in zip(self.data, col):
            line.append(newitem)

        if title and (rnd or factor or opt):
            self.column_trim(title, rnd, factor, opt=opt)


    def column_append_by_add(self, title, a, b, rnd=None, factor=None):

        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_add(cell_a, cell_b)
            aList.append(cell)
        aList[0]= title
        self.column_append(aList)     
        if rnd or factor :
            self.column_trim(title, rnd, factor)



    def column_append_by_add_quadrature(
        self, title, a, b, rnd=None, factor=None):

        aList = []

        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_add_quadrature(cell_a, cell_b)
            aList.append(cell)
        aList[0]= title
        self.column_append(aList)     
        if rnd or factor :
            self.column_trim(title, rnd, factor)

        
    def column_append_by_add_quadrature3(
        self, title, a, b, c, rnd=None, factor=None):
        self.column_append_by_add_quadrature('_tmp', a, b)
        self.column_append_by_add_quadrature(title, '_tmp', c, rnd, factor)
        self.column_delete('_tmp')
        

        

    def column_append_by_diff(self, title, a, b, 
                              rnd='0.01', factor=1,
                              err_type=None, opt =''):

        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_diff(cell_a, cell_b, rnd, factor, err_type, opt)
            aList.append(cell)

        aList[0]= title
        self.column_append(aList)     

    def column_append_by_diff_err(self, title, a, b, 
                                  rnd='0.01', factor=1,
                                  err_type=None, opt =''):
        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_diff_err(cell_a, cell_b,
                                      rnd, factor, err_type, opt)
            
            aList.append(cell)

        aList[0]= title
        self.column_append(aList)     


    def column_append_by_diff_chisq(self, title, a, b, 
                                    rnd='0.01', factor=1,
                                    err_type=None, opt =''):
        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_diff_chisq(cell_a, cell_b,
                                        rnd, factor, err_type, opt)
            
            aList.append(cell)

        aList[0]= title
        self.column_append(aList)     


    def column_append_by_diff_pct(self, title, a, b, 
                                  rnd='0.01', factor=100,
                                  err_type=None, opt=''):

        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)

        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_diff_pct(cell_a, cell_b, rnd, factor, err_type, opt)
            aList.append(cell)

        aList[0]= title
        self.column_append(aList)     

    def column_append_by_diff_sigma(self, title, a, b, 
                                     rnd='.1', factor=1):
        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_diff_sigma(cell_a, cell_b, rnd, factor)
            aList.append(cell)
        aList[0]= title
        self.column_append(aList)     


    def column_append_by_diff_sigma_pct(self, title, a, b, 
                                        rnd='.1', factor=100, err_type=None,
                                        opt=None):
        aList = []
        aList.append(title)
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            if cell_a == a:
                continue
            cell = self.cell_diff_sigma_pct(cell_a, cell_b, rnd, factor,
                                            err_type, opt)
            aList.append(cell)
        self.column_append(aList)     


    def column_append_by_diff_sigma2_pct(self, title, a, b, 
                                        rnd='.1', factor=100, err_type='Sgma2'):
        aList = []
        aList.append(title)
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            if cell_a == a:
                continue
            cell = self.cell_diff_sigma_pct(cell_a, cell_b, rnd, factor, err_type)
            aList.append(cell)
        self.column_append(aList)     



    def column_append_by_divide(self, title, a, b, err_type=None,
                                rnd=None, factor=None, 
                                rounding='ROUND_HALF_UP',table=None,
                                refTab=None, refCol=None, opt=''):
        if table == None:
            aList = self.column_divide(title, a, b, err_type,
                                       refTab, refCol)
        else:
            aList = table.column_divide(title, a, b, err_type,
                                        refTab, refCol)

        self.column_append(aList)
        if rnd or factor or err_type or opt:
            self.column_trim(title, rnd, factor, err_type, opt=opt)

    def column_append_by_max(self, title, a, b):
        
        aList = []
        row_no = -1
        for row in self.column_get(a):
            row_no+= 1
            if row_no == 0:
                aList.append(title)
                continue
            cell_a =  self.cell_get(row_no, a)
            cell_b =  self.cell_get(row_no, b)
            cell_c =  self.cell_max_abs(cell_a, cell_b)
            aList.append(cell_c)

        self.column_append(aList)     


    def column_append_by_subtract(self, title, a, b,
                                  table=None,
                                  rnd=None, factor=None,
                                  err_type=None):
        if table == None:
            aList = self.column_subtract(title, a, b)
        else:
            aList = table.column_subtract(title, a, b)

        self.column_append(aList)

        if rnd or factor or err_type:
            self.column_trim(title, rnd, factor, err_type)

    def column_append_by_subtract_number(self, title, a, num,
                                         rnd=None, factor=None,
                                         err_type=None):

        aList = self.column_subtract_by_number(title, a, num)
        
        self.column_append(aList)
        if rnd or factor or err_type:
            self.column_trim(title, rnd, factor, err_type)


    def column_append_by_subtract_quadrature(
        self, title, a, b, rnd=None, factor=None, err_type=None):

        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_subtract_quadrature(cell_a, cell_b)
            aList.append(cell)
        aList[0]= title
        self.column_append(aList)     
        if rnd or factor :
            self.column_trim(title, rnd, factor)


    def column_append_by_times_number(self, title, a, num, rnd=None):
        aList = []
        row_no = -1
        for row in self.column_get(0):
            row_no+= 1
            if row_no == 0:
                aList.append(title)
                continue
            cell_a =  self.cell_get(row_no, a)
            cell_c =  self.cell_times(cell_a, num)
            aList.append(cell_c)

        self.column_append(aList)     
        if rnd :
            self.column_trim(title, rnd)



    def column_append_from_file_list(self, title, fileList,
                                     rowName, colName,
                                     rnd=None, factor=None,
                                     err_type=None):

        aList = []
        aList.append(title)
        colNameList = colName.split(',')
        rowNameList = rowName.split(',')
        
        for f in fileList:
            if not os.access(f, os.F_OK):
                for  rowName in rowNameList:
                    aList.append('')
                continue
            
            tempTable = UserTable(f)
            for rowName in rowNameList:
                if len(colNameList) > 1:
                
                    cell_0 = tempTable.cell_get(rowName, colNameList[0])
                    cell_1 = tempTable.cell_get(rowName, colNameList[1])
                    cell = self.cell_join(cell_0, cell_1)
                
                else:
                    cell = tempTable.cell_get(rowName,colName)
                    
                cell = self.cell_trim(cell=cell, rnd=rnd, factor = factor,
                                      err_type = err_type) 
                aList.append(cell)

        self.column_append(aList)     

    def column_append_from_tab_file(self, title, tabfile, headname = None,
                                    rnd=None, factor=None, row = None):
        
        if headname == None: headname = title
        tempTable = UserTable(tabfile) 
        
        aList = tempTable.column_get(headname)
        aList[0] = title
        if row:
            start = row.split(':')[0]
            end   = row.split(':')[1]
            if start and end:
                start = int(start)
                end   = int(end)
                aList = aList[start:end]
            if start and not end:
                start = int(start)
                aList = aList[start:]
                aList.insert(0, title)
            if end and not start:
                end   = int(end)
                aList = aList[:end]
                
        self.column_append(aList)     
        if rnd or factor:
            self.column_trim(title, rnd, factor)


    def column_append_from_tex_file(self, title, texfile, headname = None,
                                    rnd=None, factor=None):

        if headname == None: headname = title
        tempTable = UserTable() 
        tempTable.input_tex(texfile)
        aList = tempTable.column_get(headname)
        aList[0] = title
        self.column_append(aList)     
        if rnd or factor:
            self.column_trim(title, rnd, factor)

    def column_append_from_table(self, title, table, head = None,
                                 rnd=None, factor=None):
        if head == None: head = title
        aList    = table.column_get(head)
        aList[0] = title
        self.column_append(aList)     
        if rnd or factor:
            self.column_trim(title, rnd, factor)

    def column_append_from_number(self, title, number):
        
        aList = []
        for k in self.data.keys():
            aList.append(str(number))
        aList[0] = title
        self.column_append(aList)     
        
        

    def column_delete(self, col_no):
        if isinstance(col_no, str):
            col_no = self.column_get_number(col_no)
        row_num = -1
        for row in self.data:
            row_num += 1
            delete_cell = row[col_no]
            self.data[row_num].remove(delete_cell)


    def column_divide(self, title, a, b, err_type=None, refTab=None,
                      refCol=None):
        c=[]
        a_err = None
        b_err = None
        ref_err = None
        if isinstance(a, str):
            a = self.column_get_number(a)
        if isinstance(b, str):
            b = self.column_get_number(b)
        row_num = -1
        for row in self.data:
            row_num += 1
            cell_a = row[a]
            cell_b = row[b]
            if row_num == 0:
                if title != None:
                    cell_c = title
                else:
                    cell_c = 'temp'
            else:
                if refCol != None:
                    if refTab != None:
                        ref_cell = refTab.column_get(refCol)[row_num]
                    else:
                        ref_cell = self.column_get(refCol)[row_num]
                    ref_err  =  self.cell_parse(ref_cell)['error']
                cell_c = self.cell_divide(cell_a, cell_b, err_type, ref_err)
            c.append(cell_c)
        return c


    def column_get(self, col_no, opt=None):
        column = []
        if isinstance(col_no, str):
            heads = self.data[0]
            for i in range(len(heads)):
                if heads[i].strip() == col_no:
                    col_no = i
                    break

        for line in self.data:
            column.append(line[col_no])

        if opt == None:
            return column

        if '>' in opt:
            opts_ = opt.split('>')
            title_ = opts_[0]
            min_ = opts_[1]

            if title_ == '':
                condition_col = column
            else:
                condition_col = self.column_get(title_)

            new_col = []
            line_num = 0
            for li, li_cond in zip(column, condition_col):
                line_num += 1
                if line_num == 1:
                    new_col.append(li)
                    continue
                if eval(li_cond) > eval(min_) :
                    new_col.append(li)
            column = new_col 
        else:
            raise NameError(opt)

        return column


    def column_get_number(self, col_name):
        heads = self.data[0]
        for i in range(len(heads)):
            if heads[i].strip() == col_name:
                return i
            
        
    def column_get_from_file(self, filename, col_no=0, title=None):
        table = UserTable()
        table.input_txt(filename)
        if col_no != 0:
            sys.stdout.write('Getting No.%s column. \n' %col_no)
        new_col = table.column_get(col_no, title)
        return new_col


    def column_print(self, column):
        for i in column:
            sys.stdout.write('%s \n' % i)

    def column_replace(self, col_no, new_col):
        if isinstance(col_no, str):
            col_no = self.column_get_number(col_no)
            
        for i in range(len(new_col)):
            self.data[i][col_no] = new_col[i]


    def column_replace_by_translate_elements(self, title, dict):
        col = self.column_get(title)
        new_col = []
        for cell in col:
            for k, v in dict.items():
                if k in cell and 'anti-'+k not in cell:
                    cell = cell.replace(k, v)
            new_col.append(cell)
        self.column_replace(title, new_col)


    def column_replace_by_translation(self, title, dict):
        col = self.column_get(title)
        new_col = []

        for cell in col:
            for k, v in dict.items():
                if k == cell.replace(' ____', ''):
                    cell = cell.replace(k, v)
            new_col.append(cell)
        self.column_replace(title, new_col)
        
       

    def column_replace_by_translation_inverse(self, title, dict):
        col = self.column_get(title)
        new_col = []
        for cell in col:
            for k, v in dict.items():
                if v == cell.replace(' ____', ''):
                    cell = cell.replace(v, k)

            new_col.append(cell)
        self.column_replace(title, new_col)
        

    def column_subtract(self, title, a, b):
        aList = []
        col_a = self.column_get(a)
        col_b = self.column_get(b)
        for cell_a, cell_b in zip(col_a, col_b):
            cell = self.cell_subtract(cell_a, cell_b)
            aList.append(cell)
        aList[0]= title
        return aList


    def column_subtract_by_number(self, title, a, num):
        aList = []
        col_a = self.column_get(a)
        for cell_a in col_a:
            cell = self.cell_subtract(cell_a, num)
            aList.append(cell)
        aList[0]= title
        return aList


    def column_trim(self, column, rnd=None, factor=None,
                    err_type=None, rounding='ROUND_HALF_UP',
                    row = None, opt = None, except_row=None,
                    format= None):

        if type(column) == types.ListType:
            new_col = []
            for cell in column:
                new_cell = self.cell_trim(
                    cell = cell,  rnd = rnd, factor=factor,
                    err_type=err_type, opt=opt, format=format)
                new_col.append(new_cell)
            return new_col



        if type(column) == types.StringType:
            column = self.column_get_number(column)

        if row == None:
            col_lenth =  len(self.column_get(column))
            row_list = [i for i in range(col_lenth) if i !=0]
                
        if type(row) == types.ListType:
            row_list = row
        if type(except_row) == types.ListType:
            row_list = [ro for ro in self.column_get(0)\
                        if (ro not in except_row and \
                            ro != self.cell_get(0,0))]
        for row in row_list:
            self.cell_trim(row = row, col = column,
                           rnd = rnd, factor=factor,
                           err_type=err_type, opt=opt, format=format)

    def columns_delete(self, cols):
        if not isinstance(cols, list):
            raise ValueError(cols)
        for col in cols:
            self.column_delete(col)


    def columns_join(self, title, col_A, col_B,
                         str=' +/- ', rnd=None, factor=None):

        aList = []
        col_A_list    = self.column_get(col_A)
        col_B_list    = self.column_get(col_B)

        for i in range(len(col_A_list)):
            if i == 0 :
                cell = title
            else:
                cell_a = col_A_list[i]
                cell_b = col_B_list[i]
                cell = self.cell_join(cell_a, cell_b, str)
            aList.append(cell)

        self.column_replace(col_A, aList)     
        self.column_delete(col_B)

        if rnd or factor:
            self.column_trim(title, rnd, factor)

    def columns_join3(self, title, col_A, col_B, col_C,
                      str=' +/- ', rnd=None, factor=None):

        self.columns_join(title+'tmp', col_A, col_B, str)
        self.columns_join(title, title+'tmp', col_C, str)

        if rnd or factor:
            self.column_trim(title, rnd, factor)

    def columns_trim(self, cols, rnd=None, factor=None):
        if not isinstance(cols, list):
            raise ValueError(cols)
        for col in cols:
            self.column_trim(col, rnd=rnd, factor=factor)



## -----------------------------------------------
## Data Method
## -----------------------------------------------

    def data_trim(self, factor=None):
        new_data = []
        for row in self.data:
            new_row = []
            for cell in row:
                new_cell = self.cell_trim(cell, factor=factor)
                new_row.append(new_cell)
            new_data.append(new_row)
        self.data = new_data

## -----------------------------------------------
## Diff Method
## -----------------------------------------------


    def diff_sigma_pct(self, tabB):

        tab_ = UserTable()
        first_col = self.column_get(0)
        tab_.column_append(first_col)

        for col_num in self.head:
            if col_num == 0:
                continue
            colA = self.column_get(col_num)
            colA[0] = 'A'
            colB = tabB.column_get(col_num)
            colB[0] = 'B'

            col_name = self.head[col_num]
            if '(' in col_name:
                col_name = col_name.split('(')[0]

            tab_.column_append(colA)
            tab_.column_append(colB)
            tab_.column_append_by_diff_sigma_pct('%s-diff(%%)' % col_name, 'B', 'A')
            tab_.column_delete('A')
            tab_.column_delete('B')

        return tab_   


## -----------------------------------------------
## Get Method
## -----------------------------------------------

    def get_length(self):
        length = len(self.column_get(0))
        if self.head:
            length = length -1
        return length

    def get_val_err_by_name(self, name, rnd=None):
        val = self.cell_get(name, 'Value')
        err = self.cell_get(name, 'Error')
        newcell = val + '+-' +  err
        newcell = self.cell_trim(newcell, rnd=rnd)
        return newcell

## -----------------------------------------------
## Row Handling
## -----------------------------------------------
    def row_add(self, a, b, rnd=None):
        a_err = None
        b_err = None

        rowMap={}
        vo = self.data[2*row-1]
        rowMap[0] = vo[0]
        try:
            ve = self.data[2*row]
        except KeyError:
            sys.stdout.write('ve does not have the right value.\n')
        for col in vo.keys():
            if col == 0:
                continue

    def row_append(self, row, name=None, factor=None, rnd=None, opt=None):
        if rnd != None:
            row = self.row_trim(row, factor=factor, rnd=rnd, opt=opt)

        if name != None:
            row[0] = name
            
        self.data.append(row)


    def row_append_by_average(self, name, column = None, rnd=None):
        new_row = {}
        new_row[0] = name
        
        for col in self.data.values()[0]:
            if col == 0: continue
            n  = 0
            for row in self.data.keys():
                if row == 0: continue
                cell = self.data[row][col]
                if n == 0:
                    new_cell = cell
                else:
                    new_cell = self.cell_add(cell, new_cell)
                n += 1

            if self.data[0][col] not in column:
                a = new_row[1]
                b = new_row[2]
                c =  self.cell_subtract(a, b)
                new_cell = self.cell_divide(c, b, err_type='Indp')
                new_cell = self.cell_trim(new_cell, factor= 100)
                
            new_row[col] = self.cell_trim(new_cell, rnd = rnd)
            
        new_row_no = len(self.data.keys())
        self.data[new_row_no]= new_row


    def row_append_by_divide(self, name, cell_A, cell_B, column_C, rnd=None):
        new_row = {}
        new_row[0] = name

        row_A  = cell_A[0]
        col_A  = cell_A[1]
        
        cell_A = self.cell_get(row_A, col_A)
        # --- need to fix the rest !!
        
        for col in self.data.values()[0]:
            if col == 0: continue

            sum_cell = ''
            n        = 0
            for row in self.data.keys():
                if row == 0: continue
                cell = self.data[row][col]
                if n == 0:
                    sum_cell = cell
                else:
                    sum_cell = self.cell_add(cell, sum_cell)
                n += 1

            
            new_row[col] = self.cell_trim(sum_cell, rnd = rnd)
            
        #avg_cell = self.cell_divide(sum_cell, str(n), err_type='Indp')
        new_row_no = len(self.data.keys())
        self.data[new_row_no]= new_row


    def row_append_by_sum(self, name='Sum', column = None,
                          row= None, rnd=None):
        new_row = {}
        col_list = self.data.values()[0]
        row_list = []
        
            
        if type(column) == types.StringType:
            heads = self.data[0]
            for k, v  in heads.items():
                if v == column: col_no = k
            
        if row == None:
            row_list = self.data.keys()

        if type(row) == types.ListType:
            row_list = row

        for col in col_list:
            if col == 0 :
                new_row[0] = name
                continue
            
            if col_no and col != col_no :
                new_row[col] = '--'
                continue
            
            n  = 0
            for row in row_list:
                if row == 0: continue
                cell = self.data[row][col]
                if n == 0:
                    new_cell = cell
                else:
                    new_cell = self.cell_add(cell, new_cell)
                n += 1

                new_row[col] = self.cell_trim(new_cell, rnd = rnd)
            
        new_row_no = max(self.data.keys())+1
        self.data[new_row_no]= new_row
        return new_row

    def row_append_by_square_sum(self, name='SqrSum', column=None,
                                 row=None, rnd=None, opt=None):
        new_row = []
        
        col_list = self.data[0]
        #row_list = []

        if isinstance(column, str): 
            col_list = [column]

        #if type(row) == types.ListType:
        #    row_list = row

        #if row == None:
        #    row_list = range(len(self.data))


        for col in col_list:
            #if col == 0 :
            #    new_row.append(name)
            #    continue
            
            #if column and col_no and col != col_no :
            #    new_row.append('--')
            #    continue
            n = -1
            for cell in self.column_get(col):
                n += 1
                if n == 0:
                    continue
                if n == 1:
                    new_cell = self.cell_square(cell)
                else:
                    tmp_cell = self.cell_square(cell)
                    new_cell = self.cell_add(tmp_cell, new_cell)

            #new_cell = self.cell_trim(new_cell, rnd=rnd, opt=opt)
            new_row.append(new_cell)
            print new_row
            sys.exit()
        self.data.append(new_row)
        return new_row


    def row_append_from_files(self, name, files):
        row = [name]
        for file_ in files:
            f = open(file_)
            cell = f.read().strip()
            f.close()
            row.append(cell)

        self.row_append(row)
        return row


    def row_delete(self, row):
        delete_row = self.row_get(row)
        self.data.remove(delete_row)
        return delete_row

        
    def row_extend(self, tab, rnd= None):
        length = len(tab.column_get(0))
        for row_no in range(1,length):
            self.row_append(tab.row_get(row_no))
        
    def row_get(self, row_no):
        if isinstance(row_no, str):
            row_no = self.row_get_number(row_no)
        row = self.data[row_no]
        return row

    def row_get_number(self, row_name):
        row_num = -1
        for row in self.data:
            row_num += 1
            if row[0] == row_name:
                return row_num

    def row_hline(self, row_no):
        if isinstance(row_no, str):
            row_name = row_no
            row_no = self.row_get_number(row_name)

        self.cell_trim(row=row_no, col=0, opt='cell ____' )
                    
    def row_output(self, row):
        line = '\t| '.join(self.row_get(row))
        sys.stdout.write(line + '\n')

    def row_trim(self, row, factor=None, rnd=None, opt=None):
        new_row = []
        for cell in row:
            new_cell = self.cell_trim(cell=cell, factor=factor,
                                      rnd=rnd, opt=opt)
            new_row.append(new_cell)
        return new_row
    
    def rows_delete(self, rows):
        if not isinstance(rows, list):
            raise ValueError(rows)
        for row in rows:
            self.row_delete(row)


    def rows_join_by_method(self, method, rnd=None):
        methodList = None
        methodList = method.split(',')
        # == need to fix  the rest

        newLineNumber= 0
        newData = {}
        newData[0]= self.data[0]
        
        keys= self.data.keys()
        length = len(keys)
        new_length= length/2
        
        rndList = None

        if rnd != None : rndList = rnd.split(',')

        for row in range(1,new_length+1):
            rowMap={}
            vo = self.data[2*row-1]
            rowMap[0] = vo[0]
            try:
                ve = self.data[2*row]
            except KeyError:
                sys.stdout.write('ve does not have the right value.\n')
                continue

            for col in vo.keys():
                if col == 0:
                    continue
                if rndList != None and len(rndList)>1:
                    rnd = rndList[col-1]


                newCell = self.cell_add(vo[col], ve[col], rnd=rnd)

                rowMap[col] = newCell

            newData[row] = rowMap

        self.data = newData


    def rows_join_by_add(self, rnd=None):
        newLineNumber= 0
        newData = {}
        newData[0]= self.data[0]
        length = len(self.data.keys())
        new_length= length/2
        self.length = new_length
        self.width  = len(self.data[0].keys())
        rndList = None
        for row in range(new_length):
            rowMap={}
            row_a = self.data[2*row+1]
            row_b = self.data[2*row+2]
            for col in row_a.keys():
                cell_a = row_a[col]
                cell_b = row_b[col]
                newCell = self.cell_add(cell_a, cell_b)
                rowMap[col] = newCell

            newData[row+1] = rowMap

        self.data = newData


    def rows_join_by_average(self, rnd=None, err_type=None):
        newLineNumber= 0
        newData = []
        newData.append(self.data[0])
        
        length = len(self.data)
        new_length= length/2

        rndList = None

        if rnd != None :
            rndList = rnd.split(',')

        for row in range(new_length):
            tmpRow = [] 
            row_a = self.data[2*row+1]
            row_b = self.data[2*row+2]

            for col in range(len(row_a)):
                cell_a = row_a[col]
                cell_b = row_b[col]
                if rndList != None and len(rndList)>1:
                    rnd = rndList[col-1]
                    
                newCell = self.cell_average(
                    cell_a, cell_b, rnd=rnd, err_type=err_type)
                tmpRow.append(newCell)

            newData.append(tmpRow)

        self.data = newData


    def rows_join_by_diff(self, title, rnd='0.01', 
                          factor=1, err_type=None,
                          denominator='second'):
        tmp_column    = []
        tmp_table = UserTable()
        col_no_list = range(len(self.data[0]))
        length = len(self.data)
        new_length= length/2
        for col_no in col_no_list:
            if col_no == 0:
                tmp_column.append(self.data[0][col_no])
                for row in range(new_length):
                    tmp_column.append(self.data[2*row+1][col_no])
                tmp_table.column_append(tmp_column)
                tmp_column = []
                
            else:
                tmp_column.append(title)
                for row in range(new_length):
                    rowMap={}
                    row_a = self.data[2*row+1]
                    row_b = self.data[2*row+2]
                    cell_a = row_a[col_no]
                    cell_b = row_b[col_no]
                    if denominator=='first' :
                        newCell = self.cell_diff(cell_b, cell_a, rnd,
                                                 factor, err_type)
                    elif denominator=='second':
                        newCell = self.cell_diff(cell_a, cell_b, rnd,
                                                 factor, err_type)
                    else:
                        sys.stdout.write('tabletools::Not valide option- %s \n'
                                         % denominator)
                    tmp_column.append(newCell)

                tmp_table.column_append(tmp_table.column_trim(tmp_column))
                tmp_column = []

        self.data = tmp_table.data

    def rows_join_by_diff_pct(self, title, rnd='0.01', 
                              factor=100, err_type=None,
                              denominator='second'):
        tmp_column  = []
        tmp_table = UserTable()
        col_no_list = range(len(self.data[0]))
        length = len(self.data)
        new_length= length/2
        for col_no in col_no_list:
            if col_no == 0:
                tmp_column.append(self.data[0][col_no])
                for row in range(new_length):
                    tmp_column.append(self.data[2*row+1][col_no])
                tmp_table.column_append(tmp_column)
                tmp_column = []
            else:
                tmp_column.append(title)
                for row in range(new_length):
                    rowMap={}
                    row_a = self.data[2*row+1]
                    row_b = self.data[2*row+2]

                    cell_a = row_a[col_no]
                    cell_b = row_b[col_no]

                    if denominator=='first' :
                        newCell = self.cell_diff_pct(cell_b, cell_a, rnd,
                                                     factor, err_type)
                    elif denominator=='second':
                        newCell = self.cell_diff_pct(cell_a, cell_b, rnd,
                                                     factor, err_type)
                    else:
                        sys.stdout.write('tabletools::Not valide option- %s \n' %
                                         denominator)
                    tmp_column.append(newCell)
                tmp_table.column_append(tmp_table.column_trim(tmp_column))
                tmp_column = []
        self.data = tmp_table.data


    def rows_join_by_max(self, col, rnd=None):
        newLineNumber= 0
        newData = []
        newData.append(self.data[0])
        length = self.length()
        new_length= length/2
        rndList = None
        for row in range(new_length):
            row_a = 2*row+1
            row_b = 2*row+2
            cell_a = self.cell_get(row_a, col)
            cell_b = self.cell_get(row_b, col)
            newCell = self.cell_max(cell_a, cell_b)
            if newCell == cell_a:
                newrow = self.data[2*row+1]
            else:
                newrow = self.data[2*row+2]
            newData.append(newrow)

        self.data = newData

#--------------------------------
# Handle Output
#--------------------------------

    def output_list(self):
        keys= self.data.keys()
        keys.sort()

        outlist = []
        
        tmpdata = copy.deepcopy(self.data)

        for k in keys:
            v = tmpdata[k]
            keys2= v.keys()
            keys2.sort()
            hline = False
            if k == 0: hline = True
            for k2 in keys2:
                v2=v[k2]
                if ' ____' in v2:
                    hline = True
                    v2 = v2.replace(' ____', '')
                    v[k2] = v2

            if k == 0: 
                outlist.append(' || '.join(v.values()))
            else:
                outlist.append(' | '.join(v.values()))

        return outlist
    

    def output_org(self, outputname=None, header=None, footer=None,
                   verbose=0):
        
        if outputname :
            if verbose > 0:
                sys.stdout.write('Writing to %s ...' %(outputname))
            fo = open(outputname, 'w')
        else:
            print_sep()

        linum = 0
        for line in self.data:
            linum += 1
            line = [self.cell_trim_for_org(li) for li in line]

            if linum == 1:
                hline = True

            if outputname :
                if linum == 1:
                    if header:
                        fo.write(header+ '\n\n') 
                    
                    fo.write('| '+'\t | '.join(line)+'|\n')
                    fo.write('|' + '-'*80 + '|\n')
                else:
                    fo.write('| ' + '\t | '.join(line)+'|\n')

            else:
                sys.stdout.write('| '+'\t | '.join(line)+'|\n')
                if hline:
                    sys.stdout.write('|' + '-'*80 + '|\n')
                    hline = False
        
        if outputname :
            if footer:
                fo.write('\n' + footer + '\n') 
            fo.close()
        else:
            print_sep()
            

    def output_root(self, outputname, tree='T', verbose = 0):
        import ROOT
        import array
        maxn = len(self.data.keys()) - 1
        #need fix
    
        f = ROOT.TFile(outputname, 'recreate')
        t = ROOT.TTree(tree, 'A Tree')
        d = array.array('f', maxn*[0.])
        t.Branch('myval', d, 'myval[')

        keys= self.data.keys()

        keys.sort()
        tmpdata = copy.deepcopy(self.data)
        

    def output_screen(self):
        print_sep()
        linum = 0 
        for line in self.data:
            linum += 1 
            sep = '\t | '
            if linum == 1: 
                sep = '\t || '

            line = [str(li) for li in line]
            sys.stdout.write(sep.join(line)+'\n')            

            if linum == 1: 
                print_sep()

        print_sep()


    def output_tex(self, outputname, top=0, bottom=0,
                   texhead=None, verbose=1, texstyle=None):
        if verbose > 0:
            sys.stdout.write('Writing to %s ...' %(outputname))

        joint_str = '\t & '
        topline = '%s\n' %'\\hline'*top
        bottomline = '%s\n' %'\\hline'*bottom
        replace_dollor = False
        if texstyle == 'eqnarray':
            joint_str = '\t &=& '
            topline = '\\begin{eqnarray}\n'
            bottomline = '\\end{eqnarray}'
            replace_dollor = True
            
        fo = open(outputname, 'w')
        fo.write(topline)
        row_num = -1
        for line in self.data:
            row_num += 1
            line = [str(li) for li in line]
            if row_num == 0 and texstyle == None:
                hline = True
            else:
                hline = False
            col_num = -1
            for cell in line:
                col_num += 1
                if ' ____' in cell:
                    hline = True
                    cell = cell.replace(' ____', '')
                if cell == '.':
                    cell = ' '
                if '+-' in cell:
                    cell = cell.replace('+-', '+/-')
                attr = self.cell_parse(cell)['attr']

                if attr == 'int' or attr == 'float':
                    cell = '$'+cell+'$'
                else:
                    cell_list = cell.split('+/-')
                    if 'sigmap' in cell:
                        continue
                    if '+/-' in cell:
                        cell = '$'+ '\pm'.join(cell_list)+ '$'
                    if 'sigma' in cell:
                        cell = '$'+cell.replace('sigma', '\sigma')+ '$'
                    if '%' in cell:
                        cell = cell.replace('%', '\%')
                    if 'x10E' in cell:
                        cell = cell.replace('x10E', '\\times 10^')
                        if '$' not in cell:
                            cell = '$'+cell+'$'
                    if '<' in cell:
                        cell = '$%s$' %cell
                    if '100 - ' in cell:
                        err = cell.split('100 - ')[-1]
                        cell = '$100^{+0}_{-%s}$' % err

                if replace_dollor:
                    cell = cell.replace('$', '')
                line[col_num] = cell
                
            if row_num == 0 :
                if texhead != None:
                    fo.write(texhead)
                if texstyle == 'eqnarray':
                    continue
                if texhead == None:
                    fo.write(joint_str.join(line))
            else:
                fo.write(joint_str.join(line))

            if hline:
                fo.write('\\\\ \\hline \n')
            elif row_num == self.length()-1 and texstyle == 'eqnarray':
                fo.write('\n')
            else:
                fo.write('\\\\\n')
                
        fo.write(bottomline)
        fo.close()
        if verbose > 0:
            sys.stdout.write(' done.\n')

 
    def output_txt(self, filename=None, verbose=1):
        if verbose > 0:
            self.output_screen()
        if not filename:
            return 

        def write_file(tmpfile):
            fo = open(tmpfile ,'w')
            linum = 0 
            for line in self.data:
                linum += 1 
                sep = '\t | '
                if linum == 1: 
                    sep = '\t || '
                line = [str(li) for li in line]
                fo.write(sep.join(line)+'\n')
            fo.close()
         
        if os.access(filename, os.F_OK) :
            tmpfile = filename+'.tmp'
            write_file(tmpfile)
             
            if filecmp.cmp(filename, tmpfile):
                message = 'up-to-date: %s' % filename
            else:
                message = 'updated %s' %filename
            os.rename(tmpfile, filename)

        else:
            head, tail = os.path.split(filename)
            if not os.access(head, os.F_OK) :
                sys.stdout.write('creating dir %s ...\n'  % head)
                os.makedirs(head)

            write_file(filename)
            message = 'created %s' %filename

        if verbose > 0:
            sys.stdout.write(message+'\n')


    
    #--------------------------------
    #  Sort Table
    #--------------------------------

    def sort_by_column(self, title, reverse=False, opt=''):
        head = self.data[0]
        body = self.data[1:]
        col = self.column_get_number(title)
        new_body = sorted(body, key=operator.itemgetter(col),
                          reverse=reverse)
        self.data = [head]
        self.data.extend(new_body)

    def width(self):
        width = len(self.data[0])
        return width

    def length(self):
        length = len(self.data)
        return length

    
if __name__ == "__main__":

    usage()
    
