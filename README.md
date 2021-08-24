# Vault-SSH
Demonstration of SSH using Hashicorp Vault

## Usage

Start container by:

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
From here you can connect to de ***ssh_server*** container via two methods:

1) OTP using Time Time Passwords
   ```
   ssh_server_otp
   ```
2) CA using SSH Public Keys signed by Vault
   ```
   ssh_server_crt
   ```

It is left as an excercise to inspect the docker-compose.yml file and corresponding dockerfiles to see what this configuration is made of.




