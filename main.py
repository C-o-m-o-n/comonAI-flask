from flask import Flask, request, render_template, redirect
import os
import openai


openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)

@app.route('/' ,methods=['POST', 'GET'])
def index():
    form_prompt = 'hi'
    if request.method == 'POST':
        form_prompt = request.form['prompt']

        start_sequence = "\nAI:"
        restart_sequence = "\nHuman: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=form_prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )
    print(form_prompt)
    return render_template("index.html", response=response)




if __name__ == "__main__":
    app.run(debug=True)
