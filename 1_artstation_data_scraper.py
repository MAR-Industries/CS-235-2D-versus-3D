import requests, json, time, random, os, sys

#Initializations
verbosity = False
starting_page = 1
num_pages = 25

def artScrape(lowerPage, upperPage):

	#Check the value of upperPage and ensure it doesn't go above 499
	if upperPage > 499:
		upperPage = 499

	#Checks whether the necessary folders exist for downloading
	if not os.path.exists("train/"):
		os.makedirs("train/Digital 2D")
		os.mkdir("train/Digital 3D")
		os.makedirs("test/Digital 2D")
		os.mkdir("test/Digital 3D")
	posts_parsed = 0
	null_mediums = 0

	#25% of the downloaded images will be held back for the test set
	random.seed()
	test_min = 0.2500
	randomVar = random.random()	
	saveDir = ""
	imageIncrement = 0
	fileExtension = ''
	image_medium = ""

	with open('artstation_links.txt', 'w') as f:
	
		## parsing the result pages from ArtStation
		for page_num in range(lowerPage,upperPage):
			response = requests.get(f'https://www.artstation.com/api/v2/community/explore/projects/trending.json?page={page_num}&dimension=all&per_page=100').text
			# open json response
			data = json.loads(response)
			
			# looping through json response
			for result in data['data']:
				# still looping and grabbing url's
				url = result['url']
				# writing each link on the new line (\n) [saving is for backup purposes]
				f.write(f'{url}\n')
				json_url = url.replace('artwork', 'projects')
				json_url += '.json'
				##print(json_url)
				json_down = requests.get(json_url)
				json_data = json.loads(json_down.content)
				
				#logic for determining tag/medium of artwork; also for determining whether to download or not
				if json_data['medium'] != None: ## null medium check
					image_medium = str(json_data['medium']['name'])
					
					##first check if the medium is 3D or 2D, we're skipping if it's neither
					if image_medium != "Digital 2D" and image_medium != "Digital 3D":
						continue
					
					##check for multiple listed mediums; for now, if they have 2D AND 3D, don't download
					if len(json_data['mediums']) > 1:
						counter = 0 ##increments on seeing 2D or 3D as a medium
						##print("Multiple mediums")
						for medium in json_data['mediums']:
							if medium['name'] == "Digital 2D":
								counter = counter + 1
							elif medium['name'] == "Digital 3D":
								counter = counter + 1	
						
						if counter 	>= 2 and verbosity: 
							print("Conflicting mediums, can't download!!! @ ", json_url)
							continue
					else: ## ensure it's 2D or 3D; for now, if neither of these, don't download	
						if image_medium != "Digital 2D" and image_medium != "Digital 3D":
							continue					
					
				else:
					null_mediums += 1
					continue ##null medium = skip entry, for now 
					
					
				##randomVar initialization to determine whether its to be downloaded to the test or train set	
				randomVar = random.random()
				if randomVar < test_min:
					saveDir = "test"
				else: 
					saveDir = "train"				
				
				#parsing each image per post and downloading only jpeg and png objects, no gifs, etc.
				for image in json_data['assets']:
					##for now, we do a check on the asset type; if not "image", do not consider it (for now)
					if image['asset_type'] != "image":
						continue
				
					link = image['image_url']
					if '.png' not in link and '.jpg' not in link and '.jpeg' not in link: ##it's not a png or jpeg, DON'T TAKE IT 
						continue
					elif '.jpg' in link:
						fileExtension = '.jpg'
					elif '.png' in link: 
						fileExtension = '.png'					
					##here is where we download the image
					img_data = requests.get(link).content
					##pull filename out of the image URL  
					filename = link[link.rindex('/'):link.rindex(fileExtension)]
					filePath = saveDir + "/" + image_medium + "/" + filename + fileExtension ##temporary file naming scheme 
					##print(filename)
					with open(filePath, 'wb') as handler:
						handler.write(img_data)
					imageIncrement = imageIncrement + 1	
				
				posts_parsed += 1	##just a tracker for how many posts have made it to the downloading stage

				if verbosity and posts_parsed % 50 == 0: ## some more prints for statistics
					print("\nNull mediums: " + str(null_mediums))
					print("\nTotal posts parsed: " + str(posts_parsed) + "\n")
				
				time.sleep(randomVar * .0625) ## trying to avoid getting blocked as a bot



for i in range(len(sys.argv)):
	if sys.argv[i] == "-v": #verbose flag
		verbosity = True
		print("read verbosity argument")
	elif sys.argv[i] == "-n": #custom results size and starting page
		try: 
			if sys.argv[i+1].isdigit() and int(sys.argv[i+1]) > 0:
				if int(sys.argv[i+1]) >= 500:
					print("Neither argument for the '-n' flag should be >= 500")
					sys.exit()					
				num_pages = int(sys.argv[i+1])
				try:
					if sys.argv[i+2].isdigit() and int(sys.argv[i+2]) > 0:
						if int(sys.argv[i+2]) >= 500:
							print("Neither argument for the '-n' flag should be >= 500")
							sys.exit()	
						num_pages = int(sys.argv[i+2])
						starting_page = int(sys.argv[i+1])
				except IndexError:
					continue
		except IndexError:
			print("No valid argument given after the '-n' flag")
			sys.exit()
	

# Below is where we call the scraping method for however many webpages of results we would like to specify	
# First parameter is the lowest page to scrape, second is the upper page to scrape LAST		
# This was originally (118,150) during testing

artScrape(starting_page,starting_page+num_pages)