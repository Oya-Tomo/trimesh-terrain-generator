import trimesh


def combine_meshes(meshes: list[trimesh.Trimesh]) -> trimesh.Trimesh:
    """
    Combine a list of trimesh objects into a single trimesh object.

    Args:
        meshes (list[trimesh.Trimesh]): List of trimesh objects to combine.

    Returns:
        trimesh.Trimesh: Combined trimesh object.
    """
    if not meshes:
        raise ValueError("The list of meshes is empty.")

    combined_mesh: trimesh.Trimesh = trimesh.util.concatenate(meshes)
    combined_mesh = combined_mesh.process(validate=True)
    return combined_mesh


if __name__ == "__main__":
    import random
    import pyramid
    import boxes_pyramid
    import boxes_cell

    pyramid_terrain = boxes_pyramid.create_boxes_pyramid(
        size=10,
        step_tread=[0.4 for i in range(10)],
        step_heights=[0.15 for i in range(10)],
    )
    depression_terrain = pyramid.create_pyramid_terrain(
        size=10,
        step_tread=[0.4 for i in range(10)],
        step_heights=[-0.2 * i for i in range(11)],
    )
    cell_terrain = boxes_cell.create_cell_terrain(
        size=10,
        cell_heights=[
            [random.randint(0, 10) / 100 for x in range(10)] for y in range(10)
        ],
    )
    rect_terrain = pyramid.create_pyramid_terrain(
        size=10,
        step_tread=[0.4 for i in range(10)],
        step_heights=[0.1 * (i % 2) for i in range(11)],
    )

    meshes = [
        cell_terrain,
        rect_terrain,
        depression_terrain,
        pyramid_terrain,
    ]
    terrain_meshes = []

    rows = 3
    cols = 3

    for y in range(rows):
        for x in range(cols):
            terrain_meshes.append(
                meshes[(y * rows + x) % len(meshes)]
                .copy()
                .apply_translation([x * 10, y * 10, 0])
            )

    combined_mesh = combine_meshes(terrain_meshes)
    combined_mesh.show()
    combined_mesh.export("combined_terrain.stl")
