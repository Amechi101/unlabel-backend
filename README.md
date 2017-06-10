# Unlabel

Types of users : Admin, Brands, Influencers, Customers

### Tech Stack
- Django/Python ( Website / Admin )
- PostgreSQL ( Database )
- AWS EC2 ( Backend Server )
- AWS S3 ( Hosting Images )
- Django REST Framework ( API )
- IOS/Swift ( Consumes our API )

### Overview
Django Oscar provides a permission based dashboard for brands and unlabel admin. The dashboard will allow to add or track
product information, stock information, user information etc. Permission based dashboard allows limited functionality 
for brands and a fully functional dashboard for admin. The django REST api provide all the information needed for the Influencers 
iOS app as JSON data.

We use postgreSQL as database and and AWS S3 bucket for storing images.
We also use the SNS service provided by Amazon for handling push notification.
Imfluencers use the iOS app. The app communicates to our backend with the help of REST api which provided response in JSON format.


### Modules
address	
analytics
basket
catalogue
checkout
customer
dashboard
offer
order
partner
payment
promotions
search	
shipping
voucher	
wishlists
Influencers
Some of the modules are from Django Oscar which are customized to meet our requirements.
https://github.com/Amechi101/unlabel-backend/tree/develop/oscarapps




