from flask import Flask, render_template, request, jsonify, send_from_directory
from Story_Generation.story_generation import generate_text, generate_pdf
import os
import time

#try making page count dynamic - when you see "The End" pages end
#next steps: pdf download option, IOS app
#change font of pdf, connect backend w/ pdf button

app = Flask("AI Storybook")

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/generate", methods=["GET"])
def generate_story():
    story_prompt = request.args.get('story_idea')
    story_genre = request.args.get('genre')

    if not story_prompt:
        return jsonify({"error": "No story prompt given"}), 400
    if not story_genre:
        return jsonify({"error": "No story genre given"}), 400

    story_pages = generate_text(
        story_prompt + " Write a short " + story_genre + " story. It should have a beginning, middle, and end. Conclude the story within "
                       "1000 words. It should be minimum 750 words and maximum 1000 words. Start printing story "
                       "immediately, don't include your own stuff like a title and other info. Begin story with "
                       "interesting hook. End the story with The End. Keep it a short concise story. The story should not be too long. "
                       "Don't start the story with a period. Start the story immediately with the word once."
    )

    formatted_pages = [
        {"text": page["text"], "image": f"/images/{os.path.basename(page['image'])}?timestamp={int(time.time())}"}
        for page in story_pages
    ]
    return jsonify(formatted_pages)

@app.route("/images/<path:filename>")
def give_image(filename):
    return send_from_directory("images", filename)

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    story_pages = request.get_json()
    output_pdf_path = "storybook.pdf"
    generate_pdf(story_pages, output_pdf_path)
    return send_from_directory(directory=os.getcwd(), path=output_pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)