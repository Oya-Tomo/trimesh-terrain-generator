import trimesh

from prim import rect_coord_to_face


def create_cell_terrain(
    size: float = 10.0,
    cell_heights: list[list[float]] = [[0.0] * 5] * 5,
    bottom_thickness: float = 1.0,
):
    rows = len(cell_heights)
    cols = len(cell_heights[0])
    col_size = size / cols
    row_size = size / rows
    bottom_height = min([min(row) for row in cell_heights]) - bottom_thickness

    verts = []
    faces = []
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            x = c * col_size
            y = r * row_size
            z = cell_heights[r][c]
            verts.extend(
                [
                    [x, y, z],
                    [x + col_size, y, z],
                    [x + col_size, y + row_size, z],
                    [x, y + row_size, z],
                    [x, y, bottom_height],
                    [x + col_size, y, bottom_height],
                    [x + col_size, y + row_size, bottom_height],
                    [x, y + row_size, bottom_height],
                ]
            )
            c1 = i * 8
            c2 = c1 + 1
            c3 = c1 + 2
            c4 = c1 + 3
            c5 = c1 + 4
            c6 = c1 + 5
            c7 = c1 + 6
            c8 = c1 + 7
            faces.extend(
                [
                    *(rect_coord_to_face(c1, c2, c3, c4)),
                    *(rect_coord_to_face(c8, c7, c6, c5)),
                    *(rect_coord_to_face(c1, c5, c6, c2)),
                    *(rect_coord_to_face(c2, c6, c7, c3)),
                    *(rect_coord_to_face(c3, c7, c8, c4)),
                    *(rect_coord_to_face(c4, c8, c5, c1)),
                ]
            )
    return trimesh.Trimesh(vertices=verts, faces=faces, process=False)


if __name__ == "__main__":
    import random

    heights = [[random.uniform(0, 0.1) for _ in range(20)] for _ in range(20)]
    terrain = create_cell_terrain(cell_heights=heights)
    terrain.show()
    terrain.export("cell_terrain.stl")
