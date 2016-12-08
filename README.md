# Technology Stack
### Language
- Python
- Swift

### Infrastructure
- AWS Ec2
- AWS s3
- AWS Cloudfront

### Server Technologies
- Django


### Database
- PostgreSQL

### Third Party Tools
-


# Backend (Administration)

## Master Module
This module contains the dashboard that controls the entire application. Anyone can be given access to login into the master module if they are made superusers. The master module as well has two **sub modules** called brand module & influencer module. 

## Sub Modules
Sub modules contain global/specific settings & data models. Each of the sub modules have the ability to generate links to create **Sub module components**. 
- Sub modules contain specific settings that apply to the individual module only.
- Sub modules have shared settings that apply to both modules.
- Sub modules contain data models that apply to the individual module only.
- Sub modules have shared data models that apply to both modules.

### Sub Module components:
Sub modules componets are made from the sub module brand or influencer. They are essentially mini applications that has a dashboard. They are created from their respective sub modulues and house data for brands or influencers which in turn is then stored in our database. Each component has an internal API that links to the root sub module.

## Module API's
Module API's have a two way communication

### Sub module to Sub module: 
-

### Sub module to Sub module components: 
-

### Sub module to IOS APP:
-

## Module Architecture
### Master Module:
**(i)  Ability to change settings & data models for each sub module.**

**(ii) Create, update, delete and view each sub module's stats & information from their components.**

### Sub Modules: 
#### Global settings
-

#### Specific settings
##### *Brand sub module*
-

##### *Influencer sub module*
-

#### Global data models
-

#### Specific data models
##### *Brand sub module*
-

##### *Influencer sub module*
-

### Brand sub module component:
**(i) Brand Information**

`a) Add Information`

1. Store Name
2. Store Image
3. City
4. State (USA) or Country (international)
5. Description
6. Brand Style Preference (Many to Many Foreign Key relationship to Style Model)
7. Brand Store Sex Type (Multiple choices) - ie Male, Women, Both
8. Brand Store Categories (Multiple choices) - ie Clothing, Accessories,..
9. Brand Website
10. Activate or Deactivate store (this will hide all information associated with brand within the app to be viewed by users)

`b) Edit Information - (i)`

**(ii) View Stats (Show based on a date range, default by current month)**

`a) New customers`
`b) Product sold`
`c) Orders`
`d) Avg order value`
`e) Revenue this period`
`f) Total revenue`
`g) Tax collected`
`h) Shipping collected`
`i) Order revenue graph`
`j) Low stock`
`k) Completed orders`
`l) Top sellers`
`m) Top customers`
`n) Store Views & Impressions`
`o) Product likes`
`p) Follows`

**(iii) Inventory Management - products**

`a) Create`

1. Name
2. Description
3. Color
4. SKU #
5. Care Info Description
6. Size & Fit Description
7. Size
8. Price
9. Image
10. Product Qty
11. Product Stock - ie Low in stock, out of stock ( based on product qty )
12. Item sex - ie Men, Women, Unisex
13. Modified
14. Created 
15. Product attribute - Shirt, Jewelry... etc

`b) Edit - (iii)`
`c) Delete - (iii)`
`d) View - (iii)`
`e) Search - (iii)`

**(iv) Order Management**

`a) Search`
`b) List`
`c) View`
`d) Filter`
`e) Change status`

**(v) Shipping**

`a) Change status`

**(vi) Taxes**

`a) Configure tax`

**(vii) Discounts**

`a) Discount configurations`

1. Fixed discount - ie get £5 off DVDs
2. Percentage discount - ie get 25% off books

**(viii) Currencies**

`a) Set base currency`
`b) (Currency switching in site based using a third party tool like(https://openexchangerates.org/)`

**(ix) Languages(Currently we are using English only)**

**(x) Shipping details can be updated (Like status) - (There is no integration with the third party services - That will be managed manually using their interface)**

**(xi) Multiple currencies**

**(xii) Commission logic implementation**

**(xiii) Sending money to brand**

`a) Using - PayPal payout`
`b) Based on a threshold of the amount`
`c) Brands need to get a PayPal ID for this and that need to be updated in there admin dashboard`

**(xiv) Payment gateway (credit cards only ) for now**

**(xv) Personal Information**

`a) edit - (xv)`

1. email
2. username
3. password
4. full name
5. last name

### Influencer sub module component:
**(i) Influencer Information**

`a) add`

1. Image
2. City
3. State (USA) or Country (international)
4. Bio
5. Style Preference (Many to Many Foreign Key relationship to Style Model)
6. Industry (Multiple choices) - ie Fashion, Tech, Fitness
7. Instagram URL
8. Website
9. Activate or Deactivate influencer (this will hide all information associated with influencer within the app to be viewed by users)

`b) Edit Information - (i)`

**(ii) Personal Information**

`a) edit - (ii)`

1. email
2. username
3. password
4. full name

**(iii) Collections** 

`a) Add`

1. Name
2. Description
3. Select Products *(Many to Many Foreign Key relationship)* - ie You see a list of brands from the `sub module brand API, *See Module API's*`, then all the products related to each brand. An Influencer can only see brands that have the same style preferences they have. Each product can only be selected once by an influencer to be added to their collection, if selected it wont be available for other influencers to add into their collection, until the influencer removes the product from their collection, deletes their collection or if a brand removes the product. Here is an example of what the selection UI would look like: http://recordit.co/kT6NT5msi6
4. Modified
5. Created 

`b) Edit - (iii)`
`c) Delete - (iii)`
`d) View - (iii)`
`e) Search - (iii)`

**(iv) View Stats (Show based on a date range, default by current month)**

`a) View individual products sold per collection` 
`b) View total overall sales commission received for all collections & View total overall sales per collection`

**(v) Billing**

`a) payment details`

1. Credit card & Billing address
- add
- update
- delete

`b) Receipts`

1. Download invoice as PDF

`c) Change subscription level`

1. Default plan

- Curator gets 1.5% commission for items that actually sell from their collections.
- Can make unlimited collections 

`d) Change Billing Cycle`

1. Monthly  - default
2. Yearly

# Front-End (Client side)

## IOS
