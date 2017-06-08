import json
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from oscar.apps.catalogue.models import Category,ProductClass
from oscarapps.catalogue.models import Product
from oscarapps.partner.models import Style
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
from push_notification.models import APNSDevice, NotificationDetails, SNS


class Command(BaseCommand):
    """
    To add initial data for
    categories and product types.
    """
    help = "To add initial data for categories and product types."

    def handle(self, *args, **options):

        gen = Category.add_root(name="Women")
        base_root = gen.add_child(name="Clothing")

        root = base_root.add_child(name="Pants")
        pants = ["Tapered","Skinny","Straight Leg","Flared","Culottes","Leather","Joggers","Boot Cut"]
        for pant in pants:
            child1 = root.add_child(name=pant)

        root = base_root.add_child(name="Jeans")
        jeans = ["Boyfriend","Skinny","Straight Leg","Flared","High Rise","Mid Rise","Low Rise","Distressed","Boot cut"]
        for jean in jeans:
            child1 = root.add_child(name=jean)

        root = base_root.add_child(name="Dresses")
        Dresses = ["Midi","Mini","Maxi","Knee Length"]
        for dress in Dresses:
            child1 = root.add_child(name=dress)

        root = base_root.add_child(name="Coats & Jackets")
        coats = ["Blazers","Vests","Coats","Denim Jacket","Leather Jacket","Puffer Jacket","Low Rise","Distressed","Boot cut"]
        for coat in coats:
            child1 = root.add_child(name=coat)

        root = base_root.add_child(name="Jumpsuits & Rompers")
        suits = ["Jumpsuits","Rompers"]
        for suit in suits:
            child1 = root.add_child(name=suit)

        root = base_root.add_child(name="Shorts")
        shorts = ["Denim","Mid Length","Short" ]
        for short in shorts:
            child1 = root.add_child(name=short)

        root = base_root.add_child(name="Skirts")
        Skirts = ["Denim","Leather","Midi","Mini","Maxi","Pencil"]
        for Skirt in Skirts:
            child1 = root.add_child(name=Skirt)

        root = base_root.add_child(name="Sweater and Knits")
        Sweaters = ["Sweaters","Cardigan","Cashmere","Sweatshirts & Hoodies","Turtleneck"]
        for Sweater in Sweaters:
            child1 = root.add_child(name=Sweater)

        root = base_root.add_child(name="Activewear")
        actives = ["Top","Bottoms"]
        for active in actives:
            child1 = root.add_child(name=active)

        root = base_root.add_child(name="Tops")
        tops = ["Tee shirts","Button Down","Blouses/Tunics","Long Sleeve","Short Sleeve","Sleeveless","Cropped tops"]
        for top in tops:
            child1 = root.add_child(name=top)

        base_root = gen.add_child(name="Bag")
        bags = ["Bagpacks","Satchels","Shoulder Bags","Crossbody","Totes","Bucket Bag","Travel Bag","Clutches","Wallets"]
        for bag in bags:
            child1 = base_root.add_child(name=bag)

        base_root = gen.add_child(name="Jewelry")
        jewelry = ["Earrings","Rings","Body Jewelry","Necklaces","Watches"]
        for jewel in jewelry:
            child1 = base_root.add_child(name=jewel)

        base_root = gen.add_child(name="Shoes")

        root3 = base_root.add_child(name="Flats")

        root2 = base_root.add_child(name="Sneakers")

        root1 = base_root.add_child(name="Sandals")

        root = base_root.add_child(name="Heels & Wedges")

        heels = ["High Heels","Midi Heels","Kitten Heels","Wedges Heels","Pumps"]
        for heel in heels:
            child1 = root.add_child(name=heel)

        root = base_root.add_child(name="Boots")
        boots = ["Ankle Boots","Knee High Boots","Over the Knee Boots","Rain Boots","High Heel Boots"]
        for boot in boots:
            child1 = root.add_child(name=boot)

        base_root = gen.add_child(name="Accessories")

        root = base_root.add_child(name="Scarves")

        root = base_root.add_child(name="Belts")

        root = base_root.add_child(name="Hats")
        hats = ["Baseball Caps","Fedora","Sun Hat","Beanies"]
        for hat in hats:
            child1 = root.add_child(name=hat)

        root = base_root.add_child(name="Sunglasses")
        glasses = ["Aviators","Round Frames","Cat Eye","Square Frames"]
        for glass in glasses:
            child1 = root.add_child(name=glass)

        root = base_root.add_child(name="Other Accessories")

        gen = Category.add_root(name="Men")
        base_root = gen.add_child(name="Clothing")

        root = base_root.add_child(name="Pants")
        pants = ["Tapered","Skinny","Straight Legged","Joggers/ sweatpants","Chino","Trousers"]
        for pant in pants:
            child1 = root.add_child(name=pant)

        root = base_root.add_child(name="Jeans")
        jeans = ["Relaxed","Skinny","Straight Legged","Boot Cut","Distressed","Trousers","Jeans"]
        for jean in jeans:
            child1 = root.add_child(name=jean)

        root = base_root.add_child(name="Activewear")
        root1 = root.add_child(name="Tops")
        tops = ["Short Sleev","Tanks","Long Sleeve","Sweatshirts"]
        for dress in tops:
            child1 = root1.add_child(name=dress)
        root1 = root.add_child(name="Bottoms")
        tops = ["Shorts","Sweat pant","Jogging pants","Tights"]
        for dress in tops:
            child1 = root1.add_child(name=dress)
        root1 = root.add_child(name="Outerwear")
        tops = ["WindBreaker","Rain Jacket","Insulated","Fleece Jacket"]
        for dress in tops:
            child1 = root1.add_child(name=dress)


        root1 = base_root.add_child(name="Coats and Jacket")
        tops = ["Blazers","Vests","Coats","Denim Jacket","Leather Jacket","Puffer Jacket",
                "Parka","Moto/ Bomber Jacket","Rain Coat","Parka/ Anorak and others"]
        for dress in tops:
            child1 = root1.add_child(name=dress)

        root1 = base_root.add_child(name="Shorts")
        tops = ["Above the knee","Below the knee","Knee Length"]
        for dress in tops:
            child1 = root1.add_child(name=dress)

        root1 = base_root.add_child(name="Sweaters and Knits")
        tops = ["Sweaters","Cardigan","Cashmere","Sweatshirts & Hoodies","Turtleneck","Crew neck","V  neck"]
        for dress in tops:
            child1 = root1.add_child(name=dress)

        root1 = base_root.add_child(name="Tops")
        tops = ["Tee shirts","Tank Tops","Button Down","Long Sleeve","Short Sleeve","Sleeveless","Polos"]
        for dress in tops:
            child1 = root1.add_child(name=dress)

        base_root = gen.add_child(name="Bags")
        items = ["Bag packs","Messenger & Duffel bags","Tote Bags","Bag packs","Travel Bag","Wallets & Card Holders"]
        for item in items:
            child1 = base_root.add_child(name=item)

        base_root = gen.add_child(name="Jewelry")
        items = [" Earrings","Rings","Necklaces","Watches","Bracelets"]
        for item in items:
            child1 = base_root.add_child(name=item)

        base_root = gen.add_child(name="Shoes")
        root1 = base_root.add_child(name="Sneakers")
        items = ["High Top","Low Top","Slip-ons"]
        for item in items:
            root = root1.add_child(name=item)
        root1 = base_root.add_child(name="Dress Shoes")
        root1 = base_root.add_child(name="Loafers & Slip-ons")
        root1 = base_root.add_child(name="Boots")
        items = ["Chukka","Rugged","Chelsea Boots","Rain Boots","Winter Boots"]
        for item in items:
            child1 = root1.add_child(name=item)

        base_root = gen.add_child(name="Accessories")
        root = base_root.add_child(name="Scarves & Gloves")
        root1 = root.add_child(name="Scarves")
        root1 = root.add_child(name="Gloves")
        root = base_root.add_child(name="Belts")
        root = base_root.add_child(name="Hats")
        items = ["Baseball Caps","Fedora","Straw Hat","Beanies & winter hats","Other hats"]
        for item in items:
            root1 = root.add_child(name=item)
        root = base_root.add_child(name="Sunglasses")
        items = ["Aviators","Round frames","Square Frames","Wayfarers","Others"]
        for item in items:
            root1 = root.add_child(name=item)

        root = base_root.add_child(name="Ties & Cufflinks")
        root = base_root.add_child(name="Socks")
        root = base_root.add_child(name="Other Accessories")

        print("")
        print("Categories and sub categories added.")

        items = ["Pants","Jeans","Activewear","Dresses","Coats & Jackets","Jumpsuits & Rompers","Shorts","Skirts",
                 "Sweater and Knits","Activewear","Tops","Bags","Jewelry","Shoes","Scarves","Gloves","Belts","Hats",
                 "Ties & Cufflinks","Socks","Sunglasses","Other Accessories"]
        for item in items:
            new_product_class = ProductClass.objects.create(name=item)
            new_product_class.save()

        print("")
        print("Product types added. ")

        style_name=["Avant-Garde","Athletic","Bohemian","Casual","Classic","Contemporary","Dressy","Eccentric","Formal",
                    "Goth + Rocker","Hipster","Minimal","Modern","Preppy + Yacht","Quirky","Skater + Surfer","Streetstyle",
                    "Vintage"]
        style_desc = ["Avant-Garde is architectural, edgy and ultramodern and often makes a dramatic statement. The designs are new, unusual or experimental ideas.",
                      "Designed for athletic workouts at a gymnasium, referred to as active wear. It is designed to keep the activity, comfort and practicality in mind.",
                      "Bohemian, or boho, style is relaxed and lived in & free-spirited with an emphasis on natural fabrics, earthy tones & gypsy looks. This style is often called hippie-chic, or even boho-chic.",
                      "A  more informal attire for men and women, worn outside of the formal setting. The clothing are informal and emphasize relaxation.",
                      "Characterized by tailored & clean cuts, a style that has stood the test of time and never looks out dated.",
                      "Popular & trendy designs that are in vogue for one season and then are replaced with new fashions that better reflect the fashion market.",
                      "Ensembles and pieces with sleek clean lines and has an innate sense of formality and elegance.",
                      "Bold, different and daring define this style. The style is adventurous , risky and meant to stands out.",
                      "Upscale clothing that is worn at formal social events like weddings or formal parties.",
                      "Style marked by conspicuously dark, mysterious, antiquated and complex features.",
                      "Defined by individualism, the style favors unconventional patterns and uncommon trends",
                      "Extreme simplicity, clean cuts and monotone color pallet with emphasis on Less is More",
                      "A combination of trends and representative of modern tastes and lifestyles. The modern style is seasonal and changes from one season to the next.",
                      "Characterized by neat and high class look. The style is very close to classic and favors timeless pieces over trendy.",
                      "With natural ability to mix and match colors, patterns, and textures, the style type is playful  & stands out.",
                      "Style that gives a young at heart, easy going and athletic vibe and created with skateboarding and surfing cultures in mind.",
                      "Style established and made popular by youth culture. The fashion is representative of culture and not created in the studios.",
                      "Style is retro and hints at a specific period of fashion from a bygone era."]

        for index in range(0,17):
            style = Style.objects.create(name=style_name[index],description=style_desc[index])
            style.save()
        print("")
        print("Styles added.")
        print("")
