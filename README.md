# Beef-over-Ngrok

Beef-over-Ngrok is a python script to enable beef to access over internet

## Usage

Use python3 to run the Beef-over-Ngrok script

```bash
sudo python3 Beef_Over_Ngrok.py
```

## Ngrok configuration

Open ngrok.yml in Location: .ngrok2/ngrok.yml

```text
NGROK Steps :-

            STEP 1 : Add these Lines To ngrok.yml [Location .ngrok2/ngrok.yml ]
                
                tunnels:
                first-app:
                    addr: 80
                    proto: http
                second-app:
                    addr: 3000
                    proto: http
                
            STEP 2 : Now Start ngrok with : \n
                    ngrok start --all
            STEP 3 : You will See 2 different links Forwarded to\n 
                    Localhost:80        [ Link To be Sent to Victim ]\n
                    Localhost:3000		  [ Your Link will be Connecting to.. ] 	
                                    
            STEP 4 : Enter these links in Script and Follow The Steps given in Script.

```
