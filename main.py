from bs4 import BeautifulSoup
import requests
import time

print("Put some skills that you are not familiar with.")
unfamiliar_skills = input(">")
if unfamiliar_skills != "none":
    # Convert the string into a list of skills separated by a comma (,)
    if "," in unfamiliar_skills:
        unfamiliar_skills = unfamiliar_skills.split(",")
    print(f"Filtering out {unfamiliar_skills}")
else:
    unfamiliar_skills = []
    print(f"NOT filtering out any skills.")


def find_jobs():
	# Get the HTML text
	html_text = requests.get(
		"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=").text
	# Parse the HTML
	soup = BeautifulSoup(html_text, "lxml")
	# Get all the jobs
	jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
	# Loop through the jobs and get the required data
	for index, job in enumerate(jobs):
		# Get the published date
		published_date = job.find("span", class_="sim-posted").span.text
		# Check if the job was published last few days
		if "few" in published_date:
			# Get the company name
			company_name = job.find(
				"h3", class_="joblist-comp-name").text.replace(" ", "")
			# Get the skills required
			skills = job.find("span", class_="srp-skills").text.replace(" ", "")
			# Get the more info link
			more_info = job.header.h2.a['href']
			# Check if the skills are not familiar
			if not any(unfamiliar_skill in skills for unfamiliar_skill in unfamiliar_skills):
				# Open a file to write the data to it (posts folder must exist)
				with open(f"posts/{index}.txt", "w") as f:
					# Write the data to a file
					f.write(f"Company Name: {company_name.strip()} \n")
					f.write(f"Required Skills: {skills.strip()} \n")
					f.write(f"More Info: {more_info}")
				print(f"File saved: {index}")


if __name__ == "__main__":
	while True:
		find_jobs()
		time_wait = 10
		print(f"Waiting {time_wait} minutes...")
		time.sleep(time_wait * 60)