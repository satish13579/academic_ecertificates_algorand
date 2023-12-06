from algosdk import account, mnemonic

# create an account
private_key, address = account.generate_account()

# get the mnemonic associated with the account
mnemonic = mnemonic.from_private_key(private_key)

# write the credentials to a file
with open('credentials.txt', 'w') as file:
    file.write(f'university public key: {address}\n')
    file.write(f'university private key: {private_key}\n')
    file.write(f'university mnemonic: {mnemonic}\n')
    print("University Credentials Saved in 'credentials.txt' File")
