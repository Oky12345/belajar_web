import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

class ClickCirculation:
    def __init__(self, target_url):
        self.target_url = target_url
        self.proxies = self.load_proxies()
        
    def load_proxies(self):
        """Load proxy list from file"""
        try:
            with open('data/proxies.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []
    
    def simulate_session(self, session_num):
        """Simulate one browsing session"""
        print(f"[Session {session_num}] Starting...")
        
        # Configure browser
        options = webdriver.ChromeOptions()
        
        # Add random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        # Add proxy if available
        if self.proxies:
            proxy = random.choice(self.proxies)
            options.add_argument(f'--proxy-server={proxy}')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            # Visit target URL
            driver.get(self.target_url)
            time.sleep(random.uniform(3, 8))
            
            # Random interactions
            actions = [
                ("scroll", random.randint(300, 1000)),
                ("click_images", None),
                ("view_variants", None),
                ("add_to_wishlist", None)
            ]
            
            for action, param in random.sample(actions, random.randint(2, 4)):
                if action == "scroll":
                    driver.execute_script(f"window.scrollBy(0, {param})")
                elif action == "click_images":
                    images = driver.find_elements(By.TAG_NAME, 'img')
                    if images:
                        random.choice(images[:5]).click()
                
                time.sleep(random.uniform(1, 3))
            
            print(f"[Session {session_num}] Completed successfully")
            
        except Exception as e:
            print(f"[Session {session_num}] Error: {e}")
        
        finally:
            driver.quit()
    
    def run_daily_sessions(self, sessions_per_day=500):
        """Run specified number of sessions"""
        print(f"Starting {sessions_per_day} sessions for {self.target_url}")
        
        for i in range(sessions_per_day):
            self.simulate_session(i + 1)
            
            # Random delay between sessions (1-5 minutes)
            if i < sessions_per_day - 1:
                delay = random.uniform(60, 300)
                print(f"Waiting {delay:.0f} seconds before next session...")
                time.sleep(delay)
        
        print("All sessions completed!")

# Example usage
if __name__ == "__main__":
    # Test with sample URL
    tool = ClickCirculation("https://tokopedia.com/sample-product")
    tool.run_daily_sessions(sessions_per_day=10)  # Reduced for testing