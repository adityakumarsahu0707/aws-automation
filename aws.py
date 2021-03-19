import os
import subprocess as sp
import boto3

aws_ec2 = boto3.resource('ec2')

def ec2():
	global name
	name=input("\n Enter name for instance : ")
	print("\n Provisioning instance with name : ", name, "\n")
	
	output = sp.getstatusoutput(f"aws ec2 run-instances --image-id ami-081bb417559035fe8 --instance-type t2.micro --count 1 --subnet-id subnet-611c1509 --security-group-ids sg-05ac300af78f49d82 --tag-specifications ResourceType=instance,Tags=[{{Key=Name,Value={name}}}] --key-name ec2_aws")
	#output=[0,1]

	if output[0]==0:
		print("\nEc2 instance with name :", name , " created successfully!!")
		os.system("sleep 5")
		input(enter)

	else:
		print(output[1])
		print("\nSome Error Occured!!")

def ebs():
	print("Creating EBS Volume... \n ")

	#output = sp.getstatusoutput("aws ec2 create-volume --volume-type gp2 --size 1  --availability-zone ap-south-1a")
	output=[0,"Status"]
	if output[0]==0:
		print(output[1])
		print("\n EBS Volume Already created!!")
		os.system("sleep 2")
		os.system("clear")
		print("\n \t Time to attach the volume!! \n")
		for instance in aws_ec2.instances.all():
			print("Available Instances :")
			print("Id: {0}\nPublic IPv4: {1}\n\n".format(instance.id,instance.public_ip_address))
			global ip
			global ins_id
			#ip = instance.public_ip_address
			#ip = "2.2.2.2"
			ins_id = instance.id
			ins_id = "i-089733a6b204ee16c"
			name="testing-aws"
			ip=os.system(f"aws ec2 describe-instances --filters 'Name=tag:Name,Values={name}' --instance-ids {ins_id} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text")
			
		for vol in aws_ec2.volumes.all():
			print("Available Volumes : \n")
			print(vol.id,"\t", vol.volume_type, "\t", vol.size,"GiB")
			if (vol.size==1) or (vol.size=='1'):
				global vol_id
				vol_id=vol.id

		#attach = sp.getstatusoutput(f"aws ec2 attach-volume --volume-id {vol_id} --instance-id {ins_id} --device /dev/sdf")

		attach=[0,"test"]

		if attach[0]==0:
			print("Volume attached successfully!! ")
			os.system("sleep 2")
			os.system("clear")
			mount()
		else:
			print(attach[1])
			print("attach failed!")

	else:
		print(output[1], "\n\n" )
		print("Some Error Occured!!")

def mount():
	os.system("figlet -tkc -f small -w 80 Mounting Volume")
	#os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip}")
	print("\n")
	#os.system("sleep 2")
	#os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip} sudo fdisk /dev/xvdf")
	#os.system("sleep 2")
	#os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip} sudo mkfs.ext4 /dev/xvdf1")
	#os.system("sleep 2")
	#os.system("clear")
	ip= "13.232.210.45"
	print("\n \t Installing HTTPD Webserver \n")
	os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip} sudo yum install httpd -y")
	os.system("sleep 2")
	os.system("clear")

	os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip} sudo mount /dev/xvdf /var/www/html")
	print("\n\t Volume Mounted successfully!! Proceeding to S3 Bucket creation")
	os.system("sleep 2")
	os.system("clear")

def s3():
	os.system("figlet -tkc -f small -w 80 S3 Bucket")
	print("Available Buckets : \n")
	os.system("aws s3api list-buckets --output yaml")
	os.system("sleep 2")
	os.system("clear")
	global bname
	bname=input(" \n Creating New Bucket \n \t Enter a unique bucket name : ")
	output=sp.getstatusoutput("aws s3 mb s3://{0}".format(bname))
	if output[0]==0:
		print("\n\nS3 Bucket created successfully!!\n\n")
		global obj
		obj=input("\n Enter object to be stored in Bucket: ")
		upload_status=sp.getstatusoutput(f"aws s3 cp \"{obj}\" s3://{bname} ")

		os.system(f"aws s3api put-object-acl --bucket {bname} --key {obj} --grant-read uri=http://acs.amazonaws.com/groups/global/AllUsers")
		if upload_status[0]==0:
			print("\n\nFile Uploaded successfully!!")
			os.system("sleep 2")
			cf()
		else:
			print(upload_status[1], "\n Error Occured!!")
			input(enter)
	else :
		print("Retry, Something went wrong !!")

def cf():

	sp.getstatusoutput(f"aws cloudfront create-distribution --origin-domain-name {bname}.s3.amazonaws.com")
	print(" \n \n \tCloud Distribution setup successfully")
	os.system("sleep 3")

def server():
	bname="testbuck12"
	obj="adi.jpg"
	ip= "13.232.210.45"
	#https://testbuck12.s3.ap-south-1.amazonaws.com/adi.jpg
	os.system("clear")
	url=sp.getoutput(f"echo https://{bname}.s3.ap-south-1.amazonaws.com/{obj}")
	index=sp.getoutput(f"echo '<img src=\"{url}\" />'")
	os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip} sudo touch /var/www/html/index.html")
	#os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip} sudo echo {index} >> /var/www/html/index.html")
	os.system(f"ssh -i 'ec2_aws.pem' ec2-user@{ip} sudo systemctl enable httpd --now")
	print("Webserver Configured")

while True:
	os.system("clear")
	os.system("tput setaf 3")
	os.system("figlet -tkc -f small -w 80 'AWS   High Availability'")
	os.system("tput setaf 7")
	print("""
	Press 1 : To create an instance
	Press 2 : To create an EBS volume
	Press 3 : To create a S3 bucket
	Press 4 : To create a Cloud Formation Distribution
	Press 5 : To configure Webserver
	Press q : To Quit
	""")
	n=input("Enter your choice: ")
	enter="\n\n--------------------- Press Enter To Continue ---------------------"
	if n=="1":
	    ec2()
	    input(enter)
	elif n=='2':
	    ebs()
	    input(enter)
	elif n=='3':
	    s3()
	    input(enter)
	elif n=='4':
		cf()
		input(enter)
	elif n=='5':
		server()
		input(enter)
	elif n=='q':
	    exit()
	else:
		print(" \n \n Wrong Input!!")
		input(enter)