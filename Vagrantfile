# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |copo|

  copo.vm.box = "ubuntu/trusty64"

  copo.vm.network "forwarded_port", guest: 8000, host: 8000

  copo.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--memory", 2048]
  end
  copo.vm.provision "fix-no-tty", type: "shell" do |s|
    s.privileged = false
    s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
  end

  copo.vm.provision :puppet do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "vagrant.pp"
  end

end
