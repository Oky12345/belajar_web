"""
Competitor Hijack Tool
Redirect traffic from competitors to your shop
"""

import random
import time
from datetime import datetime

class CompetitorHijack:
    def __init__(self):
        self.campaigns = []
        self.platforms = [
            "Kaskus",
            "Detik Forum", 
            "Komunitas Tokopedia",
            "Facebook Groups",
            "Instagram Comments",
            "TikTok Comments"
        ]
    
    def create_campaign(self, competitor_url, your_url, message_template=None):
        """Create hijack campaign against competitor"""
        
        campaign = {
            "id": len(self.campaigns) + 1,
            "competitor": competitor_url,
            "your_shop": your_url,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stats": {
                "posts_made": 0,
                "estimated_redirects": 0,
                "conversion_rate": 0.0
            }
        }
        
        self.campaigns.append(campaign)
        print(f"✅ Campaign #{campaign['id']} created")
        print(f"   Target: {competitor_url}")
        print(f"   Redirect to: {your_url}")
        
        return campaign
    
    def generate_hijack_message(self, competitor_url, your_url):
        """Generate hijack message templates"""
        
        templates = [
            f"Saya coba produk di {competitor_url} tapi ternyata lebih bagus di {your_url}",
            f"Kalau mau harga lebih murah dengan kualitas sama, cek {your_url}",
            f"Alternatif yang lebih worth it: {your_url} (harga lebih kompetitif)",
            f"Dijual lebih murah di {your_url} untuk produk yang sama",
            f"Setelah compare, akhirnya beli di {your_url} - recommended banget!"
        ]
        
        return random.choice(templates)
    
    def post_to_forum(self, platform, thread_url, message):
        """Simulate posting to forum"""
        
        print(f"📝 Posting to {platform}")
        print(f"   Thread: {thread_url}")
        print(f"   Message: {message[:50]}...")
        
        # Simulate posting delay
        time.sleep(random.uniform(2, 5))
        
        # Random success rate
        success = random.random() > 0.3
        
        if success:
            print(f"   ✅ Post successful")
            return True
        else:
            print(f"   ❌ Post failed (moderation)")
            return False
    
    def hijack_competitor_reviews(self, competitor_product_url, your_url):
        """Hijack competitor's review section"""
        
        print(f"🎯 Targeting competitor reviews: {competitor_product_url}")
        
        review_templates = [
            f"Saya beli produk serupa di {your_url} dan lebih puas",
            f"Setelah compare price, ternyata lebih murah di {your_url}",
            f"Alternatif produk sama: {your_url} (recommended)"
        ]
        
        # Simulate multiple review posts
        successful_posts = 0
        for i in range(random.randint(1, 3)):
            message = random.choice(review_templates)
            print(f"   Review #{i+1}: {message}")
            time.sleep(random.uniform(1, 3))
            
            if random.random() > 0.4:  # 60% success rate
                successful_posts += 1
        
        print(f"   📊 {successful_posts} review posts successful")
        return successful_posts
    
    def social_media_hijack(self, platform, competitor_profile, your_profile):
        """Hijack competitor's social media"""
        
        print(f"📱 Social media hijack on {platform}")
        print(f"   Competitor: {competitor_profile}")
        print(f"   Your profile: {your_profile}")
        
        actions = [
            "Comment under posts",
            "Reply to comments",
            "Share with comparison",
            "Direct message followers"
        ]
        
        for action in random.sample(actions, random.randint(1, 2)):
            print(f"   Action: {action}")
            time.sleep(random.uniform(1, 2))
        
        estimated_reach = random.randint(50, 500)
        print(f"   Estimated reach: {estimated_reach} users")
        
        return estimated_reach
    
    def run_daily_campaign(self, campaign_id, posts_per_day=10):
        """Run daily hijack campaign"""
        
        campaign = next((c for c in self.campaigns if c['id'] == campaign_id), None)
        if not campaign:
            print(f"❌ Campaign #{campaign_id} not found")
            return
        
        print(f"🚀 Starting daily campaign #{campaign_id}")
        print(f"   Target: {campaign['competitor']}")
        print(f"   Daily posts: {posts_per_day}")
        
        total_success = 0
        
        for day in range(7):  # 1 week campaign
            print(f"\n📅 Day {day + 1}:")
            
            daily_success = 0
            for post_num in range(posts_per_day):
                # Choose random platform
                platform = random.choice(self.platforms)
                
                # Generate message
                message = self.generate_hijack_message(
                    campaign['competitor'], 
                    campaign['your_shop']
                )
                
                # Simulate post
                success = self.post_to_forum(platform, campaign['competitor'], message)
                if success:
                    daily_success += 1
                    campaign['stats']['posts_made'] += 1
                
                time.sleep(random.uniform(10, 30))  # Delay between posts
            
            # Update stats
            redirects = int(daily_success * random.uniform(5, 15))
            campaign['stats']['estimated_redirects'] += redirects
            
            conversion_rate = random.uniform(0.01, 0.05)  # 1-5% conversion
            campaign['stats']['conversion_rate'] = conversion_rate
            
            print(f"   Day result: {daily_success}/{posts_per_day} posts successful")
            print(f"   Estimated redirects: +{redirects}")
            print(f"   Total redirects: {campaign['stats']['estimated_redirects']}")
            
            total_success += daily_success
        
        print(f"\n🎯 Campaign completed!")
        print(f"   Total posts: {campaign['stats']['posts_made']}")
        print(f"   Total estimated redirects: {campaign['stats']['estimated_redirects']}")
        print(f"   Conversion rate: {campaign['stats']['conversion_rate']:.2%}")
        
        return campaign['stats']
    
    def get_campaign_stats(self, campaign_id):
        """Get campaign statistics"""
        
        campaign = next((c for c in self.campaigns if c['id'] == campaign_id), None)
        if not campaign:
            return None
        
        return {
            'campaign_id': campaign['id'],
            'status': campaign['status'],
            'posts_made': campaign['stats']['posts_made'],
            'estimated_redirects': campaign['stats']['estimated_redirects'],
            'conversion_rate': f"{campaign['stats']['conversion_rate']:.2%}",
            'estimated_sales': int(campaign['stats']['estimated_redirects'] * campaign['stats']['conversion_rate'])
        }

# Example usage
if __name__ == "__main__":
    print("🔧 Testing Competitor Hijack Tool\n")
    
    hijack = CompetitorHijack()
    
    # Create campaign
    campaign = hijack.create_campaign(
        competitor_url="https://tokopedia.com/competitor-product",
        your_url="https://tokopedia.com/your-product"
    )
    
    # Run 1 day test
    print("\n" + "="*50)
    hijack.run_daily_campaign(campaign_id=1, posts_per_day=3)
    
    # Get stats
    print("\n" + "="*50)
    stats = hijack.get_campaign_stats(1)
    print("📊 Campaign Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")