import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class ChamberSpider(scrapy.Spider):
    name = "chamber"
    start_urls = [f'https://chambermaster.pompanobeachchamber.com/list/searchalpha/{letter}' for letter in 'abcdefghijklmnopqrstuvwxyz']

    def parse(self, response):
        # Extract the data for each member on the page
        for member in response.css('.gz-list-card-wrapper'):
            website = member.css('.card-header a::attr(href)').get()
            yield response.follow(website, self.parse_member)

    def parse_member(self, response):
        # Extract the data for the member's website
        business_name = response.css('h1.gz-pagetitle::text').get()
        rep_name = response.css('.gz-member-repname::text').get()
        try:
            rep_first_name, rep_last_name = rep_name.split(' ')
        except:
            rep_first_name = None
            rep_last_name = None
        rep_title = response.css('.gz-member-reptitle::text').get()
        website = response.xpath('//li[@class="list-group-item gz-card-website"]/a/@href').get()
        phone = response.css('li.list-group-item.gz-card-phone span::text').get()
        email = ''
        category = response.css('span.gz-cat::text').get()

        # Append data to the dataframe
        df = pd.DataFrame(data=[[business_name, rep_first_name, rep_last_name, rep_title, phone, email, website, category]],
                         columns=["Business Name", "Contact First Name", "Contact Last Name", "Contact Position", "Phone Number", "Email", "Website", "Business Category"])
        df_list.append(df)

# Initialize an empty dataframe and a list to store dataframes
df_list = []
df = pd.DataFrame(columns=["Business Name", "Contact First Name", "Contact Last Name", "Contact Position", "Phone Number", "Email", "Website", "Business Category"])

# Start the scraping process
process = CrawlerProcess()
process.crawl(ChamberSpider)
process.start()

# Concatenate all dataframes in the list
df = pd.concat(df_list, ignore_index=True)

# Sort the dataframe by Business Category and Business Name
df.sort_values(by=["Business Category", "Business Name"], inplace=True)

# Save the dataframe to an Excel file
df.to_excel("Business_Info_PBC.xlsx", index=False)
