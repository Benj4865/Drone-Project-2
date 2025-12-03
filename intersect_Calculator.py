from shapely.geometry import Polygon, LineString, Point
from search_leg import Search_leg
import Launch_Parameters


def calc_intersec(beach_polygon, leg):

    beach = Polygon(beach_polygon)
    start_point = Point(leg.start_pos)
    end_point = Point(leg.end_pos)

    if beach.contains(start_point) == False and beach.contains(end_point) == False:
        # both starting and end posistion of leg is outside of beach polygon and can therefore
        # we presume that the leg does not cross the beach. Edge cases may circumvent above logic,
        # #but that is beyond scope of this project
        return leg

    elif beach.contains(start_point) == True and beach.contains(end_point) == False:
        int_sec_index = 1
        leg.is_active = True

    elif beach.contains(start_point) == False and beach.contains(end_point) == True:
        int_sec_index = 0
        leg.is_active = True

    else:
        leg.is_active = False
        return leg



    leg_points = (start_point,end_point)
    line = LineString(leg_points)
    # Use Shapely to check for intersection
    inter = beach.intersection(line)


    if inter.is_empty:
        print("No intersection")

    else:
        print("Intersection geometry type:", inter.geom_type)

        #if inter.geom_type == "Point":
        #    # Single intersection point
        #    print("Point:", inter.x, inter.y)
        #   leg.intersect_point = (inter.x, inter.y)

        #elif inter.geom_type == "MultiPoint":
        #    # Several intersection points
        #    for p in inter.geoms:
        #        print("Point:", p.x, p.y)
        #        leg.intersect_point = (p.x, p.y)

        if inter.geom_type in ("LineString", "MultiLineString"):
            # The line overlaps with polygon edge(s)
            # You can sample endpoints or points along it, for example:
            for g in getattr(inter, "geoms", [inter]):
                coords = list(g.coords)
                print("Overlapping segment endpoints:", coords[0], "to", coords[-1])

        if int_sec_index == 0:
            leg.intersect_point = coords[0]
        elif int_sec_index == 1:
            leg.intersect_point = coords[-1]

    return leg
