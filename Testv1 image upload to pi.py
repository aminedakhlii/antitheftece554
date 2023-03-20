#!/usr/bin/env python
# coding: utf-8

# In[ ]:


sudo apt-get install apache2 -y
#By default, Apache is set to look in this directory for web documents to create content within a web browser. 
#To take a look at this test page and confirm Apache did indeed install correctly pull up it up in your web browser
#by typing in this URL address: http://localhost/

cd ~

#Copy and paste the Image file:
sudo cp boof/fotos/animateMe.gif /var/www/html

#Go back to the html directory:
cd /var/www/html

#Reopen the index.html file so you can add the image:
sudo nano index.html

#embed an image on an HTML page
<p><img src="animateMe.gif"></p>

