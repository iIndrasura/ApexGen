# ApexGen

ApexGen is an account generator for Apex Legends, a free-to-play battle royale game. It allows you to create multiple accounts with different modes and settings. It also verifies the email for steam and fetches the OTP/Auth Code for EA automatically. It uses discord webhook to send the account details to your discord server.

## Installation

To install and run ApexGen, you need to have Google Chrome installed on your system. You also need to install the following Python packages:
```bash
 pip3 install playwright
 pip3 install quopri
 pip3 install requests
 pip3 install beautifulsoup4
 pip3 install discord-webhook
```
You can install all the packages at once by running the following command:

```bash
pip3 install -r dependency.txt
```
You also need to edit the settings.json file and provide your discord webhook url.

## Build
To build the project, you need to have pyinstaller installed on your system. You can install it by running the following command:

```bash
pip3 install pyinstaller
```
Then, you can run the following command to create a single executable file for ApexGen:
```bash
pyinstaller --onefile --add-data "settings.json;." --icon=generator.ico main.py
```
The executable file will be located in the dist folder.

## Contributing
ApexGen is an open-source project and welcomes contributions from anyone. If you want to contribute to ApexGen, you can follow these steps:

Fork the repository
Create a new branch for your feature or bug fix
Make your changes and commit them
Push your branch to your fork
Create a pull request from your branch to the main repository
Please make sure to follow the coding style and conventions of the project. You can also run the tests and check the code quality before submitting your pull request.

If you have any issues, questions, or suggestions, you can create an issue on the issues page.

License
ApexGen is licensed under the MIT License. See the LICENSE file for details.
