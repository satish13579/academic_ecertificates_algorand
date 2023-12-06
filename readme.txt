Follow These Steps For The Successful Execution of the Dapp:

1. Open Terminal and change the Directory path to The Project Directory

2. Check your Python Installation in your Local Computer by running the commmand "python --version" in the terminal, Make Sure your Python version is 3.10 or above

3. Run the Command "pip install -r requirements.txt" and wait until all packages are installed.

4. now run the Command "python generate.py" , a credentials.txt file will be generated where the university credentials will be present.

5. now create a account in "https://developer.purestake.io/" Purestake API Platform and get your API KEY.
   Follow the Detailed instructions mentioned in "https://developer.algorand.org/tutorials/getting-started-purestake-api-service/"

6. Now Copy the university public key from credentials.txt file and API KEY from your purestake account and paste in line 10 & 9 Respectively in app.py file

7. Now run the application by command "python app.py", the server will start & go to "http://127.0.0.1:5000/" for application Home page 

8. now you can use the application normally, for university login the mnemonic is in the "credentials.txt" university mnemonic field



Useful Links :
Python 3.10.7 : https://www.python.org/ftp/python/3.10.7/python-3.10.7-amd64.exe
Purestake API Login : https://developer.purestake.io/
Purestake API Key Generation Procedure : https://developer.algorand.org/tutorials/getting-started-purestake-api-service/
Application Link : http://127.0.0.1:5000/ (will only work when flask app is turned on)