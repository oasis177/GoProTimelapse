# GoProTimelapse

This project allow us to realize a Timelapse using a Raspberry Pi and a GoPro. Our RPi will send html commands to the GoPro in order to realize a photo in the time period that we interest.

## Functionality

First of all we need to swich on the GoPro wireless connection and connect the Rpi on it. We also need to connect our RPi to Internet via Ethernet in order to control this process.
After that we have to connect the charger to our components and finnaly we only just need to create a <xml> config file with the passwords and configuration mails and save it in the same folder of our class. 

## Xml Config Format

Our program will send a email advising us when the GoPro is not saving the images correctly.

'<goPro>'

'<destmail>Destination mails to recive when Process fails</destmail>''

'<frommail>The user mail that will send mails when Process fails</frommail>'

'<mailpwd>User mail password</mailpwd>'

'<wifipwd>The GoPro wireless password</wifipwd>'

'</goPro>'

Remember: Remove de ' in our xml file.

Our program runs the main class goPro.py that by default makes a photo every 30 minutes. We can change this interval modifing time.sleep() command on the end of Start() function.
If we have not connection whith the GoPro or the imgage is not correctly saved our program execute EnviarMail() function that sends a Information mail to us.

We also need tho check if the GoPro IP is correct in the start() function. In my case this IP is 10.5.5.9 but maybe in your application this address is diferent.

## Downloading imges

If we want to download in the RPi the images from the GoPro we just need to create a folder called /img. After that we run the class DownloadImg (remember to check the IP address of the GoPro) and this class download the files the lasts files localy.
