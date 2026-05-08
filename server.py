from flask import Flask, request, Response
import requests

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

if __name__ == '__main__':
    # আপনার পিসির লোকাল হোস্ট পোর্টে সার্ভারটি চলবে
    app.run(debug=True, port=5000)
