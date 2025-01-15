from flask import Flask, render_template, request, jsonify, send_from_directory
from Story_Generation.story_generation import generate_text

app = Flask("AI Storybook")

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/generate", methods=["GET"])
def generate_story():
    story_prompt = request.args.get('story_idea')
    if not story_prompt:
        return jsonify({"error": "No story prompt given"}), 400

    story_pages = generate_text(
        story_prompt + "Write a short story. It should have a beginning, middle, and end. Conclude the story within "
                       "1000 words. It should be minimum 750 words and maximum 1000 words. Start printing story "
                       "immediately, don't include your own stuff like a title and other info. Begin story with "
                       "interesting hook. End the story with The End. Don't start the story with a period. "
                       "Start the story immediately with the word once."
    )
    formatted_pages = [
        {"text": page["text"], "image": page["image"]} for page in story_pages
    ]
    return jsonify(formatted_pages)

@app.route("/images/<path:filename>")
def give_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)