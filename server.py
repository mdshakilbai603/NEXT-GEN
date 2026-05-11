from flask import Flask, request, Response
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
        # ওয়েবসাইট থেকে ডেটা নিয়ে আসা
        resp = requests.get(target_url, stream=True)
        
        # কিছু নির্দিষ্ট হেডার বাদ দেওয়া যা ব্রাউজারে সমস্যা করতে পারে
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Error: {str(e)}", 500

# হোম রুট: এটি আপনার index.html ফাইলটি লোড করবে
@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

if __name__ == '__main__':
    # অনলাইন সার্ভারের পোর্ট কনফিগারেশন (Render/Railway এর জন্য জরুরি)
    port = int(os.environ.get('PORT', 5000))
    # host='0.0.0.0' নিশ্চিত করে যে এটি বাইরের নেটওয়ার্ক থেকে অ্যাক্সেস করা যাবে
    app.run(host='0.0.0.0', port=port)
