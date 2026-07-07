import os
import requests
import base64
import logging
from io import BytesIO
from PIL import Image
import facebook
from random import choice
import time
import random
import string

# ------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("cat-bot")

# ------------------------------------------------------------
# Environment token
# ------------------------------------------------------------
def get_env_token():
    token = os.getenv("CAT_BOT_PAGE_TOKEN")
    if not token:
        raise ValueError("CAT_BOT_PAGE_TOKEN not set")
    return token

# ------------------------------------------------------------
# Load SD.Next model
# ------------------------------------------------------------
def load_model():
    log.info("Loading SD.Next model: majicmixRealistic_v7")

    response = requests.post(
        "http://127.0.0.1:7860/sdapi/v1/options",
        json={"sd_model_checkpoint": "majicmixRealistic_v7"}
    )
    time.sleep(3)   # give SD.Next time to finish loading

    log.info(f"Model load status: {response.status_code}")
    if response.status_code != 200:
        log.error(f"Model load error: {response.text}")
        raise RuntimeError("Failed to load SD.Next model")


def generate_cat_name(letter, style):
    prompt = f"""
Generate a fictional cat name.

RULES:
- The name MUST begin with the letter: {letter}
- The name MUST be 3–10 characters long.
- The name MUST match this style: {style}
- The name MUST be a single word (no spaces, no hyphens).
- Do NOT include punctuation.

OUTPUT FORMAT (must match exactly):
Name: <CatName>

Do NOT add commentary.
Do NOT explain your reasoning.
Output ONLY the single line above.
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "temperature": 0.9}
    )
    return response.json()["response"].strip()

def generate_cat_like_style():
    like_styles = [
    "verbing the noun",
    "adjective noun"
]
    like_style = random.choice(like_styles)
    return like_style

def generate_cat_traits(cat_name):
    sound_styles = [
    "a soft sound",
    "a sharp sound",
    "a silly sound",
    "a mechanical sound",
    "a magical sound",
    "a tiny sound",
    "a grumpy sound",
    "a chirpy sound",
    "a rhythmic sound"
]

    sound_style = random.choice(sound_styles)
    like_letter = random.choice(string.ascii_uppercase)
    like_letter2 = random.choice(string.ascii_uppercase)
    like_style = generate_cat_like_style()
    dislike_letter = random.choice(string.ascii_uppercase)
    dislike_letter2 = random.choice(string.ascii_uppercase)
    dislike_style = generate_cat_like_style()
    sound_letter = random.choice(string.ascii_uppercase)
    prompt = f"""
Generate simple, whimsical traits for a fictional cat.

Cat Name: {cat_name}

RULES:
- Keep each field short (1–4 words).
- Likes and dislikes must be simple (e.g., "sunbeams", "big dogs", "soft blankets").
- The sound can be realistic or surreal, but short (e.g., "purr", "chirp", "sound of a car horn", "engine idling", "bang", "sound of metal scraping", "thwap").
- No full sentences.
- No meta commentary.
- The sound must match this style: {sound_style} and the first word of the sound should start with this letter: {sound_letter}
- The like style must match this style: {like_style} and start with these letters: {like_letter} and {like_letter2}
- The dislike style must match this style: {dislike_style} and start with this letter: {dislike_letter} and {dislike_letter2}


OUTPUT FORMAT (must match exactly):
Likes: <short phrase>
Dislikes: <short phrase>
Sound: <onomatopoeia or short phrase>

Output ONLY these three lines.
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "temperature": 1.0}
    )
    return response.json()["response"].strip()
    
def generate_cat_bio(cat_name, traits_block):
    prompt = f"""
Write a short adoption-style bio for a fictional cat.

Use these details:
Cat Name: {cat_name}
Traits:
{traits_block}

RULES:
- One paragraph only.
- Tone: warm, slightly whimsical, like a real shelter trying to make the cat sound charming.
- Include the cat's likes, dislikes, and sound naturally in the paragraph. Do not capitalize the likes, dislikes, or sound
- When you mention what the cat likes/dislike and the sound it makes, reword it to sound organic and natural.
- You may hint at a tiny backstory, but keep it grounded.
- Do NOT include meta commentary.
- Do NOT list traits; weave them into the prose.

OUTPUT FORMAT (must match exactly):
Bio: <One paragraph>

Output ONLY this single line + paragraph.
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "temperature": 1.6}
    )
    return response.json()["response"].strip()


# ------------------------------------------------------------
# Caption generation (LLM)
# ------------------------------------------------------------
def assemble_cat_caption(name_line, traits_block, bio_block):
    return (
        f"{name_line}\n"
        f"{traits_block}\n\n"
        f"{bio_block}"
    )

def generate_random_cat_elements():
    letter = random.choice(string.ascii_uppercase)

    name_styles = [
        "a realistic pet name",
        "a human name",
        "a nonsense syllable name",
        "a weather-themed name",
        "a plant-themed name",
        "a cute food name",
        "a name inspired by old cartoons",
        "a name that sounds like a tiny wizard",
        "a name inspired by a video game character",
        "a name inspired by a movie character"
    ]

    adoption_flavors = [
        "gentle and shy",
        "bold and mischievous",
        "quiet but affectionate",
        "chaotic but lovable",
        "sleepy and cuddly",
        "curious and adventurous",
        "grumpy but loyal",
        "playful and energetic",
        "mysterious and aloof",
        "clingy and attention-seeking"
    ]

    return {
        "letter": letter,
        "name_style": random.choice(name_styles),
        "adoption_flavor": random.choice(adoption_flavors)
    }

# ------------------------------------------------------------
# Image generation (SD.Next)
# ------------------------------------------------------------
def generate_cat_image(cat_bio):
    traits = [
        "sleepy", "grumpy", "majestic", "chaotic", "tiny", "fluffy",
        "long-haired", "short-haired", "tabby", "calico", "black cat",
        "orange cat", "siamese", "persian", "maine coon"
    ]

    style = random.choice([
        "photorealistic", "studio portrait", "soft natural light",
        "warm indoor lighting", "sunlit window lighting"
    ])

    prompt = (
        f"<lora:hqcat:0.9> <lora:cat_art:0.4> "
        f"{random.choice(traits)} cat portrait, {style}, "
        "solo cat, no people, no person"
        "sharp focus, detailed fur, expressive eyes, "
        f"based on this adoption bio: ({cat_bio})"
    )

    negative_prompt = (
        "human, person, woman, man, people, body, hands, arms, legs, face, "
        "portrait of person, humanoid, doll, statue, figure, "
        "blurry, foggy, low contrast, oversaturated, deformed, "
        "soft focus, AI artifacts, uncanny, malformed, extra limbs, human, ugly, 1 person"
    )

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": "Euler a",
        "width": 512,
        "height": 512,
        "steps": 30,
        "cfg_scale": 7,
        "denoising_strength": 0.3,
        "hr_scale": 2,
  "hr_upscaler": "ESRGAN_4x",
  "hr_second_pass_steps": 20,
  "denoising_strength": 0.3,
  "clip_skip": 1,
  "postprocessing": ["face_restoration", "detailer"],
    "postprocessing_strength": 0.5
    }

    r = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
    data = r.json()

    if "images" not in data:
        raise RuntimeError(f"SD.Next error: {data}")

    return data["images"][0]


# ------------------------------------------------------------
# Save image
# ------------------------------------------------------------
def save_image(b64, path="cat.jpg"):
    log.info("Decoding base64 image...")
    img = Image.open(BytesIO(base64.b64decode(b64)))
    img.save(path)
    log.info(f"Saved image to {path}")
    return path

# ------------------------------------------------------------
# Post to Facebook
# ------------------------------------------------------------
def post_to_facebook(token, image_path, message):
    log.info("Posting to Facebook...")
    graph = facebook.GraphAPI(token)
    post = graph.put_photo(image=open(image_path, "rb"), message=message)
    log.info(f"Facebook post result: {post}")

# ------------------------------------------------------------
# Main workflow
# ------------------------------------------------------------
def main():
    log.info("Starting cat bot run...")

    # Random elements
    elements = generate_random_cat_elements()
    letter = elements["letter"]
    name_style = elements["name_style"]
    adoption_flavor = elements["adoption_flavor"]

    # Facebook token
    token = get_env_token()

    # Load SD model
    load_model()
    time.sleep(2)

    # --- PASS 1A: Cat Name ---
    name_line = generate_cat_name(letter, name_style)
    cat_name = name_line.split(":", 1)[1].strip()

    # --- PASS 1B: Traits ---
    traits_block = generate_cat_traits(cat_name)

    # --- PASS 1C: Adoption Bio ---
    bio_block = generate_cat_bio(cat_name, traits_block)

    # --- PASS 2: Assemble Caption ---
    caption = assemble_cat_caption(name_line, traits_block, bio_block)

    # --- Generate Image ---
    image_b64 = generate_cat_image(bio_block)
    image_path = save_image(image_b64, "cat.jpg")

    # --- Post to Facebook ---
    post_to_facebook(token, image_path, caption)

    log.info("Cat bot run complete.")


if __name__ == "__main__":
    main()


