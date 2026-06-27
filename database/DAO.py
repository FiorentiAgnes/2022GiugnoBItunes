from database.DB_connect import DBConnect
from model.album import Album
from model.arco import Arco


class DAO():
    @staticmethod
    def getAllNodes(n):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds/1000) as durata
                    from album a, track t
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId, a.Title, a.ArtistId
                    having durata> %s"""

        cursor.execute(query, (n,))

        for row in cursor:
            results.append(Album(row["AlbumId"], row["Title"], row["ArtistId"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(num, idMapA):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select a1.albumid as id1, a2.albumid as id2, (a1.durata+a2.durata ) as peso
                    from (select a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds/1000) as durata
                    from album a, track t
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId, a.Title, a.ArtistId
                    having durata>%s
                    ) a1, 
                    (select a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds/1000) as durata
                    from album a, track t
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId, a.Title, a.ArtistId
                    having durata>%s
                    ) a2
                    where a1.durata <>a2.durata and (a1.durata+a2.durata)>4 * %s and a1.durata < a2.durata """

        cursor.execute(query, (num, num, num))

        for row in cursor:
            results.append(Arco(idMapA[row["id1"]], idMapA[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results