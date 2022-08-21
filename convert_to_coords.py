import waze_classes as waze


def get_coords_lon_lat(start_stop, end_stop):
    route = waze.WazeRouteCalculator(str(start_stop[0] + ' ' + start_stop[1]),
                                     str(end_stop[0] + ' ' + end_stop[1]))
    answer = route.calc_route_info()
    return answer


def calc_rout_path(bus_stops):
    time_and_distance = (0, 0)
    for i in range(len(bus_stops) - 1):
        time_and_distance += get_coords_lon_lat(bus_stops[i], bus_stops[i + 1])
    return time_and_distance


if __name__ == '__main__':
    get_coords_lon_lat(start_stop='בית ספר אלונים/הבנים' + ' ' + 'פרדס חנה כרכור',
                       end_stop='דרך למרחב/המעלה' + ' ' + 'פרדס חנה כרכור')
