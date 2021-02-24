import json


def test_get_menu(client):
    """Test the endpoint to get the menu."""
    payload = {
        'name': 'Milk'
    }

    response = client.get('/get_menu', data=json.dumps(payload))

    assert response.status_code == 200
    assert "menu" in response.json
    assert len(response.json["menu"]) == 17
    assert response.json == {
        "menu": [
            {
                "description": "Give the bartender you order and they will make it!",
                "img": "https://i.imgur.com/UOmoDv9.png",
                "in_stock": True,
                "item_id": "prod_Izhm4f2EyN8AY6",
                "name": "Make your Own Cocktail",
                "price": 3.99,
                "type": "Drink"
            },
            {
                "description": "Fettuccine pasta served with grilled shrimp and creamy alfredo sauce.",
                "img": "https://i.imgur.com/tQPIm8d.png",
                "in_stock": True,
                "item_id": "prod_IzhmCLlBqOvLot",
                "name": "Shrimp Alfredo",
                "price": 12.0,
                "type": "Meal"
            },
            {
                "description": "A slice of creamy cheese cake with a crispy outer crust.",
                "img": "https://i.imgur.com/gS4cqrp.jpg",
                "in_stock": True,
                "item_id": "prod_IzhmJi2h8Lug6F",
                "name": "Cheese Cake Slice",
                "price": 4.99,
                "type": "Dessert"
            },
            {
                "description": "Sweet milk chocolate lava cake served with rich vanilla bean ice cream.",
                "img": "https://i.imgur.com/lC82VJT.jpg",
                "in_stock": True,
                "item_id": "prod_IzhmYEV50XfE9T",
                "name": "Chocolate Lava Cake",
                "price": 5.99,
                "type": "Dessert"
            },
            {
                "description": "Your choice from a select number of beers.",
                "img": "https://i.imgur.com/UOmoDv9.png",
                "in_stock": True,
                "item_id": "prod_IzhmZeKlcVF75Q",
                "name": "Beer",
                "price": 0.99,
                "type": "Drink"
            },
            {
                "description": "House BLT sandwich with crispy bacon, juicy tomato, spinach, and avocado spread. "
                               "Served with your choice of fries or fresh veggies.",
                "img": "https://files.stripe.com/links/fl_test_wgadTXx9GPlnNJw0WpQHiHfD",
                "in_stock": True,
                "item_id": "prod_IzhmbOCzU9vUYN",
                "name": "BLT Sandwich",
                "price": 4.5,
                "type": "Meal"
            },
            {
                "description": "Juicy double patty burger topped with caramelized onions, mayo, and tater tots. "
                               "Served with your choice of fries or tater tots. ",
                "img": "https://i.imgur.com/irjuVgs.png",
                "in_stock": True,
                "item_id": "prod_Izhmbe6e8ozffz",
                "name": "Mushroom Burger with Tater Tots",
                "price": 9.99,
                "type": "Meal"
            },
            {
                "description": "Crispy chicken served on top of a buttery waffle with maple syrup.",
                "img": "https://i.imgur.com/32Rz9uS.png",
                "in_stock": True,
                "item_id": "prod_IzhmeB1DYzcERU",
                "name": "Chicken and Waffles",
                "price": 10.99,
                "type": "Meal"
            },
            {
                "description": "A mix of orange juice and Prosecco.",
                "img": "https://i.imgur.com/UOmoDv9.png",
                "in_stock": True,
                "item_id": "prod_IzhmfPUg6tM3zH",
                "name": "Sunrise Mimosa",
                "price": 2.99,
                "type": "Drink"
            },
            {
                "description": "12 oz soda.",
                "img": "https://i.imgur.com/UOmoDv9.png",
                "in_stock": True,
                "item_id": "prod_Izhmhoan4eg7XR",
                "name": "Canned Soda",
                "price": 1.0,
                "type": "Drink"
            },
            {
                "description": "Tacos with your choice of steak, chicken, or fish. Served with limes, cilantro, "
                               "and chopped onions",
                "img": "https://i.imgur.com/RLPm3rb.png",
                "in_stock": True,
                "item_id": "prod_IzhmjRqoRfqJGo",
                "name": "Street Tacos",
                "price": 8.99,
                "type": "Meal"
            },
            {
                "description": "A rich three-layered slice of strawberry cake with vanilla icing.",
                "img": "https://i.imgur.com/XR4mN14.png",
                "in_stock": True,
                "item_id": "prod_IzhmoqKRolTyPP",
                "name": "Strawberry Cake Slice",
                "price": 4.99,
                "type": "Dessert"
            },
            {
                "description": "Pan-seared juicy ribeye steak topped with butter, garlic, and rosemary.",
                "img": "https://i.imgur.com/PomPqle.jpg",
                "in_stock": True,
                "item_id": "prod_IzhmtV8IBA39Zu",
                "name": "Steak Dinner",
                "price": 21.99,
                "type": "Meal"
            },
            {
                "description": "A warm dish of sweet apples and apple crisp. Served with vanilla ice cream.",
                "img": "https://i.imgur.com/RKS9pzv.jpg",
                "in_stock": True,
                "item_id": "prod_IzhmzwgeL9HZys",
                "name": "Apple Crisp",
                "price": 7.0,
                "type": "Dessert"
            },
            {
                "description": "Juicy squid legs.",
                "img": "https://i.imgur.com/F47tdPH.png",
                "in_stock": True,
                "item_id": "prod_Izqnu1N4zvLOgV",
                "name": "Squid Legs",
                "price": 12.99,
                "type": "Meal"
            },
            {
                "description": "Cinnamon Milk with a hint of vanilla.",
                "img": "https://i.imgur.com/UOmoDv9.png",
                "in_stock": True,
                "item_id": "prod_Izqv5pHkCWuSoM",
                "name": "Horchata",
                "price": 3.99,
                "type": "Drink"
            },
            {
                "description": "The Krusty Crab's house favorite salted patty with cheese, lettuce, and pickles.",
                "img": "https://i.imgur.com/lINpkP7.png",
                "in_stock": True,
                "item_id": "prod_J08aSoufjhOrCv",
                "name": "Crabby Patty",
                "price": 8.99,
                "type": "Meal"
            }
        ]
    }
