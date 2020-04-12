![enter image description here](https://raw.githubusercontent.com/0301yasiru/YKEY_keylogger/master/data/Screenshot%20from%202020-04-12%2015-04-41.png)


# YKEY_keylogger
This is a small framework for generate and listen to Keylogger malwares... And also the most effective and most useful feature about this Keylogger malwares is they don't communicate through email with the hackers. It uses a MYSQL databases to communicate. So you will not face to any email issues. Not only that but also using this framework you can have a log of your victims their mac addresses and also their key logs. You can connect back to a victims no matter what your routers dynamic public IP address is.


## HOW TO INSTALL
1. Installation of this framework is so simple. If you accidentally delete any file please clone the repository from the git hub then continue.
`git clone https://github.com/0301yasiru/YKEY_keylogger.git`
3. Hence this entire program uses only python 3. you must install python 3 before installation.
4. The run the command below to install the program
 `python3 install.py`

## FIX misconfigurations
   1. To fix MySQL configuration run the command below
            `python3 install.py --configure-mysql`
    2. To fix virtual environment issues run the command below
            `python3 install.py --configure-venv`


##  Command Help

#### Universal commands (You can run these command from anywhere in the program

	help		:Using this command you can view the help guide
	exit/quit	:Using this command you can exit from the space or quit the program
	clear		:Using this command you can clear the screen
	options/show options : Using this command you can view options in the current work space
    
### Malware Generation Commands (You can only run there commands when using generation option)
	set	:SYNTAX --> set [option_name] [option_value]
		: Using this command you can change a setting of Malware
	generate: Using this command you can generate the configured malwares

### Malware Listener Commands (You can use these commands only when you using the listener option)[[reset]]
	show victims : Using this command you can view your already attacked victims
	extract      : Using this command you can pull out all the key logs recorded to your computer 
