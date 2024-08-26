from flask import Flask,jsonify,request
from flask_cors import CORS
import yt_dlp

app=Flask(__name__)

CORS(app)

@app.route("/",methods=['GET'])
def Home():
    return jsonify({"message":"Welcome to the API"}),200

@app.route("/get_video_info",methods=['GET'])
def get_video_info():
    video_url=request.args.get("video_url")
    if  video_url is None:
        return jsonify({"message":"Video URL is required"}),400
    try:
       ydl_opts = {
            'format': 'best',  
            'verbose': True,
            'skip_download': True,  
            'writesubtitles': True,  
            'subtitleslangs': ['en'],
            'noplaylist': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            return jsonify(info),200
    except yt_dlp.utils.ExtractorError as e:
        error_message = str(e)
        print(error_message)
        return jsonify({'error': error_message}), 404
    except yt_dlp.utils.DownloadError as e:
        error_message = str(e)
        print(error_message)
        return jsonify({'error': error_message}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500
