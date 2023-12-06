from flask import Flask, request,session,render_template
from algosdk.v2client import algod,indexer
from algosdk import account, mnemonic
from algosdk import util,transaction,error
import json,base64
from flask_cors import CORS

##### GLOBAL CONSTANTS ##########
API_KEY="<your-api-key>"
UNIVERSITY_PUBLIC_KEY="<your-university-public-key>"
#################################


app = Flask(__name__)
app.secret_key = 'algo-project'
CORS(app,resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uc')
def uc():
    return render_template('upload_certificate.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the mnemonic from the request parameters
    mnemoni = request.form.get('mnemonic')
    # Derive the private key from the mnemonic
    try:
        private_key = mnemonic.to_private_key(mnemoni)
    except Exception as e:
        print(e)
        return json.dumps({"status":False,"err":"Given mnemonic is Invalid"})
    # Return the public address corresponding to the private key
    public_address = account.address_from_private_key(private_key)

    if(public_address==UNIVERSITY_PUBLIC_KEY):
        session['user']=private_key
        return json.dumps({"status":True})
    else:
        return json.dumps({"status":False,"err":"Given mnemonic is Not Owned By University"})
    
@app.route('/logout', methods=['GET'])
def logout():
    if session.get('user'):
        session.pop('user')
        return json.dumps({"status":True})
    else:
        return json.dumps({"status":False,"err":"Please Login First.!!"})

@app.route('/auth', methods=['GET'])
def auth():
    if session.get('user'):
        return json.dumps({"status":True})
    else:
        return json.dumps({"status":False})

@app.route('/upload_certificate', methods=['POST'])
def upload_certificate():
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = ""
    headers = {
        "X-API-Key": API_KEY,
    }
    if session.get('user'):
        private_key=session['user']
        data=request.form.get('data')
        print('data',request.form)
        data=json.loads(data)

        algod_client = algod.AlgodClient(algod_token, algod_address, headers)
        try:
            sender_address = account.address_from_private_key(private_key)
        except Exception as e:
            return json.dumps({"status":False,"err":"Your Private Key Length is too Short"})
    # Convert the JSON data to bytes
        signature = util.sign_bytes(data['rollno'].encode('utf-8'), private_key)
        data['hash']=signature
        note = json.dumps(data).encode()
        params = algod_client.suggested_params()
        txn = transaction.PaymentTxn(sender_address,params,sender_address,0,note=note)

        # Sign the transaction with your private key
        
        signed_txn = txn.sign(private_key)
        
        # Submit the transaction to the Algorand network
        try:
            tx_id = algod_client.send_transaction(signed_txn) 
        except error.AlgodHTTPError as e:
            return json.dumps({"status":False,"err":"Your Private Key is Invalid For Signature"})
        # Wait for transaction confirmation
        confirmed_txn = algod_client.pending_transaction_info(tx_id)
        while not confirmed_txn.get('confirmed-round'):
            confirmed_txn = algod_client.pending_transaction_info(tx_id)

        return json.dumps({"status":True,"resp":{"txn_id":tx_id,"block":confirmed_txn["confirmed-round"]}})
    else:
        return json.dumps({"status":False,"err":"Please Login To Upload Certificate"})


@app.route('/get_certificate', methods=['POST'])
def get_certificate():
    algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    algod_token = ""
    headers = {
        "X-API-Key": API_KEY,
    }
    txn_id=request.form.get("txn_id")

    algod_client = indexer.IndexerClient(algod_token, algod_address, headers)
    try:
        info=algod_client.search_transactions(txid=txn_id)
    except error.AlgodHTTPError as e:
        print(e)
        if(str(e)=='no valid transaction ID was specified'):
            return json.dumps({"status":False,"err":"Invalid Certificate ID"})
    try:
        print(info)
        note=info['transactions'][0]['note']
    except KeyError as e:
        return json.dumps({"status":False,"err":"Invalid Certificate ID"})
    except IndexError as e:
        return json.dumps({"status":False,"err":"Invalid Certificate ID"})
    sender=info['transactions'][0]['sender']
    reciever=info['transactions'][0]['payment-transaction']['receiver']
    if(sender==reciever and sender==UNIVERSITY_PUBLIC_KEY):
        note=base64.b64decode(note).decode('utf-8')
        note=json.loads(note)
        sig=note['hash']
        typ=note['type']
        rollno=note['rollno']
        name=note['name']
        branch=note['branch']
        year=note['year']
        verified = util.verify_bytes(rollno.encode('utf-8'),sig, sender)
        if(verified):
            return json.dumps({"status":True,"data":{"type":typ,"rollno":rollno,"name":name,"branch":branch,"year":year}})
        else:
            return json.dumps({"status":False,"err":"Certificate Not Signed By The University"})
    else:
        return json.dumps({"status":False,"err":"Certificate Origin is Not From University"})


if __name__ == '__main__':
    app.run(debug=True)
