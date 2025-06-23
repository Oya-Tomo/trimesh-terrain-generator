import trimesh


def create_boxes_pyramid(
    size: float = 10.0,
    step_heights: list[float] = [0.5] * 5,
    step_tread: list[float] = [0.5] * 5,
    bottom_thickness: float = 1.0,
) -> trimesh.Trimesh:
    assert len(step_heights) == len(
        step_tread
    ), "Heights and treads must match in length"

    scene = trimesh.Scene()

    scene.add_geometry(
        trimesh.creation.box(bounds=[[0, 0, -bottom_thickness], [size, size, 0]])
    )

    for i in range(len(step_heights)):
        top = sum(step_heights[:i]) + step_heights[i]
        bottom = sum(step_heights[:i])
        min_coord = sum(step_tread[: i + 1])
        max_coord = size - sum(step_tread[: i + 1])
        box = trimesh.creation.box(
            bounds=[
                [min_coord, min_coord, bottom],
                [max_coord, max_coord, top],
            ]
        )
        scene.add_geometry(box)

    mesh: trimesh.Trimesh = scene.to_mesh()
    mesh = mesh.process(validate=True)
    return mesh


if __name__ == "__main__":
    size = 10.0
    step_heights = [0.15 for _ in range(10)]
    step_tread = [0.4 for _ in range(10)]
    bottom_thickness = 1.0

    terrain = create_boxes_pyramid(size, step_heights, step_tread, bottom_thickness)
    terrain.show()
