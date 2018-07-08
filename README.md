# Hershel

Hershel is a CLI patcher for NDS ROMs. Written in Python, it aims to run on a
vast array of OSes, while using OpenPatch's human-readable patch format for the
purpose of clarity and ease of customization.

-----

## Requirements

To run Hershel, you'll need **Python 3.5** or greater.

To patch a ROM, you'll need its _original_ `.nds` file and an applicable patch.

-----

## Installation

No installation is needed: downloading this repository's `.zip` and unpacking
it to your preferred location will do.

-----

## Usage

Running:

    python hershel.py -h

Will provide a very brief usage summary:

    usage: hershel.py [-h] [-o OUTPUT | -i] [-c CRC32] input patch
    
    NDS ROM patcher which supports OpenPatch's patch format.
    
    positional arguments:
      input                 the ROM to patch
      patch                 the patch or database where the patch can be found
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            the path where to put the patched ROM
      -i, --in-place        apply the patch to the input file itself
      -c CRC32, --crc32 CRC32
                            force the patch for the ROM matching this CRC-32 to be
                            used
-----

## Command-line arguments

### Mandatory

`input`: this is the path to the `.nds` file you wish to patch;

`patch`: this is the path to the `.txt` file containing the patch you wish to
apply. The file can contain either a patch specific to the input ROM, or be a
database containing patches for different ROMs: in the latter case, Hershel
will automatically search the database, stopping at the first valid patch.

### Optional

Note: `-o/--output` and `-i/--in-place` are mutually exclusive.

`-o/--output`: this is the path and file name you wish the patched ROM to be
saved in. If not specified, it will default to `[input_name] (Patched).nds`;

`-i/--in-place`: tells Hershel to patch the input file itself, rather than a
copy of it. Saves time since it skips the copy operation. Disabled by default;

`-c/--crc32`: since a ROM's CRC-32 might differ from the one in the patch file,
Hershel could be unable to find an applicable patch. If you think your ROM to
be patchable, manually enter the CRC-32 found inside the patch to make Hershel
use said patch. _A valid CRC-32 is made of hex numbers and of length 8._

-----

## Sample runs

Three runs follow. The output has not been reported here.

### Minimal run

In this run, only the two mandatory arguments have been provided.

Starting files:
 - `rom.nds` (original ROM);
 - `patch.txt` (patch).

Command:

    python hershel.py rom.nds patch.txt

Resulting files:
 - `rom.nds` (original ROM);
 - `patch.txt` (patch);
 - `rom (Patched).nds` (patched ROM).

### Manually specifying the output path

In this run, we specify an output file name by hand with `-o`.

Starting files:
 - `rom.nds` (original ROM);
 - `patch.txt` (patch);

Command:

    python hershel.py rom.nds patch.txt -o patched-rom.nds

Resulting files:
 - `rom.nds` (original ROM);
 - `patch.txt` (patch);
 - `patched-rom.nds` (patched ROM).

### Overwriting the original ROM

Here we choose to modify the original ROM directly, skipping the creation of a
copy with `-i`. _Note that the original ROM will be lost._

Starting files:
 - `rom.nds` (original ROM);
 - `patch.txt` (patch);

Command:

    python hershel.py rom.nds patch.txt -i

Resulting files:
 - `rom.nds` (patched ROM);
 - `patch.txt` (patch).

-----

## Contributing

Before contributing, ensure that your code runs without errors and analyze it
with `pycodestyle`. If no errors or warnings are emitted, feel free to open a
pull request.

-----

## License

This project is licensed under the terms of the BSD 3-Clause license. See the
[LICENSE](LICENSE) file for details.

-----

## Acknowledgements

This project has been inspired by [nds-rom-patcher](https://github.com/al3xtjames/nds-rom-patcher) by [al3xtjames](https://github.com/al3xtjames).
