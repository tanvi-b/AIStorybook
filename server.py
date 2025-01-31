from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from Story_Generation.story_generation import generate_text, generate_pdf
import os
import time

#try making page count dynamic - when you see "The End" pages end
#change font of pdf

app = Flask("AI Storybook")
CORS(app)

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
    try:
        data = request.get_json()
        if not data or 'pages' not in data:
            return jsonify({"error": "No story pages provided"}), 400

        story_pages = []
        for page in data['pages']:
            image_path = None
            if page.get('image'):
                image_url = page['image']
                filename = image_url.split('/')[-1].split('?')[0]
                image_path = os.path.join('images', filename)
                if os.path.exists(image_path):
                    print(f"Found image: {image_path}")
                else:
                    print(f"Image not found: {image_path}")

            story_pages.append({
                "text": page.get('text', ''),
                "image": image_path
            })

        output_pdf_path = "storybook.pdf"
        generate_pdf(story_pages, output_pdf_path)

        return send_from_directory(
            directory=os.getcwd(),
            path=output_pdf_path,
            as_attachment=True,
            download_name="storybook.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        print("Error generating PDF:", str(e))
        return jsonify({"error": "Failed to generate PDF"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)