set -x
mkdir -p /vagrant/WithCognito/code  
mkdir -p /vagrant/WithCognito/templates 
mkdir -p /vagrant/WithCognito/static
cp -fp /home/hadoop/serverlessapp/*.*           /vagrant/WithCognito/code/.
cp -fp /home/hadoop/serverlessapp/templates/*   /vagrant/WithCognito/templates/.
cp -fp /home/hadoop/serverlessapp/static/*      /vagrant/WithCognito/static/.
