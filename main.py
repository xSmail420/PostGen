import argparse
from GeneratePosts import QuoteImageGenerator
from pinterestScraper import ImgScraper

def main():

    parser = argparse.ArgumentParser(description="Post Generator")
    parser.add_argument("-th", "--theme", type=str, default='optional', help="Specify prefered theme for quotes")
    args = parser.parse_args()

    # Generating quotes
    generator = QuoteImageGenerator()
    prompt = f"give me dope aesthetic short (max 10 words) 3 quotes with the same theme: {args.theme}. your response need to be 'theme:[key word to search for appropiate thumbnail image with],\n quote1:[quote1],\n quote2:[quote2],\n quote3:[quote3],\n Hashtags:[all possible hastags],\n Search:[a pinterest search as a link to get an eye catching ,background image, matching the theme],\n'"
    
    generated_content = generator.get_generated_quotes(prompt)
    

    # getting backgroung image
    imgScraper = ImgScraper()
    bg_image_url = imgScraper.getBgUrlByTheme(generated_content['search'])
    imgScraper.quit()

    # Generating Posts using bg img and generated quotes
    generator.generate(bg_image_url,generated_content)
    

if __name__ == "__main__":
    main()