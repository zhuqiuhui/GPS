import folium
import preprocess.DBUtil
from folium import features


def displayMapId(fromId, toId, DBPath, i):
    """
        display the trajectory from GPS point id from
        fromId to toId in the database
        Args:
            fromId: start GPS point id
            toId: end GPS point id
            i: the i-th table
    """
    conn = preprocess.DBUtil.get_conn(DBPath)
    # find all points
    fetchAllPointSql = 'select id,lat,lon ' + \
                       'from GPS_points_' + str(i) + \
                       ' where id>=' + str(fromId) + \
                       ' and id<=' + str(toId)
    allPointRecords = preprocess.DBUtil.fetchAll(conn, fetchAllPointSql)
    if allPointRecords is None:
        print('fetch point set Fail!')
        return
    preprocess.DBUtil.closeDB(conn)
    """
    records: type list-> [(1, 36.98919, 111.823906666667).....]
    (id, lat, lon)
    id: 0
    lat: 1
    lon: 2
    """
    mapOsm = folium.Map(location=[allPointRecords[0][1],
                                  allPointRecords[0][2]],
                        zoom_start=18)
    pointLat = []
    pointLon = []
    for item in allPointRecords:
        pointLat.append(item[1])
        pointLon.append(item[2])
        # folium.CircleMarker([item[1], item[2]],
        #                     radius=3,
        #                     popup=str(item[0])).add_to(mapOsm)
    features.PolyLine(
        list(zip(pointLat, pointLon)),
        color='red',
        weight=2,
        popup='trajectory').add_to(mapOsm)
    mapOsm.save('temp/myOsm.html')


def main():
    DBPath = 'DB/GPS.db'
    i = 1
    displayMapId(73927, 87287, DBPath, i)


if __name__ == '__main__':
    main()
