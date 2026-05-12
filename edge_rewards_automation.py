"""
Edge Rewards Automation Script
Automatically searches predefined strings in Microsoft Edge with time intervals
"""

import time
import webbrowser
import urllib.parse
import random

# List of search queries - customize these as needed
SEARCH_QUERIES = ["best way to stay disciplined daily",
"easy tips to improve concentration",
"methods to wake up early without alarm",
"simple diet tips for healthy lifestyle",
"apps to track study time",
"ways to earn money using skills",
"best free tools for students",
"morning routine for better focus",
"tips to improve handwriting for exams",
"easy recipes for quick dinner"


#python edge_rewards_automation.py
]

def setup_edge_browser():
    """Configure Edge browser for searches"""
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
    return 'edge'

def perform_search(query, is_first_search=False):
    """Perform a single search on Bing by opening Edge with search URL in address bar"""
    try:
        # URL encode the query
        encoded_query = urllib.parse.quote(query)
        
        # Create Bing search URL - this will be typed in the address bar
        # Using the simplest format to ensure Microsoft Rewards counts it
        search_url = f"https://www.bing.com/search?q={encoded_query}&form=QBLH&sp=-1&pq={encoded_query}"
        
        # Open in Edge browser
        if is_first_search:
            # First search opens in a new window
            webbrowser.get('edge').open_new(search_url)
        else:
            # Subsequent searches reuse the same window/tab
            webbrowser.get('edge').open(search_url)
        
        print(f"✓ Searched: {query}")
        return True
        
    except Exception as e:
        print(f"✗ Error searching '{query}': {str(e)}")
        return False

def run_automation(num_searches=30, interval=3):
    """
    Main automation function
    
    Args:
        num_searches: Number of searches to perform
        interval: Time interval between searches in seconds
    """
    print("="*60)
    print("Edge Rewards Automation Script")
    print("="*60)
    print(f"Starting automation with {num_searches} searches")
    print(f"Interval: {interval} seconds between searches\n")
    
    try:
        # Setup Edge browser
        print("Configuring Edge browser...")
        setup_edge_browser()
        print("Browser configured successfully!\n")
        
        # Perform searches
        successful_searches = 0
        
        for i in range(num_searches):
            # Select a random query or cycle through the list
            query_index = i % len(SEARCH_QUERIES)
            query = SEARCH_QUERIES[query_index]
            
            print(f"[{i+1}/{num_searches}] ", end="")
            
            # First search opens new window, others reuse the same tab
            if perform_search(query, is_first_search=(i == 0)):
                successful_searches += 1
            
            # Wait before next search (except for the last one)
            if i < num_searches - 1:
                # Add some randomness to appear more human-like
                wait_time = interval + random.uniform(-0.5, 0.5)
                time.sleep(wait_time)
        
        # Summary
        print("\n" + "="*60)
        print(f"Automation Complete!")
        print(f"Successful searches: {successful_searches}/{num_searches}")
        print("="*60)
        print("\nAll searches opened in Edge browser tabs!")
        print("You can now manually close the browser when done.")
        
    except Exception as e:
        print(f"\n✗ An error occurred: {str(e)}")

if __name__ == "__main__":
    # Configure your automation here
    NUM_SEARCHES = len(SEARCH_QUERIES)  # Search all queries in the list (60 queries)
    INTERVAL = 8       # Seconds between searches (increased to avoid detection)
    
    print("\n⚠️  IMPORTANT REMINDERS:")
    print("1. Make sure you're SIGNED IN to your Microsoft account in Edge")
    print(f"2. Will perform {NUM_SEARCHES} searches (Note: Daily limit is ~30-35 searches)")
    print("3. Let the script run slowly - don't interrupt it")
    print("4. Microsoft Rewards points may take a few minutes to update")
    print("\nPress Ctrl+C to cancel, or wait 5 seconds to continue...")
    
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("\n\nAutomation cancelled.")
        exit(0)
    
    # Run the automation
    run_automation(num_searches=NUM_SEARCHES, interval=INTERVAL)
