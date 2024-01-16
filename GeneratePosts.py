from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import requests
from io import BytesIO
import re
import time
from openai import OpenAI

class QuoteImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key="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")
        self.font_path = "static/Raleway-Regular.ttf"
        self.font_size = 30
        self.v_margin = 10
        self.char_limit = 25
        self.text_color = "white"

        # Initialize the font attribute
        self.font = ImageFont.truetype(self.font_path, self.font_size)

    def get_generated_quotes(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        quotes_string = response.choices[0].message.content.strip()
        
        # Extract the theme using regular expression
        theme_pattern = re.compile(r'theme:(.*?),', re.IGNORECASE)
        theme_match = theme_pattern.search(quotes_string)
        theme = theme_match.group(1).strip() if theme_match else None

        # Define a regular expression pattern to match the quotes
        quote_pattern = re.compile(r'quote(.*)"')
        # Use the findall method to extract all matches
        result = quote_pattern.findall(quotes_string)
        quotes= [s.split('"', 1)[1].strip() for s in result]

        # Define a regular expression to find the text after 'Hashtags:'
        hashtags_pattern = re.compile(r'Hashtags:(.*)\n')
        # Find the first match in the text
        hashtags = hashtags_pattern.search(quotes_string)
        hashtags = hashtags.group(1).strip()

        # Define a regular expression to find the text after 'Search:'
        search_pattern = re.compile(r'Search:(.*)')
        # Find the first match in the text
        search = search_pattern.search(quotes_string)
        search = search.group(1).strip()

        return {'theme': theme, 'quotes': quotes, 'hashtags': hashtags, 'search': search}

    def get_y_and_heights(self, text_wrapped, dimensions):
        ascent, descent = self.font.getmetrics()

        # Calculate the height needed to draw each line of text (including its bottom margin)
        line_heights = [
            self.font.getmask(text_line).getbbox()[3] + descent + self.v_margin
            for text_line in text_wrapped
        ]
        # The last line doesn't have a bottom margin
        line_heights[-1] -= self.v_margin

        # Total height needed
        height_text = sum(line_heights)

        # Calculate the Y coordinate at which to draw the first line of text
        y = (dimensions[1] - height_text) // 2

        # Return the first Y coordinate and a list with the height of each line
        return (y, line_heights)

    def generate(self, bg_image_url, generated_content):
        # Generated quotes using GPT-3 API
        generated_quotes = generated_content['quotes']
        print(f'image background url :{bg_image_url}')
        try:
            # Fetch the background image from the URL
            response_bg = requests.get(bg_image_url)
            background_image = Image.open(BytesIO(response_bg.content))
            time.sleep(3)
        except:
            print('fetching image failed')
            background_image = Image.open("static/Background_frame.png")

        # Fetch the foreground image (local file)
        foreground_image = Image.open("static/Foreground_frame.png")

        # Rest of the code remains the same
        WIDTH, HEIGHT = min(background_image.width, background_image.height), min(background_image.width, background_image.height)

        img = Image.new("RGB", (WIDTH, HEIGHT))
        img.paste(background_image, (0, -(max(background_image.width, background_image.height) - WIDTH)//2 ))

        new_foreground_width = int(WIDTH * 0.8)
        aspect_ratio = foreground_image.width / foreground_image.height
        new_foreground_height = int(new_foreground_width / aspect_ratio)

        foreground_image = foreground_image.resize((new_foreground_width, new_foreground_height))

        foreground_x = (WIDTH - new_foreground_width) // 2
        foreground_y = (HEIGHT - new_foreground_height) // 2

        img.paste(foreground_image, (foreground_x, foreground_y), mask=foreground_image)

        print(f'Theme :{generated_content["theme"]}')
        print(f'Hashtags :{generated_content["hashtags"]}')

        for index, quote_text in enumerate(generated_quotes):
            print(f'quote{index}: {quote_text}')

            post = Image.new("RGB", (WIDTH, HEIGHT))
            post.paste(img, (0, 0))

            draw_interface = ImageDraw.Draw(post)

            quote_lines = wrap(quote_text, self.char_limit)

            y, line_heights = self.get_y_and_heights(
                quote_lines,
                (new_foreground_width, new_foreground_height),
            )

            for i, line in enumerate(quote_lines):
                line_width = self.font.getmask(line).getbbox()[2]
                x = ((new_foreground_width - line_width) // 2) + foreground_x

                draw_interface.text((x, y + foreground_y), line, font=self.font, fill=self.text_color)
                y += line_heights[i]

            post.save(f"./posts/img{index}.png")

