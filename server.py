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
        return jsonify({"error": "No story prompt given"}), 400

    story_pages = generate_text(story_prompt + "Write a short story. It should have a beginning, middle, and end. Conclude the story within "
                                               "1000 words. It should be minimum 750 words and maximum 1000 words. Start printing story "
                                               "immediately, don't include your own stuff like a title and other info. Begin story with "
                                               "interesting hook. End the story with The End. Don't start with the story with a period.")
    formatted_pages = [{"text": page["text"]} for page in story_pages]
    return jsonify(formatted_pages)

if __name__ == "__main__":
    run_storybook()