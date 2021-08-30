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

1) **OTP** using One Time Passwords
   ```
   ssh_server_otp
   ```

   This command is a conveniant alias for:
   ```
   vault ssh -role otp_key_role -mode otp -strict-host-key-checking=no user@ssh_server
   ```

2) **CA** using SSH Public Keys signed by Vault
   ```
   ssh_server_crt
   ```
   This command is a conveniant alias for:
   ```
   sign-cert && ssh -o StrictHostKeyChecking=no -i ~/.ssh/signed-cert.pub -i ~/.ssh/id_rsa user@ssh_server
   ```

3) **PAM** (Local User OR Vault password) 
   ```
   ssh user@ssh_server
   ```
   When you have a system password on this machine, you get access when your password matches the system password

   If password not matches, the entered password will be verified via Vault if it matches the password that is assigned in Vault to your UserPass Access Method. When that is valid, you get access as well (off course you are free to change order of the module to prioritize the method to be evaluated first, refer: **/etc/pam.d/sshd**)
   <br/>

4) [ Old School ] **Public Key Access**
    Have you public key stored into the ***~/.ssh/authorized_keys*** file on the ssh_server

It is left as an excercise to the reader to inspect the **docker-compose.yml** file and corresponding **dockerfiles** to see what this configuration is made of.




