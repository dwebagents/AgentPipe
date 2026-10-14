class Goose:
    def __init__(self):
        self.value = 71
        self.eggs = []
        self.is_secure = True

    def add_egg(self, egg):
        if self.is_secure:
            self.eggs.append(egg)
        else:
            raise Exception("Goose is not secure. Cannot add egg.")

    def get_total_value(self):
        return self.value + sum(egg.value for egg in self.eggs)

    def check_security(self):
        if not self.is_secure:
            raise Exception("Goose is not secure. Please secure the goose before proceeding.")
        return self.is_secure

class GoldenEggFactory:
    def create_egg(self):
        return Egg()

class Egg:
    def __init__(self):
        self.value = 3

def main():
    # Create a goose and a golden egg factory
    goose = Goose()
    egg_factory = GoldenEggFactory()

    # Check if the goose is secure
    try:
        goose.check_security()
    except Exception as e:
        print(e)
        return

    # Add eggs to the goose
    for _ in range(5):  # Adding 5 eggs as an example
        try:
            egg = egg_factory.create_egg()
            goose.add_egg(egg)
        except Exception as e:
            print(e)
            return

    # Calculate and print the total value
    total_value = goose.get_total_value()
    print(f"Total value: {total_value}")

if __name__ == "__main__":
    main()