from flask import Flask, request, Response, render_template
import requests
import os

app = Flask(__name__)

# প্রক্সি ফাংশন: এটি রেস্ট্রিক্টেড সাইটগুলো লোড করতে সাহায্য করবে
@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "URL missing", 400
    
    try:
        # একটি আসল ব্রাউজারের পরিচয় (User-Agent) পাঠানো হচ্ছে
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        
        # ওয়েবসাইট থেকে ডেটা নিয়ে আসা
        resp = requests.get(target_url, headers=headers, stream=True, timeout=10)
        
        # হেডার ক্লিনআপ
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        resp_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                        if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, resp_headers)
    except Exception as e:
        return f"Error: {str(e)}", 500

# হোম রুট: এটি আপনার index.html ফাইলটি লোড করবে
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # অনলাইন সার্ভারের পোর্ট কনফিগারেশন
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
