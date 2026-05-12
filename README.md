# Edge Rewards Automation

Automates Bing searches in Microsoft Edge with customizable time intervals for Microsoft Rewards points.

## Features

- 🔍 Automated Bing searches with predefined queries
- ⏱️ Configurable time intervals between searches (default: 3 seconds)
- 🎲 Random variation in timing to appear more human-like
- 📊 Progress tracking and summary statistics
- 🔧 Easy customization of search queries

## Prerequisites

- Python 3.7 or higher
- Microsoft Edge browser installed
- Microsoft Edge WebDriver (automatically managed by Selenium)

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script with default settings (30 searches, 3-second intervals):

```bash
python edge_rewards_automation.py
```

### Customization

Edit the script to customize:

1. **Number of searches**: Modify `NUM_SEARCHES` variable
2. **Time interval**: Modify `INTERVAL` variable
3. **Search queries**: Edit the `SEARCH_QUERIES` list

Example:
```python
NUM_SEARCHES = 40  # Perform 40 searches
INTERVAL = 5       # Wait 5 seconds between searches
```

### Add Your Own Search Queries

Edit the `SEARCH_QUERIES` list in the script:

```python
SEARCH_QUERIES = [
    "your custom query 1",
    "your custom query 2",
    "your custom query 3",
    # Add more...
]
```

## Configuration Options

- **Headless mode**: Uncomment the headless option in `setup_edge_driver()` to run without visible browser
- **Randomization**: The script adds random variation (±0.5s) to make searches appear more natural

## Notes

⚠️ **Important**: 
- Use responsibly and in accordance with Microsoft Rewards terms of service
- This script is for educational purposes
- Microsoft Rewards has daily limits for search points
- Don't run excessively to avoid potential account issues

## Troubleshooting

**Browser doesn't open:**
- Ensure Microsoft Edge is installed
- Selenium will automatically download the appropriate Edge WebDriver

**Searches fail:**
- Check your internet connection
- Ensure Bing.com is accessible
- Try increasing wait times in the script

**WebDriver errors:**
- Update Selenium: `pip install --upgrade selenium`
- Clear browser cache

## License

MIT License - Feel free to modify and use as needed.
