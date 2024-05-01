from flask import Flask, render_template
import threading
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rungame')
def run_game():
    def run():
        subprocess.call('conda activate cse150b && python main.py', shell=True)

    # Create a new thread to run the game
    game_thread = threading.Thread(target=run)
    game_thread.start()

    return 'Game is running.'

if __name__ == '__main__':
    app.run(debug=True)

#running python app.py works
