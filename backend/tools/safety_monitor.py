"""
Safety Monitor Tool
Risk detection and prevention system
"""

import random
import time
from datetime import datetime, timedelta

class SafetyMonitor:
    def __init__(self):
        self.risk_score = 0
        self.warnings = []
        self.activity_log = []
        
    def analyze_patterns(self, transactions, clicks, hijacks):
        """Analyze patterns for detection risks"""
        
        print("🔍 Analyzing activity patterns...")
        
        risks = []
        
        # 1. Transaction pattern analysis
        if transactions:
            trans_risk = self._analyze_transaction_pattern(transactions)
            if trans_risk:
                risks.append(("Transaction Pattern", trans_risk))
        
        # 2. Click pattern analysis
        if clicks:
            click_risk = self._analyze_click_pattern(clicks)
            if click_risk:
                risks.append(("Click Pattern", click_risk))
        
        # 3. Hijack pattern analysis
        if hijacks:
            hijack_risk = self._analyze_hijack_pattern(hijacks)
            if hijack_risk:
                risks.append(("Hijack Pattern", hijack_risk))
        
        # 4. Velocity analysis
        velocity_risk = self._analyze_velocity(transactions, clicks)
        if velocity_risk:
            risks.append(("Activity Velocity", velocity_risk))
        
        # Calculate overall risk score
        self.risk_score = min(100, len(risks) * 15 + random.randint(0, 30))
        
        # Generate warnings
        self.warnings = []
        for risk_name, risk_desc in risks:
            if random.random() > 0.5:  # 50% chance of warning
                self.warnings.append({
                    "type": risk_name,
                    "description": risk_desc,
                    "severity": random.choice(["low", "medium", "high"]),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        self.log_activity("Pattern analysis completed")
        
        return {
            "risk_score": self.risk_score,
            "risk_level": self.get_risk_level(),
            "warnings": self.warnings,
            "recommendations": self.generate_recommendations()
        }
    
    def _analyze_transaction_pattern(self, transactions):
        """Analyze transaction patterns"""
        
        if len(transactions) < 2:
            return None
        
        # Check for identical amounts
        amounts = [t.get("amount", 0) for t in transactions]
        if len(set(amounts)) < len(amounts) * 0.5:  # If more than 50% same amount
            return "Multiple transactions with identical amounts"
        
        # Check timing patterns
        if "timestamp" in transactions[0]:
            timestamps = [t["timestamp"] for t in transactions]
            if self._detect_regular_pattern(timestamps):
                return "Transactions at regular intervals detected"
        
        return None
    
    def _analyze_click_pattern(self, clicks):
        """Analyze click patterns"""
        
        if len(clicks) < 10:
            return None
        
        # Check session duration
        durations = [c.get("duration", 0) for c in clicks]
        avg_duration = sum(durations) / len(durations)
        
        if avg_duration < 30:  # Less than 30 seconds average
            return f"Average session duration too short ({avg_duration:.1f}s)"
        
        # Check bounce rate
        bounces = sum(1 for c in clicks if c.get("bounce", False))
        bounce_rate = bounces / len(clicks)
        
        if bounce_rate < 0.1:  # Less than 10% bounce rate (unnatural)
            return f"Bounce rate too low ({bounce_rate:.1%})"
        
        return None
    
    def _analyze_hijack_pattern(self, hijacks):
        """Analyze hijack patterns"""
        
        if len(hijacks) < 3:
            return None
        
        # Check message similarity
        messages = [h.get("message", "") for h in hijacks]
        if len(set(messages)) < len(messages) * 0.3:  # If less than 30% unique
            return "Similar hijack messages detected"
        
        # Check platform diversity
        platforms = [h.get("platform", "") for h in hijacks]
        if len(set(platforms)) < 3:
            return "Limited platform diversity in hijack campaign"
        
        return None
    
    def _analyze_velocity(self, transactions, clicks):
        """Analyze activity velocity"""
        
        # Check transaction velocity
        if transactions:
            trans_per_day = len(transactions) / 7  # Assuming 1 week
            if trans_per_day > 10:
                return f"High transaction velocity ({trans_per_day:.1f}/day)"
        
        # Check click velocity
        if clicks:
            clicks_per_hour = len(clicks) / 24  # Assuming 1 day
            if clicks_per_hour > 100:
                return f"High click velocity ({clicks_per_hour:.1f}/hour)"
        
        return None
    
    def _detect_regular_pattern(self, timestamps):
        """Detect regular patterns in timestamps"""
        # Simplified pattern detection
        if len(timestamps) < 3:
            return False
        
        # Convert to minutes of day
        times = []
        for ts in timestamps:
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                times.append(dt.hour * 60 + dt.minute)
            except:
                continue
        
        if len(times) < 3:
            return False
        
        # Check if times are evenly spaced
        times.sort()
        differences = [times[i+1] - times[i] for i in range(len(times)-1)]
        
        if len(set(differences)) < len(differences) * 0.3:
            return True
        
        return False
    
    def get_risk_level(self):
        """Get risk level based on score"""
        
        if self.risk_score < 30:
            return "low"
        elif self.risk_score < 70:
            return "medium"
        else:
            return "high"
    
    def generate_recommendations(self):
        """Generate recommendations based on risk"""
        
        recommendations = []
        
        if self.risk_score > 70:
            recommendations.extend([
                "⚠️ HIGH RISK: Pause all activities for 24-48 hours",
                "Rotate all proxy IP addresses",
                "Reduce transaction volume by 50%",
                "Increase delay between actions",
                "Use more diverse user agents"
            ])
        elif self.risk_score > 40:
            recommendations.extend([
                "⚠️ MEDIUM RISK: Reduce activity intensity",
                "Vary transaction amounts more",
                "Add random delays between sessions",
                "Use different shipping addresses",
                "Mix payment methods"
            ])
        else:
            recommendations.extend([
                "✅ LOW RISK: Continue current operations",
                "Maintain current safety protocols",
                "Monitor for any pattern changes",
                "Keep backup accounts ready"
            ])
        
        return recommendations
    
    def log_activity(self, activity):
        """Log activity for monitoring"""
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activity": activity,
            "risk_score": self.risk_score
        }
        
        self.activity_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.activity_log) > 1000:
            self.activity_log = self.activity_log[-1000:]
    
    def real_time_monitor(self, check_interval=300):
        """Run real-time monitoring"""
        
        print("📡 Starting real-time safety monitor...")
        print(f"   Check interval: {check_interval} seconds")
        
        while True:
            try:
                # Simulate monitoring check
                current_risk = random.randint(0, 100)
                
                if current_risk > 80:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 CRITICAL RISK: {current_risk}/100")
                    print("   ⚠️  Auto-pausing activities...")
                elif current_risk > 60:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  High risk: {current_risk}/100")
                elif current_risk > 30:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Medium risk: {current_risk}/100")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Low risk: {current_risk}/100")
                
                self.log_activity(f"Risk check: {current_risk}")
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Safety monitor stopped")
                break
    
    def get_dashboard_data(self):
        """Get data for dashboard display"""
        
        return {
            "current_risk": self.risk_score,
            "risk_level": self.get_risk_level(),
            "active_warnings": len(self.warnings),
            "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": self.generate_recommendations()[:3],  # Top 3
            "activity_count": len(self.activity_log)
        }

# Example usage
if __name__ == "__main__":
    print("🛡️ Testing Safety Monitor Tool\n")
    
    monitor = SafetyMonitor()
    
    # Simulate some data
    fake_transactions = [
        {"amount": 50000, "timestamp": "2024-01-01 10:00:00"},
        {"amount": 50000, "timestamp": "2024-01-01 12:00:00"},
        {"amount": 50000, "timestamp": "2024-01-01 14:00:00"}
    ]
    
    fake_clicks = [
        {"duration": 45, "bounce": False},
        {"duration": 28, "bounce": True},
        {"duration": 32, "bounce": False}
    ]
    
    # Run analysis
    results = monitor.analyze_patterns(fake_transactions, fake_clicks, [])
    
    print("\n" + "="*50)
    print("📊 Safety Analysis Results:")
    print(f"   Risk Score: {results['risk_score']}/100")
    print(f"   Risk Level: {results['risk_level']}")
    print(f"   Warnings: {len(results['warnings'])}")
    
    if results['warnings']:
        print("\n   ⚠️ Warnings:")
        for warning in results['warnings']:
            print(f"     • {warning['type']}: {warning['description']}")
    
    print("\n   📋 Recommendations:")
    for rec in results['recommendations']:
        print(f"     • {rec}")