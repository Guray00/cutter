# cutter

**Cutter** is a command-line tool that allows you to cut a video file or a folder containing multiple video files based on silence and noise level. It is based on [Remsi](https://github.com/bambax/Remsi), a library for audio and video processing. The tool is implemented in Python and can be used on Windows, Linux, and Mac OS.

## Installation

Pre builds are available in the [releases](https://github.com/Guray00/cutter/releases).

Before installing cutter (if you don't use the pre build version), you must have installed **ffmpeg** and **python**. Clone the repository from GitHub and install the required dependencies using pip:

```bash
git clone https://github.com/guray00/cutter.git
cd cutter
pip install -r requirements.txt
```


## Usage

```text
usage: cutter.exe [-h] [-d D] [-n N] [-fr FR] [-x X] [-vfr] [--keep-cfr] [--preview] path

positional arguments:
  path        the path of the video or the folder (for many videos) to cut

options:
  -h, --help  show this help message and exit
  -d D        duration of silence in seconds (default: 0.8)
  -n N        noise level in dB (default: -40)
  -fr FR      output video frame rate
  -x X        Speed of the video
  -vfr        variable frame rate on output (if -fr is given, it indicates the max number of duplicates frames per second)
  --keep-cfr  keeps Constant Frame Rate version of the file for future editing.
  --preview   makes a preview of 180 seconds
```

## Examples

To cut a single video file with a silence duration of 1 second and a noise level of -30 dB:

```bash
cutter.exe -d 1 -n -30 path/to/video.mp4
```

To cut all the video files in a folder with a silence duration of 0.5 seconds and a noise level of -45 dB, and create a preview of each file:

```bash
cutter.exe --preview -d 0.5 -n -45 path/to/folder
```

To cut a single video file with a silence duration of 1 second and a noise level of -30 dB, and keep the Constant Frame Rate version of the file:

```bash
cutter.exe -d 1 -n -30 --keep-cfr path/to/video.mp4
```

## Contributions

Contributions are welcome! If you want to contribute to the project, please fork the repository and create a pull request.

## License

_To be defined._
