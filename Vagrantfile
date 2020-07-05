Vagrant.configure("2") do |config|
    config.vm.define "tenflmc1" do |tenflmc1| 
        tenflmc1.vm.box = "bento/centos-7.2"
        tenflmc1.vm.network "private_network", ip:"192.168.77.10"
        tenflmc1.vm.hostname = "tenflmc1"
        tenflmc1.vm.provider :virtualbox do |vb|
           vb.name = "tenflmc1"
           vb.memory = 4096
           vb.cpus = 1
        end
    end    
end