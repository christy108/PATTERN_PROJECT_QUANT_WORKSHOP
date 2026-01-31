from Data_Storage import Data_Storage

def main():
    data_storage = Data_Storage('AAPL', '2020-01-01', '2023-01-01', 2)
    print(data_storage.get_data())

if __name__ == "__main__":
    main()