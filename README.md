# fmjpeg2k

JPEG2000 codec for DCMTK based on openjpeg

## Capabilities

DCMTK versions: 3.6.8, 3.6.9, 3.7.0

Transfer syntaxes supported:

| Name                    | Uid          | Can Encode         | Can Decode |
|-------------------------|------|--------|---------|
| JPEG 2000 (Lossless Only) | 1.2.840.10008.1.2.4.90 | Yes | Yes |
| JPEG 2000 | 1.2.840.10008.1.2.4.91 | Yes | Yes |
| JPEG 2000 Part 2 (Lossless Only) | 1.2.840.10008.1.2.4.92 | Yes | Yes |
| JPEG 2000 Part 2 | 1.2.840.10008.1.2.4.93 | Yes | Yes |
| HTJ2K (Lossless Only) | 1.2.840.10008.1.2.4.201 | No | Yes |
| HTJ2K (Lossless RPCL) | 1.2.840.10008.1.2.4.202 | No | Yes |
| HTJ2K | 1.2.840.10008.1.2.4.203 | No | Yes |

Pixel data attributes supported:

| Photometric Interpretation | Samples per Pixel | Planar Configuration | Pixel Representation | Bits Allocated | Bits Stored | High Bit |
|----------------------------|-------------------|----------------------|----------------------|----------------|-------------|----------|
| MONOCHROME1                | 1                 | -                    | 0 or 1               | 8, 16, 32      | 1-32        | 7-31     |
| MONOCHROME2                | 1                 | -                    | 0 or 1               | 8, 16, 32      | 1-32        | 7-31     |
| PALETTE COLOR              | N/A               | N/A                  | N/A                  | N/A            | N/A         | N/A      |
| YBR_RCT (file only)        | 3                 | 0                    | 0                    | 8, 16, 32      | 1-32        | 7-31     |
| YBR_ICT (file only)        | 3                 | 0                    | 0                    | 8, 16, 32      | 1-32        | 7-31     |
| RGB                        | 3                 | 0                    | 0                    | 8, 16, 32      | 1-32        | 7-31     |
| YBR_FULL                   | 3                 | 0                    | 0                    | 8, 16, 32      | 1-32        | 7-31     |

Notes:
1. `YBR_RCT` and `YBR_ICT` used only in encoded form. Automatically converted to `RGB` (or `YBR_FULL`) when decoded.
2. 32 bits allocated supported only in "lossless" mode.
3. Coder and decoder supports any combination of Planar Configuration(s) and Pixel Representation(s). Table above sticks to the DICOM Standard.

Version bumped from "original" 1.0.3 to 1.1.0

## Download
Source https://github.com/StingX84/fmjpeg2k

## Requirements
- CMake https://www.cmake.org/download/
- Conan 2 https://conan.io/downloads

## Useful commands

Prepare environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install conan
conan profile detect
```

Local build:

```sh
conan build . --build=missing --update --options="fmjpeg2k/*:build_apps=True" -s build_type=Debug
```

Test if compiling and conan package works:
```sh
conan create . --build=missing
```

## Original copyrights

## Forked from
Forked from https://github.com/DraconPern/fmjpeg2koj

## Author
Ing-Long Eric Kuo <draconpern@hotmail.com>

## License
Copyright 2015-2021 Ing-Long Eric Kuo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

