from flask import Flask, render_template, request, jsonify
from Story_Generation.story_generation import generate_text

app = Flask("AI Storybook")

def run_storybook():
    app.run(host="0.0.0.0", port=5000)

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/generate", methods=["GET"])
def generate_story():
    story_prompt = request.args.get('story_idea')
    if not story_prompt:
        return jsonify({"error": "No story prompt provided"}), 400

    story_pages = generate_text(story_prompt)
    formatted_pages = [{"text": page["text"]} for page in story_pages]
    return jsonify(formatted_pages)

if __name__ == "__main__":
    run_storybook()