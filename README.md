# SquarespaceProductManager
A personal one-offish project to bulk edit a list of products while moving from Wordpress to Squarespace

Due to Squarespace being unable to bulk import digital products, I created Service Products for the eBooks and Audiobooks.

Once the products are imported, they are then exported to a google sheet where additional information needed to describe the product and fulfill the orders is added.

This script reads from a csv exported from the google sheet.

The site uses blog posts for Author Bios and Editorial Reviews.
I didn't automate the generation of Author Bio blog posts. But it is a TODO item and will add an additional column in the spreadsheet.

Using the spreadsheet information, the script:

* adds a blog post for the editorial reviews using the book title as a tag
* updates the custom button
* adds Additional Information

The script uses a ~/.squarespacemanager.config.ini file to store login credentials and website urls

Read the comments in the script for more information on what the script accomplishes.

There is a fair amount of duplicate(ish) code. Don't judge. The purpose was to take the shortest path to migration. There's a lot of room for improvement.
Note also that Squarespace seems to frequently change css classes which breaks some of the methods. So, there's room to improve the script using better element discovery.

Also, there's absolutely zero error handling. That's another TODO.

While not a part of this script, it is worth noting that I configured a pipedream workflow to deliver the eBooks and Audiobooks to customers to fulfill their orders. The workflow makes use of the same google spreadsheet. It extracts the google drive link to the downloadable files and delivers the links via gmail.

I know people are looking for a way to solve for the limitations of Squarespace Digital Products. I found this solution to be workable.
