# Voxel Viewer

A real-time 3D-like terrain renderer built with Python using the **Voxel Space algorithm** which transforms 2D height and colour maps into an explorable (practically a 2.5D)
 landscape without relying on traditional 3D rendering engines.
<br>
[Try the web demo](http://localhost:8000)

## Features

- **Voxel Space Rendering:** Distance-based terrain projection, rendered column by column.
- **Height and Colour Maps:** Separate images define terrain elevation and surface colours.
- **Real-time Exploration:** Freely navigate and explore the terrain.

<img width="800" height="450" alt="VideoProject28-ezgif com-optimize" src="https://github.com/user-attachments/assets/25884b0b-e1dc-48ee-8f6d-99a3cffca2d8" />

## How It Works

The terrain is generated from two images:

- `C1W.png` – Colour map defining the surface colour of each location.
- `D1.png` – Grayscale height map defining terrain elevation.

These maps are taken from the game [comanche](https://en.wikipedia.org/wiki/Comanche_(video_game_series)).
The height map is resized to 1024 × 1024 pixels, with the colour map providing corresponding terrain colours with light already shaded in.

For each vertical screen column, the renderer samples terrain points at progressively increasing distances from the camera. Their screen positions are calculated using terrain elevation, camera height, viewing angle and distance.

A horizon buffer prevents terrain hidden behind previously rendered surfaces from being drawn again, producing the final 3D-like perspective.


## Installation

Install the required dependencies:

```bash
pip install pygame numpy opencv-python numba
```

Project structure:

```text
VoxelSpace/
├── index.html
├── main.py
├── C1W.png
├── D1.png
└── walksound.wav
```

Run the project:

```bash
python main.py
```

## Performance

The computationally intensive rendering function uses Numba's `njit` with parallel execution and fast-math optimisations.

Rendering is performed at 1920 × 1080 resolution, with terrain samples evaluated at increasing distances from the camera.

## Future Improvements

- Procedural terrain generation using noise.
- Improved terrain shading and dynamic lighting.
- Additional terrain features such as roads, mountains, islands and structures.
- Faster rendering on browser
