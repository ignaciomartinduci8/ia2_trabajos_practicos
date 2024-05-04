
class Motor:

    def inference(self, NOCHE, DIA, ZN, ZZ, ZP, ZCALN, ZCALZ,ZCALP, ZENFN, ZENFZ, ZENFP, TPRED_BAJA, TPRED_ALTA):

        cerrar1 = min(DIA, ZP)
        centro1 = min(DIA, ZZ)
        abrir1 = min(DIA, ZN)

        cerrar2 = min(NOCHE, TPRED_ALTA, ZENFP)
        centro2 = min(NOCHE, TPRED_ALTA, ZENFZ)
        abrir2 = min(NOCHE, TPRED_ALTA, ZENFN)

        cerrar3 = min(NOCHE, TPRED_BAJA, ZCALP)
        centro3 = min(NOCHE, TPRED_BAJA, ZCALZ)
        abrir3 = min(NOCHE, TPRED_BAJA, ZCALN)

        cerrar = max(cerrar1, cerrar2, cerrar3)
        centro = max(centro1, centro2, centro3)
        abrir = max(abrir1, abrir2, abrir3)

        return [cerrar, centro, abrir]

