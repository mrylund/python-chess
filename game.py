def main():
    while True:
        player = input("Who will start? (player/ai):")
        if player == 'ai' or player == 'player':
            print(player + " will be starting")
            break
        else:
            print("Invalid input")


main()