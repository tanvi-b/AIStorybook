from flask import Flask, render_template, request, jsonify, send_from_directory
from Story_Generation.story_generation import generate_text
import os

app = Flask("AI Storybook")

@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), filename)

def run_storybook():
    app.run(host="0.0.0.0", port=5000)

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/generate", methods=["POST"])
def generate_story():
    story_prompt = request.form.get('story_idea')
    story_pages = generate_text(story_prompt)

    for page in story_pages:
        page['image'] = f"/static/images/{os.path.basename(page['image'])}"

    return jsonify(story_pages)

if __name__ == "__main__":
    run_storybook()