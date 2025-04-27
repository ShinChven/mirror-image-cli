# Mirror Image CLI

A simple command-line tool to mirror image files horizontally or vertically.

[deepwiki](https://deepwiki.com/ShinChven/mirror-image-cli)

## Features

*   Mirror individual image files or all supported images within a directory.
*   Mirror horizontally (default) or vertically.
*   Specify an output directory **name** to be created relative to the original image's location.
*   Specify the output image format.
*   Supported input/output formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`.

## Installation

This package is not available on PyPI. You can install it directly from the GitHub repository.

```bash
pip install git+https://github.com/ShinChven/mirror-image-cli.git
```

```bash
pip install --upgrade git+https://github.com/ShinChven/mirror-image-cli.git
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
*   `-d`, `--output-dir DIRECTORY_NAME`: Specifies the name for a directory where mirrored images will be saved. This directory will be created inside the parent directory of the original image(s).
    *   Example: If processing `path/to/image.jpg` with `-d mirrored`, the output will be saved in `path/to/mirrored/image_h.jpg`.
    *   If not provided, saves alongside the original file(s) with a `_h` (horizontal) or `_v` (vertical) suffix added to the filename.
*   `-t`, `--type TEXT`: Output image type (e.g., `png`, `jpg`, `webp`). If not provided, uses the original image type. Supported types: `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`.
*   `--help`: Show the help message and exit.

**Examples:**

1.  **Mirror a single image horizontally (default):**
    ```bash
    mirror-image path/to/my_image.jpg
    ```
    (Creates `path/to/my_image_h.jpg`)

2.  **Mirror a single image vertically:**
    ```bash
    mirror-image -v path/to/my_image.png
    ```
    (Creates `path/to/my_image_v.png`)

3.  **Mirror all images in a directory horizontally and save to a specific output directory *relative to the source directory*:**
    ```bash
    # If path/to/image_folder/ contains img1.jpg and img2.gif
    mirror-image -d mirrored_output path/to/image_folder/
    ```
    (Creates `path/to/image_folder/mirrored_output/img1_h.jpg` and `path/to/image_folder/mirrored_output/img2_h.gif`. It will *not* process subdirectories.)

4.  **Mirror an image vertically, save to a relative output directory, and convert it to WebP format:**
    ```bash
    mirror-image -v -d webp_versions -t webp photos/photo.jpeg
    ```
    (Creates `photos/webp_versions/photo_v.webp`)

5.  **Mirror all images in a directory vertically, save to a relative output directory, and convert to PNG:**
    ```bash
    # If source_images/ contains pic1.gif and pic2.bmp
    mirror-image -v -d png_output -t png source_images/
    ```
    (Creates `source_images/png_output/pic1_v.png` and `source_images/png_output/pic2_v.png`)

## License

This project is licensed under the [MIT License](LICENSE).
