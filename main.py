import argparse
from GeneratePosts import QuoteImageGenerator
from pinterestScraper import ImgScraper

def main():

    parser = argparse.ArgumentParser(description="Post Generator")
    parser.add_argument("-th", "--theme", type=str, default='of your choice', help="Specify prefered theme for quotes")
    parser.add_argument("-ops", "--options", type=int, default=0, help="Specify nb of bg options to manually choose from")
    parser.add_argument("-p", "--post", action="store_true", help="Post on instagram")
    args = parser.parse_args()

    # Generating quotes
    generator = QuoteImageGenerator()
    prompt = f"give me dope aesthetic short (max 10 words) 3 quotes with the theme {args.theme}. your response need to be exactly like this 'theme:[theme here],\nquote1:[quote1],\nquote2:[quote2],\nquote3:[quote3],\nHashtags:[all possible hashtags],\nSearch: pinterest search link for background image,\n'"
    
    generated_content = generator.get_generated_quotes(prompt)

    # getting backgroung image
    imgScraper = ImgScraper()
    bg_image_url = imgScraper.getBgUrlByTheme(generated_content['search'],args.options)
    imgScraper.quit()

    # Generating Posts using bg img and generated quotes
    generator.generate(bg_image_url,generated_content)

    if args.post :
        instaBot = InstagramBot()
        instaBot.login()
        instaBot.createPost(generated_content)
        instaBot.quit()
    

if __name__ == "__main__":
    main()