import unittest
from comandos_basicos import *
from comandos_datos import *
from Consultas_numericas import *
from Comandos_booleanos import *
import Exception as myerror
from main import traducir

inputs = [12, 12.5, "hola", "este esta", [i for i in range(11)], [2*i for i
                                                                  in
                                                                  range(11)]]
data = {"este esta": [i for i in range(11)]}

class Test(unittest.TestCase):
    def test_traducir(self):
        self.assertEqual(traducir(["asignar", "x", 3 ]), None)
        self.assertTrue(traducir(["comparar", 1, "<", 2]))
        self.assertEqual(traducir(["PROM", inputs[4]]),
                                  sum(inputs[4])/len(inputs[4]))
        self.assertTrue(traducir(["DESV", inputs[4]])-3.31662479 <= 0.00001)
        self.assertTrue(traducir(["VAR",
                                  inputs[4]]) - (3.31662479)**2 <= 0.00001)
        self.assertEqual(traducir(["MEDIAN", inputs[4]]), 5)
        self.assertTrue(traducir(["comparar_columna", inputs[4], "<", "PROM",
                                  inputs[5]]))
        self.assertIsInstance(traducir(["crear_funcion", "normal", 0, 0.5]),
                              type((i for i in range(10))))


    def test_desv(self):
        self.assertTrue(desv(inputs[4]) - 3.31662479 <= 0.00001)
        self.assertRaises(myerror.ArgumentoInvalido, desv, *inputs)
        self.assertRaises(myerror.ErrorMatematico, desv, [])
if __name__ == "__main__":
    unittest.main()
