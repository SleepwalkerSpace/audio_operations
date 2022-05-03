import os

from flask import Flask, request, flash, redirect, render_template
from werkzeug.utils import secure_filename

from pydub import AudioSegment


def tonality_adjustment(level:int, source_path:str, output_path:str):
    if level < -12 or level > 12:
        return 0
    
    try:
        frame_rate = AudioSegment.from_mp3(source_path).frame_rate
    
    except:
        return 0

    status = os.system(
        "ffmpeg -i '{}' -filter_complex 'asetrate={}*2^({}/12),atempo=1/2^({}/12)' {}".format(
            source_path, frame_rate, level, level, output_path
        ))
    
    return status


project_path = os.getcwd()
project_static_path = os.path.join(project_path, "static")
project_static_uploads_path = os.path.join(project_static_path, "uploads")
project_static_outputs_path = os.path.join(project_static_path, "outputs")


app = Flask(__name__, static_url_path="/static", )
app.config['UPLOAD_FOLDER'] = project_static_uploads_path
app.config['OUTPUT_FOLDER'] = project_static_outputs_path


ALLOWED_EXTENSIONS = {"mp3"}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        lvl = request.args.get("lvl", default=0, type=int)
        if lvl == 0 or lvl < -12 or lvl > 12:
            flash('Param level error')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], "{}_{}.{}".format(
                filename.rsplit('.', 1)[0].lower(), 
                "+{}".format(lvl) if lvl > 0 else lvl, 
                filename.rsplit('.', 1)[1].lower()
            ))
            file.save(source_path)
        
            tonality_adjustment(lvl, source_path, output_path)
            return redirect(request.url)
        

def main():
    app.run()


if __name__ == "__main__":
    main()