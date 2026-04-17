# Instagram Bot - Reel Downloader & Uploader

An automated bot for downloading Instagram reels and uploading content to Instagram using Selenium WebDriver.

## Project Overview

This project provides Python-based automation tools for Instagram content management:
- **Download Instagram Reels** - Extract and save reels with metadata preservation
- **Upload Reels** - Automate the process of posting reels to Instagram accounts
- **Browser Automation** - Uses Selenium WebDriver with Chrome and Firefox support
- **Tor Network Support** - Privacy-focused downloading with Tor Browser integration

## Features

### Main Capabilities
- 🎬 Download Instagram reels in high quality
- 📱 Support for both desktop and mobile browser emulation
- 🔒 Optional Tor Browser integration for anonymous downloads
- 🚀 Automated reel uploading with captions
- 🔐 Secure credential handling
- ⏱️ Smart wait times and error handling

## Project Structure

```
inst_bot/
├── main.py                 # Download Instagram reels with Tor Browser
├── post_reel.py           # Upload reels using Chrome browser
├── post_reel_phone.py     # Upload reels with mobile device emulation
├── prototipe_1.py         # Prototype version
├── test.py                # Testing module
├── requrements.txt        # Project dependencies
├── error_screenshot.png   # Error debugging screenshot
└── .gitignore            # Git ignore rules
```

## Key Scripts

### 1. **main.py** - Download Reels with Tor
Downloads Instagram reels anonymously using Tor Browser
```python
scrape_instagram_reel(
    reel_url="https://www.instagram.com/reels/DJq5DRiM1QR/",
    username="your_username",
    password="your_password",
    output_path="instagram_reel.mp4"
)
```

### 2. **post_reel.py** - Upload Reels (Desktop)
Posts reels to Instagram using desktop browser
- Handles login automation
- Supports custom captions
- Includes proper wait times for page loading

### 3. **post_reel_phone.py** - Upload Reels (Mobile Emulation)
Advanced version with mobile device emulation
- Emulates mobile browser environment
- Better compatibility with Instagram's mobile UI
- Includes error handling and screenshot capture

## Dependencies

The project uses the following key libraries:

- **selenium** (v4.33.0) - Browser automation
- **requests** (v2.32.3) - HTTP client
- **instaloader** (v4.14.1) - Instagram content loading
- **webdriver-manager** (v4.0.2) - WebDriver management
- **python-dotenv** (v1.1.0) - Environment variables
- **beautifulsoup4** (v4.13.4) - HTML parsing

Full dependency list in `requrements.txt`

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/a-man-or-a-person/inst_bot.git
cd inst_bot
```

2. **Install dependencies**
```bash
pip install -r requrements.txt
```

3. **Download WebDrivers**
- ChromeDriver for Chrome browser automation
- Firefox/Tor Browser for Tor-based downloads

## Configuration

### System-Specific Paths

Update the following paths in the scripts based on your system:

**For Tor Browser (main.py):**
```python
tor_binary_path = r"A:\Tor_browzer\Tor Browser\Browser\firefox.exe"  # Windows
tor_profile_path = r"A:\Tor_browzer\Tor Browser\Browser\TorBrowser\Data\Browser\Caches\profile.default"  # Windows
```

**For Video Upload (post_reel.py):**
```python
video_path = r"A:\Python Development\Instagramm_bot\bydastann\video.mp4"
```

## Usage Examples

### Download a Reel
```python
from main import scrape_instagram_reel

scrape_instagram_reel(
    reel_url="https://www.instagram.com/reels/YOUR_REEL_ID/",
    username="your_instagram_username",
    password="your_instagram_password",
    output_path="downloaded_reel.mp4"
)
```

### Upload a Reel (Desktop)
```python
from post_reel import post_reel_with_selenium

post_reel_with_selenium(
    video_path="path/to/your/video.mp4",
    username="your_instagram_username",
    password="your_instagram_password",
    caption="Your caption here #hashtag"
)
```

### Upload a Reel (Mobile Emulated)
```python
from post_reel_phone import post_reel_with_selenium

post_reel_with_selenium(
    video_path="path/to/your/video.mp4",
    username="your_instagram_username",
    password="your_instagram_password",
    caption="Your caption here #hashtag"
)
```

## Requirements

- Python 3.7+
- Google Chrome browser (for desktop upload)
- Firefox/Tor Browser (for anonymous download)
- ChromeDriver and GeckoDriver
- Valid Instagram account credentials

## Troubleshooting

### Common Issues

**1. Element Not Found Error**
- Screenshot saved as `error_screenshot.png`
- Check Instagram UI changes
- Update XPath selectors

**2. Timeout Errors**
- Increase wait times in the script
- Check internet connection
- Verify Tor connection status

**3. Login Failures**
- Verify credentials
- Check for Instagram login restrictions
- Disable 2FA temporarily
- Check IP restrictions

**4. WebDriver Issues**
- Ensure WebDriver versions match browser versions
- Update with webdriver-manager
- Clear browser cache

## Security Considerations

⚠️ **Important:**
- Never commit credentials to version control
- Use environment variables for sensitive data
- Consider using .env files with python-dotenv
- Be aware of Instagram's Terms of Service
- Use responsibly and respect rate limits

## Notes

- Tor Browser download: Privacy-focused automation
- Mobile emulation: Better compatibility with Instagram's UI
- Error screenshots: Debugging aid for troubleshooting
- Extended wait times: Necessary for Tor network latency

## Author

Created by: a-man-or-a-person

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This tool is designed for automation purposes. Users are responsible for ensuring their use complies with Instagram's Terms of Service and applicable laws. Unauthorized access or scraping may violate Instagram's policies.
