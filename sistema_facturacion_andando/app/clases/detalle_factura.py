class DetalleFactura:
    def __init__(self, idDetalle=None, producto=None, cantidad=0, precioUnitario=0.0):
        self.idDetalle = idDetalle
        self.producto = producto
        self.cantidad = cantidad
        self.precioUnitario = precioUnitario
        self.subtotal = self.calcularSubtotal()

    def calcularSubtotal(self):
        return self.cantidad * self.precioUnitario

    def actualizarCantidad(self, nuevaCantidad):
        self.cantidad = nuevaCantidad
        self.subtotal = self.calcularSubtotal()
