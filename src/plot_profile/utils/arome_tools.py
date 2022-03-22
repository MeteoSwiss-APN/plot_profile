def coord_2_arome_pts(lat, lon):
    """Convert lat/lon to dy/dx in arome domain 
    Args:
        lat (float)
        lon (float)
    Returns: x,y (int)
    """
    A, B= 121/3, 201/5
    if (5<=lon<=10) and (46<=lat<=49):
        dy, dx = int(round((49-lat)*A)), int(round((lon-5)*B))
        return(dy,dx)
    else:
        print('Coordonnées lat/lon en dehors du domaine, par défaut Payerne: 46.81291/6.94418')
        return(int(round((49-46.81291)*A)), int(round((6.94418-5)*B)))