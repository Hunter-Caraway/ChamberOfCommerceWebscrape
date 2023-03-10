import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class ChamberSpider(scrapy.Spider):
    name = "chamber"
    start_urls = ['https://chamber.hollywoodchamber.org/list/search?q=&c=&sa=False&gr=25&gn=']

    def parse(self, response):
        # Extract the data for each member on the page
        for member in response.css('.card-header'):
            website = member.css('a::attr(href)').get()
            yield response.follow(website, self.parse_member)

    def parse_member(self, response):
        # Extract the data for the member's website
        print('working!')
        business_name = response.css('.gz-details-header meta[itemprop="name"]::attr(content)').get()
        categories = response.css('.gz-details-categories p span::text')[0].get()
        website = response.css('.gz-details-links .gz-list-group .gz-card-website a::attr(href)').get()
        phone = response.css('.gz-details-links .gz-list-group .gz-card-phone span::text').get()
        email = response.css('.gz-details-links .gz-list-group .gz-card-email a::text').get()
        rep_name = response.css('.gz-member-repname::text').get()
        try:
            rep_first_name, rep_last_name = rep_name.split(' ')
        except:
            rep_first_name = None
            rep_last_name = None

        # Append data to the dataframe
        df = pd.DataFrame(data=[[business_name, rep_first_name, rep_last_name, phone, email, website, categories]],
                         columns=["Business Name", "Contact First Name", "Contact Last Name", "Phone Number", "Email", "Website", "Business Category"])
        df_list.append(df)

# Initialize an empty dataframe and a list to store dataframes
df_list = []
df = pd.DataFrame(columns=["Business Name", "Contact First Name", "Contact Last Name", "Phone Number", "Email", "Website", "Business Category"])

# Start the scraping process
process = CrawlerProcess()
process.crawl(ChamberSpider)
process.start()

# Concatenate all dataframes in the list
df = pd.concat(df_list, ignore_index=True)

# Sort the dataframe by Business Category and Business Name
df.sort_values(by=["Business Category", "Business Name"], inplace=True)
df.to_excel("Business_Info_HCC.xlsx", index=False)