# Instagram browser automation experiments

Python prototypes for downloading and uploading Reels with Selenium and Instaloader.

## Status

Experimental, machine-dependent scripts. Browser selectors, login challenges and upload flows can change. This is a learning project, not a supported publishing service.

## Setup

Create and activate a Python virtual environment, then install the existing dependency file:

```sh
python -m pip install -r requrements.txt
```

Install the browser and driver required by the script. `main.py` currently requires editing the Tor Browser executable path and a running SOCKS proxy at localhost:9150.

## Run explicitly

Set these environment variables in your shell; the scripts do not automatically load a .env file:

- `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD`: your own account credentials.
- `REEL_URL`: source URL for `python main.py`.
- `VIDEO_PATH`: absolute local video path for `python post_reel.py` or `python post_reel_phone.py`.

Running an upload script can publish a video. Importing these three modules does not run their examples.
The caption in the examples is currently fixed; the mobile prototype does not reliably apply captions.

`prototipe_1.py` is an alternate interactive download experiment using `REELS_PATH`.

## Security and limitations

Keep credentials, cookies, browser profiles, downloaded media and screenshots outside Git.
Previously committed credentials must be rotated and active sessions reviewed. A source change does not remove earlier Git objects.
No live account operations or end-to-end browser checks were performed for this cleanup.
`test.py` compares two strings; it is not an automated browser test.
