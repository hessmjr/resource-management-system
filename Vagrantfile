# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|

    # sets up vagrant box using ubuntu 14.04
    config.vm.define "erms" do |app|
        # set vm to ubuntu 14.04
        app.vm.box = "ubuntu/trusty64"

        # set vm memory to 3GB for MySQL
        app.vm.provider "virtualbox" do |virtualbox|
            virtualbox.memory = 3072
        end

        # allow VM to utilize files within current directory
        app.vm.synced_folder ".", "/home/gatech/resource-management-system"

        # forward db ports to the host
        app.vm.network :forwarded_port, guest: 3306, host: 1234

        # forward the default Flask port to the host
        app.vm.network :forwarded_port, guest: 5000, host: 5000

        # Berksfile setup
        app.berkshelf.berksfile_path = "./Berksfile"
        app.berkshelf.enabled = true

        # chef provision variables
        app.omnibus.chef_version = '12.10.24'
        app.vm.provision "chef_solo" do |chef|
            chef.channel = "current"
            chef.add_recipe "chef::default"
        end
    end
end
