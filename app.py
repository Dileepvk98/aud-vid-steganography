from flask import Flask, render_template, request, send_file
import os
from audio import Audio
from image import Image
from datetime import datetime

audio = Audio()
image = Image()

app = Flask(__name__)
img_formats = ["png", "jpg", "jpeg"]

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/encode', methods = ['POST'])
def encode():

   delete_old_files()

   if request.method == 'POST': 
      # file upload
      f1 = request.files['enc_f1']  
      f2 = request.files['enc_f2']  
      f1.save(os.path.join("uploads",f1.filename))
      f2.save(os.path.join("uploads",f2.filename))

      audio.hideout_file = "./uploads/"+f1.filename
      audio.infofile = "./uploads/"+f2.filename
      if f2.filename.split(".")[1] in img_formats:
         audio.infotype = "image"
      else:
         audio.infotype = "text"
      
      audio.read_audio_hideout()
      audio.read_info()
      fn = audio.hide_info()

      os.remove("uploads/"+f1.filename)
      os.remove("uploads/"+f2.filename)
      
      return render_template("index.html",key=audio.decodekey, file2down=fn)
      
      # return audio.decodekey
   return "Error"


@app.route('/download', methods = ['POST'])
def download():
   if request.method == 'POST':
      fn = request.form["fn2down"]
      return send_file("uploads/"+fn, as_attachment=True)


def delete_old_files():
   
   files = os.listdir("uploads/")
   print(files)
   for f in files:
      ts = os.path.getmtime("uploads/"+f)
      d = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
      d = datetime.strptime(d,"%H:%M:%S")
      now = datetime.now().strftime("%H:%M:%S")
      now = datetime.strptime(now,"%H:%M:%S")

      if (now - d).total_seconds() > 150:
         os.remove("uploads/"+f)
         print("deleted : ",f)

if __name__ == '__main__':
   app.run(debug = True)