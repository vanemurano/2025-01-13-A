from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct c.GeneID, c.Localization, g.Essential
                        from classification c 
                        join genes g on c.GeneID=g.GeneID"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllLocalizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Localization
                        from classification 
                        order by Localization desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result # lista di stringhe localizzazione

    @staticmethod
    def getAllNodesWEssential(localization: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct c.GeneID, c.Localization, g.Essential
                        from classification c 
                        join genes g on c.GeneID=g.GeneID 
                        where c.Localization=%s"""
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append(Classification(**row))
                # tupla classificazione, essential

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(localization: str, idMapC: dict):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select GeneID1, GeneID2
                        from interactions i
                        join classification c1 on c1.GeneID=i.GeneID2 
                        join classification c2 on c2.GeneID=i.GeneID2 
                        where c1.Localization=%s
                        and c2.Localization=c1.Localization
                        and GeneID1!=GeneID2"""
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append((idMapC[row["GeneID1"]], idMapC[row["GeneID2"]]))
                # tupla classificazione, classificazione

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getChromosomes(id: str):
        cnx = DBConnect.get_connection()
        result=0
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Chromosome 
                        from genes 
                        where GeneID=%s"""
            cursor.execute(query, (id,))

            for row in cursor:
                result=int(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result # intero Cromosoma
