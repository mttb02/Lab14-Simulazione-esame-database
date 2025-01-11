from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_chromosomes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT Chromosome as c
                        FROM genes_small.genes
                        WHERE Chromosome != ""
                        ORDER BY Chromosome ASC"""
            cursor.execute(query, )

            for row in cursor:
                result.append(row["c"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_edges():
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT g1.Chromosome as c1, g2.Chromosome as c2, g1.GeneID as gen1, g2.GeneID as gen2, i.Expression_Corr as e
                        FROM genes_small.interactions i, genes_small.genes g1, genes_small.genes g2
                        WHERE i.GeneID1 != i.GeneID2
                        AND i.GeneID1 = g1.GeneID AND i.GeneID2 = g2.GeneID
                        AND g1.Chromosome != g2.Chromosome
                        AND g2.Chromosome > 0
                        AND g1.Chromosome > 0
                        GROUP BY g1.GeneID, g2.GeneID, g1.Chromosome, g2.Chromosome"""
            cursor.execute(query, )

            for row in cursor:

                if (row["c1"], row["c2"]) in result.keys():
                    result[(row["c1"], row["c2"])] = result[(row["c1"], row["c2"])] + row["e"]
                else:
                    result[(row["c1"], row["c2"])] = row["e"]

            cursor.close()
            cnx.close()
        return result
