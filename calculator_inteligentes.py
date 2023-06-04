
from abc import ABC,abstractproperty
class Operator(ABC):
    @abstractproperty
    def allowedVareables(self) -> list[str]:
        '''
        a list of name of the vareables to print 
        '''
        pass
    def __str__(self):
        glbl = vars(self)
        arms = [ ''.join(e) if isinstance(e,list) else e for x in self.allowedVareables for e in glbl[x]]
        return ''.join(arms)
    def __repr__(self):
        return self.__str__()
    @staticmethod
    def parser2list(a:str)->list[str]:
        return [ x for x in a]
    @staticmethod
    def str2int(a):
        return int(a,2)
class BitChain(Operator):
    @property
    def allowedVareables(self):
        return ['a']
    def __init__(self,a:str):
        super().__init__()
        self.a = a
        self.a_listed = self.parser2list(a)
    def print_operation(self,operator,a:list[str],b:list[str],response):
        if b:
            for r,q,s in zip(a,b.a,response):
                print(f"{r.center(3,' ')}{operator}{q.center(3,' ')} {s}")
        else:
            print(f"{operator}{a.center(3,' ')}")
    def update_a(self,value:list[str]):
        self.a_listed = value
        self.a = ''.join(self.a_listed)
    def __invert__(self):
        ''' ~ operator niega y coloca el resultado en a'''
        #self.update_a([ '0' if x == '1' else '1' for x in self.a])   
        inv = BitChain(''.join([ '0' if x == '1' else '1' for x in self.a]))
        self.print_operation(operator='~',a=self.a,b=None,response=inv.a)
        return inv
    def __and__(self,b):
        ''' operador ^ '''
        #b = self.parser2list(b)
        #self.update_a(['1' if(a == '1' and b == '1') else '0'  for a,b in zip(self.a_listed,b.a_listed)])
        rsp = BitChain(['1' if(a == '1' and b == '1') else '0'  for a,b in zip(self.a_listed,b.a_listed)])
        self.print_operation(operator='^',a=self.a,b=b,response=rsp.a)
        return rsp#self
    def __add__(self,b):
        ''' operador then -> '''
        #b = self.parser2list(b)
        #self.update_a(['0' if (a == '1' and b == '0') else '1' for a,b in zip(self.a_listed,b.a_listed)])
        rsp = BitChain(['0' if (a == '1' and b == '0') else '1' for a,b in zip(self.a_listed,b.a_listed)])
        self.print_operation(operator='->',a=self.a,b=b,response=rsp.a)
        return rsp#self
    def __or__(self,b):
        ''' operador or v '''
        
        #self.update_a(['0' if (a=='0' and b =='0') else '1' for a,b in zip(self.a_listed,b.a_listed)])
        #print('odd',self.a,b.a)
        rsp = BitChain(['0' if (a=='0' and b =='0') else '1' for a,b in zip(self.a_listed,b.a_listed)])
        self.print_operation(operator='v',a=self.a,b=b,response=rsp.a)
        return rsp#self
    def __sub__(self,b):
        ''' operador <->'''
        #self.update_a(['1' if ((a=='0' and b =='0') or (a =='1' and b =='1')) else '0' for a,b in zip(self.a_listed,b.a_listed)])
        rsp = itChain(['1' if ((a=='0' and b =='0') or (a =='1' and b =='1')) else '0' for a,b in zip(self.a_listed,b.a_listed)])
        self.print_operation(operator='<->',a=self.a,b=b,response=rsp.a)
        return rsp#self



#t = ThenOperator('1101')
#t  '1100'




#interface
number_inputs = lambda x: 2 **x

def generateTable(inputs:int,fill=True):
    inputs = number_inputs(inputs)
    for x in range(0,inputs +1):
        out = bin(x).split('b')[-1]
        if not(len(out) -1 >= inputs) and fill:
            #print(x,len(out))
            diff = inputs # xxx with the -1
            diff -=  len(out)
            
            yield diff * '0' + bin(x).split('b')[-1]
        elif not(fill):
            yield bin(x).split('b')[-1]






REPLACE_SYMBOLS = {
    '^':'&',
    'v':'|',
    'V':'|',
    '<->':'-',# nota lo colocamos primero dado que si colocamos primero el -> nos lo detectara con el metodo get primero y no realizara bien la operaicon
    # ejemplo p <-> q si colocamos primero el -> entonces remplazara por la cadena: p <+ q causando un error
    '->':'+'
}


def processInput(ex) -> dict:
    ''' 

    returns a resolution order dict like a tree '''
    #ex = input('ingrese el ejercicio:').lower()
    evaluateAlpha = lambda x: [x if x.isalpha() and not((x in ['v','V'])) else None][0]
    #ex_ks = [ n for n in [ REPLACE_KEYS.get(x,None) if x in REPLACE_KEYS.keys() else evaluateAlpha(x)  for x in ex ] if n != None]
    KEYS_DCT = dict( (x,idx) for idx,x in enumerate(ex) if x.isalpha() and not((x in ['v','V'])))
    #OBTIENE LAS VAREABLES QUE SE IMPLICAN EN LA OPERACION EJ A,B,C
    for x in REPLACE_SYMBOLS.keys():
        ex = ex.replace(x,REPLACE_SYMBOLS[x])
        # remplaza algunos simbolos para en lugar de crear nuestro propio ast
        # usamos el de python
    table = [ x for x in generateTable(len(KEYS_DCT.keys()) )]
    # tabla con los bits
    table_list = [[bit for bit in bits] for bits in table ]
    # tabla con los bits pero cada bit es un item de una lista
    #print(KEYS_DCT)
    #res = makeORDER(ex_ks)#,KEYS_DCT)
    #print(table)
    print(''.join(f'{x}'.center(3,' ') for x in KEYS_DCT.keys()))
    print('\n'.join("".join([bit.center(3," ") for bit in x ]) for x in table))
    KDCT = list(KEYS_DCT.keys())
    # saco solo las vareables y coloco en una lista
    for x,idxTab in zip(KDCT[::-1],enumerate(table)):
        KEYS_DCT[x] = idxTab[0] + 1# numero real no de indx
    KEYS_BIN = dict((key,'') for key in KDCT)
    COINCIDENCES = [(key[0],''.join(row[-key[1]])) for row in table_list for key in KEYS_DCT.items()]#(key[0],''.join(row[key[1]]))
    for c in COINCIDENCES:
        KEYS_BIN[c[0]] += c[1]
    #print(KEYS_BIN)
    KEYS_BIN = dict((k,bdata[::-1][1::]) for k,bdata in KEYS_BIN.items())
    #print(KEYS_BIN)
    KEYS_CBIN = {}
    for x in KEYS_BIN:
        KEYS_CBIN[x] = BitChain(KEYS_BIN[x])
        # integro al contexto global para que se reconozcan como vareables

    globals().update(KEYS_CBIN)
    # evaluo la expresion
    print(ex)
    print(eval(ex))
    input('precione enter para cerrar el programa')
         



def inputExcersice():
    print('ingrese los ejercicios separados por comas')

    inp = input('$>')
    inp = inp.split(',')
    for ex in inp:
        processInput(ex.lower())
if __name__ == '__main__':
    inputExcersice()