from mazegenerator import MazeGenerator


def generate_maze(width: int, height: int) -> list[list[int]]:
    """Generate a Pac-Man compatible maze with the assigned package."""
    generator = MazeGenerator(size=(width, height), perfect=False)
    generator.generate()
    maze: list[list[int]] = generator.maze
    return maze
