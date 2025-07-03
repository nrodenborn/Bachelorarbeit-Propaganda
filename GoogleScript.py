import os
import time
from pathlib import Path
import google.generativeai as genai

#API-Key einfügen
GEMINI_API_KEY = "API-Key einfügen"


genai.configure(api_key=GEMINI_API_KEY)



# Passen Sie diese Pfade bei Bedarf an, je nach One- oder Zero- Shot Results.
text_folder = "\ptc-corpus\all-articles"
output_folder = "\Outputs\results_gemini"
os.makedirs(output_folder, exist_ok=True)



# Den Prompt ändern je nach One oder Zero -Shot.
def build_prompt(text):
    return """
The following are a list of propaganda techniques and their definitions:

1. Name calling – Attack an object/subject of the propaganda with an insulting label.
2. Repetition – Repeat the same message over and over.
3. Slogans – Use a brief and memorable phrase.
4. Appeal to fear – Support an idea by instilling fear against other alternatives.
5. Doubt – Question the credibility of someone or something.
6. Exaggeration/minimization – Exaggerate or minimize something.
7. Flag-Waving – Appeal to patriotism or identity.
8. Loaded Language – Appeal to emotions or stereotypes.
9. Reduction ad Hitlerum – Disapprove an idea by suggesting it is popular with groups hated by the audience.
10. Bandwagon – Appeal to the popularity of an idea.
11. Causal Oversimplification – Assume a simple cause for a complex event.
12. Obfuscation, intentional vagueness – Use deliberately unclear and obscure expressions to confuse the audience.
13. Appeal to authority – Use authority’s support as evidence.
14. Black & white fallacy – Present only two options among many.
15. Thought-terminating clichés – Phrases that discourage critical thought and meaningful discussions.
16. Red herring – Introduce irrelevant material to distract.
17. Straw men – Refute an argument that was not presented.
18. Whataboutism – Charge an opponent with hypocrisy.

For each of the techniques and according to its definition, answer with a yes or no if the technique is being used in the following text with an example from the text if present. This should take the exact form of: ‘propaganda technique – Yes or no – Explanation’.

{}

Lastly, give a final verdict on whether the text is propaganda, stating a percentage likelihood on the text being propaganda followed by a detailed explanation.
This should take the form of:

‘Verdict – [Number]% – [Explanation]’
""".strip().format(text)


#Modell auswählen

generation_config = genai.GenerationConfig(temperature=0.3)
model = genai.GenerativeModel(
    model_name='gemini-2.5-pro',
    generation_config=generation_config
)

#Texte verarbeiten
for text_file in sorted(Path(text_folder).glob("*.txt")):
    try:
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read().strip()


        prompt = build_prompt(text)


        print(f"🔄 Verarbeite {text_file.name} mit Gemini 2.5 Pro...")
        response = model.generate_content(prompt)


        output = response.text


        output_path = Path(output_folder) / f"{text_file.stem}_response.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"✅ {text_file.name} erfolgreich verarbeitet.")


        time.sleep(1.5)

    except Exception as e:

        print(f"⚠️ Fehler bei der Verarbeitung von {text_file.name}: {e}")

        try:
            print(f"   API-Antwortdetails: {response.prompt_feedback}")
        except (NameError, AttributeError):
            pass