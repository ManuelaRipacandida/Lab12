from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def readAllrifugi():
        conn = DBConnect.get_connection()
        result = []
        query = "SELECT * FROM rifugio"  # Query per prendere tutti i rifugi
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:  # Creo oggetti rifugio dal DB e li aggiungo alla lista
            rifugio = Rifugio(row["id"],
                              row["nome"],
                              row["localita"],
                              row["altitudine"],
                              row["capienza"],
                              row["aperto"])
            result.append(rifugio)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def readAllConnessioniFinoAnno(year):
        conn = DBConnect.get_connection()
        result = []
        query = ("""SELECT * 
                 FROM connessione
                 WHERE anno<=%s""")  # Prendo tutte le connessini fino ad un certo anno

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (year,))  # Parametro con (, )
        for row in cursor:
            connessione = Connessione(row["id"],
                                      row["id_rifugio1"],
                                      row["id_rifugio2"],
                                      row["distanza"],
                                      row["difficolta"],
                                      row["durata"],
                                      row["anno"],
                                      )
            result.append(connessione)

        cursor.close()
        conn.close()
        return result  # Lista di oggetti connessione filtrati per anno
