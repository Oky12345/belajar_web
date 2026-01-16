"""
Micro Transaction Tool
Boost sales ranking with buffer accounts
"""

import random
import time
from datetime import datetime, timedelta

class MicroTransaction:
    def __init__(self):
        self.transactions = []
        self.buffer_accounts = []
        
    def generate_buffer_accounts(self, count=10):
        """Generate buffer accounts for transactions"""
        
        print(f"👥 Generating {count} buffer accounts...")
        
        for i in range(count):
            account = {
                "id": i + 1,
                "email": f"user{i+1}@temp-mail.org",
                "phone": f"08{random.randint(100000000, 999999999)}",
                "name": f"Customer {i+1}",
                "address": self.random_address(),
                "created": datetime.now().strftime("%Y-%m-%d"),
                "transactions_count": 0,
                "total_spent": 0
            }
            self.buffer_accounts.append(account)
        
        print(f"✅ Generated {len(self.buffer_accounts)} buffer accounts")
        return self.buffer_accounts
    
    def random_address(self):
        """Generate random Indonesian address"""
        
        cities = ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"]
        streets = ["Jl. Sudirman", "Jl. Thamrin", "Jl. Gatot Subroto", "Jl. MH Thamrin"]
        
        return {
            "street": f"{random.choice(streets)} No. {random.randint(1, 100)}",
            "city": random.choice(cities),
            "province": "Indonesia",
            "postal_code": str(random.randint(10000, 99999))
        }
    
    def create_transaction(self, product_url, amount_range=(50000, 200000)):
        """Create a single micro-transaction"""
        
        if not self.buffer_accounts:
            self.generate_buffer_accounts(5)
        
        # Select random account
        account = random.choice(self.buffer_accounts)
        
        # Random amount
        amount = random.randint(amount_range[0], amount_range[1])
        
        # Payment methods
        payment_methods = ["Gopay", "OVO", "Bank Transfer", "ShopeePay", "Dana"]
        
        transaction = {
            "id": len(self.transactions) + 1,
            "account_id": account["id"],
            "product_url": product_url,
            "amount": amount,
            "payment_method": random.choice(payment_methods),
            "status": "completed",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "review_posted": random.random() > 0.3  # 70% chance
        }
        
        # Update account stats
        account["transactions_count"] += 1
        account["total_spent"] += amount
        
        self.transactions.append(transaction)
        
        print(f"💰 Transaction #{transaction['id']} created")
        print(f"   Account: {account['name']}")
        print(f"   Amount: Rp {amount:,}")
        print(f"   Payment: {transaction['payment_method']}")
        print(f"   Review: {'✅ Yes' if transaction['review_posted'] else '❌ No'}")
        
        return transaction
    
    def schedule_daily_transactions(self, product_url, daily_count=3, days=7):
        """Schedule transactions over multiple days"""
        
        print(f"📅 Scheduling {daily_count} transactions/day for {days} days")
        print(f"   Product: {product_url}")
        
        schedule = []
        total_amount = 0
        
        for day in range(days):
            print(f"\n📆 Day {day + 1}:")
            day_transactions = []
            day_total = 0
            
            for i in range(daily_count):
                # Random time during day (9 AM - 9 PM)
                hour = random.randint(9, 21)
                minute = random.randint(0, 59)
                
                transaction = self.create_transaction(product_url)
                transaction["scheduled_time"] = f"{hour:02d}:{minute:02d}"
                
                day_transactions.append(transaction)
                day_total += transaction["amount"]
                
                # Delay between transactions
                time.sleep(0.5)
            
            schedule.append({
                "day": day + 1,
                "transactions": day_transactions,
                "daily_total": day_total
            })
            
            total_amount += day_total
            print(f"   Daily total: Rp {day_total:,}")
        
        print(f"\n🎯 Schedule complete!")
        print(f"   Total transactions: {days * daily_count}")
        print(f"   Total amount: Rp {total_amount:,}")
        print(f"   Estimated ranking boost: +{random.randint(10, 50)} positions")
        
        return schedule
    
    def simulate_reviews(self, product_url, transaction_ids):
        """Simulate posting reviews for transactions"""
        
        print(f"⭐ Simulating reviews for {len(transaction_ids)} transactions")
        
        review_templates = [
            "Produk bagus, original, pengiriman cepat!",
            "Sesuai ekspektasi, packing rapi, recommended seller",
            "Barang sampai dengan baik, kualitas oke, next order lagi",
            "Puas dengan pembelian, seller responsif, barang sesuai foto",
            "Fast response, produk asli, harga worth it banget"
        ]
        
        ratings = [5, 5, 5, 5, 4]  # Mostly 5 stars
        
        for txn_id in transaction_ids:
            transaction = next((t for t in self.transactions if t["id"] == txn_id), None)
            if transaction and transaction["review_posted"]:
                rating = random.choice(ratings)
                review = random.choice(review_templates)
                
                print(f"   Review for transaction #{txn_id}:")
                print(f"     Rating: {'⭐' * rating}")
                print(f"     Comment: {review}")
                
                # Add review to transaction
                transaction["review"] = {
                    "rating": rating,
                    "comment": review,
                    "posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        
        print(f"\n✅ {sum(1 for t in self.transactions if 'review' in t)} reviews posted")
        return True
    
    def get_statistics(self):
        """Get transaction statistics"""
        
        if not self.transactions:
            return {"error": "No transactions yet"}
        
        total_transactions = len(self.transactions)
        total_amount = sum(t["amount"] for t in self.transactions)
        total_reviews = sum(1 for t in self.transactions if t.get("review_posted", False))
        
        # Payment method distribution
        payment_counts = {}
        for t in self.transactions:
            method = t["payment_method"]
            payment_counts[method] = payment_counts.get(method, 0) + 1
        
        return {
            "total_transactions": total_transactions,
            "total_amount": total_amount,
            "average_transaction": total_amount / total_transactions if total_transactions > 0 else 0,
            "review_rate": (total_reviews / total_transactions * 100) if total_transactions > 0 else 0,
            "payment_distribution": payment_counts,
            "buffer_accounts_used": len(set(t["account_id"] for t in self.transactions))
        }

# Example usage
if __name__ == "__main__":
    print("💳 Testing Micro Transaction Tool\n")
    
    mt = MicroTransaction()
    
    # Generate buffer accounts
    mt.generate_buffer_accounts(5)
    
    # Schedule transactions
    schedule = mt.schedule_daily_transactions(
        product_url="https://tokopedia.com/your-product",
        daily_count=2,
        days=3
    )
    
    # Get statistics
    print("\n" + "="*50)
    stats = mt.get_statistics()
    print("📊 Transaction Statistics:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"     {k}: {v}")
        else:
            print(f"   {key}: {value}")