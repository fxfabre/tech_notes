# How to create / manage VM ?

Multipass
- https://canonical.com/multipass
- Create Ubuntu VM anywhere
- `multipass launch --name node1`
- `multipass exec node1 -- lsb_release -a`
- `multipass list`
- `multipass info node1 [--format json]`
- `multipass start node1`, `multipass stop node1`, `multipass delete node1`, `multipass purge`
- `multipass help <command>`
- `multipass launch -n node2 -c 2 -m 3G -d 10G` : 2 cpu, 3G ram, 10G stockage
- `multipass mount $HOME/test node1:/usr/share/test` Monter un dossier dans la VM
- `multipass transfer $HOME/test/hello node1:/tmp/hello` Copie d'un fichier


Cloud-init : https://cloudinit.readthedocs.io/en/latest/
- The standard for customizing cloud instances
- Can be used to setup a VM in AWS
- `multipass launch -n my-test-vm --cloud-init cloud-config.yaml`


```yaml
apt_update: true
apt_upgrade: true
packages:
- apache2
- rsync

ssh_authorized_keys:
  - ssh-rsa AAABBCCD keyname@host

runcmd:
  - [wget, "https://somewhere.com", -O, /tmp/index.html]
  - /bin/echo "<h1>hello</h1>" > /var/www/index.html
```