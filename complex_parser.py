import math
from lark import Lark, Transformer, v_args

calc_grammar = """
    ?start: sum
    ?sum: product
        | sum "+" product   -> op_add
        | sum "-" product    -> op_sub
    ?product: atom
        | product "*" atom   -> op_mul
        | product "/" atom   -> op_div
        | product "¬" NUMBER -> op_root
        | product "^" NUMBER -> op_power
    ?atom: IMAGINARY         -> transform_imag
         | "-" atom          -> op_negate
         | "e" "^" sum       -> op_e_z
         | "sin" atom        -> op_sin
         | "cos" atom        -> op_cos
         | "tan" atom        -> op_tan
         | "mod" atom        -> op_mod
         | "arg" atom        -> op_arg
         | "ln" atom        -> op_ln
         | "(" sum ")"
         | NUMBER            -> transform_real

    IMAGINARY.1 : /-?\d*(\.\d+)?([eE][+-]?\d+)?i/
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

class Complex():
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __repr__(self):
        sign = ""
        img = ""
        re = ""
        if self.imaginary == 1:
            sign = "+"
            img = "i"
        elif self.imaginary == -1:
            sign = "-"
            img = "i"
        elif self.imaginary < 0:
            sign = "-"
            img = str(abs(self.imaginary)) + 'i'
        elif self.imaginary == 0:
            sign = "+"
            img = "0i"
        else:
            sign = "+"
            img = str(self.imaginary) + 'i'

        if self.real == 0:
            re = "0"
        else:
            re = str(self.real)

        return f"{re} {sign} {img}"

    @staticmethod
    def add(z1, z2):
        res = Complex(z1.real + z2.real, z1.imaginary + z2.imaginary)
        return res
    
    @staticmethod
    def sub(z1, z2):
        res = Complex(z1.real - z2.real, z1.imaginary - z2.imaginary)
        return res
    
    @staticmethod
    def negate(z):
        res = Complex.mul(Complex(-1,0),z)
        return res

    @staticmethod
    def mul(z1, z2):
        res = Complex((z1.real * z2.real)-(z1.imaginary * z2.imaginary), (z1.real * z2.imaginary) + (z2.real * z1.imaginary))
        return res

    @staticmethod
    def div(z1, z2):
        den = (z2.real**2)+(z2.imaginary**2)
        if den == 0: raise ZeroDivisionError('División Compleja entre 0')
        real_part = ((z1.real * z2.real)+(z1.imaginary * z2.imaginary))/den
        imaginary_part = ((z1.imaginary * z2.real)- (z1.real * z2.imaginary))/den
        res = Complex(real_part, imaginary_part)
        return res

    @staticmethod
    def e_z(z):
        res = Complex((math.exp(z.real) * math.cos(z.imaginary)) , (math.exp(z.real) * math.sin(z.imaginary)))
        return res

    @staticmethod
    def mod(z):
        res = Complex( math.sqrt((z.real**2) + (z.imaginary**2)), 0)
        return res

    @staticmethod
    def arg(z):
        if z.real == 0:
            if z.imaginary < 0:
                res = 3 * math.pi / 2
            elif z.imaginary == 0:
                res = 0
            else:
                res = math.pi / 2
        else:
            res = math.atan(z.imaginary / z.real)
        res = Complex(res, 0)
        return res

    @staticmethod
    def sin(z):
        res = Complex.sub(Complex.div(Complex.e_z(Complex.mul(Complex(0,1), z)), Complex.mul(Complex(2,0), Complex(0,1))), Complex.div(Complex.e_z(Complex.mul(Complex(-1,0),(Complex.mul(Complex(0,1), z)))), Complex.mul(Complex(2,0), Complex(0,1))))
        return res

    @staticmethod
    def cos(z):
        res = Complex.add(Complex.div(Complex.e_z(Complex.mul(Complex(0,1), z)), Complex(2, 0)), Complex.div(Complex.e_z(Complex.mul(Complex(-1,0),(Complex.mul(Complex(0,1), z)))), Complex(2,0)))
        return res

    @staticmethod
    def ln(z):
        res = Complex(math.log(z.real), Complex.arg(z))
        return res


        

@v_args(inline=True)    
class CalculateTree(Transformer):
    # Metodo que recibe una cadena y la transforma en un complejo sin parte imaginaria
    def transform_real(self, parameter):
        res = Complex(float(parameter), 0)
        return res
    
    # Metodo que recibe una cadena y la transforma en un complejo sin parte real
    def transform_imag(self, parameter):
        aux = parameter.strip('i')
        if aux == "":
            res = Complex(0, 1)
        elif aux == "-":
            res = Complex(0, -1)
        else:
            res = Complex(0, float(aux))
        return res

    def op_add(self, z1, z2):
        res = Complex.add(z1, z2)
        return res
        
    def op_sub(self, z1, z2):
        res = Complex.sub(z1, z2)
        return res

    def op_negate(self, z):
        res = Complex.negate(z)
        return res

    def op_mul(self, z1, z2):
        res = Complex.mul(z1, z2)
        return res

    def op_div(self, z1, z2):
        res = Complex.div(z1, z2)
        return res

    def op_root(self, z, r):
        mod_z = math.sqrt((z.real**2)+(z.imaginary**2))
        if z.real == 0:
            if z.imaginary < 0:
                arg_z = 3 * math.pi / 2
            else:
                arg_z = math.pi / 2
        else:
            arg_z = math.atan(z.imaginary / z.real)
        
        z = []

        n = int(r)

        factor = mod_z ** (1/n)

        for k in range(0, n):
            
            real = round(factor * math.cos((arg_z + (2 * math.pi * k))/(n)), 4)
            imaginary = round(factor * math.sin((arg_z + (2 * math.pi * k))/(n)),4)
            z.append(Complex(real, imaginary))

        return z

    def op_power(self, z, n):
        p = int(n)
        z_aux = z
        for k in range(1, p):
            z_aux = Complex.mul(z_aux, z)
        res = z_aux
        return res
    
    def op_e_z(self, z):
        res = Complex.e_z(z)
        return res

    def op_sin(self, z):
        res = Complex.sin(z)
        return res
    
    def op_cos(self, z):
        res = Complex.cos(z)
        return res
    
    def op_tan(self, z):
        res = Complex.div(Complex.sin(z),Complex.cos(z))
        return res
    
    def op_mod(self, z):
        res = Complex.mod(z)
        return res
    
    def op_arg(self, z):
        res = Complex.arg(z)
        return res

    def op_ln(self, z):
        res = Complex.ln(z)
        return res



# Lalr -> Look Ahead Left Right
calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())

calc = calc_parser.parse