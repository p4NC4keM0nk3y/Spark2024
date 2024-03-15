from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home')  # Make sure the extension is .html

@app.route('/note-maker')
def note_maker():
    return render_template('NoteMaker')  # Adjust as per actual file name

@app.route('/note-to-pdf')
def note_to_pdf():
    return render_template('NoteToPdf')  # Adjust as per actual file name

if __name__ == '__main__':
    app.run(debug=True)

