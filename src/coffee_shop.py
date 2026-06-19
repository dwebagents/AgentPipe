program coffee_shop

    procedure division.
        main:
            display 'Welcome to the Coffee Shop!'
    
            loop with control variable i from 1 to 5 do
                select
                    when i = 1 then
                        order_coffee
                    when i = 2 then
                        order_tea
                    when i = 3 then
                        order_drink
                    when i = 4 then
                        order_milkshake
                    when i = 5 then
                        display 'Thank you for visiting us.'
                end select
    
            exit from main.
    
        order_coffee:
            display 'Ordering a coffee...'
            display 'Enjoy your morning beverage!'
    
        order_tea:
            display 'Ordering a tea...'
            display 'Delicious and refreshing.'
    
        order_drink:
            display 'Ordering a drink...'
            display 'Perfect for any occasion.'
    
        order_milkshake:
            display 'Ordering a milkshake...'
            display 'Rich and creamy, perfect for dessert!'
