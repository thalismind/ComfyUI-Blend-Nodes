# ComfyUI Blend Image Nodes

This repository contains a ComfyUI node for blending images using various blending modes.

It allows you to combine two images with different blending techniques, such as normal, multiply, screen, overlay, and
more.

The overlay image can be anchored to the center of the base image, the sides, or the corners. You can also adjust the
opacity of the overlay image.

## Installation

Clone the repository into the ComfyUI `custom_nodes` directory:

```bash
git clone https://github.com/thalismind/ComfyUI-Blend-Nodes.git custom_nodes/ComfyUI-Blend-Nodes
```

## Usage

Please see the example workflows in the `examples` directory for how to use the blend nodes in ComfyUI.

### Available Nodes

- `image/Blend Image`

### Blending Modes

All of the available blending modes from https://pypi.org/project/blend-modes/ are supported, including:

- Soft Light
- Lighten Only
- Dodge
- Addition
- Darken Only
- Multiply
- Hard Light
- Difference
- Subtract
- Grain Extract
- Grain Merge
- Divide
- Overlay
- Normal

## License

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.
