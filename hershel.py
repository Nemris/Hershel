"""NDS ROM patcher."""

__author__ = "Death Mask Salesman"
__copyright__ = "Copyright 2018, Death Mask Salesman"
__license__ = "BSD-3-Clause"
__version__ = "0.1"

import argparse
import binascii
import os
import re
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser(
        description="NDS ROM patcher which supports OpenPatch's patch format."
)
out_type = ap.add_mutually_exclusive_group()

ap.add_argument(
        "input",
        type=str,
        help="the ROM to patch"
)
ap.add_argument(
        "patch",
        type=str,
        help="the patch or database where the patch can be found"
)

out_type.add_argument(
        "-o",
        "--output",
        type=str,
        help="the path where to put the patched ROM"
)
out_type.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        default=False,
        help="apply the patch to the input file itself"
)

ap.add_argument(
        "-c",
        "--crc32",
        type=str,
        help="force the patch for the ROM matching this CRC-32 to be used"
)


def exit_fatal(msg):
    """Prints an error message and exits with status 1."""

    print("[ F ] {0}".format(msg))
    exit(1)


def parse_crc32(crc32):
    """Checks for crc32 validity and makes it an uppercase str."""

    # If crc32 comes from the patch file, perform int to str conversion
    if isinstance(crc32, int):
        crc32 = hex(crc32).lstrip("0x")

    # Make crc32 uppercase, empty it if isn't valid hex of len 8
    if isinstance(crc32, str):
        if len(crc32) != 8:
            crc32 = ""
        else:
            crc32 = crc32.upper()

            try:
                crc32 = crc32.upper()
                int(crc32, 16)
            except ValueError:
                crc32 = ""

    return crc32


def get_patch_data(patch, crc32):
    """Searches patch for patch data matching the ROM's CRC-32."""

    patch_data = {}

    with open(patch, "r") as f:
        patch_available = False

        for line in f.readlines():
            # If the CRC-32 we have is present, start reading the patch
            if crc32 in line:
                patch_available = True
                continue

            # If we see the magic Unicode char, split line,
            if patch_available:
                if "→" in line:
                    tmp = re.split(":|→", line.rstrip().replace(" ", ""))

                    # convert offset to an int and the rest to bytes
                    # and store everything in a dict
                    patch_data[int(tmp[0], 16)] = (bytes.fromhex(tmp[1]),
                                                   bytes.fromhex(tmp[2]))
                else:
                    # If no magic char, line isn't part of the patch
                    break

    return patch_data


def patch_rom(src, dst, patch_data):
    """Patch src with the contents of patch_data, saving to dst."""

    succeeded = True

    # If we can work on a copy, copy the ROM so we can work on it
    if src != dst:
        shutil.copyfile(src, dst)

    with open(dst, "r+b") as f:
        for offset in patch_data:
            # Unpack the tuple stored in patch_data
            expected = patch_data.get(offset)[0]
            new = patch_data.get(offset)[1]

            # Store the bytes we need for comparison
            f.seek(offset, 0)
            old_value = f.read(len(expected))

            if old_value == expected:
                f.seek(-len(expected), 1)
                f.write(new)

                print("[ I ] At 0x{0:08x}: {1} -> {2}".format(offset,
                                                              expected.hex(),
                                                              new.hex()))
            else:
                succeeded = False
                break

    # Cleanup in case of failure; remove dst only if it's a copy
    if src != dst and not succeeded:
        os.unlink(dst)

    return succeeded


def main(src, patch, dst, inplace, crc32):
    """Core of Hershel."""

    # Normalize paths, handle output type
    src = os.path.normpath(src)
    patch = os.path.normpath(patch)

    if dst:
        dst = os.path.normpath(dst)
    elif inplace:
        dst = src
    else:
        dst = "{0} (Patched).nds".format(src.rstrip(".nds"))

    # Routine checks
    if not os.path.exists(src):
        exit_fatal("The ROM does not exist.")

    if not os.path.exists(patch):
        exit_fatal("The patch file does not exist.")

    if not crc32:
        print("[ I ] Computing ROM's CRC-32...")
        with open(src, "rb") as f:
            crc32 = binascii.crc32(f.read())

    crc32 = parse_crc32(crc32)

    if not crc32:
        exit_fatal("Malformed CRC-32.")

    print()

    # Retrieve patch data for our CRC-32, abort if no patch
    patch_data = get_patch_data(patch, crc32)
    if not patch_data:
        exit_fatal("No patch available for the target ROM.")

    # Attempt to patch the ROM and check the result
    print("[ I ] Patching...")

    if not patch_rom(src, dst, patch_data):
        # We blame the patch for certain as we assume CRC-32 not to lie
        print()
        exit_fatal("Patch is corrupted or otherwise incorrect.")

    print("\n[ I ] Patching completed. The new ROM is at \"{0}\".".format(dst))


if __name__ == "__main__":
    args = ap.parse_args()

    main(
            src=args.input,
            patch=args.patch,
            dst=args.output,
            inplace=args.in_place,
            crc32=args.crc32
    )
