def main():

    from continent_script import continents
    from countries_script import countries

    continent_input = input("Continents (1) or Countries (2)? ").lower()

    if continent_input == '1':
        continents()
    else:
        countries()

    restart = input("Do you want to run the program again (Y/N) ?").upper()
    if restart == 'Y':
        main()
    else:
        exit()

main()

