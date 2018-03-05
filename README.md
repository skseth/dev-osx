This is a set of ansible scripts for setting up a mac laptop. 

# Bootstrapping

As a user of the script, the first thing to do is to install brew and ansible. Run ./bootstrap.sh to do so.









# Setting up a Dev Environment

As a developer of these scripts, you will need an environment to test the scripts. On OS X, the simplest thing is to use Parallels Desktop Lite. For instructions see this [link](https://www.howtogeek.com/304866/how-to-make-linux-and-macos-virtual-machines-for-free-with-parallels-lite/). A brief summary :

- Install Parallels Desktop Lite and "Install macOS High Sierra" apps - you will not see a version of macOS lower than your current one

- In Parallels, start creating a new VM. Choose the "Install Windows or other OS ...." option. Allow Parallels to search for options, then click on "Install macOS High Sierra".

- Let Parallels create the image, and then the VM

- Install Parallels Tools

- Run sudo systemsetup -setremotelogin on, to turn on ssh access

You can also do this in virtual box, following instructions [here](https://www.howtogeek.com/289594/how-to-install-macos-sierra-in-virtualbox-on-windows-10/).

