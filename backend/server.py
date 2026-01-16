from flask import Flask, jsonify, request
from flask_cors import CORS
from database.postgres_config import db
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

print("🚀 SEO Tools Backend Starting...")

# Test database connection on startup
if db.test_connection():
    print("✅ PostgreSQL database connected!")
    db.add_log('SYSTEM', 'Backend server started')
else:
    print("❌ WARNING: Database connection failed")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "app": "SEO Tools Dashboard",
        "database": "PostgreSQL",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "database": "connected" if db.test_connection() else "disconnected",
        "timestamp": datetime.now().isoformat()
    })

# ===== CAMPAIGN API =====
@app.route('/api/campaigns/create', methods=['POST'])
def create_campaign():
    """Create new SEO campaign"""
    data = request.json
    
    # Validate
    required = ['name', 'url', 'platform']
    for field in required:
        if field not in data:
            return jsonify({
                "status": "error",
                "message": f"Missing: {field}"
            }), 400
    
    try:
        # Create in database
        campaign_id = db.create_campaign(
            name=data['name'],
            url=data['url'],
            platform=data['platform'],
            sessions=data.get('sessions', 100)
        )
        
        if campaign_id:
            return jsonify({
                "status": "success",
                "message": "Campaign created",
                "campaign_id": campaign_id,
                "data": data
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to create campaign"
            }), 500
            
    except Exception as e:
        db.add_log('ERROR', f'Create campaign failed: {str(e)}')
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/campaigns/<int:campaign_id>/stats')
def get_campaign_stats(campaign_id):
    """Get campaign statistics"""
    stats = db.get_campaign_stats(campaign_id)
    
    if stats:
        return jsonify({
            "status": "success",
            "data": stats
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Campaign not found"
        }), 404

@app.route('/api/campaigns/<int:campaign_id>/log', methods=['POST'])
def log_traffic_session():
    """Log traffic session"""
    data = request.json
    
    success = db.add_traffic_log(
        campaign_id=data['campaign_id'],
        session_num=data['session_number'],
        success=data.get('success', True),
        proxy=data.get('proxy')
    )
    
    if success:
        return jsonify({
            "status": "success",
            "message": "Session logged"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to log session"
        }), 500

# ===== TOOLS API =====
@app.route('/api/tools/click-circulation/start', methods=['POST'])
def start_click_circulation():
    """Start click circulation tool"""
    data = request.json
    
    # Log ke database
    db.add_log('TOOL', f'Click Circulation started for: {data.get("url", "unknown")}')
    
    return jsonify({
        "status": "success",
        "tool": "click_circulation",
        "message": "Click circulation started",
        "data": {
            "url": data.get('url'),
            "sessions": data.get('sessions', 500),
            "started_at": datetime.now().isoformat()
        }
    })

@app.route('/api/tools/real-traffic/start', methods=['POST'])
def start_real_traffic():
    """Start REAL traffic campaign"""
    data = request.json
    
    # Create campaign in database
    campaign_id = db.create_campaign(
        name=f"real_traffic_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        url=data['url'],
        platform=data.get('platform', 'tokopedia'),
        sessions=data.get('sessions', 50)
    )
    
    db.add_log('WARNING', f'REAL Traffic started - HIGH RISK')
    
    return jsonify({
        "status": "success",
        "tool": "real_traffic",
        "message": "REAL traffic campaign started",
        "campaign_id": campaign_id,
        "warning": "HIGH RISK - Use with caution"
    })

@app.route('/api/tools/safety-monitor/check')
def safety_check():
    """Run safety check"""
    # Simulate check with random results
    import random
    
    risk_score = random.randint(0, 100)
    if risk_score < 30:
        risk_level = "low"
    elif risk_score < 70:
        risk_level = "medium"
    else:
        risk_level = "high"
    
    db.add_log('SAFETY', f'Safety check: {risk_level} ({risk_score}/100)')
    
    return jsonify({
        "status": "success",
        "tool": "safety_monitor",
        "data": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "warnings": random.randint(0, 3),
            "checked_at": datetime.now().isoformat()
        }
    })

# ===== SYSTEM API =====
@app.route('/api/logs')
def get_logs():
    """Get system logs (simplified)"""
    return jsonify({
        "status": "success",
        "message": "Logs endpoint - implement database query",
        "note": "Check database.system_logs table"
    })

@app.route('/api/db/test')
def test_db():
    """Test database connection"""
    if db.test_connection():
        return jsonify({
            "status": "success",
            "database": "PostgreSQL",
            "connected": True
        })
    else:
        return jsonify({
            "status": "error",
            "database": "PostgreSQL",
            "connected": False
        }), 500

# ===== ERROR HANDLING =====
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def server_error(error):
    db.add_log('ERROR', f'Server error: {str(error)}')
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

# ===== START SERVER =====
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SEO TOOLS BACKEND READY")
    print("="*60)
    print(f"📡 API: http://localhost:5000")
    print(f"📊 Database: PostgreSQL")
    print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("\nAvailable endpoints:")
    print("  GET  /api/status")
    print("  POST /api/campaigns/create")
    print("  GET  /api/campaigns/<id>/stats")
    print("  POST /api/tools/click-circulation/start")
    print("  POST /api/tools/real-traffic/start")
    print("  GET  /api/tools/safety-monitor/check")
    print("  GET  /api/db/test")
    print("\nPress Ctrl+C to stop")
    print("="*60)
    
    app.run(host='localhost', port=5000, debug=True)