***MAPPING POLICE VIOLENCE AGAINST STUDENTS***

For my final submission of Harvard's CS50 Web Programming with Python and JavaScript I made a mapping application for recording incidents of police violence committed against students on university campuses in South Africa.

The project utilizes the Leaflet.js mapping library and consists of one main page for displaying the map and the incidents, navigating between campuses on the map, logging new incidents, expanding incidents, and logging requests to edit incidents. The application also consists of other pages for logging in, registering an account, and for processing requests to edit incidents if the user is admin. 

***RUNNING THE APPLICATION***

1. Download the files from this repository.
2. Place them in a folder on your computer.
3. Open your IDE and navigate to that folder.
4. Download Django into that folder.
5. Set up a virtual environment in that folder.
6. Navigate to the Uprising folder.
7. Start the Django server by using the command 'python manage.py 	 runserver' in the command line on your IDE.
8. If the server has started successfully you should be given a   	 link to click on in the form of a demo URL in your terminal.    	Click that link and your browser will open this project.



All the libraries the code uses are already linked to the files so running it should be no different than the method used to run previous projects.

***MAIN FILES OF THE APPLICATION:***

A models.py file containing three Database models: User, Incident, and editRequest.

A views.py file containing server code to pass data between the front and back ends of the app, serve HTML files, and handle user authentication.

An index.html file containing HTML and JavaScript to display the map and incidents on the homepage and allow for logging, editing, and expanding incidents. I did not write one JS file for the application but chose to rather write tailored JS that was embedded in different HTML files because the different HTML files required their own unique JavaScript.

A requests.html file with two view modes. The first displays a list of all requests to edit incidents. The second is triggered when one of the items in the list gets clicked, and it displays the edit request in its expanded form, as well as the target incident in its original form. Admin users can either accept or reject edit requests and depending on their decision, the target incident either changes or not.

There are other files that are more self-explanatory: layout.html (containing the navbar), login.html, styles.css, urls.py, and other files required to build up the Django application.

***SPECIFICATIONS***

User Authentication:
The app uses the User Model and borrows server code from previous applications to handle registration, user authentication, logging in, and logging out.

Incident and editRequest Models:
The Incident model contains fields for type, location, date, description and a boolean field for storing whether a request to edit that instance has been submitted. The editRequest model contains fields for target incident and description.

Implementation of a Leaflet.js map:
Along with a navbar and title, the homepage of the app implements a dynamic Leaflet.js map. This was achieved by linking Leaflet JS and CSS files to the index.html file and, using JavaScript, instantiating an L.map() class that takes an HTML div element as a parameter. The default location and zoom level displayed by the map was set by applying the setView() method to this class. This map instantiation was saved as a variable to be accessed by subsequent methods.

Map skin customization:
The map consists of a custom map tileLayer (skin) that was chosen at https://leaflet-extras.github.io/leaflet-providers/preview/. Each skin has a unique instantiation of the L.tileLayer() class written in JavaScript associated with it. This instantiation was added to the JavaScript in the index.html file.

Navigate between campuses on the map:
The user can navigate between campuses using the navbar and each time they select a campus, the map refreshes on the corresponding location and lights up its boundary. This was achieved by instantiating a series of L.polygon()s which Leaflet uses to display boundaries. It required building arrays consisting of sets of latitude/longitude coordinates that pertain to campus boundaries and plugging them in as parameters to the L.polygon() instances. The polygons were then attached to the map using the addTo() method. The dropdown menu in the navbar that lists the campuses was built using Bootstrap. Event listeners were attached to each campus in the dropdown that trigger the getBounds() method causing the map to navigate to a view that encapsulates whichever campus was clicked. 

Display incidents on the map:
The incidents that have been logged to the database so far are displayed on the map as red dots. The dots are instantiated using an L.icon() class. JavaScript fetches all instances of the Incident model from the database and displays them at the locations they were recorded to have happened at. A forEach loop does this by plugging the relevant Incident fields as well as an L.Icon() into an L.marker() class. 

Popups containing incident details:
The same forEach loop attaches a popup to each L.Marker() using the bindPopup() class. This popup displays the case type. It also displays a link to expand the case details. Building this part of the loop was a challenge because there was a specific order that html elements had to be created in using JavaScript and then attached to the popup and marker.

Expand incident details:
Event listeners were created and embedded on "expand" links inside popups. When they are clicked, the page auto scrolls and full details of the incident are displayed below the map by plugging incident details into a chunk of previously hidden HTML. Event listeners are attached to the titles of the expanded cases so that the expanded incident gets closed if the user clicks its heading. 

Log new incident:
If a user is logged in, they can log a new incident by clicking the 'Log incident' button on the map. Getting the button onto the map was more difficult than inserting a bootstrap button into the html but required extending the L.control() class and setting it with the correct parameters. After clicking the button, JavaScript event listeners and Bootstrap modals were used to create a series of subsequent modals that both instruct and present form fields for the user to log the incident in. After clicking the Log incident button the user is presented with the first Bootstrap modal giving them instructions about how to log the incident. If they exit this modal and click the map, nothing will happen. If they click, 'Proceed' they can then click the map at the location where the incident occurred and the GPS coords will get saved. A new modal then pops up where the user can choose to proceed, abort, or try again to save a new set of coords. If they abort, the page refreshes and they have to start over again to log a case. If they click 'try again', they can click the map at a different location and the same model will pop up again presenting them with the same three options. If they proceed, a final modal comes up containing a form which has the gps coords save in it and which allows them to log the type of incident, time of occurrence, and description. Submitting the form on this modal sends a post request to the Python API in the views.py file and it adds this new incident to the database. User gets redirected to a Thank You page and when revisiting the home page, the new incident will be displayed on the map. This chunk of functionality was a significant challenge to implement.

Edit incident:
If user is logged in, they will see an edit button below incidents they expand. By clicking this button, a modal pops up containing the description of the incident and its primary key in a hidden field. They can edit the description. Submitting this form sends a post request to the API and a new editRequest model instance is created with fields for description and target post id. User cannot edit a case that already has an edit request on it. If they try, they will get an alert that a request on that case is being processed. Once the edit on the case has bee accepted by admin, that case can then have another edit request opened on it.

Requests page:
If user is a Superuser, they will see a Requests link in the navbar which when clicked will take them to a page displaying a list of edit requests, or instantiations of the editRequest model. There are event listeners on these divs and when the user clicks one, JavaScript hides the listed requests, fetches the target incident corresponding to the request that was clicked and displays both edit request and target incident in a previously hidden div. If the admin accepts the edit request, JavaScript passes the incident's Id to the api which updates the incident and deletes the request. If the admin rejects the request, it gets deleted and the target case does not change. The admin can also go back to all requests by clicking 'back'.
















