class MiException(Exception):
    def __init__(self, lugar_error, detalle="", *args):
        super().__init__(*args)
        self.lugar_error = lugar_error
        self.detalle = detalle


class ReferenciaInvalida(MiException):
    def __str__(self):
        if not self.detalle:
            return """Error de consulta: {0}
        Causa: Referencia Invalida""".format(self.lugar_error)
        else:
            return """Error de consulta: {0}
                  Causa: Referencia Invalida
                  Detalle: {1}""".format(self.lugar_error, self.detalle)


class ArgumentoInvalido(MiException):
    def __str__(self):
        if not self.detalle:
            return """Error de consulta: {0}
        Causa: Argumento Invalido""".format(self.lugar_error)
        else:
            return """Error de consulta: {0}
                  Causa: Argumento Invalido
                  Detalle: {1}""".format(self.lugar_error, self.detalle)
class ErrorDeTipo(MiException):
    def __str__(self):
        if not self.detalle:
            return """Error de consulta: {0}
        Causa: Error de Tipo""".format(self.lugar_error)
        else:
            return """Error de consulta: {0}
                  Causa: Error de Tipo
                  Detalle: {1}""".format(self.lugar_error, self.detalle)
class ErrorMatematico(MiException):
    def __str__(self):
        if not self.detalle:
            return """Error de consulta: {0}
        Causa: Error Matematico""".format(self.lugar_error)
        else:
            return """Error de consulta: {0}
                  Causa: Error Matematico
                  Detalle: {1}""".format(self.lugar_error, self.detalle)
class ImposibleProcesar(MiException):
    def __str__(self):
        if not self.detalle:
            return """Error de consulta: {0}
        Causa: Imposible Procesar""".format(self.lugar_error)
        else:
            return """Error de consulta: {0}
                  Causa: Imposible Procesar
                  Detalle: {1}""".format(self.lugar_error, self.detalle)