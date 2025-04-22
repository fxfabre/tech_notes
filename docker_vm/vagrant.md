# Vagrant

Target : Create isolated dev env using VM

3 components :
- CLI : start, stop, create, manage Vagrant VM
- Vagrantfile : small prog in ruby, stateless, to manage the config of 1 to many VMs
- Vagrant cloud : online marketplace for VMs

## Basic Vagrant commands
The commands refers to the VM described in a local Vagrantfile.  
It is also possible to add the `box_id` to refers to a different VM
- `vagrant init bento/ubuntu-18.04` : Create a default Vagrantfile in the current folder to start a VM based on ubuntu 18.04
- `vagrant up` : start the VM
- `vagrant status [box_id]` : status
- `vagrant halt [box_id]` : docker stop
- `vagrant destroy` : docker rm
- `vagrant reload` : restart the box, reloading the Vagrantfile
- `vagrant suspend`
- `vagrant status`

## Global vagrant commands
- `vagrant global-status` : all VM

## SSH
- `vagrant ssh` : docker exec bash
  - SSH to the box defined by `config.vm.box`
- `vagrant ssh box_name`
  - SSH to the box defined in `config.vm.define "box_name"`

## Vagrantfile
https://www.vagrantup.com/docs/vagrantfile

Base config :
- `vagrant.configure("2") do |config|` 
  - "2" to set the version of the configuration object
  - create the object `config`
- `config.vm.box = "bento/ubuntu-18.04"` : base box

Shared folder / volumes
- Current folder mounted by default to `/vagrant` inside the box
- `config.vm.sync-folder = "local folder", "box path"` to mount an other folder

Memory and CPU
- `vb.memory = 512` : size in Mo
- `vb.cpu = 2` : cpu count
- `vb.customize ["modifyvm", :id, "--vram", "16"]` : use the utility "vbox manage" to set dedicated video memory

Networks
- port forwarding : `config.vm.network="forward-port", guest=80, host=8080, host_ip=x.x.x.x`
- private netword : `config.vm.network="private-network", type="dhcp"`
- public network : not secure by default

Providers :
- Virtual box, hyper-V (MS), Docker

Provisioners : To customize apps in the box
- `config.vm.provision "shell", path : "path_to_file.sh"`
  - Run a script to setup the box, install apps
  - Only run at startup, not on reload (default behaviour, can be changed)
- `config.vm.provision "file", source: "source path", destination: "box_path"` : copy file to box
- Can also run a configuration manager such as `chef` or `puppet`

## Multi-VM
Define multiple VM in a vagrantfile :
```
config.vm.define "mongo" do |mongo|
    mongo.vm.box = "image name"
    mongo.vm.provider "virtualbox" do |vb|
        vb.xxx = ... # define virtualbox specific settings
    end
    mongo.vm.network "private-network, ip: "192.168.1.2"
end
```

## Packaging apps
Same as creating a docker image from a base docker image

Vagrant file load order :
- the packaged vagrantfile
- the vagrantfile in ~/.vagrant.d
- the local environment vagrantfile

Package / snapshot :
- `vagrant package --vagrantfile path_to/vagrantfile --output image_name.box` : Create a file `.box` containing the VM :
- `vagrant box list` : same as `docker images`
- `vagrant box add box_name box_path.box` : same as `docker load`
- `vagrant init image_name` : Create a vagrantfile calling the `image_name`
- `vagrant snapshot save snapshot_name`
- `vagrant snapshot list`

## Bonus : commands to run inside Ubuntu
- `vmstat -s` : virtual memory
- `lscpu` : display cpu count + infos
- `lspci -v -s 00:02.0` : video RAM
