const cheerio = require('cheerio');

const baseUrl = 'https://cn.nytimes.com/';
const linkClassSelector = '.regularSummaryHeadline > a'; // Update with your desired class selector

async function scrapeLinksAndParseContent(url) {
  try {
    const response=await fetch(baseUrl,{method:"GET"})
    const $ = cheerio.load(await response.text())

    // Extract links with the specified class selector from the current page
    const links = [];
    $(linkClassSelector).each((index, element) => {
      const link = $(element).attr('href');
      if (link) {
        const absoluteUrl = new URL(link, baseUrl).href;
        links.push(absoluteUrl);
      }
    });

    // Fetch and parse content from the extracted links
    const contentPromises = links.map(async link => {
      try {
        const response = await fetch(link,{method:"GET"});
        const $ = cheerio.load(await response.text());

        const title = $(".article-header h1").text();
        const content=[]
        $('.article-paragraph').each((index, element) => {
            $element=cheerio.load(element)  
            if($element('img').length==0)  
              content.push($(element).text())
          });

        console.log("Title: ",title)
        console.log("Content: ",content.join('\n\n'))
        console.log("-".repeat(50))
        
	
      } catch (error) {
        console.error('Error fetching and parsing data from', link, ':', error);
      }
    });

    await Promise.all(contentPromises);
  } catch (error) {
    console.error('Error fetching and parsing data:', error);
  }
}

// Start by scraping links and parsing content from the base URL
scrapeLinksAndParseContent(baseUrl)
  .then(() => console.log('Done'))
  .catch(error => console.error('Error:', error));



