# Paper Title
Official Repository of "CoTEVer: Chain of Thought Prompting Annotation Toolkit for Explanation Verification" accepted at EACL 2023 demo session.

Paper Link: https://arxiv.org/abs/2303.03628

Youtube Explanation: https://www.youtube.com/watch?v=IKT6dVxp_qE

Overview of software, CoTEVer.
<p align="center">
  <img src="./cotever.png" width="50%" height="50%">
</p>


## Setting
Using the following commands, you could install the required softwares.

#### 1. Common Installations
First, install npm, node packages. In Linux environment, you could use apt-get instead of brew.
```
brew install node
brew install npm
```

#### 2. FrontEnd Module
Second, go to the './Frontend' directory, and use the following command.
```
npm install
```
Then, run the following command, which will run the frontend as a localhost.
```
npm start
```


#### 3. BackEnd Module
Third, go to the './Backend' directory, and use the following command.


You should install JDK to run the backend, otherwise, you will get the following error.
```
The operation couldn’t be completed. Unable to locate a Java Runtime.
Please visit http://www.java.com for information on installing Java.
```
Please visit the following website to install JDK.
```
https://www.java.com/en/download/
```

Also, install the following packages.
```
brew install gradle
```

If mongod is not installed, you can install with the following command:
```
brew tap mongodb/brew
brew install mongodb-community
brew install mongodb-community-shell
```

After installation is complete, you can run MongoDB server with:
```
brew services start mongodb-community
```

and stop it with:
```
brew services stop mongodb-community
```

Then run the following command.
```
./gradlew
./gradlew bootRun
```

#### 4. Middleware Module
Third, go to the './Backend' directory.

You have to set up the following keys beforehand.
```
export GPT3_KEY=$YOUR_KEY
export GOOGLE_SEARCH_API_KEY=$YOUR_KEY 
export GOOGLE_ENGINE_ID_KEY=$YOUR_KEY 
```

You could acquire the keys at the following websites:
```
https://platform.openai.com/
https://console.cloud.google.com/
https://programmablesearchengine.google.com/
```

Then, use the following command.
```
python3 main.py
```
