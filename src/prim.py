def rect_coord_to_face(
    c1: int,
    c2: int,
    c3: int,
    c4: int,
) -> list[list[int]]:
    """
    split rect verts to two triangle faces
    input verts must be sorted in counterclockwise order.
    """
    return [[c1, c2, c3], [c1, c3, c4]]
