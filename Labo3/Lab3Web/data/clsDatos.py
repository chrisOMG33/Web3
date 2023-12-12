class clsDatos():
    # Constructor function
    def __init__(self, id=None, texto=None, descripcion=None):
        self._id = id
        self._text = texto
        self._descrip = descripcion

    # Local get/set function set
    def _getID(self):
        return self._id

    def _setID(self, id):
        self._id = id

    def _getText(self):
        return self._text

    def _setText(self, texto):
        self._text = texto

    def _getDescrip(self):
        return self._descrip

    def _setDescrip(self, descripcion):
        self._descrip = descripcion

    # Encapsulated property
    ID = property(_getID, _setID)
    Texto = property(_getText, _setText)
    Descripcion = property(_getDescrip, _setDescrip)
