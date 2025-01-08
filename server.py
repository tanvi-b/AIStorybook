from flask import Flask, render_template, request
from Story_Generation.story_generation import generate_text

app = Flask("AI Storybook")

def run_storybook():
    app.run(host="0.0.0.0", port=5000)

@app.route("/")
def sent_story():
    story_prompt = request.args.get('story-id')
    response = generate_text(story_prompt)

# @app.route("/")
# def render_index_page():
#     return render_template('index.html')

if __name__ == "__main__":
    run_storybook()
