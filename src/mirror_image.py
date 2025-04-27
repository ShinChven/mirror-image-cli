import typer
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import sys
from typing_extensions import Annotated
from typing import Optional

app = typer.Typer(help="Mirror images horizontally (default) or vertically.")

SUPPORTED_INPUT_TYPES = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
SUPPORTED_OUTPUT_TYPES = {'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp'}

def process_image(
    image_path: Path,
    output_dir_name: Optional[str], # Changed type to str
    vertical: bool,
    output_type: Optional[str]
):
    """Opens, mirrors, and saves a single image."""
    try:
        # Ensure we are working with an absolute path to reliably get the parent
        image_path = image_path.resolve()
        img = Image.open(image_path)
    except UnidentifiedImageError:
        typer.echo(f"Skipping non-image file: {image_path.name}", err=True)
        return
    except Exception as e:
        typer.echo(f"Error opening image {image_path.name}: {e}", err=True)
        return

    mirror_mode = Image.FLIP_TOP_BOTTOM if vertical else Image.FLIP_LEFT_RIGHT
    suffix = "_v" if vertical else "_h"
    mirrored_img = img.transpose(mirror_mode)

    # Determine output details
    output_stem = f"{image_path.stem}{suffix}"
    save_format = output_type if output_type else image_path.suffix[1:].lower()
    if save_format == 'jpg': # Pillow uses 'jpeg' format name
        save_format = 'jpeg'
    output_ext = f".{output_type}" if output_type else image_path.suffix

    if save_format not in SUPPORTED_OUTPUT_TYPES and save_format != 'jpeg': # Allow jpg alias
         typer.echo(f"Error: Unsupported output type '{save_format}' for {image_path.name}. Using original type '{image_path.suffix[1:].lower()}'.", err=True)
         output_ext = image_path.suffix
         save_format = image_path.suffix[1:].lower()
         if save_format == 'jpg':
             save_format = 'jpeg'


    # Determine output path
    if output_dir_name:
        # Create the output dir relative to the original image's parent dir using the provided name string
        target_parent_dir = image_path.parent / output_dir_name
        target_parent_dir.mkdir(parents=True, exist_ok=True)
        output_path = target_parent_dir / f"{output_stem}{output_ext}"
    else: # No output_dir provided, save alongside original
        output_path = image_path.parent / f"{output_stem}{output_ext}"

    # Save the image
    try:
        # Handle potential saving issues like transparency in JPEG
        save_kwargs = {}
        if save_format.lower() == 'jpeg' and mirrored_img.mode in ('RGBA', 'LA', 'P'):
             # Convert to RGB if saving as JPEG and image has alpha channel or is palette-based
             typer.echo(f"Info: Converting image {image_path.name} to RGB for JPEG output.", err=True)
             mirrored_img = mirrored_img.convert('RGB')
        elif save_format.lower() == 'bmp' and mirrored_img.mode == 'P':
             # Convert palette-based images for BMP saving if needed
             mirrored_img = mirrored_img.convert('RGB')


        mirrored_img.save(output_path, format=save_format.upper(), **save_kwargs)
        typer.echo(f"Processed '{image_path.resolve()}' -> '{output_path.resolve()}'")
    except Exception as e:
        typer.echo(f"Error saving image {output_path.name}: {e}", err=True)
    finally:
        img.close() # Close the original image file handle


@app.command()
def main(
    input_path: Annotated[Path, typer.Argument(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to the image file or directory containing images." # Removed recursive mention
    )],
    vertical: Annotated[bool, typer.Option("--vertical", "-v", help="Mirror vertically instead of horizontally.")] = False,
    output_dir: Annotated[Optional[str], typer.Option( # Changed type to Optional[str]
        "--output-dir", "-d",
        # Updated help text to reflect relative creation
        help="Directory name to create within the original image's parent directory to save mirrored images. If not provided, saves alongside original.",
        file_okay=False, # Should represent a directory name
        dir_okay=False, # It's just a name now, not necessarily an existing dir
        writable=False, # Cannot check writability of a non-existent relative name
        resolve_path=False, # Do not resolve this path relative to CWD
    )] = None,
    output_type: Annotated[Optional[str], typer.Option(
        "--type", "-t",
        help=f"Output image type ({', '.join(SUPPORTED_OUTPUT_TYPES)}). If not provided, uses original type."
    )] = None,
):
    """
    Mirrors an image or all images in a directory either horizontally (default) or vertically.
    # Removed recursive mention from docstring
    """
    if output_type and output_type.lower() not in SUPPORTED_OUTPUT_TYPES:
        typer.echo(f"Error: Unsupported output type '{output_type}'. Supported types are: {', '.join(SUPPORTED_OUTPUT_TYPES)}", err=True)
        raise typer.Exit(code=1)

    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED_INPUT_TYPES:
            typer.echo(f"Error: Input file '{input_path.name}' is not a supported image type ({', '.join(SUPPORTED_INPUT_TYPES)}).", err=True)
            raise typer.Exit(code=1)
        process_image(input_path, output_dir, vertical, output_type)
    elif input_path.is_dir():
        typer.echo(f"Processing images in directory: {input_path}") # Removed "(recursively)"
        processed_count = 0
        # Use iterdir for non-recursive search
        for item in input_path.iterdir():
            if item.is_file() and item.suffix.lower() in SUPPORTED_INPUT_TYPES:
                process_image(item, output_dir, vertical, output_type)
                processed_count += 1
        if processed_count == 0:
             typer.echo("No supported image files found in the directory.") # Removed "or its subdirectories"
        else:
            typer.echo(f"Finished processing {processed_count} image(s).")

if __name__ == "__main__":
    app()
