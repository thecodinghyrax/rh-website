## Website for the World of Warcraft guild - Renewed Hope

### Purpose:

**This project fills two needs. **
1.	This was an opportunity to learn more about Python using Flask 
2.	Served as a feature rich replacement for the guilds original Wix page.

### What does it do?
1.	Provides a public face to people in the guild as well as people looking to join. This includes announcements, news, twitter feed, calendar events, recorded devotionals, embedded podcasts from the guild and a mission statement for those who want to know more.
2.	Allows potential guild applicants to create an account, fill out an application and send messages to guild leadership. The application will trigger an email that is sent to guild leadership, so they are notified as soon as there is a new application to review. 
3.	Allows many different management options to help with application screening, messaging, updating of the website and setting admin ranks. Admin’s can log into the site and review applications, make notes about them for other admins, approve or reject an application and remove users no longer in the guild.
4.	Admins can also add/edit/remove calendar events (single and repeating), recorded devotionals, announcements, and podcasts.
5.	Admins log into a simple dashboard that shows current applications, current announcements, upcoming calendar events and recently posted devotionals.

### How was it built

This site was built using Python’s flask framework, SQL Alchemy ORM, and a MySQL database. I also utilize Azure to host all my audio files and database backups (which are performed each night via a task script on my hosting site). 

### Things that work well

Right now, the most used features are the management of guild applications and user messaging and posting/listening to guild devotionals. The application management is vital to bring onboard new applicates and the devotionals have really impressed potential new members (often nudging them to apply).

### Things that don’t work so well

The calendar is a bit of a pain point. The functionality works well enough, but it relies on manual updating which can be easily ignored. An ideal solution would be to create an in game addon to export that calendar so there could be a single data source to work with. Unfortunately, Blizzard lacks the proper API’s to retrieve this data from the game so our solution is the only way to go at this time.	
As this was a learning project, some of the structure is inconsistent (mostly relating to css).  
I have also not created unit tests for the site as I still need to learn more. Everything is manually tested atm which is not ideal. 


### Where can I see this in action?

[RenewedHope](renewedhope.us)


