# Vault-SSH
Demonstration of SSH using Hashicorp Vault

## Usage

Start containers by:

```
docker-compose up -d
```

Inspect the succesfull running of the containers by:

```
docker-compose logs -f
```

When everything is working as expected then the last log lines will show like this:

```
...
ssh_client  | SSH Client initialisation ready !
ssh_server  | Starting SSH Server...
```

Step into container ***ssh_client*** via:

```
docker exec -ti ssh_client bash
```

You are now ***user*** inside the ***ssh_client*** container
From here you can connect to de ***ssh_server*** container via following supported methods:

1) OTP using One Time Passwords
   ```
   ssh_server_otp
   ```
2) CA using SSH Public Keys signed by Vault
   ```
   ssh_server_crt
   ```
3) Local User OR Vault password. 
   ```
   ssh user@ssh_server
   ```
   When you have a system password on this machine, you get access when your password matches the system password

   If it not matches, the entered password will be verified via Vault if it matches the password that is assigned in Vault to your UserPass Access Method. When that is valid, you get access as well

4) [ Old School ] Public Key Access
    Have you public key stored into the 'Authorized Keys' file on the ssh_server

It is left as an excercise to the reader to inspect the **docker-compose.yml** file and corresponding **dockerfiles** to see what this configuration is made of.




