# Music Home

Music player server with a web-based user interface.

Run it on a raspberry pi connected to some speakers in your home or office.
Guests can control the music player by connecting with a laptop, tablet,
or smart phone. Further, you can stream your music library remotely.

## Installation on Ubuntu

Last updated for Zesty 17.04.

1. `sudo apt-get install nodejs libgrooveloudness-dev libgroovefingerprinter-dev libgrooveplayer-dev libgroove-dev`
2. Clone this repo and cd to it.
3. `npm run build`
4. `python2 main.py`

## Configuration

When the server starts it will look for `config.json` in the current
directory. If not found it creates one for you with default values.

Use this to set your music library location and other settings.

It is recommended that you generate a self-signed certificate and use that
instead of using the public one bundled with this source code.

### Future additions

* Hot word detection
* Gesture support
* Song recommendation
