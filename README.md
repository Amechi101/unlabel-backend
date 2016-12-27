# Unlabel Brand API ( v2.1.0 )

### Overview
The admin will serve the purpose of allowing labels to login, upload product information, and for us to manage all the independent labels that are within our network as well, serving an API for our IOS mobile application to consume and gather all the appropriate information to display within the app.

PostgreSQL will be our database for storing all label information. The admin interface is built using the Django Framework and python as the programming language. We will use Heroku to store and handle our DB and backend infrastructure and the REST API that will be consumed will be built using Django-Tastypie.

An API Client for the REST API will be built using Swift's request system, Alamofire or from scratch using NSMutableURLRequest, NSURL and NSURLSession. The REST API will be in charge of the CRUD operations and the client will talk with the REST API and parse the resulting JSON from the REST API. 

### Tech Stack
- Django/Python ( Website / Admin )
- PostgreSQL ( Database )
- Heroku ( Backend Server )
- Cloudinary ( Hosting Images )
- Django Tastypie ( API )
- IOS/Swift ( Consumes our API )

### Data Models 
This is the link to our [data model.](https://github.com/Amechi101/unlabelapp/blob/master/applications/models.py)

### API Authentication
The REST API will have one link to be consumed by a GET Request from the app. 
`https://unlabel.us/unlabel-network/unlabel-network-api/v1/labels/?username=xxxxxx&api_key=xxxxxxxx`

For authentication this REST API will require username and password within the link. As a suggestion the `usernmame` & `api_key` should  be stored as variables somewhere and be made reference too. The reason being is the secret information can not live on the client side(IOS app) because it can be download by everyone and ready-able available. 
**Only use this method of authentication when consuming the link from the IOS app, never input the API Key and Username in your browser.**

**Use this method instead to view the api in the browser:**
Log into the admin ```https://unlabel.us/unlabel-network-admin``` with your credentials and put this url in your browser `https://unlabel.us/unlabel-network/unlabel-network-api/v1/labels/` to view the JSON data structure.

The REST API will return the following JSON structure below:

```
{
  "meta": {
    "limit": Integer,
    "next": null,
    "offset": Integer,
    "previous": null,
    "total_count": Integer
  },
  "labels": [
    {
      "brand_description": String, 
      "brand_feature_image": String,
      "brand_isActive": Boolean,
      "brand_name": String,
      "brand_city": String,
      "brand_location": String,
      "brand_category": String,
      "created": String,
      "id": String,
      "menswear": Boolean,
      "products": [
        {
          "brand_id": String,
          "product_image": String,
          "product_isActive": Boolean,
          "product_name": String,
          "product_price": Boolean,
          "product_url": String,
          "product_isFemale": Boolean,
          "product_isMale": Boolean,
          "product_isUnisex": Boolean,
        }
      ],
      "resource_uri": String,
      "womenswear": Boolean
    }
  ]
}
```

The REST API contains a `meta` object pertaining to the api metadata. The `limit` key shows the amount of `labels` listed within the set of objects.(1000 per page is the default). The `total_count` key is the total amount of objects returned within the set of 'labels' objects.

To access additional data from the REST API, if available the `next` & `previous` keys will be are URIs to the previous & next pages used to get additional set of `labels` objects from the request. This will keep each request sane and not break the API, or slow down the request.

You can ignore the `offset` key.

The `labels` key is the heart of the REST API, as this will be an array of objects containing all the labels from the database. **brand_isActive** is booleas with the default being false, which always the brand to be displayed on the app if true. **brand_description, brand_feature_image, brand_name, brand_city, brand_location, created, id** are all strings. Some of the more important fields `id` returns the UUID of the brand, `brand_name` returns the name of the label, `created` returns the day the label was created. `products` is an array of objects that has all products information related to the brand. The `brand_id` is the UUID of the brand.

You can refer to the admin for a more detailed look of what each particular field is, and whats going on. Most of the data would have been added here by the time, but this is a high level overview of what the REST API is giving you to manipulate on the client side.



