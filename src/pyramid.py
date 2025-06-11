import trimesh

from prim import rect_coord_to_face


def create_pyramid_terrain(
    size: float = 10.0,
    step_tread: list[float] = [0.8, 0.8, 0.8, 0.8, 0.8],
    step_heights: list[float] = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
    bottom_thickness: float = 1.0,
):

    if len(step_tread) + 1 != len(step_heights):
        raise ValueError("len(step_tread) + 1 != len(step_heights)")

    bottom_coord = size / 2
    bottom_height = min(step_heights) - bottom_thickness
    verts = [
        [bottom_coord, bottom_coord, bottom_height],
        [-bottom_coord, bottom_coord, bottom_height],
        [-bottom_coord, -bottom_coord, bottom_height],
        [bottom_coord, -bottom_coord, bottom_height],
    ]
    faces = []

    for i in range(len(step_tread)):
        ex_coord = size / 2 - sum(step_tread[:i])
        in_coord = size / 2 - sum(step_tread[: i + 1])
        height = step_heights[i]
        verts.extend(
            [
                [ex_coord, ex_coord, height],
                [-ex_coord, ex_coord, height],
                [-ex_coord, -ex_coord, height],
                [ex_coord, -ex_coord, height],
                [in_coord, in_coord, height],
                [-in_coord, in_coord, height],
                [-in_coord, -in_coord, height],
                [in_coord, -in_coord, height],
            ]
        )
    top_coord = size / 2 - sum(step_tread)
    verts.extend(
        [
            [top_coord, top_coord, step_heights[-1]],
            [-top_coord, top_coord, step_heights[-1]],
            [-top_coord, -top_coord, step_heights[-1]],
            [top_coord, -top_coord, step_heights[-1]],
        ]
    )
    faces.extend(
        [
            [0, 2, 1],
            [0, 3, 2],
        ]
    )
    for i in range(len(step_tread) * 2 + 1):
        for j in range(4):
            c1 = i * 4 + j
            c2 = i * 4 + (j + 1) % 4
            c3 = c1 + 4
            c4 = c2 + 4
            faces.extend(rect_coord_to_face(c1, c2, c4, c3))

    c1 = len(verts) - 4
    c2 = len(verts) - 3
    c3 = len(verts) - 2
    c4 = len(verts) - 1
    faces.extend(rect_coord_to_face(c1, c2, c3, c4))

    terrain = trimesh.Trimesh(vertices=verts, faces=faces, process=False)
    terrain.apply_translation([size / 2, size / 2, 0])
    return terrain


if __name__ == "__main__":
    terrain = create_pyramid_terrain(
        size=10,
        step_tread=[0.4 for i in range(10)],
        step_heights=[0.15 * i for i in range(11)],
    )
    terrain.show()
