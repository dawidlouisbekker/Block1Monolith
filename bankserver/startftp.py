import argparse
from client import connectClient

def main():
    parser = argparse.ArgumentParser(description='Server connection')
    parser.add_argument('--user', help='Enter your username')
    args = parser.parse_args()
    if args.user is None:
        print("No username provided. Please enter 'python startftp.py --user [your username]'")
        return
    #Check if username correct locally to stop server flooding
    connectClient(username=args.user)
    



# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    main()