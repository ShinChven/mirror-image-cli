# Mirror Image CLI

A simple command-line tool to mirror image files horizontally or vertically.

[deepwiki](https://deepwiki.com/ShinChven/mirror-image-cli)

## Features

*   Mirror individual image files or all supported images within a directory.
*   Mirror horizontally (default) or vertically.
*   Specify an output directory for mirrored images.
*   Specify the output image format.
*   Supported input/output formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`.

## Installation

This package is not available on PyPI. You can install it directly from the GitHub repository.

**Option 1: Clone and Install Locally**

```bash
# Clone the repository
git clone https://github.com/ShinChven/mirror-image-cli.git

# Navigate into the project directory
cd mirror-image-cli

# Install the package using pip
pip install .
```

**Option 2: Install Directly from GitHub URL**

```bash
pip install git+https://github.com/ShinChven/mirror-image-cli.git
```

## Usage

The command-line tool is installed as `mirror-image`.

```bash
mirror-image [OPTIONS] INPUT_PATH
```

**Arguments:**

*   `INPUT_PATH`: Path to the image file or a directory containing images. [required]

**Options:**

*   `-v`, `--vertical`: Mirror vertically instead of horizontally. [default: False]
*   `-d`, `--output-dir DIRECTORY`: Directory to save mirrored images. If not provided, saves alongside the original file(s) with a `_h` (horizontal) or `_v` (vertical) suffix added to the filename.
*   `-t`, `--type TEXT`: Output image type (e.g., `png`, `jpg`, `webp`). If not provided, uses the original image type. Supported types: `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`.
*   `--help`: Show the help message and exit.

**Examples:**

1.  **Mirror a single image horizontally (default):**
    ```bash
    mirror-image my_image.jpg
    ```
    (Creates `my_image_h.jpg` in the same directory)

2.  **Mirror a single image vertically:**
    ```bash
    mirror-image -v my_image.png
    ```
    (Creates `my_image_v.png` in the same directory)

3.  **Mirror all images in a directory horizontally and save to a specific output directory:**
    ```bash
    mirror-image -d ./mirrored_images path/to/image_folder/
    ```
    (Creates horizontally mirrored images in the `./mirrored_images` directory)

4.  **Mirror an image vertically and convert it to WebP format:**
    ```bash
    mirror-image -v -t webp photo.jpeg
    ```
    (Creates `photo_v.webp` in the same directory)

5.  **Mirror all images in a directory vertically, save to an output directory, and convert to PNG:**
    ```bash
    mirror-image -v -d ./output -t png source_images/
    ```
    (Creates vertically mirrored PNG images in the `./output` directory)

## License

This project is licensed under the [MIT License](LICENSE).
