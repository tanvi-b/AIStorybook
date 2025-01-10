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

    story_pages = generate_text(story_prompt + "Write a short story.")
    formatted_pages = [{"text": page["text"]} for page in story_pages]
    return jsonify(formatted_pages)

if __name__ == "__main__":
    run_storybook()

#The story must end within 10 pages. The story must have a beginning, middle, and end. No title or chapters. Each page must complete the sentence. Do not continue the sentence across 2 pages.
#set min and max page count
#weird response to prompt: Girl's trip to NYC
#good response to prompt: Girl's trip to India
#shorten words per page?
#add loading sign
#once generate story i clicked any current story will be erased from pages
#errors: want to print just story but sometimes printing stuff that model adds