import trimesh


def create_cell_terrain(
    size: float = 10.0,
    cell_heights: list[list[float]] = [[0.0] * 5] * 5,
    bottom_thickness: float = 1.0,
) -> trimesh.Trimesh:
    rows = len(cell_heights)
    cols = len(cell_heights[0])
    col_size = size / cols
    row_size = size / rows
    bottom_height = min([min(row) for row in cell_heights]) - bottom_thickness

    scene = trimesh.Scene()

    for r in range(rows):
        for c in range(cols):
            x = c * col_size
            y = r * row_size
            z = cell_heights[r][c]
            box = trimesh.creation.box(
                bounds=[
                    [x, y, bottom_height],
                    [x + col_size, y + row_size, z],
                ]
            )
            scene.add_geometry(box)
    mesh: trimesh.Trimesh = scene.to_mesh()
    mesh = mesh.process(validate=True)
    return mesh


if __name__ == "__main__":
    import random

    heights = [[random.uniform(0, 0.1) for _ in range(15)] for _ in range(15)]
    terrain = create_cell_terrain(cell_heights=heights)
    terrain.show()
